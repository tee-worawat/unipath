"""Day 2: turn request values into safe preferences. The search API (Day 2) and the portfolio
route (Day 4) both use this, so a value from a browser or from an AI model is checked the same way.

Never trust values from a browser: anyone can type any URL.
ห้ามเชื่อค่าจากเบราว์เซอร์ ใครก็พิมพ์ URL อะไรก็ได้
"""
from data_loader import load_json

INFO = load_json("dataset-info.json")


def parse_preferences(args):
    """args is Flask's request.args. Return (preferences, problems)."""
    problems = []
    wanted = []
    region = "any"
    language = "any"
    include_unknown = False
    # TODO 6: Read the values the form sends. Find the field names in templates/index.html.
    # 6a. Interests: several checkboxes share one name, so use args.getlist("interests").
    #     Keep known tags from INFO["interest_tags"], without repeats.
    #     Add "unknown interest: ..." to problems for anything else.
    # 6b. Region and language: use args.get(name, "any"). Keep "any" or a value
    #     from INFO["regions"] / INFO["teaching_languages"]; otherwise report a problem
    #     and use "any".
    # 6c. A ticked include_unknown checkbox sends "yes"; an unticked one sends nothing.
    # อ่านค่าจากฟอร์ม หลาย checkbox ใช้ getlist เก็บเฉพาะค่าที่รู้จัก
    # ค่าที่ไม่รู้จักให้บันทึกใน problems แล้วใช้ "any" ช่องที่ติ๊กส่ง "yes"
    preferences = {"interests": wanted, "region": region, "language": language,
                   "include_unknown": include_unknown}
    return preferences, problems


def parse_limit(args, default=50, largest=200):
    """How many results to send. Supplied: the full MyTCAS pack has thousands of records."""
    try:
        limit = int(args.get("limit", default))
    except ValueError:
        return default
    return max(1, min(limit, largest))
