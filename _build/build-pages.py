#!/usr/bin/env python3
"""Generiert die Leistungsseiten (google-ads-agentur-bodensee.html, meta-ads-agentur.html,
amazon-ppc-agentur.html, ki-werbevideos.html) aus einem gemeinsamen Template.
Aufruf:  python3 _build/build-pages.py   (im Repo-Root)
Der Ordner _build/ wird von GitHub Pages nicht veröffentlicht (Unterstrich)."""
import json, pathlib, html, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
TODAY = "2026-09-30"
TODAY_DE = "30.09.2026"

HEAD = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Marc Nothelfer – AIclicks">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#0b0e14">
<link rel="canonical" href="https://aiclicks.de/{slug}">
<link rel="icon" href="/logo.svg" type="image/svg+xml">
<link rel="stylesheet" href="/styles.css">
<meta name="geo.region" content="DE-BW">
<meta name="geo.placename" content="Friedrichshafen">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://aiclicks.de/{slug}">
<meta property="og:site_name" content="AIclicks">
<meta property="og:locale" content="de_DE">
<meta property="og:image" content="https://aiclicks.de/{image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://aiclicks.de/{image}">
<script type="application/ld+json">
{schema}
</script>
<!-- Google Consent Mode v2 (Default: alles abgelehnt) + Google Ads Tag -->
<script>
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
gtag('consent','default',{{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied'}});
gtag('js',new Date());gtag('config','AW-304314047');
try{{const c=JSON.parse(localStorage.getItem('cookie-consent')||'null');if(c&&c.marketing){{gtag('consent','update',{{ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted',analytics_storage:'granted'}});}}}}catch(e){{}}
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-304314047"></script>
</head>
<body>
<a class="skip-link" href="#main">Zum Inhalt springen</a>
<header>
  <div class="wrap nav">
    <a class="brand" href="/"><img src="/logo.svg" alt="AIclicks Logo" width="30" height="30"><span>AI<b>clicks</b></span></a>
    <nav id="navlinks" aria-label="Hauptnavigation">
      <a href="/#leistungen">Leistungen</a>
      <a href="/#ergebnisse">Ergebnisse</a>
      <a href="/#preise">Preise</a>
      <a href="/#ueber">Über uns</a>
    </nav>
    <div class="nav-right">
      <a href="/#kontakt" class="btn">Wachstumsanalyse</a>
      <button class="menu-btn" id="menuBtn" aria-label="Menü" aria-expanded="false">☰</button>
    </div>
  </div>
</header>
<main id="main">
"""

FOOT = """
<!-- CTA -->
<section id="kontakt">
  <div class="wrap">
    <div class="panel cta-box">
      <p class="eyebrow">Kostenlos · Kein Pitch</p>
      <h2>{cta_h}</h2>
      <p>{cta_p}</p>
      <a href="/#kontakt" class="btn">Kostenlose Wachstumsanalyse anfordern</a>
      <p style="margin-top:14px;font-size:14px">Oder direkt: <a href="tel:+4915129810072">+49 151 29810072</a> · <a href="mailto:marc@aiclicks.de">marc@aiclicks.de</a> · <a href="https://calendly.com/marc-aiclicks/30min" target="_blank" rel="noopener">Termin buchen</a></p>
      <p class="updated">Autor: <a href="/#ueber">Marc Nothelfer</a>, Gründer AIclicks · Zuletzt aktualisiert: {today_de}</p>
    </div>
  </div>
</section>
</main>
<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="/" style="margin-bottom:12px"><img src="/logo.svg" alt="AIclicks" style="width:26px;height:26px"><span>AI<b style="color:var(--accent)">clicks</b></span></a>
        <p style="font-size:14px">Performance-Marketing-Agentur<br>Friedrichshafen am Bodensee · <a href="tel:+4915129810072">+49 151 29810072</a></p>
      </div>
      <div>
        <h3>Leistungen</h3>
        <a href="/google-ads-agentur-bodensee.html">Google Ads Agentur</a><a href="/meta-ads-agentur.html">Meta Ads Agentur</a><a href="/amazon-ppc-agentur.html">Amazon PPC Agentur</a><a href="/ki-werbevideos.html">Werbevideos &amp; Anzeigen</a><a href="/website-in-5-tagen.html">Website in 5 Tagen</a><a href="/automatisierung.html">Automatisierung</a>
      </div>
      <div>
        <h3>Unternehmen</h3>
        <a href="/#ergebnisse">Ergebnisse</a><a href="/#ueber">Über uns</a><a href="/#preise">Preise</a><a href="/roi-rechner.html">Wachstums-Rechner</a><a href="/#kontakt">Kontakt</a>
      </div>
      <div>
        <h3>Rechtliches</h3>
        <a href="/impressum.html">Impressum</a><a href="/datenschutz.html">Datenschutz</a>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© 2026 AIclicks · Marc Nothelfer · Friedrichshafen</span>
      <span>Made in Germany · Google Ads &amp; Meta Blueprint zertifiziert</span>
    </div>
  </div>
</footer>
<script>
document.getElementById('menuBtn').addEventListener('click',function(){{var n=document.getElementById('navlinks');n.classList.toggle('open');this.setAttribute('aria-expanded',n.classList.contains('open'));}});
</script>
</body>
</html>
"""

def faq_html(faq):
    out = ['<section><div class="wrap"><div class="section-head"><h2>Häufige Fragen</h2></div><div class="faq">']
    for q, a in faq:
        out.append(f'<details class="faqit"><summary>{q}</summary><div class="ans">{a}</div></details>')
    out.append('</div></div></section>')
    return "\n".join(out)

def schema_for(p):
    faq = [{"@type": "Question", "name": html.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": html.unescape(strip_tags(a))}} for q, a in p["faq"]]
    url = f"https://aiclicks.de/{p['slug']}"
    g = [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": p["title"], "description": p["desc"],
         "inLanguage": "de-DE", "dateModified": TODAY, "datePublished": TODAY,
         "isPartOf": {"@id": "https://aiclicks.de/#website"}, "about": {"@id": url + "#service"},
         "author": {"@id": "https://aiclicks.de/#marc"}, "publisher": {"@id": "https://aiclicks.de/#organization"},
         "breadcrumb": {"@id": url + "#breadcrumb"}},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Start", "item": "https://aiclicks.de/"},
            {"@type": "ListItem", "position": 2, "name": "Leistungen", "item": "https://aiclicks.de/#leistungen"},
            {"@type": "ListItem", "position": 3, "name": p["crumb"], "item": url}]},
        {"@type": "Service", "@id": url + "#service", "name": p["service_name"], "serviceType": p["service_type"],
         "description": p["desc"], "url": url,
         "provider": {"@id": "https://aiclicks.de/#organization"},
         "areaServed": [{"@type": "City", "name": "Friedrichshafen"}, {"@type": "AdministrativeArea", "name": "Bodenseekreis"},
                        {"@type": "Country", "name": "Deutschland"}, {"@type": "Country", "name": "Österreich"}, {"@type": "Country", "name": "Schweiz"}],
         "audience": {"@type": "BusinessAudience", "name": p["audience"]},
         "offers": {"@type": "Offer", "price": p["price"], "priceCurrency": "EUR", "url": url,
                    "priceSpecification": {"@type": "UnitPriceSpecification", "price": p["price"], "priceCurrency": "EUR", "unitText": p["unit"], "minPrice": p["price"]},
                    "availability": "https://schema.org/InStock"}},
        {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": faq},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False, indent=1)

import re
def strip_tags(s): return re.sub(r"<[^>]+>", "", s)

def build(p):
    body = HEAD.format(title=p["title"], desc=p["desc"], slug=p["slug"], image=p["image"], schema=schema_for(p))
    body += p["body"]
    body += faq_html(p["faq"])
    body += FOOT.format(cta_h=p["cta_h"], cta_p=p["cta_p"], today_de=TODAY_DE)
    (ROOT / p["slug"]).write_text(body, encoding="utf-8")
    print("wrote", p["slug"], len(body))

PROCESS = """
<section><div class="wrap"><div class="panel">
  <div class="section-head"><h2>So läuft die Zusammenarbeit ab</h2><p>Drei Schritte, keine Überraschungen. Der erste ist kostenlos.</p></div>
  <div class="grid3">
    <div class="card step"><div class="no">01 · Analyse</div><h3>Kostenlose Wachstumsanalyse</h3><p>Wir prüfen bestehende Konten, Zielgruppe, Tracking und Zahlen. Du bekommst einen konkreten Plan – ob du mit uns arbeitest oder nicht.</p></div>
    <div class="card step"><div class="no">02 · Aufbau</div><h3>Kampagnen, Creatives, Tracking</h3><p>Setup in Tagen, nicht Monaten: Kampagnenstruktur, Conversion-Tracking, erste Creative-Varianten und Landingpage-Check.</p></div>
    <div class="card step"><div class="no">03 · Skalierung</div><h3>Testen, messen, skalieren</h3><p>Wöchentliches Reporting mit einer Zahl, die zählt: Kosten pro Anfrage bzw. Bestellung. Was funktioniert, bekommt mehr Budget.</p></div>
  </div>
</div></div></section>
"""

GUAR = """
<section><div class="wrap"><div class="panel">
  <div class="section-head"><h2>Konditionen ohne Kleingedrucktes</h2></div>
  <div class="grid3 guar">
    <div class="card"><div class="g"><span class="ic">✓</span><div><h3>Monatlich kündbar</h3><p>Keine Mindestlaufzeit, keine Setup-Gebühr.</p></div></div></div>
    <div class="card"><div class="g"><span class="ic">✓</span><div><h3>Deine Konten gehören dir</h3><p>Werbekonten, Daten und Creatives bleiben in deinem Besitz – auch nach dem Ende der Zusammenarbeit.</p></div></div></div>
    <div class="card"><div class="g"><span class="ic">✓</span><div><h3>Wöchentliches Reporting</h3><p>Du siehst jede Woche, was wir tun und was es bringt. Direkter Draht zu Marc, kein Callcenter.</p></div></div></div>
  </div>
</div></div></section>
"""

PAGES = []

# ---------------------------------------------------------------- GOOGLE ADS
PAGES.append(dict(
    slug="google-ads-agentur-bodensee.html", crumb="Google Ads Agentur", image="og-image.jpg",
    title="Google Ads Agentur Bodensee & Friedrichshafen | AIclicks",
    desc="Google Ads Agentur in Friedrichshafen am Bodensee: Suchkampagnen, die Anfragen bringen statt Klicks. Ab 1.490 €/Monat, monatlich kündbar, sauberes Tracking.",
    service_name="Google Ads Management", service_type="Google Ads Agentur",
    audience="Mittelstand, Handwerk, Dienstleister, E-Commerce", price="1490", unit="Monat",
    cta_h="Wie viele Anfragen sind mit deinem Budget realistisch?",
    cta_p="In 20 Minuten schauen wir uns dein Google-Ads-Konto (oder deinen Markt) an und sagen dir ehrlich, was drin ist – kostenlos, ohne Verkaufsdruck.",
    body="""
<section class="sub-hero"><div class="wrap">
  <p class="crumbs"><a href="/">Start</a> › <a href="/#leistungen">Leistungen</a> › Google Ads Agentur</p>
  <p class="eyebrow">Google Ads Agentur · Friedrichshafen am Bodensee</p>
  <h1>Google Ads, die Anfragen bringen.<br>Nicht nur Klicks.</h1>
  <p class="lead">AIclicks ist eine Google Ads Agentur aus Friedrichshafen am Bodensee. Wir bauen Suchkampagnen für Handwerk, Dienstleister, Mittelstand und Onlineshops, die auf eine Zahl optimiert werden: Kosten pro Anfrage bzw. Bestellung. Ab 1.490 € im Monat, monatlich kündbar.</p>
  <div class="hero-cta"><a href="/#kontakt" class="btn">Kostenlose Konto-Analyse</a><a href="/#preise" class="btn ghost">Preise ansehen</a></div>
</div></section>

<section><div class="wrap"><div class="panel prose">
  <h2>Was macht eine Google Ads Agentur?</h2>
  <div class="def"><p>Eine Google Ads Agentur plant, erstellt und optimiert bezahlte Anzeigen im Google-Netzwerk (Suche, Shopping, YouTube, Display, Performance Max). Sie wählt Suchbegriffe mit Kaufabsicht aus, schreibt Anzeigentexte, richtet Conversion-Tracking ein und steuert Gebote und Budgets so, dass jede Anfrage möglichst wenig kostet. Bezahlt wird das Werbebudget direkt an Google; die Agentur erhält ein separates Honorar.</p></div>
  <p>Der Unterschied zwischen guten und schlechten Google-Ads-Konten liegt selten in der Plattform, sondern in drei Dingen: <strong>welche Suchbegriffe Geld bekommen</strong>, <strong>ob Conversions überhaupt sauber gemessen werden</strong> und <strong>ob jemand wöchentlich an den Stellschrauben dreht</strong>. Genau das ist unser Job.</p>

  <h2>Google Ads für Handwerk, Dienstleister und Mittelstand am Bodensee</h2>
  <p>Für regionale Betriebe ist Google Ads der direkteste Kanal, den es gibt: Jemand in Friedrichshafen, Ravensburg, Konstanz oder Lindau sucht „Elektriker Notdienst“, „Fensterbau“ oder „Steuerberater Friedrichshafen“ – und deine Anzeige steht ganz oben. Kein Streuverlust, keine Kaltakquise. Wir kombinieren Suchkampagnen mit lokaler Ausrichtung, Anruf-Erweiterungen und einer Landingpage, die die Anfrage auch tatsächlich einsammelt.</p>
  <ul>
    <li><strong>Regionale Ausrichtung:</strong> Radius- und Ortsziele rund um den Bodenseekreis, Oberschwaben und Allgäu – oder deutschlandweit, wenn du liefern kannst.</li>
    <li><strong>Suchbegriffe mit Kaufabsicht:</strong> „kaufen“, „Angebot“, „Kosten“, „in der Nähe“ – statt teurer Informationssuchen.</li>
    <li><strong>Negativ-Keywords:</strong> Jobs, „kostenlos“, „selber machen“ und Co. fliegen raus, bevor sie Budget fressen.</li>
    <li><strong>Anruf- und Formular-Tracking:</strong> Jede Anfrage wird gezählt, damit Google auf echte Anfragen optimieren kann.</li>
  </ul>

  <h2>Google Ads für Onlineshops: Shopping &amp; Performance Max</h2>
  <p>Für E-Commerce setzen wir auf Google Shopping und Performance Max mit sauberem Produktfeed, Margen-basierten ROAS-Zielen und Suchkampagnen für Marken- und Kategoriebegriffe. Wir betreiben selbst einen Shopify-Shop mit 286.000 € Umsatz und Conversion-Raten bis 9,7 % – wir wissen also, wie sich Werbe-Euro anfühlen, wenn es die eigenen sind.</p>

  <h2>Was kostet eine Google Ads Agentur?</h2>
  <table class="tbl">
    <thead><tr><th>Posten</th><th>Bei AIclicks</th><th>Branchenüblich</th></tr></thead>
    <tbody>
      <tr><td>Agentur-Honorar</td><td>ab 1.490 € / Monat (Setup + laufende Optimierung + wöchentliches Reporting)</td><td>10–20 % vom Werbebudget oder 800–3.000 € pauschal</td></tr>
      <tr><td>Setup-Gebühr</td><td>keine</td><td>500–2.500 € einmalig</td></tr>
      <tr><td>Mindestlaufzeit</td><td>keine, monatlich kündbar</td><td>3–12 Monate</td></tr>
      <tr><td>Werbebudget</td><td>geht direkt an Google; Empfehlung ab ca. 1.000 € / Monat</td><td>–</td></tr>
      <tr><td>Kontoinhaber</td><td>du – Konto und Daten bleiben bei dir</td><td>oft die Agentur</td></tr>
    </tbody>
  </table>
  <p>Rechenbeispiel Handwerk: Bei 1.500 € Werbebudget und 40–80 € pro Anfrage kommen 20–35 qualifizierte Anfragen im Monat zusammen. Ein einziger Auftrag im Handwerk bringt oft 3.000–10.000 € – ab dem ersten zusätzlichen Kunden ist das Honorar bezahlt. Was in deinem Fall realistisch ist, rechnen wir im <a href="/roi-rechner.html">Wachstums-Rechner</a> oder in der kostenlosen Analyse vor.</p>

  <h2>Woran du eine gute Google Ads Agentur erkennst</h2>
  <ol>
    <li><strong>Sie fragt zuerst nach deinem Deckungsbeitrag</strong>, nicht nach deinem Budget.</li>
    <li><strong>Sie richtet Conversion-Tracking ein, bevor sie Geld ausgibt</strong> – inklusive Anrufen und Formularen.</li>
    <li><strong>Sie berichtet Kosten pro Anfrage</strong>, nicht Impressionen und Klickraten.</li>
    <li><strong>Das Konto läuft auf deinen Namen</strong> und du hast jederzeit Zugriff.</li>
    <li><strong>Keine Mindestlaufzeit.</strong> Wer gute Arbeit macht, braucht keine Vertragsbindung.</li>
  </ol>
  <p>Google Ads ist stark, wenn Nachfrage existiert. Wenn dein Angebot neu ist oder erklärt werden muss, ergänzen wir mit <a href="/meta-ads-agentur.html">Meta Ads</a> und <a href="/ki-werbevideos.html">Werbevideos</a>, die Nachfrage erst erzeugen.</p>
</div></div></section>
""" + PROCESS + GUAR,
    faq=[
        ("Was kostet Google Ads Betreuung bei AIclicks?", "Ads Management kostet ab 1.490 € pro Monat inklusive Setup, laufender Optimierung, Conversion-Tracking und wöchentlichem Reporting. Dazu kommt dein Werbebudget, das direkt an Google geht. Keine Setup-Gebühr, keine Mindestlaufzeit."),
        ("Wie viel Werbebudget brauche ich für Google Ads?", "Für regionale Dienstleister und Handwerksbetriebe empfehlen wir ab etwa 1.000 € Werbebudget pro Monat, für Onlineshops ab 1.500–2.000 €. Darunter liefert Google zu wenige Daten, um sinnvoll zu optimieren."),
        ("Wie schnell bringt Google Ads Anfragen?", "Suchkampagnen liefern oft innerhalb der ersten Tage erste Anfragen, weil die Nachfrage bereits existiert. Belastbar optimiert ist ein Konto nach 30–90 Tagen, wenn genug Conversion-Daten vorliegen."),
        ("Arbeitet ihr nur am Bodensee?", "Nein. Wir sitzen in Friedrichshafen und betreuen Kunden aus Friedrichshafen, Ravensburg, Konstanz, Lindau und dem Bodenseekreis gern vor Ort – deutschlandweit, in Österreich und der Schweiz arbeiten wir remote per Video-Call. Google-Ads-Ergebnisse sind nicht ortsgebunden."),
        ("Gehört mir das Google-Ads-Konto?", "Ja, immer. Wir arbeiten in deinem Konto über einen Verwaltungszugang. Kampagnen, Daten und Conversion-Historie bleiben bei dir – auch wenn du kündigst."),
        ("Google Ads oder SEO – was ist besser?", "Beides hat seinen Platz: Google Ads bringt sofort messbare Anfragen und lässt sich tagesgenau steuern, SEO braucht Monate, wirkt dann aber ohne Klickkosten. Für die meisten Betriebe ist Google Ads der schnellste Weg zu planbaren Anfragen; SEO bauen wir parallel über Landingpages auf."),
    ],
))

# ---------------------------------------------------------------- META ADS
PAGES.append(dict(
    slug="meta-ads-agentur.html", crumb="Meta Ads Agentur", image="og-image.jpg",
    title="Meta Ads Agentur – Facebook &amp; Instagram Ads | AIclicks",
    desc="Meta Ads Agentur aus Friedrichshafen: Facebook- &amp; Instagram-Ads mit starken Creatives, sauberem Tracking und ROAS-Fokus für Shops und lokale Betriebe. Ab 1.490 €/Monat.",
    service_name="Meta Ads Management (Facebook & Instagram Ads)", service_type="Meta Ads Agentur",
    audience="E-Commerce, lokale Betriebe, Dienstleister, Fitnessstudios", price="1490", unit="Monat",
    cta_h="Lass uns deine Meta-Kampagnen anschauen.",
    cta_p="Kostenlose Analyse deines Werbekontos oder deines Marktes: Wir zeigen dir, wo Budget verbrennt und welche Creatives fehlen.",
    body="""
<section class="sub-hero"><div class="wrap">
  <p class="crumbs"><a href="/">Start</a> › <a href="/#leistungen">Leistungen</a> › Meta Ads Agentur</p>
  <p class="eyebrow">Meta Ads Agentur · Facebook &amp; Instagram · Bodensee</p>
  <h1>Meta Ads, die Nachfrage erzeugen –<br>bevor jemand sucht.</h1>
  <p class="lead">AIclicks ist eine Meta Ads Agentur aus Friedrichshafen am Bodensee. Wir schalten Facebook- und Instagram-Anzeigen für Onlineshops, lokale Betriebe und Dienstleister – mit KI-produzierten Creatives im Wochentakt, sauberem Conversion-Tracking und einem Ziel: Bestellungen und Anfragen zu Kosten, die sich rechnen.</p>
  <div class="hero-cta"><a href="/#kontakt" class="btn">Kostenlose Konto-Analyse</a><a href="/ki-werbevideos.html" class="btn ghost">Werbevideos ansehen</a></div>
</div></section>

<section><div class="wrap"><div class="panel prose">
  <h2>Was macht eine Meta Ads Agentur?</h2>
  <div class="def"><p>Eine Meta Ads Agentur plant und steuert bezahlte Werbung auf Facebook, Instagram, Messenger und im Audience Network. Anders als bei Google Ads sucht dort niemand aktiv nach deinem Produkt – Meta Ads erzeugen Nachfrage durch Creatives, die im Feed stoppen. Entscheidend sind deshalb Creative-Tests, Zielgruppen-Signale (Pixel, Conversions API) und eine Kampagnenstruktur, die Metas Algorithmus genug Daten zum Lernen gibt.</p></div>
  <p>2026 entscheidet auf Meta zu rund 70–80 % das Creative über Erfolg oder Misserfolg – Targeting übernimmt der Algorithmus weitgehend selbst (Advantage+). Wer nur alle paar Wochen ein neues Video hat, verliert. Deshalb produzieren wir Creatives mit KI: <a href="/ki-werbevideos.html">mehr Varianten, schneller, günstiger</a>.</p>

  <h2>Meta Ads für Onlineshops</h2>
  <ul>
    <li><strong>Advantage+ Shopping-Kampagnen</strong> mit Produktkatalog, dynamischen Anzeigen und Retargeting.</li>
    <li><strong>Creative-Testing im Wochentakt:</strong> Hooks, Formate (Reel, Story, Feed), UGC-Stil vs. Produkt-Demo.</li>
    <li><strong>Pixel + Conversions API:</strong> serverseitiges Tracking, damit trotz iOS-Einschränkungen Kaufdaten ankommen.</li>
    <li><strong>ROAS statt Reichweite:</strong> Budget geht dahin, wo der Deckungsbeitrag stimmt – nicht wo die Klicks billig sind.</li>
  </ul>

  <h2>Meta Ads für lokale Betriebe und Dienstleister</h2>
  <p>Für Fitnessstudios, Praxen, Handwerk, Gastronomie und Dienstleister am Bodensee nutzen wir Lead-Kampagnen mit Instant-Formularen oder WhatsApp-Kontakt, Radius-Targeting um den Standort und Angebote, die eine Handlung auslösen (Probetraining, Beratungstermin, Kostenvoranschlag).</p>

  <h2>Was kostet eine Meta Ads Agentur?</h2>
  <table class="tbl">
    <thead><tr><th>Posten</th><th>Bei AIclicks</th></tr></thead>
    <tbody>
      <tr><td>Ads Management</td><td>ab 1.490 € / Monat – Setup, Kampagnenführung, Tracking, wöchentliches Reporting</td></tr>
      <tr><td>Creatives</td><td>Werbevideo-Pakete ab 690 € – oder als monatlicher Nachschub im Ads-Paket</td></tr>
      <tr><td>Werbebudget</td><td>direkt an Meta; Empfehlung ab 1.000–1.500 € / Monat</td></tr>
      <tr><td>Setup-Gebühr / Laufzeit</td><td>keine / monatlich kündbar</td></tr>
    </tbody>
  </table>

  <h2>Meta Ads vs. Google Ads – was passt zu dir?</h2>
  <table class="tbl">
    <thead><tr><th>Kriterium</th><th>Meta Ads</th><th>Google Ads</th></tr></thead>
    <tbody>
      <tr><td>Nachfrage</td><td>erzeugt Nachfrage (Push)</td><td>fängt bestehende Nachfrage ab (Pull)</td></tr>
      <tr><td>Erfolgsfaktor</td><td>Creative &amp; Angebot</td><td>Suchbegriffe &amp; Landingpage</td></tr>
      <tr><td>Ideal für</td><td>Shops, Lifestyle, Fitness, erklärungsbedürftige Angebote</td><td>Notdienste, Handwerk, B2B, konkrete Suchanfragen</td></tr>
      <tr><td>Zeit bis Ergebnis</td><td>2–6 Wochen Lernphase</td><td>oft erste Anfragen in Tagen</td></tr>
    </tbody>
  </table>
  <p>Die meisten Kunden fahren am besten mit beidem: <a href="/google-ads-agentur-bodensee.html">Google Ads</a> für die, die schon suchen – Meta Ads für alle, die dich noch nicht kennen.</p>
</div></div></section>
""" + PROCESS + GUAR,
    faq=[
        ("Was kostet Facebook- und Instagram-Werbung über eine Agentur?", "Bei AIclicks kostet Meta Ads Management ab 1.490 € pro Monat plus dein Werbebudget, das direkt an Meta geht. Werbevideos gibt es als Paket ab 690 € oder im Full Service ab 2.900 € pro Monat inklusive. Keine Setup-Gebühr, monatlich kündbar."),
        ("Wie viel Werbebudget brauche ich für Meta Ads?", "Sinnvoll wird es ab etwa 1.000–1.500 € Werbebudget pro Monat. Metas Algorithmus braucht rund 50 Conversions pro Woche und Anzeigengruppe, um die Lernphase zu verlassen – zu kleine Budgets bleiben dauerhaft im Lernmodus."),
        ("Warum sind Creatives bei Meta Ads so wichtig?", "Weil Meta das Targeting weitgehend automatisiert hat. Ob eine Anzeige performt, entscheidet in erster Linie das Creative: der Hook in den ersten zwei Sekunden, das Angebot und das Format. Deshalb testen wir jede Woche neue Varianten – KI macht das bezahlbar."),
        ("Funktionieren Meta Ads für lokale Betriebe am Bodensee?", "Ja, sehr gut – für Fitnessstudios, Praxen, Gastronomie, Handwerk und Dienstleister mit einem klaren Angebot. Wir nutzen Radius-Targeting rund um den Standort und Lead-Formulare oder WhatsApp als Kontaktweg."),
        ("Was ist die Conversions API und brauche ich sie?", "Die Conversions API sendet Kauf- und Lead-Ereignisse serverseitig an Meta, statt nur über den Browser-Pixel. Seit den iOS-Datenschutzänderungen gehen ohne sie 20–40 % der Conversion-Daten verloren. Wir richten sie standardmäßig ein."),
    ],
))

# ---------------------------------------------------------------- AMAZON PPC
PAGES.append(dict(
    slug="amazon-ppc-agentur.html", crumb="Amazon PPC Agentur", image="og-image.jpg",
    title="Amazon PPC Agentur – profitabel skalieren | AIclicks",
    desc="Amazon PPC Agentur mit eigener 7-stelliger Amazon-Marke: Sponsored Products, Brands &amp; Display mit ACOS-Steuerung und Bid-Automatisierung. Ab 1.490 €/Monat.",
    service_name="Amazon PPC Management (Amazon Advertising)", service_type="Amazon PPC Agentur",
    audience="Amazon-Seller und -Vendoren, Marken auf Amazon, E-Commerce", price="1490", unit="Monat",
    cta_h="Wie profitabel ist dein Amazon-Werbekonto wirklich?",
    cta_p="Kostenloser PPC-Audit: Wir prüfen ACOS/TACOS, Keyword-Struktur und Budgetverteilung deiner Kampagnen und zeigen dir, wo Gewinn liegen bleibt.",
    body="""
<section class="sub-hero"><div class="wrap">
  <p class="crumbs"><a href="/">Start</a> › <a href="/#leistungen">Leistungen</a> › Amazon PPC Agentur</p>
  <p class="eyebrow">Amazon PPC Agentur · Sponsored Products, Brands &amp; Display</p>
  <h1>Amazon PPC von Leuten,<br>die selbst 7-stellig auf Amazon verkaufen.</h1>
  <p class="lead">AIclicks ist eine Amazon PPC Agentur mit eigener Amazon-Marke: über 1,6 Mio. € Umsatz, 69.425 verkaufte Einheiten und acht internationale Marktplätze – gesteuert mit datengetriebener PPC-Automatisierung. Genau dieses System setzen wir für dein Amazon-Werbekonto ein.</p>
  <div class="hero-cta"><a href="/#kontakt" class="btn">Kostenloser PPC-Audit</a><a href="/#ergebnisse" class="btn ghost">Unsere eigenen Zahlen</a></div>
</div></section>

<section><div class="wrap"><div class="panel prose">
  <h2>Was macht eine Amazon PPC Agentur?</h2>
  <div class="def"><p>Eine Amazon PPC Agentur steuert bezahlte Anzeigen auf Amazon (Sponsored Products, Sponsored Brands, Sponsored Display) für Seller und Vendoren. Sie strukturiert Kampagnen nach Keywords und Produkten, passt Gebote anhand von ACOS- und Margen-Zielen an, verschiebt Suchbegriffe aus automatischen in manuelle Kampagnen (Keyword-Harvesting) und optimiert Listings, damit Werbeklicks auch konvertieren. Ziel ist profitables Wachstum: mehr organisches Ranking bei sinkendem TACOS.</p></div>
  <p>Die meisten Amazon-Werbekonten haben dasselbe Problem: Automatische Kampagnen laufen jahrelang unangetastet, Gebote werden nach Gefühl gesetzt, und niemand kennt den Break-even-ACOS pro Produkt. Wir haben dieses Problem an der eigenen Marke gelöst – mit Regeln statt Bauchgefühl.</p>

  <h2>Unser Amazon-Ads-System</h2>
  <ul>
    <li><strong>Break-even-ACOS pro Produkt:</strong> Bevor wir ein Gebot setzen, kennen wir die Marge. Ziel-ACOS leitet sich aus dem Deckungsbeitrag ab, nicht aus Branchendurchschnitten.</li>
    <li><strong>Kampagnenstruktur:</strong> Auto → Broad → Phrase → Exact mit sauberer Negativ-Keyword-Pflege; Marken-, Wettbewerber- und Kategoriebegriffe getrennt.</li>
    <li><strong>Bid-Automatisierung:</strong> regelbasierte Gebotsanpassung nach Conversion-Rate, ACOS und Platzierung (Top of Search, Produktseiten), täglich statt monatlich.</li>
    <li><strong>Keyword-Harvesting:</strong> Suchbegriffe, die konvertieren, wandern in Exact-Kampagnen; Suchbegriffe, die nur kosten, werden negativiert.</li>
    <li><strong>Listing &amp; Creatives:</strong> Hauptbild, A+-Content und Titel entscheiden über die Conversion-Rate – und damit über den ACOS. Mit KI produzieren wir Bildvarianten in Tagen.</li>
    <li><strong>International:</strong> Erfahrung mit Amazon DE, FR, IT, ES, NL, SE, PL und UK – inklusive Übersetzung und lokaler Keyword-Recherche.</li>
  </ul>

  <h2>ACOS, TACOS, ROAS – die Kennzahlen kurz erklärt</h2>
  <table class="tbl">
    <thead><tr><th>Kennzahl</th><th>Formel</th><th>Was sie sagt</th></tr></thead>
    <tbody>
      <tr><td>ACOS</td><td>Werbekosten ÷ Werbeumsatz × 100</td><td>Wie viel Prozent des beworbenen Umsatzes an Amazon Ads geht. Unter dem Break-even-ACOS = Gewinn.</td></tr>
      <tr><td>TACOS</td><td>Werbekosten ÷ Gesamtumsatz × 100</td><td>Wie stark der gesamte Umsatz (organisch + bezahlt) von Werbung abhängt. Sinkender TACOS bei wachsendem Umsatz = gesundes Konto.</td></tr>
      <tr><td>ROAS</td><td>Werbeumsatz ÷ Werbekosten</td><td>Umsatz pro eingesetztem Werbe-Euro (Kehrwert des ACOS).</td></tr>
      <tr><td>Break-even-ACOS</td><td>Marge vor Werbung in %</td><td>Der ACOS, bei dem eine Bestellung weder Gewinn noch Verlust bringt. Bei unserer eigenen Marke in DE: ~15 %.</td></tr>
    </tbody>
  </table>

  <h2>Was kostet eine Amazon PPC Agentur?</h2>
  <p>Amazon PPC Management bei AIclicks kostet <strong>ab 1.490 € pro Monat</strong> – inklusive Kontostruktur, täglicher Gebotssteuerung, Keyword-Harvesting, Negativ-Pflege und wöchentlichem Reporting nach ACOS, TACOS und Gewinn. Keine Setup-Gebühr, keine Mindestlaufzeit. Das Werbebudget zahlst du direkt an Amazon. Für Marken mit mehreren Marktplätzen oder größerem Budget gibt es individuelle Pakete.</p>

  <h2>Für wen Amazon PPC bei AIclicks passt</h2>
  <ul>
    <li>Amazon-Seller (FBA/FBM) mit ab ca. 10.000 € Monatsumsatz oder klarer Skalierungsabsicht</li>
    <li>Marken, die von Amazon DE in weitere EU-Marktplätze expandieren wollen</li>
    <li>Shopify-Händler, die Amazon als zweiten Kanal aufbauen – gern kombiniert mit <a href="/google-ads-agentur-bodensee.html">Google Shopping</a> und <a href="/meta-ads-agentur.html">Meta Ads</a></li>
  </ul>
  <p>Nicht der richtige Partner: für Konten unter ca. 500 € Werbebudget im Monat oder ohne Marge für Werbung – dort bringt Listing-Optimierung mehr als PPC.</p>
</div></div></section>
""" + PROCESS + GUAR,
    faq=[
        ("Was kostet Amazon PPC Management bei AIclicks?", "Ab 1.490 € pro Monat inklusive Kampagnenstruktur, täglicher Gebotssteuerung, Keyword-Harvesting und wöchentlichem Reporting. Das Werbebudget geht direkt an Amazon. Keine Setup-Gebühr, monatlich kündbar."),
        ("Was ist ein guter ACOS?", "Das hängt allein von deiner Marge ab. Ein ACOS unter dem Break-even-ACOS (Marge vor Werbung) ist profitabel. Für Produktlaunches akzeptieren wir bewusst einen höheren ACOS, um Rankings aufzubauen; bei etablierten Produkten liegt der Ziel-ACOS oft bei 10–25 %."),
        ("Betreut ihr auch andere Amazon-Marktplätze als Deutschland?", "Ja. Unsere eigene Marke läuft auf acht Marktplätzen, darunter DE, FR, IT, ES, NL, SE, PL und UK. Wir übernehmen Keyword-Recherche, Übersetzung und Kampagnensteuerung pro Land."),
        ("Braucht mein Amazon-Konto eine Agentur oder reicht ein PPC-Tool?", "Ein Tool automatisiert Gebote, aber es kennt weder deine Marge noch deine Strategie. Wir kombinieren regelbasierte Automatisierung mit menschlicher Steuerung: Struktur, Launch-Strategie, Listing-Optimierung und Budgetverteilung über Produkte und Länder hinweg."),
        ("Wie schnell sehe ich Ergebnisse bei Amazon PPC?", "Strukturbereinigung und Negativ-Keywords wirken oft innerhalb von 1–2 Wochen auf den ACOS. Nachhaltige Verbesserungen bei Ranking und TACOS zeigen sich nach 60–90 Tagen, weil Amazon organische Rankings verzögert nachzieht."),
        ("Kann ich Amazon PPC mit Google Ads und Meta Ads kombinieren?", "Ja – externer Traffic auf Amazon-Listings (Brand Referral Bonus) verbessert Rankings. Wir steuern Google, Meta und Amazon aus einer Hand, damit Budgets dort landen, wo der Deckungsbeitrag am höchsten ist."),
    ],
))

# ---------------------------------------------------------------- KI-WERBEVIDEOS
PAGES.append(dict(
    slug="ki-werbevideos.html", crumb="Werbevideos & Anzeigen", image="og-image.jpg",
    title="Werbevideos &amp; Anzeigen erstellen lassen ab 690 € | AIclicks",
    desc="Werbevideos &amp; Bild-Anzeigen erstellen lassen: aus deinem Material in Tagen statt Wochen – für Meta, TikTok, YouTube und Amazon. Pakete ab 690 €.",
    service_name="Werbevideos & Anzeigen", service_type="Ad Creative Production",
    audience="Onlineshops, lokale Betriebe, Dienstleister, Amazon-Marken", price="690", unit="Paket",
    cta_h="Zeig uns dein Produkt – wir zeigen dir, was daraus wird.",
    cta_p="Schick uns Fotos oder Videos deines Angebots. In der kostenlosen Analyse zeigen wir dir, welche Creative-Formate für deine Zielgruppe funktionieren und was ein erstes Paket kostet.",
    body="""
<section class="sub-hero"><div class="wrap">
  <p class="crumbs"><a href="/">Start</a> › <a href="/#leistungen">Leistungen</a> › Werbevideos &amp; Anzeigen</p>
  <p class="eyebrow">Werbevideos &amp; Anzeigen für Meta, TikTok, YouTube und Amazon</p>
  <h1>Werbevideos in Tagen.<br>Nicht in Wochen.</h1>
  <p class="lead">Wir produzieren Werbevideos und Bild-Anzeigen aus deinem vorhandenen Foto- und Videomaterial – mit moderner Produktionstechnik statt Filmteam. Für Facebook, Instagram, TikTok, YouTube und Amazon. Mehr Varianten, schneller getestet, ab 690 € pro Paket. Ohne Filmteam, ohne Drehtag, ohne Wochen Wartezeit.</p>
  <div class="hero-cta"><a href="/#kontakt" class="btn">Kostenlose Analyse</a><a href="/meta-ads-agentur.html" class="btn ghost">Creatives + Meta Ads</a></div>
</div></section>

<section><div class="wrap"><div class="panel prose">
  <h2>Wie entstehen unsere Werbevideos?</h2>
  <div class="def"><p>Unsere Werbevideos sind Video-Anzeigen, bei denen generative KI-Modelle (z. B. für Bild-zu-Video, Voice-over, Untertitel und Schnitt) die Produktion übernehmen, die früher Filmteam, Studio und Postproduktion erforderte. Aus vorhandenen Produktfotos, Handyvideos oder Renderings entstehen in Stunden fertige Clips in mehreren Formaten und Varianten. Strategie, Hook und Angebot definieren weiterhin Menschen – die KI produziert.</p></div>
  <p>Der Punkt ist nicht, dass KI „schöner“ produziert. Der Punkt ist <strong>Menge und Geschwindigkeit</strong>: Auf Meta, TikTok und YouTube entscheidet das Creative über 70–80 % der Performance, und ein Creative ist nach 2–4 Wochen verbraucht. Wer zehn Varianten pro Monat testen kann statt eine, gewinnt – und genau das macht KI bezahlbar.</p>

  <h2>Was du bekommst</h2>
  <ul>
    <li><strong>Werbevideos</strong> 9:16, 1:1 und 16:9 – Produkt-Demos, Vorher/Nachher, UGC-Stil, Testimonial-Stil, Angebots-Clips (5–30 Sekunden)</li>
    <li><strong>Statische Ad Creatives</strong> für Feed, Story und Amazon-Listings (Hauptbild-Varianten, A+-Grafiken)</li>
    <li><strong>Hook-Varianten:</strong> Jedes Video in 3–5 Einstiegen, damit der Algorithmus den besten findet</li>
    <li><strong>Voice-over &amp; Untertitel</strong> auf Deutsch (oder Englisch), Musik lizenzfrei</li>
    <li><strong>Plattform-fertig:</strong> richtige Auflösung, Safe Zones, Dateigrößen für Meta, TikTok, YouTube Shorts, Amazon</li>
  </ul>

  <h2>Werbevideo erstellen lassen: Kosten im Vergleich</h2>
  <table class="tbl">
    <thead><tr><th></th><th>Werbevideos von AIclicks</th><th>Klassische Videoproduktion</th></tr></thead>
    <tbody>
      <tr><td>Preis</td><td>ab 690 € pro Paket (mehrere Videos + Bild-Varianten)</td><td>2.000–15.000 € pro Video (Dreh, Team, Schnitt)</td></tr>
      <tr><td>Lieferzeit</td><td>2–5 Werktage</td><td>3–8 Wochen</td></tr>
      <tr><td>Varianten</td><td>mehrere Hooks &amp; Formate inklusive</td><td>meist ein Master, Schnittvarianten kosten extra</td></tr>
      <tr><td>Ausgangsmaterial</td><td>deine Fotos/Videos, Renderings, Produktbilder</td><td>Drehtag vor Ort nötig</td></tr>
      <tr><td>Ideal für</td><td>Performance-Ads, Tests, Skalierung</td><td>Imagefilm, Markenkampagne, TV</td></tr>
    </tbody>
  </table>
  <p>Ehrliche Einordnung: Für einen emotionalen Imagefilm oder einen TV-Spot ist ein echter Dreh weiterhin die bessere Wahl. Für Performance-Ads, die getestet, verbraucht und ersetzt werden, ist KI-Produktion in Preis und Tempo nicht zu schlagen.</p>

  <h2>So läuft die Produktion</h2>
  <ol>
    <li><strong>Briefing (30 Min):</strong> Angebot, Zielgruppe, Plattform, bestehende Bestseller-Anzeigen.</li>
    <li><strong>Material:</strong> Du schickst Produktfotos, Handyvideos, Logos – oder wir arbeiten mit Renderings.</li>
    <li><strong>Produktion:</strong> Skript und Hooks, KI-Generierung, Schnitt, Voice-over, Untertitel. Erste Entwürfe in 2–3 Tagen.</li>
    <li><strong>Feedback &amp; Lieferung:</strong> eine Korrekturrunde inklusive, dann plattformfertige Dateien.</li>
    <li><strong>Optional:</strong> Wir schalten die Creatives direkt in deinen <a href="/meta-ads-agentur.html">Meta-</a> oder <a href="/google-ads-agentur-bodensee.html">Google-Ads-Kampagnen</a> und liefern jeden Monat Nachschub, basierend auf den Performance-Daten.</li>
  </ol>

  <h2>Kennzeichnung und Rechte</h2>
  <p>Alle gelieferten Creatives darfst du zeitlich und räumlich unbegrenzt für dein Unternehmen nutzen. Wir arbeiten ausschließlich mit deinem Material und lizenzfreien Assets; erkennbare Personen werden nur mit Einwilligung verwendet. Wo Plattformen oder das Gesetz (z. B. EU AI Act ab 2026) eine Kennzeichnung KI-generierter Inhalte verlangen, setzen wir sie um.</p>
</div></div></section>
""" + PROCESS + GUAR,
    faq=[
        ("Was kostet ein Werbevideo mit KI?", "Werbevideo-Pakete bei AIclicks starten bei 690 € und enthalten mehrere Videos in verschiedenen Formaten plus Bild-Varianten. Ein klassisch produziertes Werbevideo kostet je nach Aufwand 2.000–15.000 €."),
        ("Welches Material brauche ich?", "Produktfotos, kurze Handyvideos, Logo und Farben reichen in der Regel. Je mehr echtes Material, desto authentischer das Ergebnis. Renderings oder Herstellerbilder funktionieren ebenfalls."),
        ("Wie lange dauert die Produktion?", "Erste Entwürfe nach 2–3 Werktagen, fertige Lieferung meist innerhalb von 5 Werktagen inklusive einer Korrekturrunde."),
        ("Für welche Plattformen eignen sich die Werbevideos?", "Meta (Facebook, Instagram Reels, Stories), TikTok, YouTube Shorts und In-Stream, Amazon Sponsored Brands Video sowie Landingpages und Produktseiten. Wir liefern jedes Video in den passenden Formaten."),
        ("Sieht man, dass es KI ist?", "Bei Produkt-Demos, Angebots-Clips und animierten Bildern in der Regel nicht. Wo es um Menschen und Emotion geht, kombinieren wir echtes Material mit KI-Elementen. Ehrlich ist: Für Performance-Ads zählt am Ende nur, ob das Video Bestellungen bringt – und das messen wir."),
        ("Könnt ihr die Videos auch gleich schalten?", "Ja. In unseren Ads-Paketen (ab 1.490 € pro Monat) produzieren wir Creatives im Monatstakt und führen deine Google-, Meta- oder Amazon-Kampagnen – Creative-Produktion und Media-Steuerung greifen dann direkt ineinander."),
    ],
))

# ---------------------------------------------------------------- WEBSITE IN 5 TAGEN
PAGES.append(dict(
    slug="website-in-5-tagen.html", crumb="Website in 5 Tagen", image="og-image.jpg",
    title="Website erstellen lassen in 5 Tagen – 1.990 € Festpreis | AIclicks",
    desc="Website für Handwerk, Praxis &amp; Dienstleister in 5 Werktagen zum Festpreis: 1.990 € inkl. Texte, Design, Kontaktformular, Google-Optimierung. Aus Friedrichshafen.",
    service_name="Website in 5 Tagen", service_type="Webdesign & Webentwicklung",
    audience="Handwerk, Praxen, Kanzleien, Dienstleister, Gründer", price="1990", unit="Festpreis",
    cta_h="Deine neue Website – in einer Woche online.",
    cta_p="Schick uns deine aktuelle Website (oder einfach deinen Firmennamen). Wir sagen dir in 20 Minuten ehrlich, was wir daraus machen würden – kostenlos.",
    body="""
<section class="sub-hero"><div class="wrap">
  <p class="crumbs"><a href="/">Start</a> › <a href="/#leistungen">Leistungen</a> › Website in 5 Tagen</p>
  <p class="eyebrow">Website erstellen lassen · Festpreis · Friedrichshafen am Bodensee</p>
  <h1>Deine Website in 5 Tagen.<br>1.990 € Festpreis. Fertig.</h1>
  <p class="lead">Eine professionelle Website für deinen Betrieb – Texte, Design, Kontaktformular, Google-Optimierung, mobil perfekt – innerhalb von fünf Werktagen online. Kein monatelanges Hin und Her, kein Baukasten, keine versteckten Kosten.</p>
  <div class="hero-cta"><a href="/#kontakt" class="btn">Kostenlos anfragen</a><a href="#preis" class="btn ghost">Was ist drin?</a></div>
</div></section>

<section><div class="wrap"><div class="panel prose">
  <h2>Was ist „Website in 5 Tagen“?</h2>
  <div class="def"><p>„Website in 5 Tagen“ ist ein Festpreis-Angebot von AIclicks für kleine und mittlere Betriebe: Innerhalb von fünf Werktagen nach dem Briefing geht eine komplette, suchmaschinenoptimierte Website mit bis zu fünf Unterseiten online – inklusive Texten, Design, Bildern, Kontaktformular, Impressum/Datenschutz und Google-Anbindung. Der Preis beträgt 1.990 € einmalig; es gibt keine Pflicht-Abos.</p></div>
  <p>Die meisten Websites für Handwerker, Praxen und Dienstleister scheitern nicht am Design, sondern an drei Dingen: <strong>sie werden nie fertig</strong>, <strong>sie bringen keine Anfragen</strong> und <strong>niemand findet sie bei Google</strong>. Wir bauen deshalb keine Kunstwerke, sondern Websites, die genau eines tun: Besucher zu Anrufen und Anfragen machen.</p>

  <h2 id="preis">Was im Festpreis enthalten ist</h2>
  <table class="tbl">
    <thead><tr><th>Leistung</th><th>Website in 5 Tagen (1.990 €)</th><th>Klassische Webagentur</th></tr></thead>
    <tbody>
      <tr><td>Umfang</td><td>Startseite + bis zu 4 Unterseiten (Leistungen, Über uns, Referenzen, Kontakt)</td><td>nach Angebot</td></tr>
      <tr><td>Texte</td><td>inklusive – wir schreiben sie nach einem 30-Minuten-Gespräch</td><td>meist Kundensache oder Aufpreis</td></tr>
      <tr><td>Design</td><td>individuell auf deine Farben, Logo und Branche</td><td>individuell</td></tr>
      <tr><td>Google-Optimierung</td><td>Seitentitel, Beschreibungen, Struktur, Ladezeit, lokale Suchbegriffe, Google-Unternehmensprofil-Verknüpfung</td><td>oft Aufpreis</td></tr>
      <tr><td>Kontakt &amp; Anfragen</td><td>Formular, Klick-zu-Anruf, WhatsApp-Button, Anfrage-Tracking</td><td>Formular</td></tr>
      <tr><td>Rechtliches</td><td>Impressum, Datenschutz, Cookie-Hinweis vorbereitet</td><td>Kundensache</td></tr>
      <tr><td>Dauer</td><td>5 Werktage nach Briefing</td><td>6–16 Wochen</td></tr>
      <tr><td>Preis</td><td>1.990 € einmalig, Hosting ab 0 € (statisch) bzw. eigene Domain</td><td>4.000–15.000 € + monatliche Pflege</td></tr>
    </tbody>
  </table>
  <p>Optional dazu: weitere Unterseiten (190 € je Seite), Blog/News-Bereich, Online-Terminbuchung, mehrsprachige Version oder eine Wartungs-Flatrate (49 €/Monat für Änderungen, Updates und Sicherheit). Nichts davon ist Pflicht.</p>

  <h2>So läuft es ab</h2>
  <ol>
    <li><strong>Tag 0 – Briefing (30 Min):</strong> Was bietest du an, wer soll anrufen, was unterscheidet dich? Du schickst Logo, Fotos und ggf. deine alte Website.</li>
    <li><strong>Tag 1–2 – Struktur und Texte:</strong> Wir schreiben alle Texte suchmaschinenfreundlich und in deiner Tonalität. Du liest gegen.</li>
    <li><strong>Tag 3–4 – Design und Aufbau:</strong> Die Seite entsteht, mobil zuerst. Du bekommst einen Vorschau-Link und eine Korrekturrunde.</li>
    <li><strong>Tag 5 – Live:</strong> Domain verbinden, Google Search Console und Unternehmensprofil anbinden, Formular und Tracking testen. Fertig.</li>
  </ol>

  <h2>Für wen das passt – und für wen nicht</h2>
  <ul>
    <li><strong>Passt:</strong> Handwerksbetriebe, Praxen, Kanzleien, Berater, Gastronomie, Studios, Gründer, regionale Dienstleister – alle, die eine saubere Visitenkarte im Netz brauchen, die Anfragen bringt.</li>
    <li><strong>Passt nicht:</strong> Onlineshops mit Warenkorb (dafür <a href="/amazon-ppc-agentur.html">optimieren wir bestehende Shops</a>), Portale mit Login-Bereichen oder große Unternehmensseiten mit 30+ Seiten. Das geht auch – aber nicht in 5 Tagen und nicht zum Festpreis; dafür sprechen wir über ein <a href="/automatisierung.html">individuelles Projekt</a>.</li>
  </ul>

  <h2>Website ist da – und dann?</h2>
  <p>Eine Website allein bringt selten Anfragen. Deshalb ist „Website in 5 Tagen“ bei uns der Einstieg: Wer will, schaltet danach <a href="/google-ads-agentur-bodensee.html">Google Ads</a> oder <a href="/meta-ads-agentur.html">Meta Ads</a> auf die neue Seite und bekommt ab dem ersten Monat messbar Anfragen. Beides greift ineinander – die Seite ist von Anfang an darauf gebaut.</p>
</div></div></section>
""" + GUAR,
    faq=[
        ("Was kostet eine Website bei AIclicks?", "1.990 € einmalig zum Festpreis: Startseite plus bis zu vier Unterseiten, Texte, Design, Kontaktformular, Google-Optimierung und rechtliche Seiten. Weitere Unterseiten kosten 190 € je Seite, eine optionale Wartungs-Flatrate 49 € pro Monat."),
        ("Schafft ihr wirklich 5 Werktage?", "Ja – wenn das Briefing steht und wir Logo und Fotos haben. Der Prozess ist standardisiert und wir arbeiten mit modernen Werkzeugen, die Texte, Design und Technik parallel entstehen lassen. Verzögerungen entstehen fast nur, wenn Feedback länger auf sich warten lässt."),
        ("Muss ich Texte und Fotos selbst liefern?", "Texte schreiben wir nach dem Briefing komplett für dich. Fotos: Eigene Bilder von Team, Werkstatt oder Projekten wirken am besten; wo sie fehlen, ergänzen wir professionelles Bildmaterial."),
        ("Gehört mir die Website?", "Ja, vollständig – Code, Texte, Bilder und Domain gehören dir. Es gibt keine Bindung an uns, keine Lizenzgebühr und keine Pflicht-Wartung."),
        ("Wird die Website bei Google gefunden?", "Sie wird technisch sauber, schnell und mit lokalen Suchbegriffen aufgebaut und wir verknüpfen sie mit deinem Google-Unternehmensprofil. Für umkämpfte Suchbegriffe braucht es darüber hinaus Zeit oder Google Ads – das besprechen wir ehrlich im Briefing."),
        ("Kann ich später selbst Änderungen machen?", "Kleine Änderungen (Öffnungszeiten, Texte, Bilder) erledigen wir in der Wartungs-Flatrate innerhalb von 48 Stunden. Wer lieber selbst editieren möchte, bekommt auf Wunsch ein einfaches Redaktionssystem – das besprechen wir im Briefing."),
    ],
))

# ---------------------------------------------------------------- AUTOMATISIERUNG
PAGES.append(dict(
    slug="automatisierung.html", crumb="Automatisierung", image="og-image.jpg",
    title="Prozesse automatisieren lassen – Automatisierung für Betriebe | AIclicks",
    desc="Automatisierung für kleine und mittlere Unternehmen: Anfragen, Angebote, Belege, Berichte und Wiederkehrendes laufen von selbst. Kostenloser Prozess-Check, kleine Automatisierungen ab 490 € Festpreis.",
    service_name="Automatisierung & individuelle Lösungen", service_type="Prozessautomatisierung & Softwareentwicklung",
    audience="Kleine und mittlere Unternehmen, Handwerk, Handel, Onlineshops, Dienstleister", price="490", unit="Projekt",
    cta_h="Welche Aufgabe kostet dich jede Woche am meisten Zeit?",
    cta_p="Erzähl uns in 20 Minuten, was bei euch täglich von Hand passiert. Wir sagen dir kostenlos, was sich automatisieren lässt, was es kostet – und was sich nicht lohnt.",
    body="""
<section class="sub-hero"><div class="wrap">
  <p class="crumbs"><a href="/">Start</a> › <a href="/#leistungen">Leistungen</a> › Automatisierung</p>
  <p class="eyebrow">Automatisierung &amp; individuelle Lösungen · Friedrichshafen am Bodensee</p>
  <h1>Abläufe, die von selbst laufen.<br>Statt jeden Tag von Hand.</h1>
  <p class="lead">Anfragen beantworten, Angebote schreiben, Belege sortieren, Bestellungen übertragen, Berichte zusammenstellen – vieles davon macht in deinem Betrieb jemand jeden Tag per Hand. Wir bauen dir Abläufe, die das übernehmen. Kleine Automatisierungen ab 490 € Festpreis, individuelle Tools ab 1.990 €.</p>
  <div class="hero-cta"><a href="/#kontakt" class="btn">Kostenloser Prozess-Check</a><a href="#beispiele" class="btn ghost">Beispiele ansehen</a></div>
</div></section>

<section><div class="wrap"><div class="panel prose">
  <h2>Was bedeutet Automatisierung für einen Betrieb?</h2>
  <div class="def"><p>Automatisierung im Unternehmen heißt: Wiederkehrende Aufgaben, die heute Menschen per Hand erledigen – Daten von A nach B übertragen, E-Mails beantworten, Dokumente erstellen, Zahlen zusammentragen – werden von Software übernommen, die deine bestehenden Programme miteinander verbindet. Bei AIclicks reicht das von kleinen Verknüpfungen zwischen zwei Tools (z. B. Anfrage-Formular → CRM → Antwort-Mail) bis zu individuell entwickelten Anwendungen, die es so noch nicht gibt.</p></div>
  <p>Wir wissen, wovon wir reden: Unser eigener Onlineshop verkauft personalisierte Produkte in acht Länder – Bestellabwicklung, Produktion, Werbesteuerung und Buchhaltung laufen dort weitgehend automatisch. Ohne diese Abläufe wäre das mit einem kleinen Team nicht machbar. Genau dieses Wissen bauen wir jetzt für andere Betriebe.</p>

  <h2 id="beispiele">Was wir typischerweise automatisieren</h2>
  <table class="tbl">
    <thead><tr><th>Bereich</th><th>Vorher (von Hand)</th><th>Nachher (automatisch)</th></tr></thead>
    <tbody>
      <tr><td>Anfragen</td><td>Mails lesen, Rückfragen stellen, ins Excel tippen, Tage später antworten</td><td>Anfrage wird sofort qualifiziert, beantwortet, in dein System eingetragen und dir mit Vorschlag vorgelegt</td></tr>
      <tr><td>Angebote</td><td>Vorlage suchen, Preise raussuchen, PDF bauen, 45 Minuten pro Angebot</td><td>Angebot in wenigen Minuten aus Preisliste und Kundendaten, inklusive Nachfass-Mail nach 5 Tagen</td></tr>
      <tr><td>Büro &amp; Buchhaltung</td><td>Belege sammeln, umbenennen, an den Steuerberater mailen</td><td>Belege werden erkannt, benannt, abgelegt und monatlich gebündelt übergeben</td></tr>
      <tr><td>Onlineshop &amp; Amazon</td><td>Bestellungen übertragen, Lagerbestände abgleichen, Werbegebote anpassen</td><td>Bestellungen, Bestände und Werbebudgets synchronisieren sich nach deinen Regeln – rund um die Uhr</td></tr>
      <tr><td>Bewertungen &amp; Kundenpflege</td><td>Vergessen, nach Bewertungen zu fragen</td><td>Nach jedem Auftrag automatisch Dankesnachricht und Bewertungsbitte, Geburtstags- und Wartungserinnerungen</td></tr>
      <tr><td>Berichte</td><td>Zahlen aus 4 Programmen in eine Tabelle kopieren</td><td>Ein Dashboard oder eine Montagsmail mit allen Zahlen, ohne dass jemand etwas tut</td></tr>
    </tbody>
  </table>

  <h2>Individuelle Lösungen: wenn es das Tool noch nicht gibt</h2>
  <p>Manchmal reicht Verbinden nicht – dann entwickeln wir das passende Werkzeug: einen Konfigurator für deine Website, ein internes Tool für Auftragsplanung, eine Schnittstelle zwischen zwei Systemen, die sich nicht verstehen, oder eine kleine App für dein Team. Dank moderner Entwicklungsmethoden entsteht so etwas heute in Tagen bis wenigen Wochen statt in Monaten – und zu Preisen, die auch für einen Zehn-Personen-Betrieb Sinn ergeben.</p>

  <h2>Was kostet Automatisierung?</h2>
  <table class="tbl">
    <thead><tr><th>Paket</th><th>Beispiel</th><th>Preis</th></tr></thead>
    <tbody>
      <tr><td>Prozess-Check</td><td>20 Minuten Gespräch, danach eine Liste: was sich lohnt, was es kostet, was nicht</td><td>kostenlos</td></tr>
      <tr><td>Kleine Automatisierung</td><td>Anfrage-Formular → Antwort-Mail + Eintrag in CRM/Excel; Beleg-Sortierung; Bewertungsanfrage nach Auftrag</td><td>ab 490 € Festpreis</td></tr>
      <tr><td>Ablauf-Paket</td><td>Mehrere verknüpfte Schritte, z. B. komplette Angebotserstellung mit Nachfassen, oder Shop-/Amazon-Synchronisation</td><td>ab 1.490 € Festpreis</td></tr>
      <tr><td>Individuelles Tool / Projekt</td><td>Eigene Anwendung, Konfigurator, Schnittstelle, internes Dashboard</td><td>ab 1.990 €, Festpreis nach Prozess-Check</td></tr>
      <tr><td>Betreuung (optional)</td><td>Überwachung, Anpassungen, kleine Erweiterungen</td><td>ab 149 € / Monat</td></tr>
    </tbody>
  </table>
  <p>Faustregel: Eine Aufgabe, die jemanden 30 Minuten am Tag kostet, kostet den Betrieb rund 3.000 € im Jahr. Die meisten Automatisierungen haben sich deshalb nach zwei bis vier Monaten bezahlt – und laufen dann weiter.</p>

  <h2>So gehen wir vor</h2>
  <ol>
    <li><strong>Prozess-Check (kostenlos):</strong> Du zeigst uns, was täglich von Hand passiert. Wir priorisieren nach Zeitersparnis pro Euro.</li>
    <li><strong>Festpreis-Angebot:</strong> Klar beschrieben, was gebaut wird, was es kostet und wann es läuft. Keine Stundenabrechnung.</li>
    <li><strong>Umsetzung:</strong> Kleine Automatisierungen in 2–5 Werktagen, Projekte in 1–4 Wochen. Wir arbeiten mit deinen bestehenden Programmen – kein Systemwechsel nötig.</li>
    <li><strong>Übergabe:</strong> Du bekommst eine Erklärung in einfacher Sprache und eine Dokumentation. Alles gehört dir und läuft in deinen Konten.</li>
  </ol>
  <p>Und wenn im Gespräch klar wird, dass sich etwas nicht lohnt, sagen wir das. Lieber ein ehrliches Nein als eine Automatisierung, die niemand braucht.</p>
</div></div></section>
""" + GUAR,
    faq=[
        ("Was kostet es, einen Prozess automatisieren zu lassen?", "Kleine Automatisierungen (zwei bis drei verknüpfte Schritte) kosten bei AIclicks ab 490 € Festpreis, umfangreichere Ablauf-Pakete ab 1.490 €, individuell entwickelte Tools ab 1.990 €. Vorab gibt es einen kostenlosen Prozess-Check, danach ein Festpreis-Angebot – keine Stundenabrechnung."),
        ("Muss ich dafür neue Software kaufen?", "In den meisten Fällen nicht. Wir verbinden die Programme, die du bereits nutzt – E-Mail, Kalender, Excel oder Google Sheets, Shop-System, Buchhaltung, CRM. Nur wo ein Baustein wirklich fehlt, empfehlen wir ein passendes, meist günstiges Tool."),
        ("Wie lange dauert die Umsetzung?", "Kleine Automatisierungen laufen nach 2–5 Werktagen, größere Ablauf-Pakete und individuelle Tools nach ein bis vier Wochen. Der Prozess-Check vorab dauert 20 Minuten."),
        ("Was passiert, wenn etwas nicht mehr funktioniert?", "Jede Automatisierung bekommt eine Fehlerbenachrichtigung, und du erhältst eine Dokumentation. Mit der optionalen Betreuung ab 149 € pro Monat überwachen wir die Abläufe, passen sie an und erweitern sie bei Bedarf."),
        ("Ist das nur für Onlineshops oder auch für Handwerk und Büro?", "Für beides. Bei Onlineshops und Amazon-Händlern geht es oft um Bestellungen, Bestände und Werbesteuerung; bei Handwerk, Praxen und Dienstleistern um Anfragen, Angebote, Terminerinnerungen, Belege und Bewertungsanfragen. Die Technik ist dieselbe – der Ablauf wird auf deinen Betrieb zugeschnitten."),
        ("Könnt ihr auch etwas komplett Eigenes entwickeln?", "Ja. Wenn es das Werkzeug nicht gibt, entwickeln wir es: Konfiguratoren, interne Tools, Schnittstellen, Dashboards oder kleine Apps. Dank moderner Entwicklungsmethoden geht das heute in Tagen bis Wochen und zu Festpreisen ab 1.990 €."),
        ("Wem gehört die Automatisierung danach?", "Dir. Alles läuft in deinen Konten und wird an dich übergeben – inklusive Dokumentation. Du bist nicht an uns gebunden."),
    ],
))

if __name__ == "__main__":
    for p in PAGES:
        build(p)
