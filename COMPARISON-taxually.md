# Taxually vs. BEACON — an honest head-to-head

Where Taxually sits, where BEACON (as scoped across this project — the NL-centred,
synthesis-led wedge with the obligations configurator and the guided dashboard)
is genuinely differentiated, and where Taxually simply beats us today.
Researched June 2026 from Taxually/Stripe primary sources and reviews; uncertainty
flagged. Not legal or investment advice.

> **Premise correction up front.** A working assumption going in was that Taxually
> had rolled up several VAT firms (LOVAT, Counto, Taxmen). That's wrong: **LOVAT is
> an independent competitor** (Edinburgh), and Counto/Taxmen show no link. The
> **only confirmed acquisition is LumaTax (US sales tax, April 2023)**. And a
> second correction to our own earlier research: Taxually **does** cover
> EPR/Verpackungsgesetz (its **EcoTax** module), so bundling EPR is *not*, by
> itself, our wedge.

---

## Snapshot, side by side

| | **Taxually** | **BEACON** (as scoped here) |
|---|---|---|
| **Shape** | Horizontal, global VAT/sales-tax compliance platform + managed filing | Vertical wedge: NL-based commerce SMEs expanding to DE & BE |
| **Founded / base** | 2018, Budapest; ex-KPMG founders; Ardian minority stake (2022) | New entrant (this project) |
| **Coverage** | 100+ filing jurisdictions (claims vary 50+/100+/150+); EU + UK + US (via LumaTax) | Three markets, deliberately: NL (home), DE, BE |
| **Model** | Hybrid software + humans who register & file for you | Synthesis + guided execution; "you stay seller of record, we run the tax" |
| **Distribution** | **Platform-embedded — Stripe Tax's non-US registration/filing partner** | Direct, demand-led on the "synthesis gap" |
| **Adjacent obligations** | VAT, OSS/IOSS, **EPR (EcoTax)**, US sales tax (LumaTax), payments (OneTax) | VAT/OSS + EPR as *sequenced* steps, NL→DE/BE only |
| **Pricing** | Quote-led, opaque; sometimes bundled into Stripe Tax | (Intended) fixed, transparent corridor pricing |
| **Public API** | None found publicly; integration is via the Stripe app | (Intended differentiator — but constrained, see §7) |
| **Reputation** | Trustpilot ~4.1, polarized: praise + serious registration-delay/"sales-then-silence" complaints | n/a (pre-launch) |

---

## 1. Strategy — horizontal roll-up vs. vertical wedge

Taxually is a **breadth** play: be the compliance engine for *everywhere*, across VAT,
EPR, and US sales tax, and grow by distribution and acquisition. The four-brand
structure (CrossTax / LumaTax / EcoTax / OneTax) and the Ardian "external growth"
mandate are consistent with that.

BEACON, as we've built it, is the opposite bet: **depth on one corridor.** The whole
project — the editorial landing page, the obligations configurator, the Bloomwell
dashboard sequenced around Finanzamt Kleve — is designed to be *unmistakably* about
"a Dutch shop's first step into Germany/Belgium," not "tax, anywhere."

The strategic question this raises: a vertical wedge only wins if the corridor has
**depth Taxually's generic breadth doesn't reach** — Dutch-language handholding, the
exact NL→DE sequence, the FBA-stock-in-Germany trigger, LUCID timing. That depth is
plausible but **unproven**; breadth is a real, defensible asset for Taxually.

---

## 2. Distribution — the Stripe moat is the biggest single fact

Taxually is **Stripe Tax's partner for registering and filing outside the US** (Stripe's
own words). For a Stripe merchant, "Register for me" → Taxually is the *in-dashboard
default*, with two-way sync back into Stripe Tax. That's an enormous, low-CAC funnel
a new entrant cannot displace head-on.

Two honest implications:
- **We should not try to out-Stripe Stripe.** Much of Taxually's SME inflow is
  *Stripe merchants*, captured at the moment of need inside a product they already use.
- **But Stripe Tax is calculation-first**, and the Taxually flow is self-serve "upload
  docs, we submit." That leaves the **guided, sequenced, "what do I do first and by
  when"** experience underserved — which is exactly what our configurator + dashboard
  are. The opening is the *non-Stripe-native* SME and the *first-timer who needs a
  hand*, not the Stripe merchant who just wants a filing done.

---

## 3. Product & experience — managed filing vs. sequenced guidance

