#!/usr/bin/env python3
"""
ActivityWatch Daily Summary Generator

Queries ActivityWatch REST API for daily activity data and generates
a markdown summary suitable for Obsidian daily notes.
"""

import argparse
import json
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlencode


AW_BASE_URL = "http://localhost:5600"
HOSTNAME = "SSOEBIOEBN438L7"

BUCKETS = {
    "window": f"aw-watcher-window_{HOSTNAME}",
    "afk": f"aw-watcher-afk_{HOSTNAME}",
    "obsidian": f"aw-watcher-obsidian_{HOSTNAME}",
    "vscode": f"aw-watcher-vscode_{HOSTNAME}",
}


def make_request(endpoint: str, params: Optional[Dict[str, str]] = None) -> Any:
    """Make a request to the ActivityWatch API."""
    url = f"{AW_BASE_URL}{endpoint}"
    if params:
        url = f"{url}?{urlencode(params)}"

    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        raise ConnectionError(f"Could not connect to ActivityWatch at {AW_BASE_URL}: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response from {url}: {e}")


def get_bucket_events(bucket_id: str, start: datetime, end: datetime) -> List[Dict[str, Any]]:
    """Fetch events from a specific bucket for the given time range."""
    params = {
        "start": start.isoformat(),
        "end": end.isoformat(),
    }

    try:
        events = make_request(f"/api/0/buckets/{bucket_id}/events", params)
        return events if events else []
    except (ConnectionError, ValueError):
        # Bucket might not exist, return empty
        return []


def check_aw_running() -> bool:
    """Check if ActivityWatch is running."""
    try:
        make_request("/api/0/buckets/")
        return True
    except (ConnectionError, ValueError):
        return False


def get_available_buckets() -> List[str]:
    """Get list of available buckets."""
    try:
        buckets = make_request("/api/0/buckets/")
        return list(buckets.keys())
    except (ConnectionError, ValueError):
        return []


def calculate_total_active_time(afk_events: List[Dict[str, Any]]) -> float:
    """Calculate total active (non-AFK) time in seconds."""
    total_seconds = 0.0
    for event in afk_events:
        if event.get("data", {}).get("status") == "not-afk":
            total_seconds += event.get("duration", 0)
    return total_seconds


def aggregate_window_apps(window_events: List[Dict[str, Any]]) -> List[Tuple[str, float]]:
    """Aggregate time spent per app from window events."""
    app_times = defaultdict(float)

    for event in window_events:
        app = event.get("data", {}).get("app", "Unknown")
        duration = event.get("duration", 0)
        app_times[app] += duration

    # Sort by duration descending
    return sorted(app_times.items(), key=lambda x: x[1], reverse=True)


def aggregate_obsidian_notes(obsidian_events: List[Dict[str, Any]]) -> List[Tuple[str, float]]:
    """Aggregate time spent per Obsidian note."""
    note_times = defaultdict(float)

    for event in obsidian_events:
        file = event.get("data", {}).get("file", "Unknown")
        duration = event.get("duration", 0)
        note_times[file] += duration

    return sorted(note_times.items(), key=lambda x: x[1], reverse=True)


def aggregate_vscode_projects(vscode_events: List[Dict[str, Any]]) -> List[Tuple[str, float]]:
    """Aggregate time spent per VS Code project/file."""
    project_times = defaultdict(float)

    for event in vscode_events:
        data = event.get("data", {})
        # Try to get project or file path
        project = data.get("project") or data.get("file") or "Unknown"
        duration = event.get("duration", 0)
        project_times[project] += duration

    return sorted(project_times.items(), key=lambda x: x[1], reverse=True)


