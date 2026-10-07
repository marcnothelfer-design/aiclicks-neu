#!/usr/bin/env python3
"""Erzeugt Impressum, Datenschutz, 404 und den Wachstums-Rechner im gemeinsamen Design (styles.css).
Aufruf: python3 _build/build-static.py  (im Repo-Root). Nutzt HEAD/FOOT aus build-pages.py."""
import importlib.util, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("bp", ROOT / "_build" / "build-pages.py")
bp = importlib.util.module_from_spec(spec); spec.loader.exec_module(bp)

def head(title, desc, slug, robots="index, follow, max-image-preview:large, max-snippet:-1", extra=""):
    h = bp.HEAD.format(title=title, desc=desc, slug=slug, image="og-image.jpg", schema="")
    h = h.replace('<script type="application/ld+json">\n\n</script>\n', "")
    h = re.sub(r'<script type="application/ld\+json">\s*</script>\s*', "", h)
    h = h.replace('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">', f'<meta name="robots" content="{robots}">')
    if extra: h = h.replace("</head>", extra + "\n</head>")
    return h

# Footer ohne CTA-Band (Rechtsseiten brauchen keinen Verkaufsblock)
FOOT_PLAIN = bp.FOOT[bp.FOOT.index("</main>"):].replace("{today_de}", bp.TODAY_DE)
FOOT_PLAIN = "</main>" + FOOT_PLAIN.split("</main>", 1)[1]

def legal_page(slug, title, desc, h1, intro, body_html):
    return (head(title, desc, slug, robots="noindex, follow")
        + f'''
<section class="sub-hero"><div class="wrap">
  <p class="crumbs"><a href="/">Start</a> › {h1}</p>
  <h1>{h1}</h1>
  {intro}
</div></section>
<section class="tight" style="padding-top:0"><div class="wrap"><div class="prose legal">
{body_html}
</div></div></section>
''' + FOOT_PLAIN)

# ---------- Impressum ----------
IMPRESSUM = '''
<h2>Angaben gemäß § 5 DDG</h2>
<p>Marc Nothelfer<br>AIclicks<br>Pirolweg 8<br>88048 Friedrichshafen<br>Deutschland</p>
<h2>Kontakt</h2>
<p>Telefon: <a href="tel:+4915129810072">+49 151 29810072</a><br>E-Mail: <a href="mailto:marc@aiclicks.de">marc@aiclicks.de</a></p>
<h2>Umsatzsteuer-ID</h2>
<p>Umsatzsteuer-Identifikationsnummer gemäß § 27 a Umsatzsteuergesetz: DE346598869</p>
<h2>Redaktionell verantwortlich (§ 18 Abs. 2 MStV)</h2>
<p>Marc Nothelfer, Anschrift wie oben</p>
<h2>Verbraucherstreitbeilegung / Universalschlichtungsstelle</h2>
<p>Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
<h2>Haftung für Inhalte</h2>
<p>Als Diensteanbieter sind wir gemäß § 7 Abs. 1 DDG für eigene Inhalte auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich. Nach §§ 8 bis 10 DDG sind wir als Diensteanbieter jedoch nicht verpflichtet, übermittelte oder gespeicherte fremde Informationen zu überwachen oder nach Umständen zu forschen, die auf eine rechtswidrige Tätigkeit hinweisen. Verpflichtungen zur Entfernung oder Sperrung der Nutzung von Informationen nach den allgemeinen Gesetzen bleiben hiervon unberührt. Eine diesbezügliche Haftung ist jedoch erst ab dem Zeitpunkt der Kenntnis einer konkreten Rechtsverletzung möglich. Bei Bekanntwerden entsprechender Rechtsverletzungen werden wir diese Inhalte umgehend entfernen.</p>
<h2>Haftung für Links</h2>
<p>Unser Angebot enthält Links zu externen Websites Dritter, auf deren Inhalte wir keinen Einfluss haben. Deshalb können wir für diese fremden Inhalte auch keine Gewähr übernehmen. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber der Seiten verantwortlich. Bei Bekanntwerden von Rechtsverletzungen werden wir derartige Links umgehend entfernen.</p>
<h2>Urheberrecht</h2>
<p>Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem deutschen Urheberrecht. Beiträge Dritter sind als solche gekennzeichnet. Downloads und Kopien dieser Seite sind nur für den privaten, nicht kommerziellen Gebrauch gestattet.</p>
'''

