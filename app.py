"""Day 2 page (supplied) and Day 3 API (TODO 7). Matching does not assess admission eligibility."""
from flask import Flask, jsonify, render_template, request
from data_loader import load_json, load_programmes
from finder import find_programmes
from preferences import parse_limit, parse_preferences
from edition import EDITION

app = Flask(__name__)
app.json.ensure_ascii = False  # Send Thai as readable UTF-8, not \u0e... codes.
PROGRAMMES = load_programmes()
INFO = load_json("dataset-info.json")
DISPLAY = load_json("display-text.json")
PAGE_LIMIT = 50


def search(preferences):
    return find_programmes(PROGRAMMES, preferences["interests"], preferences["region"],
                           preferences["language"], preferences["include_unknown"])


def public_record(programme, wanted):
    """The fields API.md promises for one programme, and nothing more."""
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


@app.get("/")
def index():
    return app.send_static_file("index.html")


@app.get("/api/programmes")
def api_programmes():
    """Day 3: the same search, answered as JSON data for JavaScript. See API.md.
    http://localhost:5001/api/programmes?region=north&format=internationl
    """
    # preferences, problems = parse_preferences(request.args)
    #programmes, region, interest_tags, format, include_unresolved, match_all=False

    region = request.args.get("region", "any")
    format = request.args.get("format", "any")
    print(request.args.getlist("interests"))
    interest_tags = request.args.getlist("interests")
    match_all = request.args.get("match_all", True)
    include_unresolved = request.args.get("include_unresolved", False)

    results = find_programmes(PROGRAMMES,region, interest_tags, 
                              format, include_unresolved, match_all)
    

    return jsonify({"count": len(results), "returned": len(results), "filters": region,
                    "format":format, "interest_tags":interest_tags, "results":[public_record(programme, interest_tags) for programme in results]})

@app.get("/api/spark-coding-lab")
def api_spark_coding_lab():
    return jsonify({"message": "spark coding lab"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
