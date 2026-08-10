"""Multi-angle sourcing so one blind spot can't hide a good role."""

ANGLES = [
    ("keyword",  "Director Data Platform AI"),
    ("semantic", "Head of Data and AI Platform"),
    ("title",    "VP Data AI Strategy"),
]


def source_roles(levels, remote_or_metro, salary_min, jobs_api=None):
    seen, out = set(), []
    for mode, q in ANGLES:
        for role in jobs_api.search(
            q, mode=mode, seniority=levels,
            salary_min=salary_min, posted_within="7d",
        ):
            if role.id in seen:
                continue
            seen.add(role.id)
            out.append(role)
    return out
