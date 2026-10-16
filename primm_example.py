"""Predict first. These three fictional records are for tracing, not admissions."""
programmes = [
    {"name": "Digital Lab", "interest_tags": ["technology", "data"]},
    {"name": "Design Studio", "interest_tags": ["design", "communication"]},
    {"name": "Shop Simulator", "interest_tags": ["business", "data"]},
]
wanted = "design"
for programme in programmes:
    if wanted in programme["interest_tags"]:
        print(programme["name"])
