#!/usr/bin/env python3
"""Local-only campaign workspace and readiness records. No network or ad actions."""
import argparse
import hashlib
import json
import math
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CHECKS = (
    "brief_confirmed", "account_ready", "research_done", "settings_verified",
    "creative_approved", "lead_test_passed", "review_complete",
)


def run_path(root, slug):
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or len(slug) > 63:
        raise ValueError("Use a short name such as dallas-hvac: lowercase letters, digits, hyphens.")
    if re.fullmatch(r"con|prn|aux|nul|com[1-9]|lpt[1-9]", slug):
        raise ValueError("That name is reserved on Windows; choose another business slug.")
    workspace = Path(root).resolve()
    base = (workspace / "runs").resolve()
    if not base.is_relative_to(workspace):
        raise ValueError("The private runs folder must stay inside this workspace.")
    target = (base / slug).resolve()
    if not target.is_relative_to(base):
        raise ValueError("The run must stay inside the private runs folder.")
    return target


def init_run(root, slug, mode="demo"):
    if mode not in ("demo", "live"):
        raise ValueError("Mode must be demo or live.")
    target = run_path(root, slug)
    if target.exists():
        raise ValueError("That business already has a run. Resume it; nothing was overwritten.")
    templates = Path(root) / "templates"
    state = json.loads((templates / "state.json").read_text(encoding="utf-8-sig"))
    state["mode"] = mode
    target.mkdir(parents=True)
    (target / "evidence").mkdir()
    for name in ("brief.md", "campaign-plan.md", "ad-concepts.md", "launch-review.md", "NEXT.md"):
        shutil.copyfile(templates / name, target / name)
    (target / "state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return target


def load_state(run):
    state = json.loads((Path(run) / "state.json").read_text(encoding="utf-8-sig"))
    if not isinstance(state, dict):
        raise ValueError("state.json must contain a JSON object.")
    return state


def config_digest(state):
    config = state.get("configuration")
    if not isinstance(config, dict):
        raise ValueError("configuration must be a JSON object.")
    payload = json.dumps(config, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def valid_text(value):
    return isinstance(value, str) and bool(value.strip())


def positive(value):
    return type(value) in (int, float) and math.isfinite(value) and value > 0


def aware_time(value):
    if not valid_text(value):
        return None
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return result if result.utcoffset() is not None else None
    except ValueError:
        return None


def validate_state(state, run, launch=False):
    """Return missing/invalid local records, not a certification of external state."""
    errors = []
    if not isinstance(state, dict):
        return ["State must be a JSON object."]
    if type(state.get("schema_version")) is not int or state["schema_version"] != 1:
        errors.append("Use schema_version 1.")
    if state.get("mode") not in ("demo", "live"):
        errors.append("Choose mode demo or live.")
    config = state.get("configuration")
    if not isinstance(config, dict):
        return errors + ["configuration must be a JSON object."]

    def group(name):
        value = config.get(name)
        if not isinstance(value, dict):
            errors.append(f"configuration.{name} must be an object.")
            return {}
        return value

    def required(data, keys, label):
        for key in keys:
            if not valid_text(data.get(key)):
                errors.append(f"Missing {label}.{key}.")

    business = group("business")
    required(business, ("name", "service", "customer", "offer"), "business")
    if not positive(business.get("capacity")):
        errors.append("Record positive business.capacity for this campaign's outcome, with its period in brief.md.")
    settings = group("settings")
    for label, values in (("business.service_area", business.get("service_area")),
                          ("settings.geography", settings.get("geography"))):
        if not isinstance(values, list) or not values or not all(valid_text(x) for x in values):
            errors.append(f"Record a nonempty list for {label}.")
    required(settings, ("objective", "audience", "placements", "optimization", "category"), "settings")
    account = group("account")
    required(account, ("id", "page_id", "currency", "timezone"), "account")
    budget = group("budget")
    if budget.get("type") not in ("daily", "lifetime"):
        errors.append("Choose budget.type daily or lifetime.")
    for key in ("amount", "max_total"):
        if not positive(budget.get(key)):
            errors.append(f"Record a positive budget.{key}.")
    if positive(budget.get("amount")) and positive(budget.get("max_total")) and budget["amount"] > budget["max_total"]:
        errors.append("Budget amount exceeds the maximum total authorized spend.")
    currency = budget.get("currency")
    if not isinstance(currency, str) or not re.fullmatch(r"[A-Z]{3}", currency):
        errors.append("Record a three-letter uppercase budget.currency.")
    elif currency != account.get("currency"):
        errors.append("Budget currency must match the actual account currency.")
    start, end = aware_time(budget.get("start")), aware_time(budget.get("end"))
    if start is None or end is None:
        errors.append("Budget start/end must be ISO timestamps with timezone offsets.")
    elif end <= start:
        errors.append("Budget end must be later than start.")
    destination = group("destination")
    if destination.get("type") not in ("instant_form", "website"):
        errors.append("Choose destination.type instant_form or website.")
    required(destination, ("reference", "privacy_url"), "destination")
    privacy = destination.get("privacy_url")
    try:
        url = urlparse(privacy) if isinstance(privacy, str) else None
    except ValueError:
        url = None
    if not url or url.scheme != "https" or not url.netloc or url.username or url.password:
        errors.append("Use an HTTPS privacy URL without embedded credentials.")
    route = group("lead_route")
    required(route, ("owner", "method", "destination", "response_expectation"), "lead_route")
    ads = config.get("ads")
    if not isinstance(ads, list) or not ads:
        errors.append("Record at least one approved ad concept/asset mapping.")
    else:
        for i, ad in enumerate(ads):
            if not isinstance(ad, dict):
                errors.append(f"ads[{i}] must be an object.")
                continue
            required(ad, ("id", "concept", "copy", "asset", "destination"), f"ads[{i}]")
    objects = config.get("objects")
    if not isinstance(objects, list) or not objects:
        errors.append("Record saved campaign, ad_set and ad objects.")
    else:
        kinds, ids = set(), set()
        for obj in objects:
            if not isinstance(obj, dict):
                errors.append("Each saved object must be an object.")
                continue
            kind, identity = obj.get("kind"), obj.get("id")
            if kind not in ("campaign", "ad_set", "ad"):
                errors.append("Saved object kind must be campaign, ad_set or ad.")
            else:
                kinds.add(kind)
            if not valid_text(identity) or identity in ids:
                errors.append("Saved objects need distinct nonempty string IDs.")
            else:
                ids.add(identity)
            if obj.get("status") != "PAUSED":
                errors.append("Every reviewed object must have actual PAUSED status before launch.")
        if kinds != {"campaign", "ad_set", "ad"}:
            errors.append("Saved objects must include campaign, ad_set and ad.")
        if isinstance(ads, list):
            saved_ad_ids = {o.get("id") for o in objects if isinstance(o, dict) and o.get("kind") == "ad" and valid_text(o.get("id"))}
            mapped_ids = {a.get("id") for a in ads if isinstance(a, dict) and valid_text(a.get("id"))}
            if mapped_ids != saved_ad_ids:
                errors.append("Approved ad mappings must match the saved ad IDs exactly.")
    checks = state.get("checks")
    checks = checks if isinstance(checks, dict) else {}
    root = Path(run).resolve()
    for name in CHECKS:
        check = checks.get(name)
        if not isinstance(check, dict) or check.get("passed") is not True:
            errors.append(f"Not verified: {name}.")
            continue
        evidence = check.get("evidence")
        if not valid_text(evidence):
            errors.append(f"Missing evidence file for {name}.")
            continue
        evidence_path = Path(evidence)
        target = (root / evidence_path).resolve()
        if evidence_path.is_absolute() or not target.is_relative_to(root) or not target.is_file() or target.stat().st_size == 0:
            errors.append(f"Evidence for {name} must be a nonempty file inside this run.")
    if launch:
        if state.get("mode") != "live":
            errors.append("Demo mode cannot be approved for live activation.")
        approval = state.get("approval")
        approval = approval if isinstance(approval, dict) else {}
        if approval.get("decision") != "activate":
            errors.append("No recorded owner decision to activate.")
        required(approval, ("by", "source"), "approval")
        if aware_time(approval.get("at")) is None:
            errors.append("Record approval.at with a timezone offset.")
        try:
            if approval.get("config_sha256") != config_digest(state):
                errors.append("Owner approval is missing or stale for this configuration.")
        except (ValueError, TypeError):
            errors.append("Configuration is not valid canonical JSON.")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="Create a private local workspace; no external actions")
    init.add_argument("slug")
    init.add_argument("--mode", choices=("demo", "live"), default="demo")
    for name in ("status", "check"):
        cmd = sub.add_parser(name)
        cmd.add_argument("slug")
        if name == "check":
            cmd.add_argument("--launch", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            print(f"Created {init_run(ROOT, args.slug, args.mode)}. No service was contacted.")
            return 0
        run = run_path(ROOT, args.slug)
        state = load_state(run)
        if args.command == "status":
            print(f"Run: {args.slug}; mode: {state.get('mode')}; stage: {state.get('stage')}")
            print(f"Configuration SHA-256: {config_digest(state)}")
            print("Read NEXT.md for decisions and the next action. This is local status only.")
            return 0
        errors = validate_state(state, run, args.launch)
        print(f"Configuration SHA-256: {config_digest(state)}")
        print("Local records only: not live Meta verification or permission to spend.")
        if errors:
            for error in errors:
                print(f"- {error}")
            return 1
        print("Local review records complete. Inspect live objects and the owner's current approval before acting.")
        return 0
    except (ValueError, OSError, TypeError) as error:
        print(f"Cannot continue: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