# ---------- Datenschutz ----------
DATENSCHUTZ = '''
<h2>1. Verantwortlicher</h2>
<p>Marc Nothelfer, AIclicks, Pirolweg 8, 88048 Friedrichshafen. E-Mail: <a href="mailto:marc@aiclicks.de">marc@aiclicks.de</a>, Telefon: +49 151 29810072.</p>
<h2>2. Allgemeines</h2>
<p>Wir verarbeiten personenbezogene Daten nur, soweit dies zur Bereitstellung einer funktionsfähigen Website sowie unserer Inhalte und Leistungen erforderlich ist oder Sie eingewilligt haben. Rechtsgrundlagen sind insbesondere Art. 6 Abs. 1 DSGVO.</p>
<h2>3. Hosting</h2>
<p>Diese Website wird als statische Seite über GitHub Pages bereitgestellt (GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA). GitHub verarbeitet beim Aufruf der Seite technisch notwendige Zugriffsdaten (siehe Server-Logfiles). Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO (sichere und effiziente Bereitstellung). GitHub ist unter dem EU-US Data Privacy Framework zertifiziert; ergänzend gelten die EU-Standardvertragsklauseln. Weitere Informationen: <a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener">GitHub Privacy Statement</a>.</p>
<h2>4. Server-Logfiles</h2>
<p>Beim Aufruf der Website erhebt der Hosting-Anbieter automatisch Informationen in Server-Logfiles (IP-Adresse, Datum/Uhrzeit, aufgerufene Seite, Browsertyp, Betriebssystem, Referrer). Zweck: technische Auslieferung und Sicherheit. Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO. Wir selbst haben auf diese Logfiles keinen Zugriff; die Speicherdauer richtet sich nach den Vorgaben des Anbieters.</p>
<h2>5. Kontakt- und Anfrageformular, E-Mail-Kontakt</h2>
<p>Wenn Sie uns über ein Formular oder per E-Mail kontaktieren, verarbeiten wir Ihre Angaben (Name, E-Mail, Telefon, Thema und Nachricht; im Wachstums-Rechner zusätzlich die von Ihnen eingegebenen Planwerte) zur Bearbeitung Ihrer Anfrage. Rechtsgrundlage: Art. 6 Abs. 1 lit. b DSGVO (vorvertragliche Maßnahmen) bzw. lit. f DSGVO. Die Formulare werden technisch über den Dienst FormSubmit (formsubmit.co) übermittelt, der die Eingaben per E-Mail an uns weiterleitet und nach unserer Kenntnis nicht dauerhaft speichert. Die Daten werden gelöscht, sobald sie nicht mehr erforderlich sind, spätestens nach Ablauf gesetzlicher Aufbewahrungsfristen.</p>
<h2>6. Terminbuchung</h2>
<p>Für Beratungstermine nutzen wir Calendly (Calendly LLC, 115 E Main St, Ste A1B, Buford, GA 30518, USA). Verarbeitet werden Name, E-Mail und Termindaten, sobald Sie über den Link eine Buchung vornehmen. Rechtsgrundlage: Art. 6 Abs. 1 lit. b DSGVO. Calendly ist unter dem EU-US Data Privacy Framework zertifiziert; es besteht ein Auftragsverarbeitungsvertrag.</p>
<h2>7. Cookies und Einwilligung</h2>
<p>Unsere Website verwendet Cookies und ähnliche Technologien. Technisch notwendige Speicherung (z. B. Ihre Cookie-Entscheidung im Local Storage) erfolgt auf Grundlage von § 25 Abs. 2 TDDDG bzw. Art. 6 Abs. 1 lit. f DSGVO. Alle nicht notwendigen Technologien (Analyse, Marketing) setzen wir nur mit Ihrer Einwilligung nach § 25 Abs. 1 TDDDG und Art. 6 Abs. 1 lit. a DSGVO ein. Ihre Einwilligung erteilen Sie über unser Consent-Banner und können sie jederzeit mit Wirkung für die Zukunft widerrufen, indem Sie die Website-Daten in Ihrem Browser löschen.</p>
<h2>8. Google Ads &amp; Conversion-Tracking</h2>
<p>Mit Ihrer Einwilligung nutzen wir Google Ads inkl. Conversion-Tracking und ggf. Remarketing (Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland). Wir setzen den Google Consent Mode v2 ein; ohne Einwilligung werden keine Marketing-Cookies gesetzt und keine personenbezogenen Daten an Google übermittelt. Rechtsgrundlage: Art. 6 Abs. 1 lit. a DSGVO. Übermittlungen in die USA stützen sich auf das EU-US Data Privacy Framework bzw. Standardvertragsklauseln.</p>
<h2>9. Meta-Pixel (Facebook/Instagram)</h2>
<p>Mit Ihrer Einwilligung nutzen wir den Meta-Pixel der Meta Platforms Ireland Ltd. (Merrion Road, Dublin 4, Irland) zur Messung und Optimierung von Werbeanzeigen. Der Pixel wird erst nach Ihrer Zustimmung geladen. Rechtsgrundlage: Art. 6 Abs. 1 lit. a DSGVO. Mit Meta besteht eine Vereinbarung über gemeinsame Verantwortlichkeit (Art. 26 DSGVO).</p>
<h2>10. Schriftarten</h2>
<p>Wir binden Schriftarten lokal von unserem eigenen Server ein. Es findet dabei keine Verbindung zu Servern Dritter (z. B. Google Fonts) statt.</p>
<h2>11. Ihre Rechte</h2>
<p>Sie haben das Recht auf Auskunft (Art. 15), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch (Art. 21 DSGVO). Erteilte Einwilligungen können Sie jederzeit widerrufen. Es besteht ein Beschwerderecht bei einer Aufsichtsbehörde – zuständig: Der Landesbeauftragte für den Datenschutz und die Informationsfreiheit Baden-Württemberg, Lautenschlagerstraße 20, 70173 Stuttgart.</p>
<h2>12. SSL-/TLS-Verschlüsselung</h2>
<p>Diese Seite nutzt aus Sicherheitsgründen eine SSL-/TLS-Verschlüsselung. Sie erkennen dies am „https://“ in der Adresszeile Ihres Browsers.</p>
'''

