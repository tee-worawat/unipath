"""Optional: build data/programmes-all.json from the public MyTCAS course index.

    python3 fetch_mytcas.py                     # download (needs internet once), then convert
    python3 fetch_mytcas.py --from courses.json  # convert a copy your teacher gave you

MyTCAS supplies names, campus, field group, programme type and a cost note. Province,
region and interest tags come from mytcas_rules.json: our editorial guesses, not MyTCAS
facts. The result is for classroom exploration. Do not publish it on a public website
until your teacher confirms the data terms. Standard library only.

ดาวน์โหลดดัชนีหลักสูตร MyTCAS แล้วแปลงเป็น programmes-all.json จังหวัด ภูมิภาค และแท็กมาจาก
mytcas_rules.json ซึ่งเป็นการเดาเชิงบรรณาธิการ ใช้ในห้องเรียนเท่านั้น ห้ามเผยแพร่สาธารณะจนกว่าครูยืนยัน
"""
import argparse
import gzip
import json
import re
import urllib.request
import zlib
from collections import Counter
from datetime import date
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
SOURCE_URL = "https://my-tcas.s3.ap-southeast-1.amazonaws.com/mytcas/courses.json"
PROGRAMME_PAGE = "https://course.mytcas.com/programs/{}"


def read_json_bytes(raw):
    """MyTCAS serves gzip-compressed JSON; a saved copy may be plain."""
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return json.loads(raw.decode("utf-8"))


def download(url=SOURCE_URL):
    request = urllib.request.Request(url, headers={"User-Agent": "UniPath classroom project"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return read_json_bytes(response.read())


def clean(text):
    return re.sub(r"\s+", " ", text or "").strip()


def university_names(courses, rules):
    """One display name per university: a rule override, else the most common spelling."""
    seen = {}
    for course in courses:
        names = seen.setdefault(course["university_id"], (Counter(), Counter()))
        names[0][clean(course["university_name_en"])] += 1
        names[1][clean(course["university_name_th"])] += 1
    result = {}
    for university_id, (english, thai) in seen.items():
        override = rules["university_names"].get(university_id, {})
        result[university_id] = (override.get("en") or english.most_common(1)[0][0],
                                 override.get("th") or thai.most_common(1)[0][0])
    return result


def programme_type(label, rules):
    for rule in rules["programme_types"]:
        if label.startswith(rule.get("starts_with", "\0")) or rule.get("contains", "\0") in label:
            return rule["programme_format"], rule["teaching_language"], rule["language_evidence"]
    return "unknown", "unknown", "not_established"


FORMAT_WORDS = re.compile(r"\(?(english|international|bilingual) program(me)?\)?|ภาคภาษาอังกฤษ|หลักสูตรนานาชาติ|หลักสูตรสองภาษา", re.I)


def interest_tags(course, rules):
    """Field group tags, plus keyword tags. Format words such as "English Program" are ignored."""
    tags = list(rules["group_tags"].get(course["group_field_id"], []))
    fields = ("field_name", "faculty_name", "program_name", "major_name")
    english = FORMAT_WORDS.sub(" ", " ".join(course.get(f + "_en") or "" for f in fields)).lower()
    thai = FORMAT_WORDS.sub(" ", " ".join(course.get(f + "_th") or "" for f in fields))
    for rule in rules["keyword_tags"]:
        hit = any(re.search(r"\b" + re.escape(word), english) for word in rule["en"])
        if (hit or any(word in thai for word in rule["th"])) and rule["tag"] not in tags:
            tags.append(rule["tag"])
    return tags or ["society"]


def one_row_per_major(courses):
    """MyTCAS lists each major as a row, and sometimes repeats a row. Keep the newest copy of each."""
    newest = {}
    for course in courses:
        major = clean(course.get("major_id")) or clean(course.get("major_name_th"))
        key = (course["program_id"], major)
        if key not in newest or course.get("updated_at", "") > newest[key].get("updated_at", ""):
            newest[key] = course
    return newest


def convert(courses, rules, checked_on):
    names = university_names(courses, rules)
    rows = one_row_per_major(courses)
    majors_per_programme = Counter(program_id for program_id, _ in rows)
    records = []
    for (program_id, major), course in rows.items():
        key = f'{course["university_id"]}/{course["campus_id"]}'
        province = rules["campus_province"].get(key)
        fmt, language, evidence = programme_type(clean(course.get("program_type_name_th")), rules)
        programme_th = clean(course.get("program_name_th")) or clean(course.get("field_name_th"))
        programme_en = clean(course.get("program_name_en")) or clean(course.get("field_name_en")) or programme_th
        if major:
            major_th = clean(course.get("major_name_th"))
            programme_th = f"{programme_th} — {major_th}" if major_th else programme_th
            programme_en = f'{programme_en} — {clean(course.get("major_name_en")) or major_th}'
        suffix = ""
        if majors_per_programme[program_id] > 1:
            suffix = "-" + (re.sub(r"\W+", "", clean(course.get("major_id"))) or format(zlib.crc32(major.encode("utf-8")), "x"))
        notes = [f'MyTCAS programme type: {clean(course.get("program_type_name_th")) or "not given"}.']
        if province is None:
            notes.append("Campus province not mapped yet.")
        records.append({
            "id": "mytcas-" + program_id + suffix,
            "university_id": course["university_id"],
            "university_en": names[course["university_id"]][0],
            "university_th": names[course["university_id"]][1],
            "university_group": rules["university_groups"].get(course.get("university_type_name_th"), "unknown"),
            "programme_en": programme_en,
            "programme_th": programme_th,
            "official_title": clean(course.get("program_name_th")),
            "faculty_or_college": clean(course.get("faculty_name_en")) or clean(course.get("faculty_name_th")),
            "campus": clean(course.get("campus_name_th")),
            "province": province,
            "region": rules["province_region"].get(province, "unknown"),
            "programme_format": fmt,
            "teaching_language": language,
            "language_evidence": evidence,
            "interest_tags": interest_tags(course, rules),
            "summary_th": None,
            "cost_text_th": clean(course.get("cost")) or None,
            "programme_url": PROGRAMME_PAGE.format(course["program_id"]),
            "admission_url": None,
            "admission_reference_year_be": None,
            "admission_criteria": None,
            "tuition_total_thb": None,
            "source": "mytcas-course-index",
            "checked_on": checked_on,
            "data_notes": notes,
        })
    records.sort(key=lambda r: (r["university_id"], r["id"]))
    return records


def main():
    parser = argparse.ArgumentParser(description="Build data/programmes-all.json from MyTCAS.")
    parser.add_argument("--from", dest="source", help="convert a saved courses.json instead of downloading")
    parser.add_argument("--out", default=str(PROJECT / "data" / "programmes-all.json"))
    parser.add_argument("--checked-on", default=date.today().isoformat())
    args = parser.parse_args()
    rules = json.loads((PROJECT / "mytcas_rules.json").read_text(encoding="utf-8"))
    courses = read_json_bytes(Path(args.source).read_bytes()) if args.source else download()
    records = convert(courses, rules, args.checked_on)
    lines = ",\n".join(json.dumps(record, ensure_ascii=False) for record in records)
    Path(args.out).write_text("[\n" + lines + "\n]\n", encoding="utf-8")  # One programme per line.
    unmapped = sum(r["province"] is None for r in records)
    print(f"Wrote {len(records)} programmes from {len({r['university_id'] for r in records})} universities "
          f"to {args.out}. Province not mapped: {unmapped}.")
    print('To use it, set PROGRAMME_FILE = "programmes-all.json" in settings.py. Keep it off public websites.')


if __name__ == "__main__":
    main()
