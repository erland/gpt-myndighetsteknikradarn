#!/usr/bin/env python3
from __future__ import annotations
import argparse, re, html
from pathlib import Path
from datetime import date, datetime, timezone
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
    'agency_official': 'Myndighetens egen källa',
    'official_job_ad': 'Officiell jobbannons',
    'procurement_contract': 'Avtal',
    'procurement_calloff': 'Avrop',
    'conference_presentation': 'Konferenspresentation',
    'conference_or_presentation': 'Konferens/presentation',
    'professional_profile': 'Professionell profil',
    'industry_press': 'Branschpress',
}


def dt(v):
    if v is None: return ''
    if isinstance(v, (date, datetime)): return v.isoformat()
    return str(v)


def validate(analysis, contacts=None):
    c=analysis['coverage']
    if c['scoped_agency_count'] != c['analyzed_count'] + c['not_analyzed_count']:
        raise ValueError('scope counts do not reconcile')
    if c['analyzed_count'] != c['likely_count'] + c['trace_count'] + c['no_trace_count'] + c['unresolved_count']:
        raise ValueError('analyzed counts do not reconcile')
    if analysis['run_status']=='complete' and c['not_analyzed_count']:
        raise ValueError('complete result cannot have not_analyzed_count > 0')
    if contacts:
        for cand in contacts.get('candidates',[]):
            cp=cand.get('contact_path') or {}
            if cp.get('kind') in {'public_work_email','public_work_phone','public_work_email_and_phone'} and not cp.get('verified_public_professional'):
                raise ValueError(f"unverified direct contact for {cand.get('candidate_id')}")


def positive(items):
    return sorted([x for x in items if x['display_category'] in {'likely_or_confirmed','trace'}],
                  key=lambda x:(-int(x['score']), -(int(re.sub(r'\D','',dt(x.get('latest_relevant_evidence_date'))) or '0')), x['agency_name'].casefold()))


def recommended_contacts(contacts):
    if not contacts: return []
    return sorted([x for x in contacts.get('candidates',[]) if x.get('role_status') not in {'former','unresolved'}],
                  key=lambda x:(x.get('agency_name','').casefold(), -int(x.get('confidence',0)), x.get('name','').casefold()))


def contact_value(c):
    cp=c.get('contact_path') or {}
    bits=[]
    if cp.get('email'): bits.append(cp['email'])
    if cp.get('phone'): bits.append(cp['phone'])
    if cp.get('url'): bits.append(cp['url'])
    return ' / '.join(bits) if bits else 'Ingen direkt kontaktuppgift'


def md_escape(v):
    return str(v).replace('|','\\|').replace('\n',' ')


