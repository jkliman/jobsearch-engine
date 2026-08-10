"""Align the story to the target — same career, sharper framing."""

BEFORE = "Senior Director"                       # functional title, no signal
AFTER  = "Data & AI Platform Leader · Solutions Architect"

COMMERCIAL = {"commercial", "ai_native"}
FEDERAL    = {"federal", "cleared"}


def reposition(resume, target: str):
    resume.headline = AFTER                       # lead with platform + AI
    resume.title    = "Senior Director"           # function, not department
    resume.summary  = lead_with(resume, ["platform", "AI", "governance"])
    if target in FEDERAL:
        resume.emphasize("Secret clearance · FISMA · NIST")
    if target in COMMERCIAL:
        resume.emphasize("Snowflake · AWS · GenAI in production")
    return tailor_cover_letter(resume, target)
