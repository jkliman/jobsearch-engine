"""Transparent, rules-based fit scoring. No black box, gaps named in plain language."""
from dataclasses import dataclass

SENIOR = {"Director", "Sr. Director", "VP", "Principal"}


@dataclass
class Fit:
    pct: int
    why: str

    def __lt__(self, other):  # so results sort by score
        return self.pct < other.pct


def score_fit(role, profile) -> Fit:
    r = role.title.lower()
    if "data platform" in r and role.level in SENIOR:
        return Fit(90, "literal stack (Snowflake/AWS) + founding-style build")
    if "solutions architect" in r:
        return Fit(85, "data-platform SA is the core wheelhouse")
    if "vp" in r and "ai" in r:
        return Fit(82, "AI strategy + adoption at VP level")
    if "governance" in r:
        return Fit(82, "GDPR/consent governance is a strength")
    # gaps are surfaced, not hidden
    if "gpu" in r or "model training" in r:
        return Fit(70, "deep DL-infra / training depth is the gap")
    return Fit(72, "general data/AI-platform fit")
