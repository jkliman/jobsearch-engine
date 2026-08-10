"""Connections x live openings -> ranked warm paths. Export, don't scrape."""
from itertools import groupby
from score import score_fit


def warm_paths(connections_csv, openings, me):
    conns = load_csv(connections_csv)                 # official platform export (ToS-friendly)
    conns.sort(key=lambda c: c.company)
    hits = []
    for company, people in groupby(conns, key=lambda c: c.company):
        people = list(people)
        for role in openings.at(company):
            if score_fit(role, me).pct >= 78:
                lead = max(people, key=seniority)     # most senior connection
                hits.append((lead, role))
    hits.sort(key=lambda h: seniority(h[0]), reverse=True)
    return [draft_referral_note(lead, role) for lead, role in hits]
