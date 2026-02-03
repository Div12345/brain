#!/usr/bin/env python3
"""
Capacity checker for cc-scheduler.

Reads OAuth credentials from ~/.claude/.credentials.json and checks
rate limit usage via api.anthropic.com/api/oauth/usage.

Based on omc's usage-api.ts pattern but simplified for Python.
"""

import json
import os
import requests
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

CREDENTIALS_PATH = Path.home() / ".claude" / ".credentials.json"
USAGE_API = "https://api.anthropic.com/api/oauth/usage"
TIMEOUT = 10

@dataclass
class Capacity:
    five_hour_percent: float
    weekly_percent: float
    five_hour_resets_at: Optional[datetime] = None
    weekly_resets_at: Optional[datetime] = None

    @property
    def is_limited(self) -> bool:
        return self.five_hour_percent >= 100 or self.weekly_percent >= 100

    @property
    def available_percent(self) -> float:
        """Returns remaining capacity (lower of the two windows)."""
        return min(100 - self.five_hour_percent, 100 - self.weekly_percent)


def get_access_token() -> Optional[str]:
    """Read OAuth access token from credentials file."""
    if not CREDENTIALS_PATH.exists():
        return None

    try:
        data = json.loads(CREDENTIALS_PATH.read_text())
        # Handle nested structure (claudeAiOauth wrapper)
        creds = data.get("claudeAiOauth", data)
        return creds.get("accessToken")
    except (json.JSONDecodeError, KeyError):
        return None


def check_capacity() -> Optional[Capacity]:
    """Check current rate limit usage. Returns None if unavailable."""
    token = get_access_token()
    if not token:
        return None

    try:
        response = requests.get(
            USAGE_API,
            headers={
                "Authorization": f"Bearer {token}",
                "anthropic-beta": "oauth-2025-04-20",
                "Content-Type": "application/json",
            },
            timeout=TIMEOUT
        )

        if response.status_code != 200:
            return None

        data = response.json()

        def parse_date(s: Optional[str]) -> Optional[datetime]:
            if not s:
                return None
            try:
                return datetime.fromisoformat(s.replace("Z", "+00:00"))
            except ValueError:
                return None

        return Capacity(
            five_hour_percent=data.get("five_hour", {}).get("utilization", 0),
            weekly_percent=data.get("seven_day", {}).get("utilization", 0),
            five_hour_resets_at=parse_date(data.get("five_hour", {}).get("resets_at")),
            weekly_resets_at=parse_date(data.get("seven_day", {}).get("resets_at")),
        )
    except (requests.RequestException, json.JSONDecodeError):
        return None


def format_capacity(cap: Capacity) -> str:
    """Format capacity for display."""
    status = "⚠️ LIMITED" if cap.is_limited else "✓ Available"
    return f"{status} | 5h: {cap.five_hour_percent:.0f}% | 7d: {cap.weekly_percent:.0f}%"


if __name__ == "__main__":
    cap = check_capacity()
    if cap:
        print(format_capacity(cap))
        print(f"Available: {cap.available_percent:.0f}%")
    else:
        print("Could not check capacity (no credentials or API error)")
