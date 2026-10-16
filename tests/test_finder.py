"""Behaviour checks. Student TODOs initially fail these checks by design."""
import unittest
from data_loader import load_json
from finder import find_programmes, shared_interests


class FinderChecks(unittest.TestCase):
    def setUp(self):
        self.programmes = load_json("programmes.json")

    def ids(self, results):
        return {r["programme"]["id"] for r in results}

    def test_shared_interests_are_unique(self):
        self.assertEqual(shared_interests(["design", "food", "design"], {"interest_tags":["design"]}), ["design"])

    def test_no_filters_keeps_all_records(self):
        self.assertEqual(len(find_programmes(self.programmes, [])), 16)

    def test_northern_games(self):
        self.assertEqual(self.ids(find_programmes(self.programmes, ["games"], "north")), {"cmu-digital-game"})

    def test_language_known_and_unknown_are_different(self):
        self.assertEqual(find_programmes(self.programmes, [], "south", "en", False), [])
        results = find_programmes(self.programmes, [], "south", "en", True)
        self.assertEqual(self.ids(results), {"psu-digital-business", "psu-digital-engineering"})
        self.assertTrue(all(r["programme"]["teaching_language"]=="unknown" for r in results))

    def test_bilingual_policy(self):
        self.assertEqual(self.ids(find_programmes(self.programmes, [], "north", "en", False)), {"cmu-software-engineering", "cmu-digital-game", "cmu-management-it"})

    def test_empty_result_and_no_source_mutation(self):
        before = load_json("programmes.json")
        self.assertEqual(find_programmes(self.programmes, ["environment"], "north"), [])
        find_programmes(self.programmes, ["technology"])
        self.assertEqual(self.programmes, before)


if __name__ == "__main__":
    unittest.main()
