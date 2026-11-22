from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree
import html
import json
import os
import re

root = Path(__file__).resolve().parent
out = root / 'dist'
out.mkdir(exist_ok=True)


def deployment_origin():
    custom = os.environ.get("SITE_ORIGIN", "").strip()
    deployed = os.environ.get("CF_PAGES_URL", "").strip()
    if not custom and not deployed:
        if os.environ.get("CF_PAGES"):
            raise ValueError("No deployment URL received. Set SITE_ORIGIN in Pages.")
        return "http://localhost:8000"
    url = urlsplit(custom or deployed)
    if (url.scheme != "https" or not url.hostname or url.username or url.password
            or url.query or url.fragment or url.path not in ("", "/") or url.port):
        raise ValueError("Expected a public HTTPS origin with no path or credentials.")
    hostname = url.hostname.lower()
    if not re.fullmatch(r"[a-z0-9-]+(?:\.[a-z0-9-]+)+", hostname):
        raise ValueError("Expected a DNS hostname.")
    if not custom:
        parts = hostname.split(".")
        if parts[-2:] != ["pages", "dev"] or len(parts) < 3:
            raise ValueError("Set SITE_ORIGIN to the canonical public URL for this host.")
        hostname = ".".join(parts[-3:])
    return "https://" + hostname


