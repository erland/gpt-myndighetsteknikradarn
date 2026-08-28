#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from datetime import date, datetime
import yaml

LABELS = {
    'level_5_direct_confirmed': 'Direkt bekräftat',
    'level_4_very_strong': 'Mycket stark indikation',
    'level_3_likely': 'Trolig',
    'level_2_trace': 'Spår/indikation',
    'level_1_weak_trace': 'Svagt spår',
    'level_0_no_relevant_evidence': 'Inga relevanta belägg',
    'unresolved': 'Unresolved',
}
SOURCE_LABELS = {
    'official_agency': 'Myndighetens egen källa',
    'official_job_ad': 'Officiell jobbannons',
    'procurement_contract': 'Avtal',
    'procurement_calloff': 'Avrop',
    'conference_presentation': 'Konferenspresentation',
    'professional_profile': 'Professionell profil',
    'industry_press': 'Branschpress',
}

def _date_key(value):
    if value is None: return ''
    if isinstance(value, (date, datetime)): return value.isoformat()
    return str(value)

def validate_counts(c):
    if c['scoped_agency_count'] != c['analyzed_count'] + c['not_analyzed_count']:
        raise ValueError('scope counts do not reconcile')
    if c['analyzed_count'] != c['likely_count'] + c['trace_count'] + c['no_trace_count'] + c['unresolved_count']:
        raise ValueError('analyzed counts do not reconcile')

def ranked_positive(items):
    pos=[x for x in items if x['display_category'] in {'likely_or_confirmed','trace'}]
    return sorted(pos, key=lambda x: (-int(x['score']), ''.join(chr(255-ord(ch)) for ch in _date_key(x.get('latest_relevant_evidence_date'))), x['agency_name'].casefold()))

def render(data):
    c=data['coverage']; validate_counts(c)
    if data['run_status']=='complete' and c['not_analyzed_count'] != 0:
        raise ValueError('complete result cannot have not_analyzed_count > 0')
    target=data['target']['canonical_name']
    lines=[f'# {target} – svenska myndigheter','']
    if data['run_status']=='partial':
        lines += [f"> **Delresultat:** {c['analyzed_count']} av {c['scoped_agency_count']} myndigheter har analyserats. {c['not_analyzed_count']} återstår. Resultaten nedan ska inte extrapoleras till ej analyserade myndigheter.",'']
    else:
        lines += ['**Status:** Slutlig sammanställning för angiven analysomfattning.','']
    lines += ['## Sammanfattning','', '| Mått | Antal |','|---|---:|',
      f"| Myndigheter i aktuell analysomfattning | {c['scoped_agency_count']} |",
      f"| Faktiskt analyserade | {c['analyzed_count']} |",
      f"| Relativt trolig eller bekräftad användning | {c['likely_count']} |",
      f"| Spår av möjlig användning | {c['trace_count']} |",
      f"| Inga relevanta spår hittades | {c['no_trace_count']} |",
      f"| Unresolved | {c['unresolved_count']} |",
      f"| Ännu inte analyserade | {c['not_analyzed_count']} |",'',
      '> "Inga relevanta spår hittades" betyder att analysen inte hittade tillräckliga belägg. Det bevisar inte att tekniken saknas.','',
      '## Myndigheter med belägg','',
      '| Myndighet | Bedömning | Säkerhetsvärde | Evidenssammanfattning | Källtyper | Senaste relevanta belägg |',
      '|---|---|---:|---|---|---|']
    for a in ranked_positive(data['ranked_assessments']):
        sources=', '.join(SOURCE_LABELS.get(s,s) for s in a.get('source_types',[])) or '–'
        latest=_date_key(a.get('latest_relevant_evidence_date')) or 'Okänt'
        rationale=str(a.get('rationale','')).replace('|','\\|').replace('\n',' ')
        lines.append(f"| {a['agency_name']} | {LABELS.get(a['evidence_level'],a['evidence_level'])} | {a['score']}/100 | {rationale} | {sources} | {latest} |")
    unresolved=[x for x in data['ranked_assessments'] if x['display_category']=='unresolved']
    if unresolved:
        lines += ['','## Unresolved','']
        for a in sorted(unresolved,key=lambda x:x['agency_name'].casefold()):
            lines.append(f"- **{a['agency_name']}** – {a['rationale']}")
    names={x.get('agency_id'):x.get('agency_name',x.get('agency_id')) for x in data['ranked_assessments']}
    positive_ids={x.get('agency_id') for x in data['ranked_assessments'] if x['display_category'] in {'likely_or_confirmed','trace'}}
    details=[x for x in data.get('evidence_details',[]) if x.get('agency_id') in positive_ids]
    if details:
        lines += ['','## Evidens och källor','']
        current=None
        for e in sorted(details,key=lambda x:(names.get(x.get('agency_id'),''), x.get('source_date') or '', x.get('evidence_id',''))):
            if e.get('agency_id') != current:
                current=e.get('agency_id'); lines += [f"### {names.get(current,current)}",'']
            src=SOURCE_LABELS.get(e.get('source_type'),e.get('source_type','Okänd källtyp'))
            dt=_date_key(e.get('source_date')) or 'datum okänt'
            title=e.get('source_title') or e.get('evidence_id','Källa')
            url=e.get('source_url')
            ref=f"[{title}]({url})" if url else title
            lines.append(f"- **{src}, {dt}:** {e.get('summary','')} Källa: {ref}.")
    lines += ['','## Källtyper i underlaget','', '| Källtyp | Myndigheter med stöd | Evidensposter |','|---|---:|---:|']
    for s in data.get('source_type_summary',[]):
        lines.append(f"| {SOURCE_LABELS.get(s['source_type'],s['source_type'])} | {s['agencies_supported']} | {s['evidence_items']} |")
    lines += ['','## Metod i korthet','',data['methodology_note'],'','## Begränsningar','']
    lim=data.get('limitations') or ['Inga särskilda begränsningar registrerade.']
    lines += [f'- {x}' for x in lim]
    if data.get('next_actions'):
        lines += ['','## Möjliga nästa steg','']+[f'- {x}' for x in data['next_actions']]
    return '\n'.join(lines)+'\n'

def main():
    p=argparse.ArgumentParser(); p.add_argument('input'); p.add_argument('-o','--output')
    a=p.parse_args(); data=yaml.safe_load(Path(a.input).read_text(encoding='utf-8')); out=render(data)
    if a.output: Path(a.output).write_text(out,encoding='utf-8')
    else: print(out,end='')
if __name__=='__main__': main()