Taxually genuinely **registers and files** (IOSS intermediary, UK MTD, OSS, multi-country
returns) — it is not a calculator. Data sync and return generation are automated;
registration review and submission are human. Its product surface is organised by
*module* (CrossTax, EcoTax…), i.e. by **obligation type**.

What we've built is organised by **the customer's journey**, not the obligation type:
- **The configurator** turns "where do you sell / where's your stock / are you over
  €10k" into the *specific, ordered* obligation map — the synthesis no portal (or
  Taxually's module list) hands you.
- **The dashboard** shows that as a *timeline with status* — Finanzamt Kleve submitted,
  ELSTER pending, LUCID before first sale, first Umsatzsteuervoranmeldung scheduled —
  plus "needs you" tasks and monitoring.

This is the crux: Taxually answers *"file my returns."* We're answering *"tell me what
this expansion actually requires, in order, and walk me through it."* Different jobs.
The risk is that for a sophisticated seller the second job collapses into the first
once they've done it once.

---

## 4. Adjacent obligations — our earlier EPR claim needs walking back

Our `RESEARCH.md` white-space note implied almost nobody bundles VAT + OSS + EPR.
**Taxually's EcoTax disproves the strong version of that.** So the differentiator is
**not** "we also do Verpackungsgesetz." It's narrower and more defensible:
**weaving VAT + OSS + EPR into one *sequenced* SME flow** where LUCID appears as
"step 8, before your first German sale," rather than as a separate module the seller
has to know to buy. Existence of coverage ≠ integrated sequencing. We should market
the *sequencing*, not the *coverage*.

---

## 5. Trust & onboarding — their weakness is our entire thesis

The most striking finding is that Taxually's pain is **execution and communication,
not features**: recurring reviews cite *"sales team disappears after payment,"*
multi-month-to-multi-year registration delays, lost files, and surprise billing
(Trustpilot ~4.1 but polarized). This is the same pattern our `RESEARCH.md` found
across the whole category.

That is precisely the wedge the BEACON experience is built around — **visible status,
proactive deadlines, "we chase the Finanzamt for you," and a sequenced plan that tells
a first-timer what's next.** If we can deliver *reliable, communicative execution*
with an SLA on first registration, that beats "more dashboards" — and it's the one
area where a focused newcomer can credibly out-operate a high-volume incumbent.

The catch (see §8): execution reliability is *operational*, and Taxually has already
built the filing machinery and authorisations. Claiming we'll execute better is easy;
proving it pre-launch is not.

---

## 6. Pricing & transparency