def render_markdown(a, contacts=None, generated_at=None):
    validate(a, contacts); c=a['coverage']; target=a['target']['canonical_name']
    lines=[f'# {target} – svenska myndigheter','']
    if a['run_status']=='partial':
        lines += [f"> **Delresultat:** {c['analyzed_count']} av {c['scoped_agency_count']} myndigheter har analyserats. {c['not_analyzed_count']} återstår.",'']
    else: lines += ['**Status:** Slutlig sammanställning för angiven analysomfattning.','']
    lines += ['## Sammanfattning','', '| Mått | Antal |','|---|---:|']
    rows=[('Myndigheter i aktuell analysomfattning','scoped_agency_count'),('Faktiskt analyserade','analyzed_count'),('Relativt trolig eller bekräftad användning','likely_count'),('Spår av möjlig användning','trace_count'),('Inga relevanta spår hittades','no_trace_count'),('Unresolved','unresolved_count'),('Ännu inte analyserade','not_analyzed_count')]
    lines += [f'| {label} | {c[key]} |' for label,key in rows]
    lines += ['', '> "Inga relevanta spår hittades" betyder att analysen inte hittade tillräckliga belägg. Det bevisar inte att tekniken saknas.','', '## Myndigheter med belägg','', '| Myndighet | Bedömning | Säkerhetsvärde | Evidenssammanfattning | Källtyper | Senaste relevanta belägg |','|---|---|---:|---|---|---|']
    for x in positive(a['ranked_assessments']):
        src=', '.join(SOURCE_LABELS.get(s,s) for s in x.get('source_types',[])) or '–'
        lines.append(f"| {md_escape(x['agency_name'])} | {LABELS.get(x['evidence_level'],x['evidence_level'])} | {x['score']}/100 | {md_escape(x.get('rationale',''))} | {md_escape(src)} | {dt(x.get('latest_relevant_evidence_date')) or 'Okänt'} |")
    unresolved=[x for x in a['ranked_assessments'] if x['display_category']=='unresolved']
    if unresolved:
        lines += ['','## Unresolved','']+[f"- **{x['agency_name']}** – {x.get('rationale','')}" for x in sorted(unresolved,key=lambda z:z['agency_name'].casefold())]
    names={x.get('agency_id'):x.get('agency_name',x.get('agency_id')) for x in a['ranked_assessments']}; pids={x.get('agency_id') for x in positive(a['ranked_assessments'])}
    details=[x for x in a.get('evidence_details',[]) if x.get('agency_id') in pids]
    if details:
        lines += ['','## Evidens och källor','']; current=None
        for e in sorted(details,key=lambda x:(names.get(x.get('agency_id'),''), dt(x.get('source_date')),x.get('evidence_id',''))):
            if e.get('agency_id') != current:
                current=e.get('agency_id'); lines += [f"### {names.get(current,current)}",'']
            title=e.get('source_title') or e.get('evidence_id','Källa'); url=e.get('source_url'); ref=f'[{title}]({url})' if url else title
            lines.append(f"- **{SOURCE_LABELS.get(e.get('source_type'),e.get('source_type','Okänd källtyp'))}, {dt(e.get('source_date')) or 'datum okänt'}:** {e.get('summary','')} Källa: {ref}.")
    lines += ['','## Källtyper i underlaget','', '| Källtyp | Myndigheter med stöd | Evidensposter |','|---|---:|---:|']
    for s in a.get('source_type_summary',[]): lines.append(f"| {SOURCE_LABELS.get(s['source_type'],s['source_type'])} | {s['agencies_supported']} | {s['evidence_items']} |")
    lines += ['','## Metod i korthet','',a['methodology_note'],'','## Begränsningar',''] + [f'- {x}' for x in (a.get('limitations') or ['Inga särskilda begränsningar registrerade.'])]
    if contacts:
        lines += ['','## Kontaktpersoner','',f"Kontaktresearch: {contacts.get('searched_agency_count',0)} av {contacts.get('selected_agency_count',0)} valda myndigheter analyserade.",'', '| Person | Roll | Myndighet | Relevans | Säkerhet | Kontaktväg |','|---|---|---|---|---:|---|']
        for x in recommended_contacts(contacts):
            lines.append(f"| {md_escape(x.get('name',''))} | {md_escape(x.get('role_title',''))} | {md_escape(x.get('agency_name',''))} | {md_escape(x.get('rationale',''))} | {x.get('confidence',0)}/100 | {md_escape(contact_value(x))} |")
        if contacts.get('fallbacks'):
            lines += ['','### Endast generell kontaktväg','']
            for f in contacts['fallbacks']:
                cp=f.get('contact_path') or {}; val=cp.get('phone') or cp.get('url') or cp.get('email') or 'Officiell kontaktväg'
                lines.append(f"- **{f.get('agency_name','')}** – {val}")
        lines += ['','> Direkt e-post/telefon visas endast när den är offentligt publicerad i professionellt sammanhang. Uppgifter gissas aldrig.']
    if a.get('next_actions'): lines += ['','## Möjliga nästa steg','']+[f'- {x}' for x in a['next_actions']]
    lines += ['','## Exportmetadata','',f"- Genererad: {generated_at or datetime.now(timezone.utc).isoformat(timespec='seconds')}",'- Källa: samma strukturerade analysdata som chattresultatet. Ingen ny research görs i exportfasen.']
    return '\n'.join(lines)+'\n'