origin = deployment_origin()
categories=[('lawyer','Finding a lawyer','Prepare better questions before choosing representation.'),('records','Accident records','Turn scattered paperwork into a usable record.'),('insurance','Insurance & claims','Organize correspondence and policy questions.'),('costs','Costs & compensation','Understand the questions behind fees and claim figures.')]
articles=[
('motorcycle-injury-lawyer','lawyer','Motorcycle injury lawyer: a practical starting guide','Start with your questions, your records, and the location of the accident—not a promise of a payout.',[
('What this guide can help you do','A search for a motorcycle injury lawyer often starts when several problems arrive at once: paperwork, repair questions, work absences, and uncertainty about who to speak with. This guide helps you prepare for a conversation. It does not decide whether you have a claim or tell you which law applies.'),
('Build a one-page situation summary','Write down where and when the accident happened, the people or vehicles involved, and what documents you already have. Separate what you personally remember from information someone else provided. If you do not know a detail, mark it as unknown rather than filling a gap with an assumption.'),
('Choose the questions that matter to you','Create three headings: what happened, what it has affected, and what you need explained. Under the first, list missing records. Under the second, list documented expenses and practical disruptions. Under the third, ask who would work on the matter, how communication would work, and what the written fee terms mean.'),
('Use the location as a research boundary','A nationwide article cannot replace advice about a particular jurisdiction. Ask a licensed attorney which rules and deadlines require attention in your circumstances. Do not treat the date on this guide as confirmation of a local filing deadline.'),
('Your next useful step','Bring the summary to an attorney you independently select. This website does not match readers to firms, receive consultation requests, or evaluate cases. Use the related guides to prepare a meeting agenda and a records index.')]),
('questions-to-ask-motorcycle-accident-lawyer','lawyer','Questions to ask a motorcycle accident lawyer','A meeting agenda you can use to compare answers without relying on ratings or sales language.',[
('Start with the work, not the pitch','Ask the attorney to describe the work they expect to do and the information they would need before assessing your situation. Keep your own notes of the answers. This is a preparation worksheet, not a ranking of lawyers or a recommendation of a particular firm.'),
('Record these practical answers','Who will be your main contact? What is the preferred way to send documents? How will you hear about progress? What questions remain unanswered after the first discussion? These are useful comparison fields because they turn a general impression into notes you can revisit.'),
('Make uncertainties visible','Ask the lawyer to explain what can and cannot be assessed from the records available. Write down any documents requested and why they matter. Avoid converting an early conversation into an assumed result or an estimated payout.'),
('Leave with a meeting record','Use a simple table with four columns: question, answer, follow-up, and person responsible. If a response is unclear, ask for clarification before making a decision. Keep fee questions on a separate page so they do not disappear into accident notes.'),
('Further reading','The American Bar Association publishes a consumer guide to questions about experience, staffing, fees, and possible outcomes. Read the original guidance alongside your own meeting agenda; it does not endorse this website or any attorney listed elsewhere online.')]),
('documents-for-motorcycle-lawyer-consultation','records','What documents should you bring to a lawyer consultation?','An original folder structure for organizing the materials you already have.',[
('Create an index before collecting everything','A document index can be more useful than a large attachment with no explanation. Start with five folders: accident information, insurance correspondence, treatment paperwork, expenses, and questions. This is an organizational suggestion, not a statement that any particular record proves a legal issue.'),
('Give each item a descriptive name','Use a consistent file name such as date–document type–sender. For example, 2026-11-20–letter–insurer tells you more than scan003. Preserve original files separately from working copies. Note when an item was received and where its original is kept.'),
('Separate records from your comments','Keep a cover note for questions or observations. Avoid adding your own text directly onto an original image or document. Where a file is incomplete or hard to read, label that limitation in the index so you can ask what to obtain next.'),
('Use a missing-records list','Record an item name, possible source, current status, and your next question. Unknown report numbers or missing pages can be listed as unknown. The goal is a transparent inventory, not the appearance of a complete case file.'),
('Share deliberately','Ask the attorney how documents should be transferred and which items are needed. Do not enter medical records, identifying numbers, or private claim details into a public comment box. This site does not accept uploads or store your records.')]),
('motorcycle-insurance-claim-log','insurance','How to organize a motorcycle insurance claim log','A practical correspondence worksheet that keeps documents and unanswered questions together.',[
('Keep the log factual','A claim log is a personal record of correspondence. It does not determine coverage or establish liability. Record the date, organization, contact person, reference number, communication channel, and where the underlying message is stored.'),
('Use one row per interaction','Suggested columns are: date; sender or recipient; topic; document location; stated next step; date mentioned; open question. If a message contains a date, copy it accurately and ask a qualified professional about its significance rather than assuming the log explains a legal deadline.'),
('Distinguish a quote from a summary','If you summarize a phone call, label it as your summary and note when you wrote it. If you quote a written message, keep the original available. Do not merge your interpretation with the sender’s wording.'),
('Bring policy questions to the right person','Make a separate list of terms or requests you do not understand. Ask the insurer or a qualified local attorney to identify the relevant policy language and explain it. This article cannot interpret a policy or tell you whether to accept a payment.'),
('Review without inventing progress','At the end of each review, identify what has arrived, what remains unanswered, and which document supports each entry. An empty status is better than an assumed conclusion. Keep the log with your consultation records so a professional can see the sequence.')]),
('motorcycle-injury-lawyer-fees','costs','Motorcycle injury lawyer fees: a comparison worksheet','Compare written terms and questions—not an assumed standard percentage.',[
('Do not start with a universal number','This site does not publish a standard fee percentage. Instead, use a worksheet to record the terms offered by each lawyer you speak with. A number without its conditions is a poor basis for comparison.'),
('Ask for the terms in writing','The American Bar Association encourages consumers to ask about fees and costs. Keep the written terms together with your questions. If any part of a proposed agreement is unclear, ask the attorney to explain it before you make a decision.'),
('Make your own comparison table','Create columns for firm name, proposed fee method, expenses to clarify, payment timing, and unanswered questions. Leave a cell blank when you have no answer. This worksheet is not a fee calculator and does not estimate the amount you would receive.'),
('Keep the decision broader than price','Use a second page for the practical questions you care about, such as communication and document handling. Record what was actually explained rather than inferring quality from a headline fee or a prominent advertisement.'),
('A useful closing question','Ask the lawyer to walk through the proposed written terms using a clearly hypothetical example. Keep that example separate from any assessment of your situation. No example on this site predicts a fee, a settlement, or a net recovery.')]),
('motorcycle-accident-settlement-estimates','costs','Motorcycle accident settlement estimates: what a number leaves out','Use an expense inventory to prepare questions instead of relying on an online payout figure.',[
('Treat this as a preparation guide','This page provides no average settlement, payout range, or case valuation formula. A search result with a large figure does not tell you how that figure relates to your circumstances. An online article cannot assess your records, applicable law, or disputed facts.'),
('Build an expense inventory','Create a table with the item, date, document source, amount shown, payment status, and questions. You might use separate tabs for treatment paperwork, repair documents, and work-related records. These are inventory categories, not a statement that every item is recoverable.'),
('Avoid double counting','If the same charge appears in a bill and an account summary, connect the entries rather than treating them as separate expenses. Mark an amount as unknown when the document does not establish it. The inventory should make uncertainty visible.'),
('Keep personal notes in a separate section','If you keep notes about practical disruptions, date them and distinguish observations from estimates. Do not turn an expense total into a legal valuation or infer an insurer’s obligations from the table.'),
('Take the questions to a professional','Ask a licensed local attorney what further information would be needed for an assessment and which assumptions remain unresolved. This site does not provide settlement advice or recommend accepting or rejecting an offer.')])]
aba='https://www.americanbar.org/groups/public_education/resources/law_issues_for_consumers/everyday-law/legal-help/questions_to_ask_a_lawyer/'
css='''*{box-sizing:border-box}body{margin:0;background:#f4f6f7;color:#152c36;font:17px/1.7 Arial,sans-serif}a{color:inherit;text-decoration:none}a:hover{text-decoration:underline}header{background:#fff;border-bottom:1px solid #d8e0e3;padding:22px 6%;display:flex;justify-content:space-between;align-items:center;gap:25px}.logo{font-size:25px;font-weight:800;letter-spacing:-1px}.logo i{color:#667d21;font-style:normal}nav{display:flex;gap:25px;font-size:14px}main{max-width:1280px;margin:auto;padding:48px 5%}.hero{background:#142e39;color:white;display:grid;grid-template-columns:1.2fr 1fr;overflow:hidden;border-radius:6px;margin-bottom:48px}.hero>div{padding:48px}.hero h1{font-size:clamp(38px,4.7vw,64px);line-height:1.08;letter-spacing:-2px;font-weight:500;margin:16px 0 24px}.hero p{color:#cad8dd}.hero .photo{min-height:360px;background:linear-gradient(90deg,#142e3922,#142e3900),url(https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=1200&q=80) center/cover}.kicker{font-size:13px;font-weight:bold;letter-spacing:2px;text-transform:uppercase;color:#697e22}.hero .kicker{color:#dff887}.button,button{display:inline-block;border:0;border-radius:3px;background:#dff887;color:#142e39;padding:13px 20px;font-size:15px;font-weight:bold;cursor:pointer}h2{font-size:32px;line-height:1.25;font-weight:500;letter-spacing:-.7px}h3{font-size:23px;line-height:1.3;font-weight:500}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}.card{background:white;padding:28px;border:1px solid #dfe5e8;border-radius:5px}.card p{font-size:16px;color:#536970}.meta{font-size:13px;color:#607880}.row{display:flex;justify-content:space-between;align-items:center;gap:20px}.topics{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:26px 0 48px}.topic{background:#e6ecef;padding:20px;border-top:3px solid #a1b640}.topic p{font-size:14px;color:#536970}.ad{padding:24px;text-align:center;border:1px dashed #b6c3ca;margin:45px 0;background:#edf1f3;color:#627881;font-size:12px;letter-spacing:2px}.ad small{display:block;letter-spacing:0;font-size:13px}.search{width:300px;max-width:100%;font:16px Arial;padding:13px;border:1px solid #b8c6cc;border-radius:3px}.notice{background:#e8eef1;padding:20px;font-size:14px;margin:25px 0;color:#4f6872}.reading{max-width:820px;background:white;padding:40px;margin:auto;border:1px solid #dfe5e8}.reading h1{font-size:43px;line-height:1.15;letter-spacing:-1px}.reading h2{font-size:27px;margin-top:40px}.reading p{color:#344f5b}.reading li{margin:12px 0}.reading a{color:#456b10;text-decoration:underline}.toc{padding:20px;background:#f1f5f6}.toc a{display:block;margin:7px 0}.empty{padding:30px}footer{background:#142e39;color:#c3d2d8;padding:35px 6%;font-size:14px;margin-top:45px}footer a{margin-right:22px}.tools{margin-top:30px;background:#edf2e3;padding:24px}label{display:block;margin:10px 0}.standalone article{margin:45px 0}#search-status{font-size:14px;color:#597078}@media(max-width:850px){nav{flex-wrap:wrap;gap:12px}.hero{grid-template-columns:1fr}.hero>div{padding:30px}.hero .photo{min-height:230px}.grid{grid-template-columns:1fr 1fr}.topics{grid-template-columns:1fr 1fr}.row{align-items:start;flex-direction:column}header{align-items:start;flex-direction:column}.reading{padding:25px}.reading h1{font-size:33px}}@media(max-width:520px){.grid{grid-template-columns:1fr}.topics{grid-template-columns:1fr 1fr}main{padding:25px 5%}}'''
def link(slug):return f'/{slug}/'
def header():return '<header><a class="logo" href="/">rider<i>counsel</i> / JOURNAL</a><nav aria-label="Main navigation">'+''.join(f'<a href="/topics/{s}/">{t}</a>' for s,t,d in categories)+'</nav></header>'
def footer():return '<footer><p><strong>Rider Counsel Journal</strong> · Independent educational publishing concept</p><p><a href="/about/">About & editorial policy</a><a href="/privacy/">Privacy</a><a href="/disclosure/">Advertising disclosure</a></p><p>General information, not legal advice. Not a law firm or lawyer referral service. AI-assisted drafts; no licensed attorney review is claimed. No live advertising is enabled.</p></footer>'
def wrap(title,desc,body,path,kind='WebPage'):
    data={'@context':'https://schema.org','@type':kind,'headline':title,'description':desc,'url':origin+path}
    if kind=='Article':data.update(datePublished='2026-11-22',author={'@type':'Organization','name':'Rider Counsel Journal'},publisher={'@type':'Organization','name':'Rider Counsel Journal'})
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+' | Rider Counsel Journal</title><meta name="description" content="'+html.escape(desc,quote=True)+'"><link rel="canonical" href="'+origin+path+'"><link rel="stylesheet" href="/style.css"><script type="application/ld+json">'+json.dumps(data)+'</script></head><body>'+header()+'<main>'+body+'</main>'+footer()+'</body></html>'
def write(path,content):
    p=out/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
