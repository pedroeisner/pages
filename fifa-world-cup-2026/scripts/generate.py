import os
import re
import sys
import html
import hashlib
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from typing import Any, Dict, List, Optional, Tuple

import requests
from icalendar import Calendar, Event, vText

API_BASE = "https://v3.football.api-sports.io"
LEAGUE_ID = 1
SEASON = 2026
OUTPUT_FILE = "worldcup2026.ics"
CALENDAR_TZ = "America/New_York"

COUNTRY_FLAGS = {
    "Argentina": "🇦🇷", "Australia": "🇦🇺", "Austria": "🇦🇹", "Belgium": "🇧🇪", "Brazil": "🇧🇷",
    "Canada": "🇨🇦", "Chile": "🇨🇱", "Colombia": "🇨🇴", "Costa Rica": "🇨🇷", "Croatia": "🇭🇷",
    "Czech Republic": "🇨🇿", "Denmark": "🇩🇰", "Ecuador": "🇪🇨", "Egypt": "🇪🇬", "England": "🏴",
    "France": "🇫🇷", "Germany": "🇩🇪", "Ghana": "🇬🇭", "Iran": "🇮🇷", "Italy": "🇮🇹",
    "Japan": "🇯🇵", "Mexico": "🇲🇽", "Morocco": "🇲🇦", "Netherlands": "🇳🇱", "New Zealand": "🇳🇿",
    "Norway": "🇳🇴", "Paraguay": "🇵🇾", "Poland": "🇵🇱", "Portugal": "🇵🇹", "Qatar": "🇶🇦",
    "Saudi Arabia": "🇸🇦", "Scotland": "🏴", "Senegal": "🇸🇳", "Serbia": "🇷🇸", "South Africa": "🇿🇦",
    "South Korea": "🇰🇷", "Spain": "🇪🇸", "Switzerland": "🇨🇭", "Tunisia": "🇹🇳", "Uruguay": "🇺🇾",
    "USA": "🇺🇸", "United States": "🇺🇸", "Wales": "🏴", "Ukraine": "🇺🇦", "Turkey": "🇹🇷",
}

# Optional normalization for names that APIs commonly vary.
TEAM_ALIASES = {
    "Korea Republic": "South Korea",
    "United States": "USA",
    "Czechia": "Czech Republic",
}