def cf(v): return str(v).replace('|','¦').replace('\n',' ')
def cflink(title,url): return f'[{cf(title)}|{url}]' if url else cf(title)


def render_confluence(a, contacts=None, generated_at=None):
    validate(a, contacts); c=a['coverage']; target=a['target']['canonical_name']; lines=[f'h1. {target} – svenska myndigheter','']
    if a['run_status']=='partial': lines += ['{note}',f"*Delresultat:* {c['analyzed_count']} av {c['scoped_agency_count']} myndigheter har analyserats. {c['not_analyzed_count']} återstår.",'{note}','']
    else: lines += ['*Status:* Slutlig sammanställning för angiven analysomfattning.','']
    lines += ['h2. Sammanfattning','','||Mått||Antal||']
    rows=[('Myndigheter i aktuell analysomfattning','scoped_agency_count'),('Faktiskt analyserade','analyzed_count'),('Relativt trolig eller bekräftad användning','likely_count'),('Spår av möjlig användning','trace_count'),('Inga relevanta spår hittades','no_trace_count'),('Unresolved','unresolved_count'),('Ännu inte analyserade','not_analyzed_count')]
    lines += [f'|{label}|{c[key]}|' for label,key in rows]
    lines += ['','{info}','"Inga relevanta spår hittades" betyder att analysen inte hittade tillräckliga belägg. Det bevisar inte att tekniken saknas.','{info}','','h2. Myndigheter med belägg','','||Myndighet||Bedömning||Säkerhetsvärde||Evidenssammanfattning||Källtyper||Senaste relevanta belägg||']
    for x in positive(a['ranked_assessments']):
        src=', '.join(SOURCE_LABELS.get(s,s) for s in x.get('source_types',[])) or '–'
        lines.append(f"|{cf(x['agency_name'])}|{LABELS.get(x['evidence_level'],x['evidence_level'])}|{x['score']}/100|{cf(x.get('rationale',''))}|{cf(src)}|{dt(x.get('latest_relevant_evidence_date')) or 'Okänt'}|")
    unresolved=[x for x in a['ranked_assessments'] if x['display_category']=='unresolved']
    if unresolved:
        lines += ['','h2. Unresolved','']+[f"* *{cf(x['agency_name'])}* – {cf(x.get('rationale',''))}" for x in sorted(unresolved,key=lambda z:z['agency_name'].casefold())]
    names={x.get('agency_id'):x.get('agency_name',x.get('agency_id')) for x in a['ranked_assessments']}; pids={x.get('agency_id') for x in positive(a['ranked_assessments'])}
    details=[x for x in a.get('evidence_details',[]) if x.get('agency_id') in pids]
    if details:
        lines += ['','h2. Evidens och källor','']; current=None
        for e in sorted(details,key=lambda x:(names.get(x.get('agency_id'),''),dt(x.get('source_date')),x.get('evidence_id',''))):
            if e.get('agency_id')!=current:
                current=e.get('agency_id'); lines += [f"h3. {cf(names.get(current,current))}",'']
            lines.append(f"* *{SOURCE_LABELS.get(e.get('source_type'),e.get('source_type','Okänd källtyp'))}, {dt(e.get('source_date')) or 'datum okänt'}:* {cf(e.get('summary',''))} Källa: {cflink(e.get('source_title') or e.get('evidence_id','Källa'),e.get('source_url'))}.")
    lines += ['','h2. Källtyper i underlaget','','||Källtyp||Myndigheter med stöd||Evidensposter||']
    for s in a.get('source_type_summary',[]): lines.append(f"|{SOURCE_LABELS.get(s['source_type'],s['source_type'])}|{s['agencies_supported']}|{s['evidence_items']}|")
    lines += ['','h2. Metod i korthet','',cf(a['methodology_note']),'','h2. Begränsningar','']+[f'* {cf(x)}' for x in (a.get('limitations') or ['Inga särskilda begränsningar registrerade.'])]
    if contacts:
        lines += ['','h2. Kontaktpersoner','',f"Kontaktresearch: {contacts.get('searched_agency_count',0)} av {contacts.get('selected_agency_count',0)} valda myndigheter analyserade.",'','||Person||Roll||Myndighet||Relevans||Säkerhet||Kontaktväg||']
        for x in recommended_contacts(contacts): lines.append(f"|{cf(x.get('name',''))}|{cf(x.get('role_title',''))}|{cf(x.get('agency_name',''))}|{cf(x.get('rationale',''))}|{x.get('confidence',0)}/100|{cf(contact_value(x))}|")
        if contacts.get('fallbacks'):
            lines += ['','h3. Endast generell kontaktväg','']
            for f in contacts['fallbacks']:
                cp=f.get('contact_path') or {}; val=cp.get('phone') or cp.get('url') or cp.get('email') or 'Officiell kontaktväg'; lines.append(f"* *{cf(f.get('agency_name',''))}* – {cf(val)}")
        lines += ['','{info}','Direkt e-post/telefon visas endast när den är offentligt publicerad i professionellt sammanhang. Uppgifter gissas aldrig.','{info}']
    lines += ['','h2. Exportmetadata','',f"* Genererad: {generated_at or datetime.now(timezone.utc).isoformat(timespec='seconds')}", '* Källa: samma strukturerade analysdata som chattresultatet. Ingen ny research görs i exportfasen.']
    return '\n'.join(lines)+'\n'


