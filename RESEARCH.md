# Cross-border VAT for commerce SMEs — research

Scope: a Netherlands-based e-commerce / commerce SME making its first
cross-border expansion into **Germany** and **Belgium**. This is the wedge for
the larger SME growth/expansion platform. Researched June 2026 from tax-authority
sources, Your Europe, and specialist providers; planning-grade timelines are
flagged as estimates, not official SLAs.

**One-line thesis:** the market is split between *tools that tell you the rules*
and *expensive humans who do the work*. Almost nobody produces the **specific,
sequenced workflow** for a given seller — "you hold stock in DE, so OSS won't
cover it; register at Finanzamt Kleve, in this order, by these dates" — and then
executes it. That synthesis-plus-execution gap is the opening.

---

## 1. Is it actually a mess? Yes — and structurally, not just unfamiliar

The difficulty isn't any single step. It's the **combinatorial explosion**: OSS
*plus* N local registrations *plus* N packaging-EPR regimes *plus* B2B reporting,
each on a different portal, cadence, and penalty clock — and the worst traps are
invisible until you've already breached them.

**Genuinely hard:**
- **OSS-vs-local-registration is a real conceptual trap.** OSS is marketed as
  "one registration for all of Europe." The moment stock crosses a border (the
  Amazon Pan-EU FBA default), that promise breaks and you need a *local*
  registration *on top of* OSS. The boundary — dispatch transaction (OSS) vs.
  domestic supply + stock movement (local) — is non-obvious and routinely
  misunderstood.
- **The FBA surprise.** Holding stock in a country triggers a local VAT
  registration **instantly — no threshold, no grace period**. Pan-EU FBA
  silently distributes stock to several countries at once. Sellers discover the
  obligation retroactively, often with penalties already accrued.
- **Per-country divergence in everything operational.** Different portals (Mijn
  Belastingdienst / ELSTER / Intervat), cadences (NL quarterly default; DE
  **monthly for the first two years**; BE monthly-or-quarterly), deadlines (NL
  last day of month; DE the 10th; BE the 20th), and penalty regimes.
- **Two numbers, two authorities in Germany.** Steuernummer (Finanzamt Kleve)
  *then* USt-IdNr (BZSt), sequential, with realistic multi-week lead times for a
  foreign applicant — long enough to stall a launch.
- **The EPR overlap nobody expects.** Germany's Verpackungsgesetz / LUCID is
  *environmental law, not tax*, yet it's a hard precondition for selling to
  German consumers, marketplace-enforced, with fines up to €200,000 — and it has
  its own registration, dual-system contract, and reporting.

**Mostly just unfamiliar (not intrinsically hard):**
- **Language.** German filings are German-language, though Finanzamt Kleve
  deliberately offers Dutch support; Belgium allows Dutch — so for an NL seller
  this is more navigable than for most.
- **The €10k threshold itself** is simple once understood (one EU-wide net
  figure); the edge case is that it's cumulative across all EU and bites mid-year
  with no grace period.
- **OSS quarterly filing** is a genuine simplification *for pure distance
  selling* — the mess only appears once stock-holding or B2B enters.

---

## 2. The process, accurately

### 2.1 NL home baseline
- Register the business with **KvK**; it passes data to the **Belastingdienst**,
  which issues VAT numbers (~10 working days). You get **two**: the public
  **btw-id** (on invoices) and the **omzetbelastingnummer** (Belastingdienst
  correspondence only).
- **Quarterly BTW return** by default, via Mijn Belastingdienst Zakelijk, due one
  month after quarter-end (30 Apr / 31 Jul / 31 Oct / 31 Jan).

### 2.2 Cross-border B2C + OSS
- Since **1 July 2021**, a single **EU-wide €10,000** net distance-selling
  threshold (cumulative across all EU, bundling goods + TBE services). Below it,
  charge NL VAT; above it, charge **destination-country** rates from the sale
  that crosses the line.
- **Union OSS**: register via Mijn Belastingdienst Zakelijk; one **quarterly**
  return covers all intra-EU B2C distance sales; one payment to the
  Belastingdienst, which distributes to each member state.

> **What OSS does NOT cover** (the critical callout):
> 1. **Holding/moving stock in another country** → local registration.
> 2. **Domestic sales within a foreign country** (sold from local stock) → local
>    return, not OSS.
> 3. **B2B / intra-Community** supplies → reverse-charge + EC Sales List
>    (Zusammenfassende Meldung).
> 4. **Input VAT recovery** → separate refund procedure / local registration.