def api_get(path: str, params: Dict[str, Any]) -> Dict[str, Any]:
    key = os.getenv("API_FOOTBALL_KEY")
    if not key:
        raise RuntimeError("Missing API_FOOTBALL_KEY secret")
    r = requests.get(
        f"{API_BASE}{path}",
        params=params,
        headers={"x-apisports-key": key},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    errors = data.get("errors")
    if errors:
        raise RuntimeError(f"API returned errors: {errors}")
    return data


def norm_team(name: Optional[str]) -> str:
    if not name:
        return "TBD"
    return TEAM_ALIASES.get(name, name)


def flag_for(team: str) -> str:
    return COUNTRY_FLAGS.get(team, "")


def title_for(team1: str, team2: str) -> str:
    left_flag = flag_for(team1)
    right_flag = flag_for(team2)
    left = f"{left_flag} {team1}" if left_flag else team1
    right = f"{right_flag} {team2}" if right_flag else team2
    return f"{left} - {right}"


def is_group_stage(round_name: str) -> bool:
    return "group" in round_name.lower()


def stage_from_round(round_name: str) -> str:
    text = round_name.replace("Group Stage", "Group stage")
    return text.strip() or "FIFA World Cup 2026"


def build_group_map(standings_response: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    groups: Dict[str, List[str]] = {}
    for comp in standings_response:
        league = comp.get("league", {})
        for table in league.get("standings", []) or []:
            group_name = None
            teams = []
            for row in table:
                group_name = group_name or row.get("group") or row.get("description")
                team = row.get("team", {}).get("name")
                if team:
                    teams.append(norm_team(team))
            if group_name and teams:
                groups[group_name] = teams
    return groups


def infer_group_from_fixture(fixture: Dict[str, Any]) -> Optional[str]:
    league_round = fixture.get("league", {}).get("round", "")
    # API-Football rounds may be "Group Stage - 1" and may not include group letter.
    # If a fixture exposes a group elsewhere, use it. Otherwise leave blank.
    for key_path in [
        ("league", "group"),
        ("group", "name"),
        ("group",),
    ]:
        cur = fixture
        ok = True
        for k in key_path:
            if isinstance(cur, dict) and k in cur:
                cur = cur[k]
            else:
                ok = False
                break
        if ok and isinstance(cur, str) and cur:
            return cur
    # Common placeholder in some sources: "Group A - 1"
    m = re.search(r"Group\s+([A-L])", league_round, re.I)
    if m:
        return f"Group {m.group(1).upper()}"
    return None


def description_for(stage: str, group_name: Optional[str], group_teams: Optional[List[str]]) -> str:
    lines = [f"Stage: {stage}"]
    if group_name:
        lines.append(f"Group: {group_name}")
    if group_teams:
        lines.append("Teams in group: " + ", ".join(group_teams))
    lines.append("Auto-updated World Cup 2026 calendar feed.")
    return "\n".join(lines)


def parse_utc_datetime(value: str) -> datetime:
    # API-Football dates are ISO 8601 with timezone, e.g. 2026-06-11T19:00:00+00:00
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value).astimezone(timezone.utc)


def stable_uid(fixture_id: Any) -> str:
    raw = f"fifa-world-cup-2026-{fixture_id}@pedro-calendar"
    return raw


def event_duration(stage: str) -> timedelta:
    lower = stage.lower()
    if "group" in lower:
        return timedelta(hours=2)
    return timedelta(hours=3)


def main() -> int:
    fixtures_data = api_get("/fixtures", {"league": LEAGUE_ID, "season": SEASON})
    standings_data = api_get("/standings", {"league": LEAGUE_ID, "season": SEASON})

    fixtures = fixtures_data.get("response", [])
    group_map = build_group_map(standings_data.get("response", []))

    cal = Calendar()
    cal.add("prodid", "-//Pedro Eisner//FIFA World Cup 2026 Auto Calendar//EN")
    cal.add("version", "2.0")
    cal.add("calscale", "GREGORIAN")
    cal.add("method", "PUBLISH")
    cal.add("x-wr-calname", "FIFA World Cup 2026")
    cal.add("x-wr-timezone", CALENDAR_TZ)
    cal.add("x-published-ttl", "PT3H")

    generated_at = datetime.now(timezone.utc)

    for item in sorted(fixtures, key=lambda x: x.get("fixture", {}).get("date", "")):
        fixture = item.get("fixture", {})
        league = item.get("league", {})
        teams = item.get("teams", {})
        venue = fixture.get("venue", {}) or {}

        fixture_id = fixture.get("id")
        date_value = fixture.get("date")
        if not fixture_id or not date_value:
            continue

        start = parse_utc_datetime(date_value)
        round_name = league.get("round") or "FIFA World Cup 2026"
        stage = stage_from_round(round_name)

        team1 = norm_team((teams.get("home") or {}).get("name"))
        team2 = norm_team((teams.get("away") or {}).get("name"))

        group_name = infer_group_from_fixture(item) if is_group_stage(round_name) else None
        group_teams = group_map.get(group_name or "") if group_name else None

        ev = Event()
        ev.add("uid", stable_uid(fixture_id))
        ev.add("dtstamp", generated_at)
        ev.add("dtstart", start)
        ev.add("dtend", start + event_duration(stage))
        ev.add("summary", title_for(team1, team2))

        stadium = venue.get("name") or venue.get("city") or ""
        city = venue.get("city") or ""
        location = stadium if stadium and city in stadium else ", ".join([p for p in [stadium, city] if p])
        if location:
            ev.add("location", vText(location))

        ev.add("description", description_for(stage, group_name, group_teams))
        ev.add("status", "CONFIRMED")
        cal.add_component(ev)

    with open(OUTPUT_FILE, "wb") as f:
        f.write(cal.to_ical())

    print(f"Wrote {OUTPUT_FILE} with {len(fixtures)} fixtures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
