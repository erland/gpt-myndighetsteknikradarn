#!/usr/bin/env python3
"""Generate deterministic query families for inspection/testing.
This helper does not perform web searches.
"""
from __future__ import annotations
import argparse, json


def q(s: str) -> str:
    return s.strip()


def build(agency: str, term: str, domain: str | None = None) -> dict:
    screen = [q(f'"{agency}" "{term}"')]
    if domain:
        screen.append(q(f'site:{domain} "{term}"'))
    deepen = {
        'procurement': [q(f'"{agency}" "{term}" upphandling OR avtal OR avrop'), q(f'"{agency}" "{term}" tilldelning OR efterannons'), q(f'"{agency}" "{term}" RFI OR marknadsdialog')],
        'jobs': [q(f'"{agency}" "{term}" jobb OR "lediga jobb"')],
        'vendor': [q(f'"{agency}" "{term}" kundcase OR customer OR reference')],
        'migration': [q(f'"{agency}" "{term}" migrering OR avveckling OR ersätt')],
    }
    if domain:
        deepen['official'] = [q(f'site:{domain} "{term}"'), q(f'site:{domain} "{term}" filetype:pdf')]
    return {'agency': agency, 'term': term, 'screen': screen, 'deepen': deepen}


def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument('--agency', required=True)
    p.add_argument('--term', required=True)
    p.add_argument('--domain')
    args=p.parse_args()
    print(json.dumps(build(args.agency,args.term,args.domain), ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