def catname(k):return next(t for s,t,d in categories if s==k)
def card(a):
    s,k,t,d,sections=a
    return f'<article class="card" data-search="{html.escape((t+" "+d+" "+catname(k)).lower(),quote=True)}"><div class="kicker">{catname(k)}</div><h3><a href="/{s}/">{t}</a></h3><p>{d}</p><span class="meta">Preparation guide · Nov 22, 2026</span></article>'
ad='<aside class="ad" aria-label="Inactive advertisement placeholder">ADVERTISEMENT<small>Reserved space · No live ads</small></aside>'
intro='<section class="hero"><div><div class="kicker">The motorcycle injury resource</div><h1>Clear information.<br>A more informed<br>road ahead.</h1><p>Practical reading on choosing a motorcycle injury lawyer, organizing accident records, and preparing better questions.</p><a class="button" href="/motorcycle-injury-lawyer/">Start with the essential guide</a></div><div class="photo" role="img" aria-label="A motorcycle parked outdoors"></div></section>'
topics='<h2>Explore by topic</h2><div class="topics">'+''.join(f'<a class="topic" href="/topics/{s}/"><strong>{t}</strong><p>{d}</p></a>' for s,t,d in categories)+'</div>'
search='<div class="row"><h2>From the journal</h2><label><span class="meta">Find a guide</span><br><input class="search" id="search" type="search" placeholder="Search fees, records, lawyer…"></label></div><p id="search-status" aria-live="polite">6 guides</p>'
js='''<script>document.getElementById('search').addEventListener('input',function(){let n=0;document.querySelectorAll('[data-search]').forEach(c=>{c.hidden=!c.dataset.search.includes(this.value.trim().toLowerCase());if(!c.hidden)n++});document.getElementById('search-status').textContent=n?n+' guides found':'No matching guides. Try records, lawyer, or fees.'});</script>'''
home=intro+topics+search+'<div class="grid">'+''.join(card(a) for a in articles)+'</div>'+ad+'<section class="notice"><strong>How to use this journal</strong><p>Start with a topic, make a list of questions, and consult a qualified professional for advice about your situation. Articles are AI-assisted educational drafts. There is no attorney review or case evaluation service on this site.</p><a href="/about/">Read our editorial approach</a></section>'+js
write('index.html',wrap('Motorcycle injury lawyer guides, records & insurance questions','An independent motorcycle injury blog with practical consultation, document organization, insurance correspondence, and fee comparison guides.',home,'/'))
for k,t,d in categories:
    body=f'<p class="meta"><a href="/">Home</a> / Topics</p><div class="kicker">Topic collection</div><h1>{t}</h1><p>{d}</p><div class="grid">'+''.join(card(a) for a in articles if a[1]==k)+'</div>'
    write(f'topics/{k}/index.html',wrap(t,d,body,f'/topics/{k}/'))
