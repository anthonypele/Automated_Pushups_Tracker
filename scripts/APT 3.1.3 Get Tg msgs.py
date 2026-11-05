import json
import datetime
import shutil
import os
import re

from utilities.choose_file import choose_file
from utilities.convert_time import convert_time
from utilities.aliases import FROM_TG_ID_TO_NAME

# =========================
# 1) Telegram settings
# =========================

def is_pure_number(text: str) -> bool:
    return isinstance(text, str) and text.isdigit()

def format_date_telegram(date_str: str) -> tuple[str, str]:
    """
    Telegram JSON date example: "2026-01-08T23:14:16"
    Output: ("DD.MM.YYYY", "HH:MM")
    No timezone handling.
    """
    dt = datetime.datetime.fromisoformat(date_str)
    return dt.strftime("%d.%m.%Y"), dt.strftime("%H:%M")

def extract_telegram_pushups(json_path: str) -> tuple[list[str], set[str]]:
    """
    Returns:
      - lines formatted as: "[DD.MM.YYYY HH:MM] [tg] Name: N"
      - unknown_ids: from_id values that are not in FROM_TG_ID_TO_NAME
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict) or "messages" not in data:
        raise ValueError('Expected JSON like {"messages": [...]}')

    lines = []
    unknown_ids = set()

    for msg in data["messages"]:
        if msg.get("type") != "message":
            continue

        from_id = msg.get("from_id")
        if not isinstance(from_id, str):
            continue

        text = msg.get("text")
        # exclude non-string text structures
        if not is_pure_number(text):
            continue

        date_str = msg.get("date")
        if not isinstance(date_str, str):
            continue

        name = FROM_TG_ID_TO_NAME.get(from_id)
        if not name:
            unknown_ids.add(from_id)
            continue

        date_ddmmyyyy, time_hhmm = format_date_telegram(date_str)

        # Your pipeline expects convert_time(date, time, name)
        new_date, new_time = convert_time(date_ddmmyyyy, time_hhmm, name)

        # Final format with TG tag
        lines.append(f'[{new_date} {new_time}] [tg] {name}: {int(text)}')

    return lines, unknown_ids


# =========================
# 2) File save logic + NEW de-dup (date+name)
# =========================

filename = "pushups_data2.txt"
save_folder = r"C:\Users\Anthony\YandexDisk\_Programming\APT\Data"
file_path = os.path.join(save_folder, filename)

# Parse lines of the form:
# [DD.MM.YYYY HH:MM] [tg] Name: N
# [DD.MM.YYYY HH:MM] Name: N          (tag optional)
LINE_RE = re.compile(
    r"^\[(\d{2}\.\d{2}\.\d{4})\s+\d{2}:\d{2}\]\s+(?:\[(\w+)\]\s+)?(.+?):\s+(\d+)\s*$"
)
# groups:
# 1) date "DD.MM.YYYY"   (time intentionally ignored)
# 2) optional source tag like "tg"/"wa"
# 3) name
# 4) number

def parse_key_date_name(line: str):
    """
    Returns:
      key: (date_str, name) OR None if line doesn't match
      source: 'tg'/'wa'/None
    """
    m = LINE_RE.match(line.strip())
    if not m:
        return None, None
    date_str, source, name, _num = m.groups()
    source = source.lower() if source else None
    name = name.strip()
    return (date_str, name), source

def prefer_line(existing_line: str, candidate_line: str) -> str:
    """
    Keep the one with [tg] when (date,name) collides.
    If both or neither are [tg], keep existing (stable).
    """
    _, src_existing = parse_key_date_name(existing_line)
    _, src_candidate = parse_key_date_name(candidate_line)

    if src_existing == "tg":
        return existing_line
    if src_candidate == "tg":
        return candidate_line
    return existing_line

def merge_unique_by_date_name(file_path: str, new_lines: list[str]) -> None:
    """
    Enforces uniqueness by (date, name) only.
    Prefers lines containing [tg] if collisions happen.
    Rewrites file with merged unique result.
    """
    # Read existing
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            existing_raw = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        existing_raw = []

    chosen = {}
    leftovers = []  # lines that don't match pattern; keep them as-is

    # Index existing
    for line in existing_raw:
        key, _src = parse_key_date_name(line)
        if key is None:
            leftovers.append(line)
            continue
        if key not in chosen:
            chosen[key] = line
        else:
            chosen[key] = prefer_line(chosen[key], line)

    # Merge new
    for line in new_lines:
        clean_line = line.strip()
        if not clean_line:
            continue

        key, _src = parse_key_date_name(clean_line)
        if key is None:
            leftovers.append(clean_line)
            continue

        if key not in chosen:
            chosen[key] = clean_line
        else:
            chosen[key] = prefer_line(chosen[key], clean_line)

    # Write merged result back
    with open(file_path, "w", encoding="utf-8") as f:
        for line in leftovers:
            f.write(line + "\n")
        for line in chosen.values():
            f.write(line + "\n")

def extract_datetime(line: str) -> datetime.datetime:
    try:
        timestamp = line.split("]")[0].strip("[")
        return datetime.datetime.strptime(timestamp, "%d.%m.%Y %H:%M")
    except Exception:
        print(f"⚠️ Could not parse line: {line}")
        return datetime.datetime.min

def backup_file(original_path: str) -> str:
    folder = os.path.dirname(original_path)
    name_only, ext = os.path.splitext(os.path.basename(original_path))

    backup_folder = os.path.join(folder, "Backup")
    os.makedirs(backup_folder, exist_ok=True)

    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    backup_filename = f"{name_only}_backup_{timestamp_str}{ext}"
    backup_path = os.path.join(backup_folder, backup_filename)

    if os.path.exists(original_path):
        shutil.copy(original_path, backup_path)
        print(f"🔒 Backup saved to: {backup_path}")
        return backup_path
    else:
        print("ℹ️ No original file to backup (file does not exist yet).")
        return ""

def sort_file_desc(file_path: str) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    lines.sort(key=extract_datetime, reverse=True)

    with open(file_path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


# =========================
# 3) MAIN with gating logic
# =========================

def main():
    telegram_json_path = choose_file()
    converted_lines, unknown_ids = extract_telegram_pushups(telegram_json_path)

    # (1) If there are unknown IDs -> print ONLY them and stop
    if unknown_ids:
        print("Unknown from_id values (add them to FROM_TG_ID_TO_NAME):")
        for uid in sorted(unknown_ids):
            print(uid)
        return

    # (2) If no unknown IDs -> update file with new "date+name unique" rule
    print(f"✅ Found {len(converted_lines)} valid pushup messages (all users recognized)")

    backup_file(file_path)

    # NEW: merge with uniqueness by (date, name) only, preferring [tg]
    merge_unique_by_date_name(file_path, converted_lines)

    # Keep your sort
    sort_file_desc(file_path)

    print("✅ File updated, de-duplicated by (date+name), and sorted successfully")
    os.startfile(file_path)

if __name__ == "__main__":
    main()
