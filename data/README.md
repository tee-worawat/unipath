# UniPath Thailand: bootcamp dataset

16 undergraduate programme examples at five public universities. Prepared 7 October 2026 for a proposed four-day bootcamp for 15-year-old learners with some Python experience.

## Start here

`programmes.json` is the one editable programme list. It loads directly into Python as a list of dictionaries. No package installation, network connection, database, API key or student account is required to use the files.

```python
import json
from pathlib import Path

data_folder = Path("curriculum/unipath-thailand/data")
programmes = json.loads((data_folder / "programmes.json").read_text(encoding="utf-8"))
print(len(programmes))
print(programmes[0]["programme_th"])
print(programmes[0]["interest_tags"])
```

Run this example from the workspace root in VS Code. If copying the data folder into a different project, change `data_folder` to its new location. Thai text requires UTF-8. JSON `null` becomes Python `None`.

## Files

- `programmes.json`: learner-facing records, bilingual display names, location, programme format, language evidence, interest tags, suggested projects and official links.
- `dataset-info.json`: field meaning, controlled tag labels, provenance, matching limits and official source register.
- `tcas-context.json`: four TCAS round names and general application references. Its reference year is 2570 / 2027; it has no deadlines or eligibility rules.
- `practice-preferences.json`: five fictional inputs for prediction and testing. These are not student records.

## Useful fields

Use `programme_th` or `programme_en` for cards, `university_th` or `university_en` for the institution, and `province` and `region` for location filters. Province values are English identifiers. Regions are a simplified teaching grouping, with Bangkok in `central`; they are not an official geographic classification.

Use `programme_format` to distinguish `thai`, `international`, `bilingual` and `unknown`. This is separate from `teaching_language` (`th`, `en`, `th_en`, `unknown`). Never automatically turn `international` into `en`.

`language_evidence` records the basis: a programme statement, college statement, directory label, conflicting content or information not established. College-level evidence describes the main language, not every module. Display unknowns as “ยังไม่ยืนยันข้อมูลภาษา” and offer a choice to include them. Do not silently classify them as English or Thai.

`interest_tags`, `summary_th` and `suggested_project_th` are teaching suggestions authored for this bootcamp. They are not university endorsements, official entry requirements, guaranteed careers or prescribed portfolio tasks. Display names are editorial short labels; `official_title` preserves the title seen in the source.

`source_refs` maps factual fields to source IDs in `dataset-info.json`. `checked_on` is the date of source inspection, not an admission year or a guarantee of current applications.

## Matching exercise

Begin with region filters and a shared-interest check. Later students can count shared tags, sort results and explain which interests matched. Any score must be called “matching interests”, not admission probability or suitability certification.

Language filtering should distinguish bilingual and unknown records. Discuss whether an English preference includes bilingual programmes; make the choice explicit. Never relax a filter invisibly. A useful no-result response is “No match in this sample. Try another filter or explore the official catalogue.”

The fictional inputs cover northern design/technology, southern business/data, Thai-language food/science, a no-result case and unknown-language handling. Practice 04 has no northern environment-tagged record in this small sample. That is a sample coverage limit, not proof that northern Thailand has no such programmes.

## Admissions and source limits

All `admission_criteria` and `tuition_total_thb` values are intentionally `null`: those details were not collected. Unknown tuition is not free tuition. Unknown criteria do not establish eligibility. `admission_url` is either a reviewed official reference or `null`; for a null value, offer the programme link and MyTCAS rather than inventing an application URL.

The Chulalongkorn Communication Arts admission link is explicitly historical TCAS69 (2569). Show that year beside the link. Programme-specific acceptance rounds, GPAX/TGAT/TPAT/A-Level requirements, deadlines and current intake availability are outside this dataset. Generic TCAS rounds must not be copied into every programme record. These learners will likely apply in a later admissions year.

CMU Animation has conflicting degree and language labels on its official page, so format/language remain unknown. CMU Digital Game displays bilingual instruction but a separate 2026 slide describes a Thai format; its conflict note must remain visible. Both pages flag curriculum updates. PSU Digital Engineering and Digital Business have confirmed international format but unresolved instructional language. Kasetsart Environmental Engineering has unresolved format/language, and its location uses the department address.

This is a curated discovery sample, not a comprehensive or representative Thai university database. Version 1 contains only public universities and no northeastern institutions. Source-review notes, including excluded candidates, live in `research/unipath-thailand/source-review.json` outside the distributable data folder.

## Editing and verification

Keep IDs stable. Choose tags from `dataset-info.json`. When adding a programme, read its official page, record source IDs and inspection date, and preserve uncertainty. To add admissions rules later, record the exact programme, round, academic year, applicant category and dated official announcement before writing any thresholds.

From the workspace root, run:

```sh
python3 skills/spark-curriculum-design/scripts/check_programme_dataset.py curriculum/unipath-thailand/data
```

This validates structure, tags, source references and unknown handling. It does not reconfirm the web pages or establish admission eligibility. Recheck official sources before using this dataset for a real application. Source notes contain public academic information only. Full lesson development, publication and classroom trials have not been performed.