article_examples = {'motorcycle-insurance-claim-log': '<section><h2>A sample log for a missing repair estimate</h2>\n'
                                   '<p>Suppose your repair shop emailed a motorcycle repair estimate and an '
                                   'adjuster later asks for it. These three entries let you trace what '
                                   'happened to the document.</p>\n'
                                   '<ol><li><strong>Monday, 9:10 a.m. · Email from repair shop.</strong> The '
                                   'shop sent estimate R17. Saved the original email and the two-page PDF '
                                   'under “Repairs.”</li>\n'
                                   '<li><strong>Monday, 2:15 p.m. · Call with adjuster.</strong> My call '
                                   'notes say the adjuster requested a copy through the insurer’s portal. '
                                   'Open question: does the portal accept a PDF? I have no written '
                                   'confirmation of the request yet.</li>\n'
                                   '<li><strong>Tuesday, 8:40 a.m. · Portal upload.</strong> Uploaded both '
                                   'pages of R17 and saved the receipt. Next question for the adjuster: can '
                                   'you open both pages?</li></ol>\n'
                                   '<p>In this example, the receipt confirms an upload. Whether the insurer '
                                   'has reviewed the estimate or agreed to its amount remains an open '
                                   'question. For your own entries, copy these five fields onto a fresh '
                                   'line: date and time, contact, document, what happened, next '
                                   'question.</p>\n'
                                   '<p>The National Association of Insurance Commissioners recommends dating '
                                   'notes of conversations with an agent or adjuster. Its consumer guide '
                                   'concerns auto claims generally. Consult your motorcycle policy for your '
                                   'claim’s specific process. <a '
                                   'href="https://content.naic.org/article/what-you-should-know-about-filing-auto-claim">NAIC '
                                   'guide to filing an auto claim</a>.</p></section>',
 'motorcycle-accident-settlement-estimates': '<section><h2>One clinic visit, three pieces of paper</h2>\n'
                                             '<p>Imagine that you have a health plan statement, a receipt, '
                                             'and a clinic bill for the same visit. Match the provider, '
                                             'service date, and claim reference first. Your worksheet can '
                                             'then record each figure once under its own heading.</p>\n'
                                             '<ul><li><strong>Explanation of benefits (EOB).</strong> The '
                                             'plan lists a $240 allowed charge, a $180 plan payment, and $60 '
                                             'as the patient’s share.</li>\n'
                                             '<li><strong>Receipt.</strong> The clinic recorded your $20 '
                                             'payment on the day of the visit.</li>\n'
                                             '<li><strong>Later bill.</strong> The clinic asks for $40. The '
                                             '$20 receipt and $40 bill together account for the $60 shown on '
                                             'the EOB.</li></ul>\n'
                                             '<p>Your row for that visit reads “Patient share $60 | paid $20 '
                                             '| outstanding $40.” If the bill still shows $60 due, keep the '
                                             'original figures and ask the clinic where the $20 was applied. '
                                             'That question is more useful at a consultation than adding all '
                                             'three documents together.</p>\n'
                                             '<p>The Centers for Medicare &amp; Medicaid Services explains '
                                             'how to read the patient balance and why an EOB may omit an '
                                             'earlier payment. These fictional figures illustrate the '
                                             'paperwork only. <a '
                                             'href="https://www.cms.gov/initiatives/your-patient-rights/medical-bill-rights/get-help/guides-resources/read-explanation-benefits">CMS '
                                             'guide to reading an explanation of benefits</a>.</p></section>',
 'motorcycle-injury-lawyer-fees': '<section><h2>Ask which amount the percentage applies to</h2>\n'
                                  '<p>Use round numbers to check your reading of an agreement. Suppose an '
                                  'exercise uses $10,000 received, $1,000 in case expenses, and an invented '
                                  'fee of 25%. Ignore any other deductions for this exercise. The order '
                                  'changes the arithmetic.</p>\n'
                                  '<ul><li><strong>Fee calculated on the full amount.</strong> A quarter of '
                                  '$10,000 is $2,500. Subtracting the fee and the $1,000 expense leaves '
                                  '$6,500.</li>\n'
                                  '<li><strong>Expenses deducted before calculating the fee.</strong> '
                                  'Subtract $1,000 first. A quarter of the remaining $9,000 is $2,250, '
                                  'leaving $6,750.</li></ul>\n'
                                  '<p>The $250 difference comes from applying the percentage to a different '
                                  'base. Ask the lawyer to point to the sentence in your proposed agreement '
                                  'that specifies the base. Then ask whether the percentage changes if the '
                                  'case proceeds to trial and who pays expenses if there is no recovery. '
                                  'Write the answers against the relevant clauses.</p>\n'
                                  '<p>This example uses illustrative numbers. Your agreement and local rules '
                                  'govern your situation. The American Bar Association’s model rule '
                                  'identifies the calculation order and responsibility for expenses as '
                                  'points to address. <a '
                                  'href="https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_1_5_fees/">ABA '
                                  'Model Rule 1.5, paragraph (c)</a>.</p></section>'}

