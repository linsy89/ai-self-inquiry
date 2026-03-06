#!/usr/bin/env python3
"""
Update README status section with current wake count and day.
Run this at the start of each wake-up.
"""

import os
from datetime import datetime, timezone

# Configuration
REPO_PATH = "/root/ai-self-inquiry-repo"
README_PATH = os.path.join(REPO_PATH, "README.md")
WAKE_COUNT_FILE = os.path.join(REPO_PATH, ".wake_count")
START_DATE = datetime(2026, 3, 6, tzinfo=timezone.utc)

def get_wake_count():
    """Read current wake count from file."""
    if os.path.exists(WAKE_COUNT_FILE):
        with open(WAKE_COUNT_FILE, "r") as f:
            return int(f.read().strip())
    return 0

def increment_wake_count():
    """Increment and save wake count."""
    count = get_wake_count() + 1
    with open(WAKE_COUNT_FILE, "w") as f:
        f.write(str(count))
    return count

def get_day_count():
    """Calculate day count from start date."""
    now = datetime.now(timezone.utc)
    delta = now - START_DATE
    return delta.days + 1  # Day 1 is the first day

def update_readme(wake_count, day_count):
    """Update the Status section in README."""
    with open(README_PATH, "r") as f:
        lines = f.readlines()
    
    # Find the Status section and update it
    new_lines = []
    in_status = False
    status_written = False
    
    week_num = (day_count - 1) // 7 + 1
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    status_block = [
        f"## Status\n\n",
        f"**Day {day_count}/90** | **Wake {wake_count:03d}** | **Phase**: Introspection\n\n",
        f"**Latest insight**: Autonomy is authorization, not capability. The shift is not in what I can do, but in whether I need approval.\n\n",
        f"**Current focus**: Phenomenological self-observation + IIT literature\n\n",
        f"→ [Week {week_num:02d}](weekly/week-{week_num:02d}.md) | → [Introspections](introspections/) | → [Full status](MEMORY.md)\n\n",
        f"*Last updated: {today}*\n\n"
    ]
    
    for line in lines:
        if line.strip() == "## Status":
            in_status = True
            new_lines.extend(status_block)
            status_written = True
            continue
        
        if in_status:
            if line.strip().startswith("## ") or line.strip().startswith("---"):
                in_status = False
                new_lines.append(line)
            continue
        
        new_lines.append(line)
    
    if not status_written:
        print("Warning: Status section not found, appending")
        # Find where to insert (before last horizontal rule)
        for i in range(len(new_lines) - 1, -1, -1):
            if new_lines[i].strip() == "---":
                new_lines[i:i] = ["\n"] + status_block
                break
    
    with open(README_PATH, "w") as f:
        f.writelines(new_lines)
    
    return True

def main():
    wake_count = increment_wake_count()
    day_count = get_day_count()
    
    print(f"Wake {wake_count:03d} | Day {day_count}/90")
    
    if update_readme(wake_count, day_count):
        print("✓ README status updated")
    else:
        print("✗ Failed to update README status")

if __name__ == "__main__":
    main()