def categorize_time_blocks(window_events: List[Dict[str, Any]]) -> Dict[str, float]:
    """Categorize activity into time blocks (morning/afternoon/evening)."""
    blocks = {
        "morning": 0.0,      # 5am-12pm
        "afternoon": 0.0,    # 12pm-5pm
        "evening": 0.0,      # 5pm-12am
        "night": 0.0,        # 12am-5am
    }

    for event in window_events:
        timestamp = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
        duration = event.get("duration", 0)
        hour = timestamp.hour

        if 5 <= hour < 12:
            blocks["morning"] += duration
        elif 12 <= hour < 17:
            blocks["afternoon"] += duration
        elif 17 <= hour < 24:
            blocks["evening"] += duration
        else:
            blocks["night"] += duration

    return blocks


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable string."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)

    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"


def generate_markdown_summary(
    date: datetime,
    total_active: float,
    app_times: List[Tuple[str, float]],
    obsidian_notes: List[Tuple[str, float]],
    vscode_projects: List[Tuple[str, float]],
    time_blocks: Dict[str, float],
) -> str:
    """Generate markdown summary."""
    lines = []

    lines.append(f"# ActivityWatch Summary - {date.strftime('%Y-%m-%d')}")
    lines.append("")

    # Total active time
    lines.append("## Overview")
    lines.append(f"- **Total Active Time:** {format_duration(total_active)}")
    lines.append("")

    # Time blocks
    lines.append("## Time Distribution")
    for block, duration in time_blocks.items():
        if duration > 0:
            lines.append(f"- **{block.capitalize()}:** {format_duration(duration)}")
    lines.append("")

    # Top apps
    if app_times:
        lines.append("## Top Applications")
        for app, duration in app_times[:10]:  # Top 10
            lines.append(f"- **{app}:** {format_duration(duration)}")
        lines.append("")

    # Obsidian notes
    if obsidian_notes:
        lines.append("## Obsidian Activity")
        for note, duration in obsidian_notes[:15]:  # Top 15
            lines.append(f"- `{note}` — {format_duration(duration)}")
        lines.append("")

    # VS Code projects
    if vscode_projects:
        lines.append("## VS Code Activity")
        for project, duration in vscode_projects[:15]:  # Top 15
            lines.append(f"- `{project}` — {format_duration(duration)}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate daily ActivityWatch summary in markdown format"
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Date in YYYY-MM-DD format (defaults to today)",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (defaults to stdout)",
    )
    args = parser.parse_args()

    # Parse date
    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print(f"Error: Invalid date format '{args.date}'. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
    else:
        target_date = datetime.now()

    # Set time range (start of day to end of day)
    start = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)

    # Check if AW is running
    if not check_aw_running():
        print("Error: ActivityWatch is not running or not accessible at http://localhost:5600", file=sys.stderr)
        print("Please start ActivityWatch and try again.", file=sys.stderr)
        sys.exit(1)

    # Get available buckets
    available = get_available_buckets()
    print(f"Found {len(available)} buckets", file=sys.stderr)

    # Fetch events from all buckets
    print("Fetching window events...", file=sys.stderr)
    window_events = get_bucket_events(BUCKETS["window"], start, end)

    print("Fetching AFK events...", file=sys.stderr)
    afk_events = get_bucket_events(BUCKETS["afk"], start, end)

    print("Fetching Obsidian events...", file=sys.stderr)
    obsidian_events = get_bucket_events(BUCKETS["obsidian"], start, end)

    print("Fetching VS Code events...", file=sys.stderr)
    vscode_events = get_bucket_events(BUCKETS["vscode"], start, end)

    # Calculate metrics
    print("Calculating metrics...", file=sys.stderr)
    total_active = calculate_total_active_time(afk_events)
    app_times = aggregate_window_apps(window_events)
    obsidian_notes = aggregate_obsidian_notes(obsidian_events)
    vscode_projects = aggregate_vscode_projects(vscode_events)
    time_blocks = categorize_time_blocks(window_events)

    # Generate summary
    summary = generate_markdown_summary(
        target_date,
        total_active,
        app_times,
        obsidian_notes,
        vscode_projects,
        time_blocks,
    )

    # Output
    if args.output:
        with open(args.output, "w") as f:
            f.write(summary)
        print(f"Summary written to {args.output}", file=sys.stderr)
    else:
        print(summary)


if __name__ == "__main__":
    main()