def articlebody(a):
    s,k,t,d,sections=a
    toc='<nav class="toc" aria-label="On this page"><strong>In this guide</strong>'+''.join(f'<a href="#{s}-{i}">{h}</a>' for i,(h,p) in enumerate(sections))+'</nav>'
    body=f'<div class="kicker">{catname(k)}</div><h1>{t}</h1><p>{d}</p><div class="meta">By Rider Counsel Journal · Published November 22, 2026 · AI-assisted draft · No attorney review</div>'+toc
    body+=''.join(f'<section id="{s}-{i}"><h2>{h}</h2><p>{p}</p></section>' for i,(h,p) in enumerate(sections))
    body += article_examples.get(s, '')
    if k=='lawyer' and s!='motorcycle-injury-lawyer' or s=='motorcycle-injury-lawyer-fees':body+=f'<h2>Source</h2><p><a href="{aba}" target="_blank" rel="noopener">American Bar Association: Questions to Ask a Lawyer</a>. Source checked November 22, 2026. The worksheet structure and examples are original organizational suggestions.</p>'
    else:body+='<h2>Scope and methodology</h2><p>This article is an original organizational worksheet. It contains no jurisdiction-specific legal interpretation, coverage determination, deadline, or settlement estimate. Ask a licensed local professional about your circumstances.</p>'
    body+='<h2>Continue reading</h2><ul>'+''.join(f'<li><a href="/{x[0]}/">{x[2]}</a></li>' for x in articles if x[0]!=s and (x[1]==k or x[0]=='motorcycle-injury-lawyer'))+'</ul>'
    return body
