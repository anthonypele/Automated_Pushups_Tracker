import json
from datetime import datetime

from utilities.choose_file import choose_file

# -------- settings you edit ----------
FROM_ID_TO_NAME = {
    "user5594775531": "Роман Аландаров",
    "user117031123": "Павел Антонюк РТ",
    "user971233787": "Анна Русанова РТ"
    # "user1234567890": "Roma",
}
# -------------------------------------

def is_pure_number(text: str) -> bool:
    return isinstance(text, str) and text.isdigit()

def format_date(date_str: str) -> str:
    dt = datetime.fromisoformat(date_str)
    return dt.strftime("%d.%m.%Y %H:%M")

def main():
    with open(choose_file(), "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict) or "messages" not in data:
        raise ValueError('Expected JSON like {"messages": [...]}')

    unknown_ids = set()  # ← collect unknown users only once

    for msg in data["messages"]:
        if msg.get("type") != "message":
            continue

        from_id = msg.get("from_id")
        if not isinstance(from_id, str):
            continue

        text = msg.get("text")
        if not is_pure_number(text):
            continue

        date_str = msg.get("date")
        if not isinstance(date_str, str):
            continue

        name = FROM_ID_TO_NAME.get(from_id)

        if not name:
            unknown_ids.add(from_id)
            continue

        print(f"[{format_date(date_str)}] {name}: {int(text)}")

    # Report unknown users at the end
    if unknown_ids:
        print("\nUnknown from_id values (add them to FROM_ID_TO_NAME):")
        for uid in sorted(unknown_ids):
            print(uid)

if __name__ == "__main__":
    main()
