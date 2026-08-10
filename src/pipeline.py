"""Source -> Score -> Track -> Act. The whole loop, end to end."""
from search import source_roles
from score import score_fit
import tracker


def run_search(profile, floor: int = 180_000):
    roles = source_roles(
        levels=["Director", "VP", "Principal"],
        remote_or_metro="DC",
        salary_min=floor,
    )
    scored = [(score_fit(r, profile), r) for r in roles]
    fresh = dedupe(sorted(scored, reverse=True))
    for fit, role in fresh:
        tracker.upsert(role, fit)            # colour-coded sheet
        if fit.pct >= 85:
            queue_outreach(role)             # tailor + apply + refer
    return tracker.summary()


def dedupe(scored):
    seen, out = set(), []
    for fit, role in scored:
        if role.id in seen:
            continue
        seen.add(role.id)
        out.append((fit, role))
    return out
