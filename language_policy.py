"""Supplied policy: bilingual is accepted for Thai or English preferences.

Unknown records may be included explicitly, but remain labelled unknown.
This helper is supplied in both editions so data uncertainty is handled clearly.
"""


def language_matches(programme, wanted_language, include_unknown):
    actual_language = programme["teaching_language"]
    if wanted_language == "any":
        return True
    if actual_language == wanted_language:
        return True
    if actual_language == "th_en" and wanted_language in ["th", "en"]:
        return True
    if actual_language == "unknown" and include_unknown and wanted_language != "unknown":
        return True
    return False
