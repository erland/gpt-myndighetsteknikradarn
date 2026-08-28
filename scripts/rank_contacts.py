#!/usr/bin/env python3
"""Deterministiska hjälpfunktioner för rangordning och säker kontaktpresentation."""
from __future__ import annotations

ROLE_WEIGHT = {
    'chief_architect': 95,
    'enterprise_architect': 92,
    'it_architect': 88,
    'solution_architect': 82,
    'platform_architect': 86,
    'infrastructure_architect': 82,
    'product_or_platform_owner': 84,
    'technology_domain_lead': 85,
    'cio_or_it_director': 72,
    'digitalization_director': 66,
    'other_relevant_professional': 50,
}
STATUS_WEIGHT = {
    'current_verified': 30,
    'current_probable': 18,
    'stale_or_uncertain': 3,
    'former': -100,
    'unresolved': -20,
}
TARGET_WEIGHT = {
    'explicit': 35,
    'domain_related': 24,
    'general_it': 8,
    'unknown': 0,
}
CONTACT_KIND_WEIGHT = {
    'public_work_email': 4,
    'public_work_phone': 4,
    'agency_switchboard': 2,
    'agency_contact_form': 1,
    'agency_general_email': 1,
    'none_found': 0,
}

def ranking_score(candidate: dict) -> int:
    """Rangordningssignal; kontaktbarhet är medvetet bara en liten tie-break."""
    if candidate.get('role_status') == 'former':
        return 0
    raw = (
        ROLE_WEIGHT.get(candidate.get('role_class'), 0)
        + STATUS_WEIGHT.get(candidate.get('role_status'), 0)
        + TARGET_WEIGHT.get(candidate.get('target_relevance', 'unknown'), 0)
        + CONTACT_KIND_WEIGHT.get(candidate.get('contact_path', {}).get('kind', 'none_found'), 0)
    )
    return max(0, min(100, round(raw / 1.64)))

def safe_contact(candidate: dict) -> str:
    cp = candidate.get('contact_path') or {}
    kind = cp.get('kind', 'none_found')
    verified = cp.get('verified_public_professional', False)
    if kind == 'public_work_email':
        if not verified or not cp.get('email'):
            raise ValueError('Direkt e-post saknar verifierad offentlig professionell källa')
        return cp['email']
    if kind == 'public_work_phone':
        if not verified or not cp.get('phone'):
            raise ValueError('Direkttelefon saknar verifierad offentlig professionell källa')
        return cp['phone']
    if kind == 'agency_switchboard':
        if not cp.get('phone'):
            raise ValueError('Växelnummer saknas')
        return f"Växel: {cp['phone']}"
    if kind == 'agency_contact_form':
        return cp.get('url') or 'Officiellt kontaktformulär'
    if kind == 'agency_general_email':
        return cp.get('email') or 'Myndighetens generella e-post'
    return 'Ingen verifierad kontaktväg hittad'

def ranked(candidates: list[dict]) -> list[dict]:
    active = [c for c in candidates if c.get('role_status') != 'former']
    return sorted(active, key=lambda c: (-ranking_score(c), -int(c.get('confidence', 0)), c.get('name','').casefold()))