(ROOT / "impressum.html").write_text(legal_page("impressum.html", "Impressum – AIclicks",
    "Impressum von AIclicks – Performance-Marketing-Agentur, Marc Nothelfer, Friedrichshafen am Bodensee.",
    "Impressum", "", IMPRESSUM), encoding="utf-8")
(ROOT / "datenschutz.html").write_text(legal_page("datenschutz.html", "Datenschutzerklärung – AIclicks",
    "Datenschutzerklärung von AIclicks (aiclicks.de): Informationen zu Hosting, Kontaktformular, Cookies, Google Ads und Meta-Pixel.",
    "Datenschutzerklärung", f'<p class="meta">Stand: Oktober 2026</p>', DATENSCHUTZ), encoding="utf-8")

# ---------- 404 ----------
(ROOT / "404.html").write_text(head("Seite nicht gefunden – AIclicks", "Diese Seite gibt es nicht (mehr).", "404.html", robots="noindex, follow")
    + '''
<section class="sub-hero" style="padding-bottom:96px"><div class="wrap">
  <h1>Diese Seite gibt es nicht.</h1>
  <p class="meta">Fehler 404</p>
  <p class="lead">Vielleicht ist der Link alt oder vertippt. Das Wichtigste findest du hier:</p>
  <div class="cta-row"><a href="/" class="btn">Zur Startseite</a><a href="/#leistungen" class="link">Leistungen</a><a href="/#kontakt" class="link">Kontakt</a></div>
</div></section>
''' + FOOT_PLAIN, encoding="utf-8")

