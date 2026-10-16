"""Day 4 behaviour checks for the portfolio module. Needs Flask and pypdf (see README).

These checks never contact an AI service: they use the offline reader or a pretend model reply.
"""
import io
import unittest
from pathlib import Path

try:
    import app as web
    import ai_reader
    import portfolio as portfolio_module
    import search
except ImportError as error:  # Flask or pypdf not installed yet: Day 1 checks still run.
    raise unittest.SkipTest(f"Flask app not importable yet: {error}")
from data_loader import load_json

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "portfolios"


class PortfolioChecks(unittest.TestCase):
    def setUp(self):
        search.PROGRAMMES = load_json("programmes.json")
        self.client = web.app.test_client()
        self.real_reader = portfolio_module.read_interests

    def tearDown(self):
        portfolio_module.read_interests = self.real_reader

    def pretend_model(self, items):
        """Replace the AI with a fixed reply, as if the model had answered with these items."""
        def fake(text):
            return {"reader": "claude", "items": items, "notes": []}
        portfolio_module.read_interests = fake

    def upload(self, name, data=None, **fields):
        content = data if data is not None else (SAMPLES / name).read_bytes()
        fields["portfolio"] = (io.BytesIO(content), name)
        response = self.client.post("/api/portfolio", data=fields, content_type="multipart/form-data")
        return response, response.get_json()

    def test_prompt_lists_every_tag_asks_for_json_and_ends_with_the_text(self):
        prompt = ai_reader.build_prompt("I built a robot.")
        for tag in load_json("dataset-info.json")["interest_tags"]:
            self.assertIn(tag, prompt)
        self.assertIn('{"interests": [{"tag": "...", "quote": "..."}]}', prompt)
        self.assertIn("admission", prompt.lower())
        self.assertTrue(prompt.endswith("I built a robot."))

    def test_offline_reader_quotes_the_portfolio(self):
        items = ai_reader.offline_reader("We measured water quality. I volunteer to plant mangrove trees.")
        self.assertEqual(items[0]["tag"], "environment")
        self.assertTrue(all(ai_reader.quote_found(item["quote"], "We measured water quality. I volunteer to plant mangrove trees.") for item in items))

    def test_not_a_pdf_is_refused(self):
        response, data = self.upload("notes.pdf", data=b"just some text")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["error"], "invalid_portfolio")

    def test_sample_portfolio_gives_interests_and_programmes(self):
        self.pretend_model([{"tag": "games", "quote": "I write small games in Python"},
                            {"tag": "design", "quote": "I designed every level on paper"}])
        response, data = self.upload("sample-1-game-maker.pdf", region="north")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("filters", {}).get("interests"), ["games", "design"])
        self.assertEqual([item["tag"] for item in data["evidence"]], ["games", "design"])
        self.assertIn("cmu-digital-game", [result["id"] for result in data["results"]])
        self.assertTrue(all(result["region"] == "north" for result in data["results"]))

    def test_invented_tag_is_refused(self):
        self.pretend_model([{"tag": "astronaut", "quote": "I write small games in Python"},
                            {"tag": "games", "quote": "I write small games in Python"}])
        _, data = self.upload("sample-1-game-maker.pdf")
        self.assertEqual(data.get("filters", {}).get("interests"), ["games"])
        self.assertTrue(any("astronaut" in problem for problem in data["refused"]))

    def test_made_up_quote_is_dropped(self):
        self.pretend_model([{"tag": "science", "quote": "I won a national physics medal"}])
        _, data = self.upload("sample-1-game-maker.pdf")
        self.assertEqual(data["evidence"], [])
        self.assertEqual((data["count"], data["results"]), (0, []))
        self.assertTrue(any("science" in note for note in data["notes"]))


if __name__ == "__main__":
    unittest.main()