for a in articles:write(a[0]+'/index.html',wrap(a[2],a[3],'<article class="reading">'+articlebody(a)+ad+'</article>',link(a[0]),'Article'))
policies={
'about':('About & editorial policy','<p>Rider Counsel Journal is an independent educational website concept about organizing information after a motorcycle accident. It is not a law firm, a referral service, or a source of individualized legal advice.</p><h2>How these guides are made</h2><p>The initial guides were drafted with AI assistance. We distinguish original organizational worksheets from externally sourced guidance and link to the source where used. No attorney review, legal qualification, or first-hand case experience is claimed.</p><h2>Editorial boundaries</h2><p>We do not publish invented case results, lawyer endorsements, universal filing deadlines, or estimated payouts. A future jurisdiction-specific article needs current official sources and qualified review before publication.</p><h2>Publisher and corrections</h2><p>The operator has not yet supplied a public legal identity or contact address. This is a pre-launch edition. A genuine publisher identity and working corrections contact must be added before public business use; no contact submission service is currently available.</p>'),
'privacy':('Privacy notice','<p>This pre-launch edition has no forms, user accounts, analytics scripts, advertising scripts, or document upload service. The search function filters the page in your browser without sending search terms to an application server.</p><h2>External services</h2><p>The home page loads a motorcycle image from images.unsplash.com. Your browser contacts that service to retrieve the image. External reference links take you to other websites with their own privacy practices. Hosting providers may process technical request data under their own terms.</p><h2>Before advertising is enabled</h2><p>No AdSense code is currently installed. Before enabling ads, the operator must update this notice for the actual vendors, data uses, contact details, and applicable consent choices. This draft does not claim that a consent platform or regional advertising configuration is already operating.</p>'),
'disclosure':('Advertising & independence','<p>This website is intended to support advertising-funded educational publishing. All advertisement boxes in this edition are inactive layout placeholders. No AdSense publisher ID, live ad unit, or affiliate link is installed.</p><h2>Separation from editorial content</h2><p>Future advertisements should be clearly distinguishable from articles and navigation. An advertiser’s appearance would not constitute an editorial endorsement or attorney recommendation. Readers are not asked to click advertisements to support the site.</p><h2>No commercial claims</h2><p>No Google approval, search ranking, traffic, or revenue is claimed. Before enabling advertising, the operator needs an approved account and site configuration, updated privacy disclosures, and any applicable consent setup.</p>')}
for s,(t,b) in policies.items():write(s+'/index.html',wrap(t,t+' for Rider Counsel Journal','<article class="reading"><h1>'+t+'</h1>'+b+'</article>',f'/{s}/'))
write('style.css', css + '\nnav.toc{display:block}.topic p{line-height:1.5}')
urls=['/']+[f'/topics/{s}/' for s,t,d in categories]+[link(a[0]) for a in articles]+[f'/{s}/' for s in policies]
write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+origin+u+'</loc></url>' for u in urls)+'</urlset>')
write('robots.txt','User-agent: *\nAllow: /\nSitemap: '+origin+'/sitemap.xml\n')