# ---------- Wachstums-Rechner ----------
CALC_CSS = '''<style>
.calc{display:grid;grid-template-columns:1.05fr .95fr;gap:48px;align-items:start}
.calc-form{display:grid;gap:18px}
.calc-form .field label small{display:block;font-weight:400;color:var(--muted);font-size:13px;margin-top:2px}
.result{position:sticky;top:104px;background:var(--dark);border:1px solid var(--line);color:var(--on-dark);border-radius:var(--r-lg);padding:34px 36px}
.result .lab{font-size:13.5px;color:var(--on-dark-muted);margin-bottom:10px}
.result .big{font-family:var(--display);font-size:clamp(34px,3.6vw,46px);font-weight:500;letter-spacing:-.02em;line-height:1.05;color:#fff;font-variant-numeric:tabular-nums lining-nums}
.result .row{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:26px;padding-top:22px;border-top:1px solid rgba(255,255,255,.14)}
.result .n{font-family:var(--display);font-size:22px;font-weight:500;color:#fff;font-variant-numeric:tabular-nums lining-nums}
.result .t{font-size:13px;color:var(--on-dark-muted);margin-top:4px;line-height:1.4}
.result .assump{font-size:13px;color:var(--on-dark-muted);margin-top:22px;line-height:1.5}
.disclaimer{font-size:14px;color:var(--muted);margin-top:18px;max-width:none}
.lead-box{margin-top:64px;padding-top:56px;border-top:1px solid var(--line);display:grid;grid-template-columns:1fr 1.2fr;gap:48px;align-items:start}
.lead-box form{display:grid;gap:16px}
@media(max-width:860px){.calc{grid-template-columns:1fr}.result{position:static}.lead-box{grid-template-columns:1fr;gap:28px}.result .row{grid-template-columns:1fr 1fr}}
</style>'''

