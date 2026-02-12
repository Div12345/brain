---
module: System
date: 2026-02-11
problem_type: workflow_issue
component: development_workflow
symptoms:
  - "Calendar events too sparse compared to day plan"
  - "Duplicate travel events conflicting with Reclaim auto-buffers"
  - "Generic location text instead of Google Maps addresses"
  - "Confusion about what belongs in calendar vs Day Planner"
root_cause: missing_workflow_step
resolution_type: workflow_improvement
severity: medium
tags: [google-calendar, obsidian, day-planner, reclaim, daily-planning, time-blocking]
---

# Troubleshooting: Daily Calendar and Obsidian Day Planner Integration Rules

## Problem
When creating Google Calendar events from an Obsidian Day Planner daily note, multiple iterations were needed to get the right level of detail, avoid conflicts with Reclaim AI auto-buffers, and use proper location formats.

## Environment
- Module: System (daily planning workflow)
- Tools: Google Calendar MCP, Obsidian Day Planner plugin, Reclaim AI
- Platform: Claude Code managing calendar + Obsidian via MCPs
- Date: 2026-02-11

## Symptoms
- First attempt: only 3 events (yoga, lab, dinner) — too sparse, missing personal blocks
- Added transit events manually → duplicated Reclaim's auto-generated travel buffers
- Location set as "The Shala, East Liberty, Pittsburgh" instead of actual street address
- User confused about which tool is source of truth

## What Didn't Work

**Attempted Solution 1:** Sparse calendar — only "important" events
- **Why it failed:** User wants to see full day structure on phone calendar, not just highlights. The Day Planner has all blocks; calendar should match.

**Attempted Solution 2:** Mirror everything including transit
- **Why it failed:** Reclaim AI automatically generates travel buffer events when a calendar event has a proper Google Maps location. Manually adding transit events creates duplicates that clutter the calendar.

**Attempted Solution 3:** Generic location text
- **Why it failed:** Reclaim needs real Google Maps addresses to calculate travel time and auto-generate buffers. "Bioengineering Lab, University of Pittsburgh" doesn't trigger Reclaim; "Benedum Hall, 3700 O'Hara St, Pittsburgh, PA 15213" does.

## Solution

**Rules for calendar ↔ Day Planner integration:**

1. **Mirror 1:1:** Every time block in the Day Planner gets a calendar event. Personal blocks (wake, get ready, bed) included.
2. **No transit events:** Reclaim auto-generates travel buffers when events have proper locations. Don't duplicate them.
3. **Real Google Maps addresses:** Use full street addresses for any location-based event so Reclaim can calculate travel time.
4. **Day Planner is the detailed source:** It has the fallback decisions, checklists, and notes. Calendar has the time blocks and locations.
5. **Calendar descriptions for context:** Lab work events get the task checklist in the event description field.

**Correct event creation pattern:**
```
Personal blocks (no location):  wake, get ready, cook, bed
Location blocks (real address):  yoga → "113 N Highland Ave, Pittsburgh, PA 15206"
                                 lab → "Benedum Hall, 3700 O'Hara St, Pittsburgh, PA 15213"
Skip entirely:                   transit (Reclaim handles it)
```

## Why This Works

1. **Single glance on phone:** User opens Google Calendar on Android and sees the full day, including personal routine blocks. No need to also check Obsidian.
2. **Reclaim integration:** Real addresses trigger Reclaim's travel time calculation. It creates buffer events automatically with correct durations.
3. **No confusion about source of truth:** Calendar = time blocks visible on phone. Day Planner = same blocks plus detailed notes/checklists/fallbacks.

## Prevention

- When creating daily calendar events from a Day Planner note, always mirror ALL blocks
- Never manually create transit/travel events — check if Reclaim or similar tool handles them
- Always use full street addresses from Google Maps, not descriptive location names
- Put task checklists in the calendar event description for lab/work blocks
- Ask user about their calendar automation tools (Reclaim, Clockwise, etc.) before creating events

## Related Issues

No related issues documented yet.