Taxually is **quote-led**, with no public price list and **inconsistent self-reported
country counts (50+/100+/150+)**. For a first-time NL SME, opacity is friction. A
**fixed, transparent NL→DE/BE package** ("here's the price to get compliant in Germany,
all-in") is a clean, honest contrast — and cheap to deliver because the corridor is
narrow and the steps are known.

---

## 7. Tech / API — and the integration-constraint reality check

No public Taxually API/developer docs were found; their "integration" story is mainly
the Stripe app. "Open API for NL accounting/marketplace tools" is therefore a *possible*
differentiator — **but our own integrations research is a reality check on how far
"API-first" can go:**
- **DE filing is ERiC only** (a native library you embed; no REST), and **preparing
  returns on behalf is reserved to Steuerberater under the StBerG.**
- **NL** needs **PKIoverheid certs + eHerkenning chain mandates**; **OSS is portal-bound.**
- **BE** only opened Intervat/MyMinfin APIs in 2025, behind a "recognized user" process.

So nobody — Taxually included — gets a clean API-first path to *government* filing; the
moat is operational (authorisations, ERiC integration, a Steuerberater relationship).
Where an open API *does* differentiate is on the **input side**: pulling
**Amazon SP-API FBA-inventory-by-country** to detect the stock-location trigger, plus
Shopify/Stripe — turning our configurator's static logic into *live* monitoring. That's
a credible, buildable technical edge that plays to the corridor story.

---

## 8. Where Taxually genuinely beats us today (no spin)

1. **It actually files, in 100+ jurisdictions** — real, working registration/filing
   machinery and IOSS-intermediary status. We have a design, not a filing engine.
2. **The Stripe distribution moat** — default in-dashboard funnel, low CAC.
3. **Breadth as a retention story** — when the SME later goes beyond DE/BE, Taxually
   already covers it; our deliberate narrowness means we'd hand that customer off.
4. **EPR + US already covered** (EcoTax, LumaTax) — so several "we also do X" pitches
   don't land against them.
5. **Operational authorisations already solved** — the StBerG/ERiC/eHerkenning hurdles
   that we'd have to clear, they've cleared.

---

## 9. The defensible wedge for BEACON

Stack-ranked, what actually holds up against Taxually:
1. **Sequenced, guided first-expansion experience** for the NL→DE/BE corridor — the
   configurator + dashboard journey, not a module list. *(Strong; this is the product.)*
2. **Reliable, communicative execution with a first-registration SLA** — attacking
   Taxually's single biggest complaint. *(Strong, but operational to prove.)*
3. **Transparent fixed corridor pricing.** *(Easy win on friction.)*
4. **Live stock-location/threshold monitoring via Amazon SP-API + Shopify.** *(Real
   technical edge on the input side.)*
5. **Dutch-language, NL-corridor depth** (Finanzamt Kleve nuance, BE local quirks).
   *(Plausible; verify it's real depth, not just claimed.)*

What is **not** a wedge: "we do EPR," "we do OSS," "we file returns" — table stakes
Taxually already meets.

---

## 10. Risks & what would need to be true

- **Job collapses on repeat.** Sequencing is most valuable the *first* time; a seller
  who's expanded once may just want cheap filing — where Taxually/Stripe win. Mitigate
  by making the recurring monitoring/filing genuinely better, not just the onboarding.
- **Operational debt.** Out-executing an incumbent on registrations means building (or
  partnering for) the ERiC integration, the eHerkenning mandates, and a Steuerberater
  relationship — the unglamorous moat. The strategy is only real if we commit to this.
- **Distribution.** Without a Stripe-grade funnel, CAC is the existential risk for a
  vertical wedge; the corridor focus has to translate into sharp, cheap demand-gen
  (NL e-commerce communities, Amazon-FBA NL sellers, accountants).
- **Narrowness as a ceiling.** The wedge is a start; the "SME growth/expansion platform"
  vision needs a credible path from one corridor to many without becoming a thinner
  Taxually.

---

## Scorecard

| Dimension | Taxually | BEACON (scoped) | Edge |
|---|---|---|---|
| Breadth of coverage | Strong | Narrow by design | Taxually |
| Files/registers today | Yes, proven | Design only | Taxually |
| Distribution | Stripe moat | TBD | Taxually |
| Guided first-expansion UX | Weak (self-serve) | Strong (configurator + dashboard) | BEACON |
| Execution reliability / comms | Weak (top complaint) | Thesis (unproven) | BEACON if delivered |
| Pricing transparency | Opaque | Fixed/transparent | BEACON |
| EPR / adjacent obligations | Covered (EcoTax) | Covered, *sequenced* | Tie (edge on sequencing) |
| NL/BE corridor depth | Generic | Deliberate | BEACON if real |
| Input-side data integration | Limited public API | SP-API stock trigger | BEACON if built |
| Operational authorisations | Solved | To build | Taxually |

**Bottom line.** Taxually wins on breadth, distribution, and the fact that it actually
works at scale today. BEACON's defensible space is *not* features or coverage — it's the
**guided, sequenced, reliably-executed first expansion on one corridor, priced
transparently, with live stock-trigger monitoring.** That's a real wedge against
Taxually's documented weakness (post-sale execution), provided we treat the unglamorous
operational moat — authorisations, ERiC, a Steuerberater partner, a cheap NL funnel — as
the actual product, not an afterthought.

---

## Sources (selected)

Taxually: taxually.com (home, about-us, crosstax, onetax, stripe); support.taxually.com
(coverage; EPR). Stripe: docs.stripe.com/tax (use-taxually-to-register; file-with-taxually;
filing); stripe.com/tax. Corporate: ardian.com (minority-stake press release & feature);
pitchbook.com Taxually profile. LumaTax: prnewswire.com & finsmes.com (April 2023
acquisition); taxually.com blog. Reputation: trustpilot.com/review/taxually.com; Amazon
Seller Central EU forum thread; glassdoor.com. Comparisons (lower confidence):
goodvat.com (Stripe Tax vs Taxually); trykintsugi.com. LOVAT (independent, not acquired):
vatcompliance.co / lovat.io. Cross-referenced with this project's own RESEARCH.md and
INTEGRATIONS.md.