CALC_BODY = '''
<section class="sub-hero"><div class="wrap">
  <p class="crumbs"><a href="/">Start</a> › Wachstums-Rechner</p>
  <h1>Was ist mit deinem Budget realistisch?</h1>
  <p class="meta">Wachstums-Rechner · Schätzung auf Basis branchenüblicher Werte</p>
  <p class="lead">Gib deine Zahlen ein und sieh eine unverbindliche Orientierung, was mit sauber optimiertem Marketing branchenüblich erreichbar wäre. Eine Schätzung – kein Versprechen.</p>
</div></section>

<section class="tight" style="padding-top:0"><div class="wrap">
  <div class="calc">
    <div class="calc-form">
      <div class="field"><label for="branche">Branche<small>bestimmt die Annahmen</small></label>
        <select id="branche"><option value="handwerk">Handwerk</option><option value="dienstleister">Dienstleister</option><option value="lokal">Lokales Geschäft</option><option value="ecommerce">E-Commerce / Onlineshop</option></select></div>
      <div class="field"><label for="budget">Monatliches Werbebudget (€)<small>ohne Agenturhonorar</small></label><input id="budget" type="number" inputmode="numeric" min="0" step="100" value="2000"></div>
      <div class="field"><label for="wert">Ø Auftrags- / Bestellwert (€)</label><input id="wert" type="number" inputmode="numeric" min="0" step="10" value="800"></div>
      <div class="field"><label for="close">Abschlussquote deiner Anfragen (%)<small id="closeHint">optional</small></label><input id="close" type="number" inputmode="numeric" min="1" max="100" step="1" value="30"></div>
      <p class="disclaimer"><strong>Wichtig:</strong> Diese Berechnung ist eine unverbindliche Schätzung auf Basis branchenüblicher Durchschnittswerte und stellt keine Zusage oder Garantie dar. Tatsächliche Ergebnisse hängen von Markt, Angebot, Wettbewerb und Umsetzung ab.</p>
    </div>
    <div class="result" id="result" aria-live="polite">
      <div class="lab">Geschätzter möglicher Zusatzumsatz pro Monat</div>
      <div class="big" id="umsatz">– €</div>
      <div class="row">
        <div><div class="n" id="anfragen">–</div><div class="t">mögliche Anfragen / Monat</div></div>
        <div><div class="n" id="auftraege">–</div><div class="t">mögliche Aufträge / Monat</div></div>
        <div><div class="n" id="jahr">– €</div><div class="t">hochgerechnet / Jahr</div></div>
      </div>
      <div class="assump" id="assump"></div>
    </div>
  </div>

  <div class="lead-box" id="analyse">
    <div>
      <h2 style="font-size:clamp(26px,3vw,36px)">Willst du deine echten Zahlen statt einer Schätzung?</h2>
      <p style="margin-top:14px">In der kostenlosen Wachstumsanalyse rechnen wir dein Potenzial an deinen tatsächlichen Daten durch – ehrlich, ohne Verkaufsdruck. Deine Eingaben aus dem Rechner schicken wir gleich mit.</p>
    </div>
    <form id="calcform" onsubmit="return submitLead(event)" action="https://formsubmit.co/marc@aiclicks.de" method="POST" novalidate>
      <input type="hidden" name="_subject" value="Wachstumsanalyse angefordert (Rechner)">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_captcha" value="false">
      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
      <input type="hidden" name="rechner" id="rechner-ctx">
      <div class="field"><label for="name">Name *</label><input id="name" name="name" required autocomplete="name"></div>
      <div class="field"><label for="mail">E-Mail *</label><input id="mail" name="email" type="email" required autocomplete="email"></div>
      <div class="field"><label for="tel">Telefon (für den Analyse-Call) *</label><input id="tel" name="phone" type="tel" required autocomplete="tel"></div>
      <label class="consent"><input type="checkbox" required id="cf-consent"><span>Ich habe die <a href="/datenschutz.html">Datenschutzerklärung</a> gelesen und stimme der Verarbeitung meiner Angaben zur Bearbeitung meiner Anfrage zu.</span></label>
      <p class="fine" id="cf-err" hidden role="alert">Bitte Name, E-Mail und Telefon ausfüllen und den Datenschutz bestätigen.</p>
      <button class="btn lg" type="submit" id="cf-submit">Kostenlose Wachstumsanalyse anfordern</button>
      <div id="cf-ok" class="ff-ok" hidden><b>Danke, <span id="okname">–</span>.</b><span>Marc meldet sich innerhalb von 24 Stunden mit deinem persönlichen Wachstums-Report.</span></div>
      <p class="fine">Kostenlos &amp; unverbindlich · Antwort in 24 Stunden · Kein Verkaufsgespräch, ein Fahrplan</p>
    </form>
  </div>
</div></section>

<script>
  // Branchen-Annahmen: konservative Kosten pro Anfrage (Lead) bzw. ROAS-Spanne. Bewusst vorsichtig.
  const A = {
    handwerk:     {cplLow:30, cplHigh:70, label:"Ø 30–70 € pro qualifizierter Anfrage (branchenüblich)"},
    dienstleister:{cplLow:25, cplHigh:60, label:"Ø 25–60 € pro qualifizierter Anfrage (branchenüblich)"},
    lokal:        {cplLow:15, cplHigh:45, label:"Ø 15–45 € pro Anfrage (branchenüblich)"},
    ecommerce:    {roasLow:2.0, roasHigh:4.0, label:"ROAS-Spanne 2,0–4,0 (branchenüblich bei sauberer Optimierung)"}
  };
  const fmt = n => new Intl.NumberFormat('de-DE',{maximumFractionDigits:0}).format(Math.round(n));
  const $ = id => document.getElementById(id);
  function calc(){
    const branche=$('branche').value, budget=Math.max(0,+$('budget').value||0), wert=Math.max(0,+$('wert').value||0);
    const closeInput=Math.min(100,Math.max(1,+$('close').value||30))/100, a=A[branche];
    let umsatzLow,umsatzHigh,anfLow,anfHigh,aufLow,aufHigh,assumpText;
    const t=document.querySelectorAll('.result .t');
    if(branche==='ecommerce'){
      $('closeHint').textContent="bei E-Commerce nicht nötig"; $('close').disabled=true;
      umsatzLow=budget*a.roasLow; umsatzHigh=budget*a.roasHigh;
      anfLow=wert>0?umsatzLow/wert:0; anfHigh=wert>0?umsatzHigh/wert:0; aufLow=anfLow; aufHigh=anfHigh;
      assumpText="Annahme: "+a.label+". Bestellungen = Umsatz ÷ Bestellwert.";
      t[0].textContent="mögliche Bestellungen / Monat"; t[1].textContent="mögliche Bestellungen / Monat";
    } else {
      $('closeHint').textContent="optional"; $('close').disabled=false;
      anfLow=budget/a.cplHigh; anfHigh=budget/a.cplLow; aufLow=anfLow*closeInput; aufHigh=anfHigh*closeInput;
      umsatzLow=aufLow*wert; umsatzHigh=aufHigh*wert;
      assumpText="Annahmen: "+a.label+", Abschlussquote "+Math.round(closeInput*100)+" %. Aufträge = Anfragen × Abschlussquote.";
      t[0].textContent="mögliche Anfragen / Monat"; t[1].textContent="mögliche Aufträge / Monat";
    }
    $('umsatz').textContent=fmt(umsatzLow)+" – "+fmt(umsatzHigh)+" €";
    $('anfragen').textContent=fmt(anfLow)+"–"+fmt(anfHigh);
    $('auftraege').textContent=fmt(aufLow)+"–"+fmt(aufHigh);
    $('jahr').textContent=fmt(umsatzLow*12)+" – "+fmt(umsatzHigh*12)+" €";
    $('assump').textContent=assumpText;
    $('rechner-ctx').value="Branche: "+branche+" | Budget: "+budget+" € | Auftragswert: "+wert+" € | Abschlussquote: "+Math.round(closeInput*100)+" % | Schätzung: "+$('umsatz').textContent+" / Monat";
  }
  function submitLead(e){
    e.preventDefault();
    const f=e.target, err=$('cf-err'), btn=$('cf-submit');
    if(!f.checkValidity()){err.hidden=false;const bad=f.querySelector(':invalid');if(bad)bad.focus();return false;}
    err.hidden=true; btn.disabled=true; btn.textContent='Wird gesendet …';
    const name=$('name').value.trim();
    fetch('https://formsubmit.co/ajax/marc@aiclicks.de',{method:'POST',headers:{'Accept':'application/json'},body:new FormData(f)})
      .then(r=>r.json()).then(j=>{
        if(j&&(j.success==='true'||j.success===true)){f.querySelectorAll('.field,.consent,#cf-submit,.fine').forEach(el=>el.hidden=true);$('okname').textContent=name.split(' ')[0];$('cf-ok').hidden=false;}
        else throw new Error('send failed');
      }).catch(()=>{
        btn.disabled=false; btn.textContent='Kostenlose Wachstumsanalyse anfordern';
        const body=encodeURIComponent('Name: '+name+'\\nE-Mail: '+$('mail').value+'\\nTelefon: '+$('tel').value+'\\n\\n'+$('rechner-ctx').value);
        window.location.href='mailto:marc@aiclicks.de?subject='+encodeURIComponent('Wachstumsanalyse – '+name)+'&body='+body;
      });
    return false;
  }
  ['branche','budget','wert','close'].forEach(id=>{$(id).addEventListener('input',calc);$(id).addEventListener('change',calc);});
  calc();
</script>
'''
(ROOT / "roi-rechner.html").write_text(
    head("Wachstums-Rechner: Was ist mit deinem Werbebudget realistisch? | AIclicks",
         "Kostenloser Wachstums-Rechner: Wie viele Anfragen oder Bestellungen sind mit deinem Werbebudget realistisch? Schätzung für Handwerk, Dienstleister und E-Commerce.",
         "roi-rechner.html", extra=CALC_CSS)
    + CALC_BODY + FOOT_PLAIN, encoding="utf-8")
print("wrote impressum.html, datenschutz.html, 404.html, roi-rechner.html")