### 2.3 The FBA / stock trigger
Storing inventory in a German warehouse (Amazon FBA, Pan-EU FBA, or a 3PL)
creates a taxable presence **immediately**, regardless of sales volume. A sale
from German stock to a German consumer is a **domestic** supply (outside OSS),
and the movement of your own stock NL→DE is itself reportable. Recommended
hybrid: **OSS for distance sales from NL stock + local registration wherever you
hold stock.**

### 2.4 NL → Germany sequence (used verbatim in the product demo)
1. (If over €10k) **OSS in NL** — covers DE distance sales from NL stock.
2. **German VAT registration at Finanzamt Kleve** — the office *centrally
   responsible for Netherlands-resident businesses* (a "Europa-Finanzamt" with
   Dutch-language support). Submit the **Fragebogen zur steuerlichen Erfassung**
   plus KvK extract, NL btw-id, org chart.
3. **Receive the Steuernummer** (planning estimate: ~4–12 weeks for a foreign
   applicant; not an official SLA).
4. **Obtain the USt-IdNr from the BZSt** — issued *after* the Steuernummer;
   requestable on the same Fragebogen. Two different numbers, two authorities.
5. **File via ELSTER** (mandatory electronic portal).
6. **Umsatzsteuervoranmeldung (advance returns)** — **monthly for the first two
   calendar years** for new registrations; due the **10th** of the following
   month. (Afterwards: >€7,500 prior-year liability → monthly; €1,000–7,500 →
   quarterly; <€1,000 → annual only.)
7. **Annual Umsatzsteuererklärung** — due ~31 July of the following year
   (extended with a Steuerberater).
8. **Zusammenfassende Meldung (EC Sales List)** for any B2B — separate from OSS.
9. **Verpackungsgesetz / LUCID** registration with the ZSVR — a **precondition**
   for selling packaged goods to German consumers: (a) register in LUCID (free),
   (b) sign a dual-system/licensing contract (paid), (c) report packaging
   volumes. Marketplace-enforced; fines to €200,000.

