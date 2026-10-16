"""Day 1 terminal entry point. Flask is not needed for this exercise."""
from data_loader import load_json
from finder import find_programmes
from edition import EDITION

programmes = load_json("programmes.json")
wanted = ["technology", "design"]
region = "north"
results = find_programmes(programmes, wanted, region)

print("UniPath:", EDITION)
print("Interests:", wanted, "Region:", region)
if EDITION == "student":
    print("Starter: complete the TODOs in finder.py. Initially there are no results.")
for result in results:
    programme = result["programme"]
    print(programme["programme_en"], "|", result["matched_interests"])
if not results:
    print("No results from the current code and this sample. Check the rules and filters.")