def render_pdf(a, output, contacts=None, generated_at=None):
    validate(a, contacts)
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    if Path(font).exists():
        pdfmetrics.registerFont(TTFont('RadarSans',font)); pdfmetrics.registerFont(TTFont('RadarSansBold',bold)); base='RadarSans'; bbase='RadarSansBold'
    else: base='Helvetica'; bbase='Helvetica-Bold'
    styles=getSampleStyleSheet();
    for s in styles.byName.values(): s.fontName=base
    title=ParagraphStyle('RadarTitle',parent=styles['Title'],fontName=bbase,fontSize=18,leading=22,spaceAfter=8)
    h1=ParagraphStyle('RadarH1',parent=styles['Heading1'],fontName=bbase,fontSize=13,leading=16,spaceBefore=8,spaceAfter=5)
    h2=ParagraphStyle('RadarH2',parent=styles['Heading2'],fontName=bbase,fontSize=11,leading=14,spaceBefore=6,spaceAfter=4)
    body=ParagraphStyle('RadarBody',parent=styles['BodyText'],fontName=base,fontSize=8.5,leading=11)
    small=ParagraphStyle('RadarSmall',parent=body,fontSize=7.2,leading=9)
    note=ParagraphStyle('RadarNote',parent=body,leftIndent=7,rightIndent=7,borderWidth=.4,borderPadding=5,spaceAfter=6)
    c=a['coverage']; target=a['target']['canonical_name']; story=[Paragraph(html.escape(target)+' – svenska myndigheter',title)]
    if a['run_status']=='partial': story += [Paragraph(f"<b>Delresultat:</b> {c['analyzed_count']} av {c['scoped_agency_count']} myndigheter har analyserats. {c['not_analyzed_count']} återstår.",note)]
    else: story += [Paragraph('<b>Status:</b> Slutlig sammanställning för angiven analysomfattning.',body)]
    story += [Paragraph('Sammanfattning',h1)]
    rows=[['Mått','Antal'],['Myndigheter i aktuell analysomfattning',c['scoped_agency_count']],['Faktiskt analyserade',c['analyzed_count']],['Relativt trolig eller bekräftad användning',c['likely_count']],['Spår av möjlig användning',c['trace_count']],['Inga relevanta spår hittades',c['no_trace_count']],['Unresolved',c['unresolved_count']],['Ännu inte analyserade',c['not_analyzed_count']]]
    t=Table([[Paragraph(html.escape(str(x)),small) for x in r] for r in rows],colWidths=[130*mm,25*mm],repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('FONTNAME',(0,0),(-1,0),bbase),('GRID',(0,0),(-1,-1),.25,colors.grey),('VALIGN',(0,0),(-1,-1),'TOP'),('ALIGN',(1,1),(1,-1),'RIGHT'),('BOTTOMPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),4)])); story += [t,Spacer(1,4*mm),Paragraph('"Inga relevanta spår hittades" betyder att analysen inte hittade tillräckliga belägg. Det bevisar inte att tekniken saknas.',note),Paragraph('Myndigheter med belägg',h1)]
    data=[['Myndighet','Bedömning','Säkerhet','Evidenssammanfattning','Källtyper','Senaste']]
    for x in positive(a['ranked_assessments']):
        src=', '.join(SOURCE_LABELS.get(s,s) for s in x.get('source_types',[])) or '–'; data.append([x['agency_name'],LABELS.get(x['evidence_level'],x['evidence_level']),f"{x['score']}/100",x.get('rationale',''),src,dt(x.get('latest_relevant_evidence_date')) or 'Okänt'])
    td=[[Paragraph(html.escape(str(v)),small) for v in r] for r in data]
    tab=Table(td,colWidths=[27*mm,29*mm,17*mm,67*mm,31*mm,20*mm],repeatRows=1,hAlign='CENTER')
    tab.setStyle(TableStyle([('FONTNAME',(0,0),(-1,0),bbase),('GRID',(0,0),(-1,-1),.25,colors.grey),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)])); story += [tab]
    unresolved=[x for x in a['ranked_assessments'] if x['display_category']=='unresolved']
    if unresolved:
        story += [Paragraph('Unresolved',h1)]
        for x in sorted(unresolved,key=lambda z:z['agency_name'].casefold()): story.append(Paragraph(f"<b>{html.escape(x['agency_name'])}</b> – {html.escape(x.get('rationale',''))}",body))
    names={x.get('agency_id'):x.get('agency_name',x.get('agency_id')) for x in a['ranked_assessments']}; pids={x.get('agency_id') for x in positive(a['ranked_assessments'])}
    details=[x for x in a.get('evidence_details',[]) if x.get('agency_id') in pids]
    if details:
        story += [Paragraph('Evidens och källor',h1)]; current=None
        for e in sorted(details,key=lambda x:(names.get(x.get('agency_id'),''),dt(x.get('source_date')),x.get('evidence_id',''))):
            if e.get('agency_id')!=current:
                current=e.get('agency_id'); story.append(Paragraph(html.escape(names.get(current,current)),h2))
            src=SOURCE_LABELS.get(e.get('source_type'),e.get('source_type','Okänd källtyp')); title=html.escape(e.get('source_title') or e.get('evidence_id','Källa')); url=e.get('source_url'); ref=f'<link href="{html.escape(url,quote=True)}">{title}</link>' if url else title
            story.append(Paragraph(f"<b>{html.escape(src)}, {html.escape(dt(e.get('source_date')) or 'datum okänt')}:</b> {html.escape(e.get('summary',''))} Källa: {ref}.",body))
    story += [Paragraph('Källtyper i underlaget',h1)]
    sd=[['Källtyp','Myndigheter med stöd','Evidensposter']]+[[SOURCE_LABELS.get(s['source_type'],s['source_type']),s['agencies_supported'],s['evidence_items']] for s in a.get('source_type_summary',[])]
    st=Table([[Paragraph(html.escape(str(v)),small) for v in r] for r in sd],colWidths=[90*mm,45*mm,35*mm],repeatRows=1,hAlign='LEFT'); st.setStyle(TableStyle([('FONTNAME',(0,0),(-1,0),bbase),('GRID',(0,0),(-1,-1),.25,colors.grey),('VALIGN',(0,0),(-1,-1),'TOP')])); story += [st,Paragraph('Metod i korthet',h1),Paragraph(html.escape(a['methodology_note']),body),Paragraph('Begränsningar',h1)]
    for x in a.get('limitations') or ['Inga särskilda begränsningar registrerade.']: story.append(Paragraph('• '+html.escape(x),body))
    if contacts:
        story += [PageBreak(),Paragraph('Kontaktpersoner',h1),Paragraph(f"Kontaktresearch: {contacts.get('searched_agency_count',0)} av {contacts.get('selected_agency_count',0)} valda myndigheter analyserade.",body)]
        cd=[['Person','Roll','Myndighet','Relevans','Säkerhet','Kontaktväg']]
        for x in recommended_contacts(contacts): cd.append([x.get('name',''),x.get('role_title',''),x.get('agency_name',''),x.get('rationale',''),f"{x.get('confidence',0)}/100",contact_value(x)])
        ct=Table([[Paragraph(html.escape(str(v)),small) for v in r] for r in cd],colWidths=[28*mm,30*mm,28*mm,58*mm,18*mm,36*mm],repeatRows=1,hAlign='CENTER'); ct.setStyle(TableStyle([('FONTNAME',(0,0),(-1,0),bbase),('GRID',(0,0),(-1,-1),.25,colors.grey),('VALIGN',(0,0),(-1,-1),'TOP')])); story.append(ct)
        if contacts.get('fallbacks'):
            story += [Paragraph('Endast generell kontaktväg',h2)]
            for f in contacts['fallbacks']:
                cp=f.get('contact_path') or {}; val=cp.get('phone') or cp.get('url') or cp.get('email') or 'Officiell kontaktväg'; story.append(Paragraph(f"<b>{html.escape(f.get('agency_name',''))}</b> – {html.escape(str(val))}",body))
        story.append(Paragraph('Direkt e-post/telefon visas endast när den är offentligt publicerad i professionellt sammanhang. Uppgifter gissas aldrig.',note))
    story += [Paragraph('Exportmetadata',h1),Paragraph(f"Genererad: {html.escape(generated_at or datetime.now(timezone.utc).isoformat(timespec='seconds'))}<br/>Källa: samma strukturerade analysdata som chattresultatet. Ingen ny research görs i exportfasen.",body)]
    def footer(canvas, doc):
        canvas.saveState(); canvas.setFont(base,7); canvas.drawCentredString(A4[0]/2,9*mm,f'Sida {doc.page}'); canvas.restoreState()
    doc=SimpleDocTemplate(str(output),pagesize=A4,rightMargin=10*mm,leftMargin=10*mm,topMargin=12*mm,bottomMargin=15*mm,title=f'{target} – svenska myndigheter',author='Myndighetsteknikradarn')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)


