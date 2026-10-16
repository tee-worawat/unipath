"""Day 4: the portfolio module. A PDF goes in; suggested interests and matching programmes come out.

Module map: browser → portfolio.py → pdf_text.py → ai_reader.py → preferences.py → search.py → JSON.
A Blueprint is a group of routes in its own file; app.py plugs it in with register_blueprint.
The file is read in memory and never saved. Use the fictional samples in data/portfolios/.
"""
from flask import Blueprint, current_app, jsonify, request
from werkzeug.datastructures import MultiDict
from ai_reader import quote_found, read_interests
from pdf_text import extract_text
from preferences import parse_limit, parse_preferences
from search import search_answer

portfolio = Blueprint("portfolio", __name__)


@portfolio.get("/portfolio")
def page():
    return current_app.send_static_file("portfolio.html")


@portfolio.post("/api/portfolio")
def api_portfolio():
    """See API.md, "Portfolio"."""
    text, problems = extract_text(request.files.get("portfolio"))
    if problems:
        return jsonify({"error": "invalid_portfolio", "problems": problems}), 400
    reading = read_interests(text)
    notes = list(reading["notes"])
    # TODO 12: Never trust the model. Check its suggestions before searching.
    # 12a. Keep only items whose quote is really in the portfolio: quote_found(item["quote"], text).
    #      Add a note for each item you drop.
    # 12b. args = MultiDict(request.form), then args.setlist("interests", [the tags you kept]).
    #      preferences, refused = parse_preferences(args)   <- the same check as Day 2.
    #      Keep only the evidence whose tag is in preferences["interests"].
    # 12c. No interests left? Answer count 0, returned 0, filters, no results, and add a note.
    #      Otherwise answer = search_answer(preferences, parse_limit(request.form)).
    # 12d. Add reader, characters_read, text_preview (first 300 characters), evidence, refused
    #      and notes to the answer, then return jsonify(answer). See API.md.
    # ตรวจคำแนะนำของ AI ก่อนใช้: เก็บเฉพาะคำพูดที่มีจริงในแฟ้ม และแท็กที่ผ่าน parse_preferences
    return jsonify({"count": 0, "returned": 0, "filters": {}, "results": [],
                    "reader": reading["reader"], "characters_read": len(text),
                    "text_preview": text[:300], "evidence": [], "refused": [],
                    "notes": notes + ["TODO 12 in portfolio.py is not finished yet"]})
