"""Day 2 behaviour checks for the JSON API in API.md. Needs Flask (see README)."""
import unittest

try:
    import app as web
    import search
except ImportError as error:  # Flask not installed yet: Day 1 checks still run.
    raise unittest.SkipTest(f"Flask app not importable yet: {error}")
from data_loader import load_json

FIELDS = {"id", "programme_en", "programme_th", "university_en", "university_th", "province",
          "region", "programme_format", "teaching_language", "matched_interests", "summary_en",
          "summary_th", "programme_url", "admission_url", "admission_reference_year_be", "data_notes"}


class ApiChecks(unittest.TestCase):
    def setUp(self):
        search.PROGRAMMES = load_json("programmes.json")  # Checks always use the curated sample.
        self.client = web.app.test_client()

    def get(self, query):
        response = self.client.get("/api/programmes?" + query)
        return response, response.get_json()

    def test_the_page_is_served(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn('id="finder-form"', response.get_data(as_text=True))

    def test_answers_json_in_the_agreed_shape(self):
        response, data = self.get("interests=games&region=north")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        self.assertEqual(set(data), {"count", "returned", "filters", "results"})
        self.assertEqual(data["count"], 1)
        self.assertEqual(set(data["results"][0]), FIELDS)
        self.assertEqual(data["results"][0]["matched_interests"], ["games"])

    def test_filters_echo_what_the_server_understood(self):
        _, data = self.get("interests=games&interests=food&region=any")
        self.assertEqual(data.get("filters", {}).get("interests"), ["games", "food"])
        self.assertEqual(data.get("count"), 3)

    def test_no_filters_counts_every_record_and_limit_trims(self):
        _, data = self.get("")
        self.assertEqual((data["count"], data["returned"]), (16, 16))
        _, data = self.get("limit=5")
        self.assertEqual((data["count"], data["returned"], len(data["results"])), (16, 5, 5))

    def test_unknown_language_needs_explicit_choice(self):
        self.assertEqual(self.get("region=south&language=en")[1]["count"], 0)
        _, data = self.get("region=south&language=en&include_unknown=yes")
        self.assertEqual(data["count"], 2)
        self.assertTrue(all(r["teaching_language"] == "unknown" for r in data["results"]))

    def test_invalid_values_get_status_400(self):
        response, data = self.get("region=mars")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["error"], "invalid_preferences")
        self.assertTrue(any("region" in problem for problem in data["problems"]))

    def test_thai_text_is_readable_utf8(self):
        response, _ = self.get("interests=games&region=north")
        self.assertIn("มหาวิทยาลัยเชียงใหม่", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