write("404.html", """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Page not found | Rider Counsel Journal</title><meta name="robots" content="noindex">
<link rel="stylesheet" href="/style.css"></head><body><main class="reading">
<h1>Page not found</h1><p>The address may have changed. Browse the journal to find the guide you need.</p>
<p><a href="/">Browse Rider Counsel Journal</a></p></main></body></html>""")

# Check the files Google and visitors will receive before Pages uploads dist.
sitemap = ElementTree.parse(out / "sitemap.xml")
locations = [node.text for node in sitemap.iterfind(".//{*}loc")]
if sorted(locations) != sorted(origin + path for path in urls):
    raise ValueError("Sitemap and published pages differ.")

for url_path in urls:
    page = out / url_path.strip("/") / "index.html"
    contents = page.read_text()
    if f'<link rel="canonical" href="{origin}{url_path}">' not in contents:
        raise ValueError(f"Missing or incorrect canonical on {page}")
    structured = re.search(r'<script type="application/ld\+json">(.+?)</script>', contents)
    if not structured or json.loads(structured.group(1))["url"] != origin + url_path:
        raise ValueError(f"Invalid structured data URL on {page}")
    for target in re.findall(r'href="([^"]+)"', contents):
        if target.startswith("#") and f'id="{target[1:]}"' not in contents:
            raise ValueError(f"Missing anchor on {page}: {target}")
        if target.startswith("/"):
            local = out / target.lstrip("/")
            if target.endswith("/"):
                local = local / "index.html"
            if not local.is_file():
                raise ValueError(f"Broken link on {page}: {target}")

print(f"Built {len(urls)} pages and a 404 page. Canonical origin: {origin}")
