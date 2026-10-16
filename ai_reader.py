"""Day 4: suggest interest tags from portfolio text, with Claude or with the offline keyword reader.

The AI only suggests tags, each with a quote as evidence. find_programmes still does the matching,
and portfolio.py checks every suggestion before it is used.
"""
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path
from data_loader import load_json
from settings import AI_MODE, AI_MODEL

INFO = load_json("dataset-info.json")
KEYWORDS = load_json("portfolio-keywords.json")
API_URL = "https://api.anthropic.com/v1/messages"
MAX_INTERESTS = 4


def build_prompt(text):
    """The instructions sent to Claude, followed by the portfolio text."""
    tags = ", ".join(INFO["interest_tags"])
    # TODO 11: Write the instructions for Claude. Your instructions must:
    # 11a. Say the portfolio is fictional and the task is to suggest interests, not to judge.
    # 11b. Allow only the tags in tags, and at most MAX_INTERESTS of them.
    # 11c. Ask for a short quote, copied word for word from the portfolio, as evidence for each tag.
    # 11d. Forbid grades, admission chances and personal details in the reply.
    # 11e. Ask for JSON only, in exactly this shape: {"interests": [{"tag": "...", "quote": "..."}]}
    # เขียนคำสั่งถึง Claude: แฟ้มเป็นเรื่องสมมติ ใช้เฉพาะแท็กที่กำหนด ยกคำพูดจากแฟ้มเป็นหลักฐาน
    # ห้ามพูดถึงเกรด โอกาสรับเข้า หรือข้อมูลส่วนตัว และตอบเป็น JSON ตามรูปแบบนี้เท่านั้น
    instructions = "TODO 11: write the instructions"
    return instructions + "\n\nPortfolio text:\n" + text


def api_key():
    """Supplied: the key from the environment, or from a .env file in this folder. Never put it in code."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return os.environ["ANTHROPIC_API_KEY"]
    env = Path(__file__).resolve().parent / ".env"
    if env.is_file():
        for line in env.read_text(encoding="utf-8").splitlines():
            name, _, value = line.partition("=")
            if name.strip() == "ANTHROPIC_API_KEY":
                return value.strip().strip('"') or None
    return None


def ask_claude(prompt, key):
    """Supplied: one request to the Claude API. Like fetch() on Day 3, but from Python."""
    body = json.dumps({"model": AI_MODEL, "max_tokens": 500,
                       "messages": [{"role": "user", "content": prompt}]}).encode("utf-8")
    request = urllib.request.Request(API_URL, data=body, method="POST", headers={
        "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)
    return "".join(block.get("text", "") for block in data["content"] if block.get("type") == "text")


def parse_reply(reply):
    """Supplied: find the JSON in the model's reply. Return [{"tag", "quote"}, ...]; [] if unusable."""
    match = re.search(r"\{.*\}", reply, re.S)
    try:
        data = json.loads(match.group(0)) if match else {}
    except json.JSONDecodeError:
        return []
    items, seen = [], set()
    for item in data.get("interests", []) if isinstance(data, dict) else []:
        if isinstance(item, dict) and isinstance(item.get("tag"), str) and isinstance(item.get("quote"), str):
            tag = item["tag"].strip().lower()
            if tag not in seen:
                seen.add(tag)
                items.append({"tag": tag, "quote": item["quote"].strip()})
    return items[:MAX_INTERESTS]


def sentence_with(text, start):
    """Supplied: the sentence (or line) around position start, at most 200 characters."""
    stops = ".!?\n"
    left = max(text.rfind(mark, 0, start) for mark in stops) + 1
    ends = [text.find(mark, start) for mark in stops if text.find(mark, start) != -1]
    right = min(ends, default=len(text))
    if right < len(text) and text[right] in ".!?":
        right += 1  # Keep the full stop.
    return text[left:right].strip()[:200]


def offline_reader(text):
    """Supplied: no AI. Count each tag's keywords; quote the sentence where the first one appears."""
    lowered = text.lower()
    found = []
    for tag, words in KEYWORDS.items():
        positions = [lowered.find(word.lower()) for word in words if word.lower() in lowered]
        if positions:
            found.append((len(positions), tag, min(positions)))
    found.sort(key=lambda item: item[0], reverse=True)  # Most keywords first; ties keep file order.
    return [{"tag": tag, "quote": sentence_with(text, start)} for _, tag, start in found[:MAX_INTERESTS]]


def quote_found(quote, text):
    """Supplied: True if the quote really is in the portfolio, ignoring case and spaces."""
    def squash(value):
        return "".join(value.lower().split())
    return bool(squash(quote)) and squash(quote) in squash(text)


def read_interests(text):
    """Return {"reader": "claude" or "offline", "items": [{"tag", "quote"}, ...], "notes": [...]}."""
    key = api_key()
    if AI_MODE == "offline" or (AI_MODE == "auto" and not key):
        return {"reader": "offline", "items": offline_reader(text), "notes": []}
    if not key:
        return {"reader": "offline", "items": offline_reader(text),
                "notes": ["no ANTHROPIC_API_KEY is set, so the offline reader was used"]}
    try:
        reply = ask_claude(build_prompt(text), key)
    except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as error:
        return {"reader": "offline", "items": offline_reader(text),
                "notes": [f"Claude could not answer ({type(error).__name__}), so the offline reader was used"]}
    return {"reader": "claude", "items": parse_reply(reply), "notes": []}