### 2.5 NL → Belgium sequence
1. (If over €10k) **OSS** already covers BE distance sales from NL stock.
2. **Belgian VAT registration** only when a local trigger arises (stock in BE,
   domestic supplies, imports). EU companies register **directly** — **no fiscal
   representative required** (that's a non-EU rule).
3. **Periodic returns via Intervat** — monthly by default; quarterly allowed
   under €2.5M turnover (with conditions); due the **20th** of the following
   month.
4. **EPR note:** Belgium has its own packaging EPR (**Fost Plus**), analogous to
   LUCID; expect an obligation if shipping packaged goods to BE consumers.
   *(Flagged for deeper verification.)*

---

## 3. Competition

### Categories
- **Calculators / aggregators** (compute, don't file): Quaderno, Stripe Tax
  (core), Fonoa, Octobat, Eurora. Get the math right; the registration and the
  return are someone else's job. Quaderno explicitly doesn't file; Stripe Tax
  routes filing to partners (Taxually globally, TaxJar US).
- **Self-serve filing software** (modular): Avalara, Taxually, plus AI-native
  **Kintsugi** and **Numeral**. Can register and file, but Avalara is modular and
  pricey, and — notably — **retired Returns for Small Business on 31 Dec 2024**,
  abandoning the SME end. Kintsugi/Numeral are SMB-friendly but **US-sales-tax
  first**; EU/VAT depth is still maturing.
- **Hybrid managed services** (software + human + filing): **Taxdoo**,
  **hellotax**, **countX**, **Marosa**. Closest to "do it for me," and the most
  fit-for-purpose category for an SME — but quality is uneven and pricing opaque.
- **Enterprise** (Vertex, Sovos, Avalara top tier): deep, but built and priced
  for large finance teams. Overkill for a small NL seller.
- **Local accountants** (the status quo): most flexible and judgment-rich, but
  slow, ~€500–2,000+/mo, and dependent on you knowing what to ask. This is what
  most SMEs fall back on — especially after Amazon's exit.

### The Amazon "VAT Services on Amazon" exit — the demand driver
Amazon's in-platform program let sellers get multi-country EU VAT registrations
and filings cheaply inside Seller Central. **Amazon discontinued it on 31 October
2024**, ending its tax-agent arrangements. It promised an "improved programme by
2025" that, as of mid-2026, hasn't materialised. The cohort hit hardest is
exactly ours — pan-EU FBA sellers holding stock in DE and needing multi-country
registration. Amazon still provides the *data*; it no longer does the *work*.
This pushed tens of thousands of sellers into the open market and is the single
biggest current driver of demand. (Every provider now runs an "Amazon VAT
Services is ending" landing page.)

### Where the complaints actually are
Across hellotax (Trustpilot ~3.7), Avalara (~3.0), Taxdoo (~3.5), the pain isn't
missing features — it's **execution and trust**: broken Shopify/Amazon connectors
mislabeling sales, slow registrations (hellotax reportedly ~3 months vs. ~days
elsewhere), account managers who don't know VAT, missed filings, and surprise
billing / forced upgrades. The winning move is **reliably doing the boring work
and communicating**, not more dashboards.

---

## 4. White space — what we should build into

1. **The sequenced-workflow gap (core).** Calculators give numbers; portals give
   rules. Nobody hands a *single ordered playbook* for "NL seller, first FBA
   stock in DE, distance sales to BE" — when OSS suffices vs. when you must
   register locally, in what order, with deadlines. The seller self-assembles it
   from tools + rule pages + an accountant. **This is exactly the configurator
   and the dashboard timeline we built.**
2. **The orphaned "first expansion" SME.** Enterprise tools are too heavy;
   AI-native entrants are US-first; Avalara dropped small-business returns;
   Amazon left. The guided, EU-VAT-native, SME-priced product is thinly served.
3. **Adjacent obligations are siloed.** VAT + OSS + **EPR/LUCID** + (where
   needed) fiscal representation are handled by different vendors. Almost no
   SME-grade product bundles them into one onboarding. We should treat EPR as
   first-class, not a footnote.
4. **Trust/execution as the product.** Reliability and communication are the real
   differentiator. Status visibility (what's done, what's pending, what needs
   you), proactive deadline handling, and "we chase the Finanzamt for you" beat
   feature breadth.
5. **NL/BE depth.** Most tooling is DE/UK/US-centric. NL-origin nuance and Belgium
   specifically are under-served — which is why starting NL-centred with BE/DE is
   a defensible, under-contested wedge.

---

## 5. How this maps to what's been built

- **Landing `index.html`** — reframed entirely around cross-border VAT; the
  "what one sale sets off" problem section encodes the real triggers (€10k line,
  stock-abroad, second tax office, filing rhythm, Verpackungsgesetz).
- **Interactive configurator** — the synthesis gap made tangible: pick markets,
  threshold, and where stock sits; it derives OSS vs. local registration,
  USt-IdNr/ELSTER, monthly Voranmeldung, LUCID, and Intervat live.
- **Dashboard `dashboard.html`** — a fictional NL skincare SME (Bloomwell B.V.)
  midway through the DE sequence above: Finanzamt Kleve registration submitted,
  ELSTER and templates in progress, USt-IdNr / LUCID / first Voranmeldung
  pending. Filings, templates, and monitoring panels reflect the real cadences.

---

## 6. Open items to verify before relying on this commercially
- Exact current designation of Belgium's Central VAT Office for foreign
  taxpayers, and BE packaging-EPR (Fost Plus) specifics.
- Concrete, current Steuernummer lead times for NL applicants at Finanzamt Kleve
  (we use a planning range, not an official figure).
- Live pricing for hellotax / countX / Marosa / Avalara full stack (quote-based).
- "Staclar" could not be confirmed as a real VAT/tax company — likely a
  misremembered name. Genuine AI-native names in scope: Kintsugi, Numeral, VATai.

---

## Sources (selected)

**EU / OSS:** vat-one-stop-shop.ec.europa.eu · PwC "New e-commerce EU VAT rules
July 2021" · amavat OSS threshold guide.
**NL:** belastingdienst.nl (Union scheme; btw-id vs omzetbelastingnummer) ·
business.gov.nl · kvk.nl e-commerce VAT.
**FBA trigger:** amavat "Amazon FBA and VAT in Germany" / "Pan-European FBA".
**Germany:** finanzamt.nrw.de (Umsatzsteuer für niederländische Unternehmer /
Finanzamt Kleve "Europa-Finanzamt") · gesetze-im-internet.de UStZustV · bzst.de
USt-IdNr · firma.de advance VAT return · elster.de.
**Verpackungsgesetz/LUCID:** verpackungsregister.org (ZSVR) · lizenzero.de.
**Belgium:** finance.belgium.be periodic VAT return · Intervat · Marosa Belgium
VAT manual · Eurofiscalis.
**Competition:** taxdoo.com/price · hellotax blog "Amazon VAT services ended" ·
carbon6 / AVASK / amavat on the Amazon discontinuation · countx.com · marosavat.com
· stripe.com/tax + docs/tax/filing · quaderno.io comparison · taxcloud "Avalara
RSB ending" · trykintsugi.com · numeral.com.