def slug(s):
    s=s.casefold().replace('å','a').replace('ä','a').replace('ö','o'); s=re.sub(r'[^a-z0-9]+','-',s).strip('-'); return s or 'analys'


def main():
    p=argparse.ArgumentParser(description='Exportera Myndighetsteknikradarns strukturerade resultat.')
    p.add_argument('analysis'); p.add_argument('--contacts'); p.add_argument('--format',choices=['markdown','pdf','confluence','all'],default='all'); p.add_argument('--out-dir',default='out'); p.add_argument('--basename'); p.add_argument('--generated-at')
    args=p.parse_args(); a=yaml.safe_load(Path(args.analysis).read_text(encoding='utf-8')); contacts=yaml.safe_load(Path(args.contacts).read_text(encoding='utf-8')) if args.contacts else None; validate(a,contacts)
    out=Path(args.out_dir); out.mkdir(parents=True,exist_ok=True); base=args.basename or f"myndighetsteknikradarn-{slug(a['target']['canonical_name'])}-{date.today().isoformat()}"; generated=args.generated_at or datetime.now(timezone.utc).isoformat(timespec='seconds')
    made=[]
    if args.format in {'markdown','all'}:
        path=out/(base+'.md'); path.write_text(render_markdown(a,contacts,generated),encoding='utf-8'); made.append(path)
    if args.format in {'confluence','all'}:
        path=out/(base+'.confluence.txt'); path.write_text(render_confluence(a,contacts,generated),encoding='utf-8'); made.append(path)
    if args.format in {'pdf','all'}:
        path=out/(base+'.pdf'); render_pdf(a,path,contacts,generated); made.append(path)
    for x in made: print(x)

if __name__=='__main__': main()
