#!/usr/bin/env python3
"""
ActivityWatch Android Import Script

Imports events from ActivityWatch Android app JSON export into local AW server.
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Any, Dict, List
from urllib import request, error
from urllib.parse import quote


class AWImporter:
    def __init__(self, base_url: str = "http://localhost:5600"):
        self.base_url = base_url.rstrip("/")
        self.stats = {
            "buckets_created": 0,
            "events_imported": 0,
            "events_skipped": 0,
            "errors": 0,
        }

    def _make_request(
        self, method: str, endpoint: str, data: Any = None
    ) -> Dict[str, Any]:
        """Make HTTP request to AW server."""
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}

        req_data = json.dumps(data).encode("utf-8") if data else None
        req = request.Request(url, data=req_data, headers=headers, method=method)

        try:
            with request.urlopen(req) as response:
                if response.status in (200, 201, 304):
                    body = response.read().decode("utf-8")
                    return json.loads(body) if body else {}
                else:
                    raise Exception(f"Unexpected status: {response.status}")
        except error.HTTPError as e:
            if e.code == 304:  # Not Modified - bucket already exists
                return {}
            error_body = e.read().decode("utf-8") if e.fp else ""
            raise Exception(f"HTTP {e.code}: {error_body}")

    def bucket_exists(self, bucket_id: str) -> bool:
        """Check if bucket exists on server."""
        try:
            self._make_request("GET", f"/api/0/buckets/{quote(bucket_id)}")
            return True
        except Exception:
            return False

    def create_bucket(self, bucket_id: str, bucket_data: Dict[str, Any]) -> None:
        """Create bucket on AW server."""
        # Extract metadata from bucket
        client = bucket_data.get("client", "unknown")
        bucket_type = bucket_data.get("type", "unknown")
        hostname = bucket_data.get("hostname", "android")

        payload = {
            "client": client,
            "type": bucket_type,
            "hostname": hostname,
        }

        try:
            self._make_request("POST", f"/api/0/buckets/{quote(bucket_id)}", payload)
            self.stats["buckets_created"] += 1
            print(f"  Created bucket: {bucket_id}")
        except Exception as e:
            if "already exists" in str(e).lower():
                print(f"  Bucket already exists: {bucket_id}")
            else:
                raise

    def get_existing_events(self, bucket_id: str) -> List[str]:
        """Get timestamps of existing events to detect duplicates."""
        try:
            response = self._make_request(
                "GET", f"/api/0/buckets/{quote(bucket_id)}/events"
            )
            return [event["timestamp"] for event in response]
        except Exception:
            return []

    def import_events(
        self, bucket_id: str, events: List[Dict[str, Any]], show_progress: bool = True
    ) -> None:
        """Import events into bucket."""
        if not events:
            print(f"  No events to import for {bucket_id}")
            return

        # Get existing event timestamps to avoid duplicates
        existing_timestamps = set(self.get_existing_events(bucket_id))
        print(f"  Found {len(existing_timestamps)} existing events")

        # Filter out duplicates
        new_events = [
            e for e in events if e["timestamp"] not in existing_timestamps
        ]

        if not new_events:
            print(f"  All events already exist, skipping")
            self.stats["events_skipped"] += len(events)
            return

        print(f"  Importing {len(new_events)} new events (skipping {len(events) - len(new_events)} duplicates)")

        # Import events in batches
        batch_size = 100
        for i in range(0, len(new_events), batch_size):
            batch = new_events[i : i + batch_size]

            try:
                self._make_request(
                    "POST", f"/api/0/buckets/{quote(bucket_id)}/events/", batch
                )
                self.stats["events_imported"] += len(batch)

                if show_progress:
                    progress = min(i + batch_size, len(new_events))
                    print(f"    Progress: {progress}/{len(new_events)}", end="\r")

            except Exception as e:
                print(f"\n  Error importing batch: {e}")
                self.stats["errors"] += 1

        if show_progress:
            print()  # Newline after progress

        self.stats["events_skipped"] += len(events) - len(new_events)

    def import_from_file(self, file_path: str, hostname_suffix: str = "_android") -> None:
        """Import all buckets and events from JSON export file."""
        print(f"Loading export file: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}")
            sys.exit(1)

        if "buckets" not in data:
            print("Error: No 'buckets' key in export file")
            sys.exit(1)

        buckets = data["buckets"]
        print(f"Found {len(buckets)} buckets\n")

        for bucket_id, bucket_data in buckets.items():
            # Add hostname suffix to distinguish from desktop
            new_bucket_id = bucket_id
            if hostname_suffix and not bucket_id.endswith(hostname_suffix):
                # Split bucket_id and add suffix before the last part
                parts = bucket_id.rsplit("_", 1)
                if len(parts) == 2:
                    new_bucket_id = f"{parts[0]}{hostname_suffix}_{parts[1]}"
                else:
                    new_bucket_id = f"{bucket_id}{hostname_suffix}"

            print(f"Processing: {bucket_id} -> {new_bucket_id}")

            # Ensure hostname is set to android
            if "hostname" not in bucket_data:
                bucket_data["hostname"] = "android"

            try:
                # Create bucket if it doesn't exist
                if not self.bucket_exists(new_bucket_id):
                    self.create_bucket(new_bucket_id, bucket_data)
                else:
                    print(f"  Bucket exists: {new_bucket_id}")

                # Import events
                events = bucket_data.get("events", [])
                if events:
                    self.import_events(new_bucket_id, events)
                else:
                    print(f"  No events in bucket")

            except Exception as e:
                print(f"  Error: {e}")
                self.stats["errors"] += 1

            print()

    def print_summary(self) -> None:
        """Print import summary."""
        print("=" * 60)
        print("Import Summary:")
        print(f"  Buckets created: {self.stats['buckets_created']}")
        print(f"  Events imported: {self.stats['events_imported']}")
        print(f"  Events skipped (duplicates): {self.stats['events_skipped']}")
        print(f"  Errors: {self.stats['errors']}")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Import ActivityWatch Android export into local AW server"
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Path to JSON export file from AW Android app",
    )
    parser.add_argument(
        "--server",
        default="http://localhost:5600",
        help="ActivityWatch server URL (default: http://localhost:5600)",
    )
    parser.add_argument(
        "--suffix",
        default="_android",
        help="Hostname suffix to add to bucket IDs (default: _android)",
    )
    parser.add_argument(
        "--no-suffix",
        action="store_true",
        help="Don't add hostname suffix to bucket IDs",
    )

    args = parser.parse_args()

    suffix = "" if args.no_suffix else args.suffix

    importer = AWImporter(base_url=args.server)

    try:
        importer.import_from_file(args.file, hostname_suffix=suffix)
        importer.print_summary()
    except KeyboardInterrupt:
        print("\n\nImport cancelled by user")
        importer.print_summary()
        sys.exit(1)
    except Exception as e:
        print(f"\nFatal error: {e}")
        importer.print_summary()
        sys.exit(1)


if __name__ == "__main__":
    main()
