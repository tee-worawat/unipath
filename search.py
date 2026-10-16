"""Search the loaded programmes and shape the answer that API.md promises.

The search route (Day 2) and the portfolio route (Day 4) both use search_answer.
"""
from data_loader import load_json, load_programmes
from finder import find_programmes

PROGRAMMES = load_programmes()
DISPLAY = load_json("display-text.json")


def public_record(programme, results):
    """Supplied: the fields API.md promises for each result, and nothing more."""
    return {
        "id": programme["id"],
        "programme_en": programme["programme_en"],
        "programme_th": programme["programme_th"],
        "university_en": programme["university_en"],
        "university_th": programme["university_th"],
        "province": programme["province"],
        "region": programme["region"],
        "programme_format": programme["programme_format"],
        "teaching_language": programme["teaching_language"],
        "matched_interests": [tag for tag in wanted if tag in programme["interest_tags"]],
        "summary_en": DISPLAY.get(programme["id"], {}).get("summary_en"),
        "summary_th": programme.get("summary_th"),
        "programme_url": programme["programme_url"],
        "admission_url": programme.get("admission_url"),
        "admission_reference_year_be": programme.get("admission_reference_year_be"),
        "data_notes": programme.get("data_notes", []),
    }

def search_answer(preferences, limit):
    """The success answer in API.md: count, returned, filters and results."""
    # TODO 7c: Build the answer API.md describes.
    # - results = find_programmes(PROGRAMMES, ...) with the four values in preferences.
    # - count is every match; results holds at most limit of them (results[:limit]).
    # - returned is how many are in results; filters is preferences.
    # - Turn each result into public_record(result).
    # ค้นหาด้วยค่าใน preferences ส่งไม่เกิน limit รายการ แปลงแต่ละรายการด้วย public_record
    return {"count": 0, "returned": 0, "filters": {}, "results": [],
            "todo": "TODO 7c in search.py is not finished yet"}
