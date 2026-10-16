"""Check that the frontend (static/) still matches API.md. Run after every AI edit. No Flask needed."""
import json
import re
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]


def without_comments(path):
    source = path.read_text(encoding="utf-8")
    return re.sub(r"(?m)^\s*//.*$|\s//\s.*$", "", source)


def documented_fields():
    """The field names in the success example of API.md."""
    text = (PROJECT / "API.md").read_text(encoding="utf-8")
    example = json.loads(re.search(r"```json\n(\{.*?\})\n```", text, re.S).group(1).replace("…", ""))
    return set(example), set(example["results"][0])


class ContractChecks(unittest.TestCase):
    def setUp(self):
        self.script = without_comments(PROJECT / "static" / "app.js")  # Ignore comments.
        self.portfolio_script = without_comments(PROJECT / "static" / "portfolio.js")
        page = (PROJECT / "static" / "index.html").read_text(encoding="utf-8")
        self.page = re.sub(r"<!--.*?-->", "", page, flags=re.S)  # Ignore HTML comments.
        self.top_fields, self.result_fields = documented_fields()

    def test_page_keeps_ids_and_field_names(self):
        for needle in ('id="finder-form"', 'id="status"', 'id="results"', 'name="interests"',
                       'name="region"', 'name="language"', 'name="include_unknown"'):
            self.assertIn(needle, self.page)
        tags = json.loads((PROJECT / "data" / "dataset-info.json").read_text(encoding="utf-8"))["interest_tags"]
        missing = [tag for tag in tags if f'value="{tag}"' not in self.page]
        self.assertFalse(missing, f"Interest checkboxes missing from index.html: {missing}")

    def test_frontend_is_plugged_in(self):
        self.assertIn('form.addEventListener("submit", handleSearch)', self.script,
                      "Plug the frontend in at the end of static/app.js")

    def test_script_calls_the_documented_endpoint(self):
        self.assertIn("/api/programmes?", self.script)

    def test_card_template_is_wired(self):
        self.assertIn('id="card-template"', self.page, "Keep <template id=\"card-template\"> in index.html")
        template = re.search(r'<template id="card-template">(.*?)</template>', self.page, re.S)
        self.assertTrue(template and 'data-field="programme_en"' in template.group(1),
                        'Mark the programme name in the card template with data-field="programme_en"')

    def test_reads_only_documented_result_fields(self):
        used = set(re.findall(r"\bprogramme\.([a-z_]+)", self.script + self.portfolio_script))
        used |= set(re.findall(r'data-(?:field|link)="([^"]*)"', self.page))
        used |= {value.split(":")[0] for value in re.findall(r'data-show="([^"]*)"', self.page)}
        self.assertLessEqual(used, self.result_fields, f"Not in API.md: {sorted(used - self.result_fields)}")

    def test_script_reads_only_documented_top_level_fields(self):
        used = set(re.findall(r"\bdata\.([a-z_]+)", self.script)) - {"problems"}
        self.assertLessEqual(used, self.top_fields, f"Not in API.md: {sorted(used - self.top_fields)}")

    def test_data_is_written_as_text_not_html(self):
        self.assertNotIn("innerHTML", self.script + self.portfolio_script)


if __name__ == "__main__":
    unittest.main()
