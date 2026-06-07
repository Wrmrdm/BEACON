# Back-end integrations, identity & required data — NL / BE / DE

What a VAT-compliance platform like BEACON can actually integrate to file on
behalf of e-commerce SMEs, what regulatory back-ends each country exposes, and
what personal information each path legally requires. Researched June 2026 from
official sources (Belastingdienst, Logius, ELSTER, BZSt, FPS Finance, ZSVR, EU
Commission) plus vendor docs. Time-sensitive and single-source items are
flagged; this is engineering/product research, **not legal advice**.

---

## 0. The three things that shape everything

1. **"Filing on your behalf" is gated by permissions and professional rules, not
   APIs.** The technical channel usually exists; the right to use it for a client
   is the hard part.
   - **NL:** you need **eHerkenning EH3 + a chain mandate (ketenmachtiging)** to
     act for a client.
   - **DE:** preparing a VAT return for a third party is **reserved tax advice
     under the Steuerberatungsgesetz (StBerG)** — a non-Steuerberater SaaS may
     **not** sell "we prepare and file your VAT returns." You can be the
     *technical* transmitter; you cannot be the *adviser* without a Steuerberater
     in the loop.
   - **BE:** filing for a client runs through the **CSAM mandate model
     (Mandatenbeheer)**.

2. **Identity numbers are legally restricted — design to avoid them.** The Dutch
   **BSN** in particular may only be processed with an explicit statutory basis;
   a private filer almost certainly has none. Architect around company-level keys
   (KvK/RSIN, btw-id, enterprise number, Steuernummer) and minimise buyer PII.

3. **The real integration is commercial, not governmental.** The data that drives
   VAT logic — sales by destination, and *where stock physically sits* (the
   trigger for local registration) — comes from **Amazon SP-API, Shopify, Stripe**
   etc., not from tax portals. Government back-ends are mostly *output* (filing);
   marketplaces are the *input*.

---

## 1. Cross-cutting / EU layer

| System | Purpose | Integration | Access / auth | Notes |
|---|---|---|---|---|
| **VIES** (DG TAXUD) | Validate EU VAT numbers of B2B counterparties | **SOAP** (`checkVat`, `checkVatApprox`) + a public **REST** endpoint | **None** — public, no key, no SLA | Pass your own VAT no. to the *approx/qualified* call to get a **consultation number** = cross-border evidence of verification. Best-effort, Commission-disclaimed; weaker than DE's BZSt qualified confirmation. Store consultation number + UTC timestamp + raw response. |
| **EU OSS / IOSS** | One VAT return for distance sales | **No EU filing API** — always **national** portals | Per-MS national eID | SaaS can *prepare/validate* the return; *submission is national*. |
| **eIDAS / EUDI Wallet** | Cross-border login / KYC of SME users | eIDAS notified eID today; **EU Digital Identity Wallet** mandated across 27 MS | Relying-party onboarding per scheme | Future single route to authenticate users across NL/BE/DE. Go-live dates phased/slipping — treat 2026–27 as targets. |
| **Company registries / EU BRIS** | KYB / company master data | **BRIS = e-Justice web UI only, no public API** | Web search | For automation use national APIs (KvK is best) or commercial KYB. |
| **Identity proofing** (Onfido/Entrust, Veriff, itsme, iDIN) | Passport/liveness onboarding | Vendor REST/SDK | Vendor contract | **iDIN (NL) being retired** — itsme acquired it, full phase-out ~end-2027. Build NL identity onboarding around **itsme / EUDI**, not iDIN. |
| **PSD2 / open banking** *(optional)* | Reconcile VAT paid vs declared | Bank APIs via aggregator (Tink/Yapily/Enable Banking) | AISP licence + eIDAS QWAC, or a licensed aggregator; PSU consent | Nice-to-have reconciliation layer, not core. |

---

## 2. The real VAT input: commercial data sources

### Amazon SP-API — detecting the stock-location trigger
Holding stock in a country generally forces a **local VAT registration** there and
takes those sales out of OSS. Detecting *where stock physically sits* is the
single most valuable integration, and Amazon exposes it:

- **`GET_LEDGER_SUMMARY_VIEW_DATA`** (and `..._DETAIL_...`) with
  **`reportOptions.aggregateByLocation = "COUNTRY"`** → tells you which EU country
  your inventory is in → drives the local-registration trigger.
- **`GET_AFN_INVENTORY_DATA_BY_COUNTRY`** — quantity available for fulfilment
  **by country**, near-real-time (ideal for Pan-EU FBA).
- **`GET_VAT_TRANSACTION_DATA`** / **`SC_VAT_TAX_REPORT`** (VCS) — transaction-level
  VAT incl. cross-border inbound and FC transfers; covers NL, BE, DE.

**Access path:** register as an SP-API public developer → **Login with Amazon
(LWA) OAuth**. Inventory/order roles are non-PII; the **Tax Invoicing / Tax
Remittance roles are *restricted* (PII)** and require an architecture review plus
a **Restricted Data Token (RDT)** for any buyer personal data.

### Other channels
- **Shopify Admin API** — REST + GraphQL, OAuth scoped tokens; orders carry
  `tax_lines` and a `fulfillment_origin_location` (tax sourcing).
- **WooCommerce** — REST, consumer key/secret over HTTPS.
- **eBay Sell API** — OAuth 2.0 scoped tokens.
- **Stripe** — secret/restricted keys; OAuth (Connect); Stripe Tax line data.

### PII / GDPR when pulling order data
Order feeds contain buyer name, address, email. You are a controller; you only
need address → jurisdiction + VAT rate, so **minimise**: pseudonymise/aggregate to
country + amount where possible. Amazon enforces this technically (restricted
roles + RDT + mandatory data-protection review); mirror those controls for every
channel and for VIES consultation logs.

---

## 3. Netherlands

| Back-end | Purpose | Integration | Access requirements | Data needed |
|---|---|---|---|---|
| **Digipoort** (Logius) + **SBR/XBRL** | M2M filing of **btw return + ICP/EC sales list** to Belastingdienst | **SOAP** (WUS 2.0 request/response; ebMS notifications; SFTP for large files). Payload = **XBRL** vs the Nederlandse Taxonomie. **Not REST.** | **PKIoverheid services certificate**; Digikoppeling + **OIN** registration; preproduction + ValidatieTestService sandbox | XBRL return data; omzetbelastingnummer; signing cert |
| **OSS / IOSS** | Quarterly cross-border B2C VAT | ⚠️ **Portal only** — Mijn Belastingdienst Zakelijk → "EU-btw éénloketsysteem". No documented SBR/Digipoort channel | eHerkenning (or EU eID) | Per-country net sales + rates |
| **DigiD** | **Citizen** auth | Gov-only broker | ⚠️ **Not usable by a business SaaS** — natural persons only | Citizen BSN-linked login |
| **eHerkenning** | **Business** login to Belastingdienst | SAML SSO (auth, not a filing API) | **EH3**; to act for clients, **ketenmachtiging (chain mandate)**. Foreign providers without a KvK number can get "EH3 without KvK number" | Client consent form; provider middel |
| **KvK API** | Company/KYB lookup | **REST/JSON, GET-only** (Zoeken, Basisprofiel, Vestigingsprofiel, Naamgeving) | API key (paid); test env + public test key | KvK no. / RSIN as keys |

**Identifiers & the BSN constraint.** Two VAT numbers exist: the public **btw-id**
(on invoices; since 2020 deliberately *not* derived from BSN for sole traders) and
the internal **omzetbelastingnummer** (RSIN-based for entities; may still embed a
BSN for sole traders). **BSN may be processed only where a law explicitly allows
it** (UAVG art. 46 / Wabb) — the regulator (AP) even banned the *Belastingdienst*
from putting BSN in VAT numbers, forcing the 2020 change. **A private SaaS should
key on btw-id / omzetbelastingnummer / RSIN / KvK and avoid BSN.** Passport/ID
(KYC) needs its own basis (e.g. Wwft if you're an obliged entity — a generic VAT
filer usually isn't); flag for NL counsel.

**Automatable vs manual.** ✅ Periodic btw + ICP via SBR/Digipoort; ✅ company
lookup via KvK; ✅ on-behalf access via eHerkenning + ketenmachtiging.
❌ **OSS submission is portal-bound** today — you can automate prep/calculation,
not the final submit. (Verify with Belastingdienst/Logius before committing.)

---

## 4. Germany

| Back-end | Purpose | Integration | Access requirements | Data needed |
|---|---|---|---|---|
| **ELSTER + ERiC** | Submit **UStVA, annual USt, ZM, Fragebogen** | **Embed the ERiC native C library.** **No public REST/SOAP API.** | Register on ELSTER Entwickler-Bereich; **Hersteller-ID** per product; ERiC is free; test modes behind dev login | Tax XML + ELSTER certificate |
| **ELSTER certificate** | Authenticate transmissions | `.pfx` Organisationszertifikat embedded in ERiC | Requires a German **Steuernummer** (no German location needed); 3-yr validity; one cert files for many clients | Org identity |
| **Vollmachtsdatenbank (VDB)** | E-power-of-attorney + pre-filled data | App by Bundessteuerberaterkammer | ⚠️ **Steuerberater only** — not open to a general SaaS | Mandate data |
| **BZSt — USt-IdNr** | Issue DE VAT-ID | Via ELSTER Fragebogen → BZSt | Through registration; up to ~2 months | — |
| **BZSt — VAT-ID confirmation** (VIES front) | Simple + **qualified** confirmation of foreign EU VAT-IDs | **New REST API since 01.07.2025** (bulk). Old XML-RPC **shut down 30.11.2025** | Own DE USt-IdNr; **BOP certificate** (existing ELSTER cert reusable) | Own + target USt-IdNr (+ name/address for qualified) |
| **Verpackungsregister / LUCID** | Packaging EPR registration + Mengenmeldung | **Manual XML upload via portal.** Register-*excerpt* check has an API; **reporting has no M2M API** and **third-party submission is prohibited** | LUCID login; registration is personal (foreign-rep exception does **not** cover registration) | Brand names, packaging volumes |
| **Handelsregister / Unternehmensregister** | Company/KYB | Free since DiRUG (2022) but **no official developer API** | — | Company no./name |

> **The StBerG constraint (the binding limitation).** Preparing VAT returns for
> third parties is reserved "tax advice" under §§ 2–3 StBerG; only Steuerberater,
> lawyers, Wirtschaftsprüfer etc. may do it. Even trained bookkeepers may **not**
> prepare the Umsatzsteuervoranmeldung (BFH, II R 22/15). A non-Steuerberater SaaS
> can build the tooling and act as the **technical transmitter** (taxpayer owns
> the authorisation / signs), or offer self-service prep — but cannot sell
> "we prepare and file for you" without a Steuerberater in the loop.

**Identifiers.** Personal **Steuer-ID (IdNr)** (11-digit, lifelong) vs
**Steuernummer** (per Finanzamt; needed for the ELSTER cert) vs **USt-IdNr** (BZSt,
EU trade) vs the new universal **W-IdNr** (rollout ongoing). NL sellers register
via the ELSTER **Fragebogen zur steuerlichen Erfassung** (foreign-law-corporation
form), providing their Dutch BTW-nummer; NRW Finanzämter (Kleve) handle NL cases.
Foreign sellers can get a **Mein Unternehmenskonto / ELSTER cert** with a German
Steuernummer but no German location; **BundID** supports EU eID login.

**Automatable vs manual.** ✅ ERiC filing (only via the native lib, no REST); ✅
BZSt REST VAT-ID validation; ⚠️ on-behalf preparation is **legally** constrained;
❌ LUCID registration/reporting is manual and non-delegable; 🟡 no official
Handelsregister API.

---

## 5. Belgium

| Back-end | Purpose | Integration | Access requirements | Data needed |
|---|---|---|---|---|
| **Intervat** (FPS Finance) | Periodic VAT return, IC statement, annual client listing, OSS | (1) **Browser XML upload** vs published XSDs; (2) **NEW Intervat-API since ~Feb 2025** for periodic returns from software | "Recognized user of FPS Finance APIs" registration via MyMinfin; user agreement; validation tests. **Specs released only after registration** | VAT/enterprise no.; XSD-conformant data; IC client VAT nos. validated vs VIES |
| **MyMinfin-API** | Retrieve filing **receipts/confirmations** | REST-style, live ~Feb 2025 | Same "recognized user" model; **required companion to Intervat-API** | Enterprise no., doc refs |
| **CSAM + FAS** (BOSA) | Identity / auth front-door | **Interactive login only** (eID, **itsme**, eIDAS, TOTP). **No M2M auth**; certificate auth discontinued 03/2024 | A human with a recognised key acting for the company | Human identity credential |
| **Mandates (Mandatenbeheer)** | File VAT on behalf of a client | Web app; mandate validity carries into the API | Both parties authenticate via CSAM; client approves | Enterprise nos. of both parties |
| **KBO/BCE** | Company/KYB | Free Public Search UI; Public Search web service (paid); **Open Data bulk CSV + SFTP** | Register for web service/open data | Enterprise no. (10 digits, leading 0) |
| **IVCIE + Fost Plus / Valipac** | Packaging EPR | **Portal only — no public API found** | IVCIE registration; foreign sellers appoint a representative | Packaging quantities/materials |
| **FORREG** | Foreign-company VAT registration | Web app; login via CSAM or eIDAS | Foreign company; document upload; manual validation → enterprise no. | Company legal data, foreign tax ID, ID docs |

**Identifiers.** Company key = **enterprise number (KBO/BCE)**; VAT no. = `BE` +
enterprise number. **Rijksregisternummer** is for natural persons only (the human
who authenticates). **An NL (EU) company does *not* need a fiscal representative**
in Belgium — only non-EU companies do.

**Automatable vs manual.** The picture **changed in early 2025**: ✅ periodic VAT
return filing + receipt retrieval are now automatable via the new Intervat/MyMinfin
APIs; ✅ KBO open data. Still manual: ❌ IC statement & annual client listing (XSD
upload, human submit); ❌ CSAM auth (interactive only); ❌ FORREG registration &
mandate setup; ❌ Fost Plus/IVCIE EPR (no API — the biggest gap vs DE's LUCID
excerpt API). Protocol details (REST/OAuth, certs, sandbox) are **unpublished
until you register** — flag as unverified.

---

## 6. What personal information you actually need

Keep it to **company-level identifiers** wherever possible; collect person-level
data only for the human who authenticates or signs, and ID documents only with a
clear legal basis.

| | Netherlands | Germany | Belgium |
|---|---|---|---|
| **Company identifier** | KvK number, RSIN, btw-id, omzetbelastingnummer | Steuernummer, USt-IdNr, (W-IdNr) | Enterprise number (KBO/BCE), BE VAT no. |
| **Person identifier** | BSN — **avoid; legally restricted** | Steuer-ID (IdNr) — only where required | Rijksregisternummer — for the authenticating person only |
| **Auth credential** | eHerkenning EH3 (+ ketenmachtiging) | ELSTER Organisationszertifikat | CSAM via eID / itsme / eIDAS |
| **Passport / ID (KYC)** | Only if Wwft-obliged or for registration; basis required | For Fragebogen / legal reps; verify form version | For FORREG registration & foreign signatories without eID |
| **Beneficial owner** | UBO register (separate) | Transparenzregister (separate, not the Fragebogen) | UBO register (separate) |

**Rule of thumb:** identifiers like NL **BSN** and buyer PII from order feeds are
the highest-risk data. Avoid BSN entirely if you can; pull only the order fields
needed to determine place of supply; hold ID documents only behind a named legal
basis and DPA-bound processors.

---

## 7. Consolidated build verdict

| Capability | NL | DE | BE |
|---|---|---|---|
| **File periodic VAT return (M2M)** | ✅ SBR/Digipoort (SOAP+XBRL, PKIoverheid) | ✅ ERiC native lib (no REST) | ✅ Intervat-API (since 2025) |
| **File EC sales list / IC listing** | ✅ via SBR | ✅ ZM via ERiC | ❌ XSD upload, manual submit |
| **File OSS** | ❌ portal only | ❌ portal (BZSt) | ❌ portal |
| **VAT-ID validation** | VIES (EU) | ✅ BZSt REST (2025) | VIES (EU) |
| **Act on behalf — mechanism** | eHerkenning + ketenmachtiging | ELSTER cert (technical) | CSAM mandate |
| **Act on behalf — legal limit** | mandate required | ⚠️ **StBerG: Steuerberater only** to *prepare* | mandate required |
| **Company/KYB API** | ✅ KvK REST | ❌ no official API | 🟡 KBO open data |
| **Packaging EPR API** | n/a | 🟡 excerpt check only; reporting manual & non-delegable | ❌ none |
| **Auth = machine-to-machine?** | cert-based (PKIoverheid) | cert-based (ELSTER) | ❌ interactive CSAM; APIs use "recognized user" reg |

---

## 8. What this means for BEACON's architecture

1. **Be the system of record + technical transmitter, not the unlicensed adviser.**
   In DE especially, run filing as **self-service prep + ERiC transmission**, and
   **partner with a Steuerberater** for anything that crosses into preparation/
   advice. In NL/BE, obtain the **eHerkenning chain mandate** / **CSAM mandate**.
2. **Make Amazon SP-API (stock-by-country) a first-class integration** — it's what
   detects the OSS-breaks-here moment and turns the configurator's logic into live
   monitoring. Add Shopify/Stripe for non-Amazon sellers.
3. **Three filing back-ends, three certificate/identity models:** PKIoverheid
   (NL), ELSTER cert (DE), CSAM "recognized user" (BE). Budget for ERiC being a
   native library you must embed and ship, not a REST call.
4. **Treat OSS + EPR as prep-and-guide, not auto-file** — OSS submission is portal-
   bound in all three; EPR (LUCID/Fost Plus) is manual and, in DE, legally
   non-delegable. Productise these as guided workflows + document generation.
5. **Privacy by design:** key on company identifiers, **avoid BSN**, minimise buyer
   PII, mirror Amazon's restricted-data controls everywhere, DPA every processor.

---

## 9. Open items to verify before building
- NL **OSS via Digipoort** — no channel found; confirm with Belastingdienst/Logius.
- NL **BSN lawful basis** and **Wwft** status — NL counsel.
- DE **StBerG** boundary for fully-automated filing-as-a-service — DE tax counsel.
- DE **ERiC** sandbox specifics, **W-IdNr** rollout status (behind dev login).
- BE **Intervat/MyMinfin API** protocol, certs, sandbox (unpublished pre-registration);
  KBO web-service pricing (third-party reported).
- Time-sensitive: **EUDI Wallet** dates, **itsme/iDIN** migration, all API rate
  limits/pricing — re-verify at build time.

---

## Sources (selected)

**NL:** belastingdienst.nl (SBR / filing via accounting software; btw-id vs
omzetbelastingnummer); logius.nl (Digipoort WUS koppelvlak; nieuwe Digipoort);
sbr-nl.nl; odb.belastingdienst.nl (test facilities); eherkenning.nl
(chain authorisation); developers.kvk.nl; AP/UAVG BSN rulings (hekkelman.nl,
theprivacyofficers.nl).
**DE:** elster.de/elsterweb/infoseite/entwickler (ERiC); gesetze-im-internet.de
StBerG §§2–3, dejure.org §3, BFH II R 22/15 (haufe.de); bstbk.de
Vollmachtsdatenbank; bzst.de (USt-IdNr; Bestätigungsverfahren REST API newsletters
2025); verpackungsregister.org (XML upload; data reporting; status-check API);
unternehmensregister.de; info.mein-unternehmenskonto.de.
**BE:** finance.belgium.be / financien.belgium.be (Intervat; APIs MyMinfin/Intervat
2025; FORREG); csam.be / iamapps.belgium.be (CSAM/FAS); mandates-csam.minfin.fgov.be;
economie.fgov.be (KBO Open Data); ivcie.be (EPR).
**EU / data sources:** ec.europa.eu/taxation_customs/vies; vat-one-stop-shop.ec.europa.eu;
EC EU Digital Identity Wallet; developer-docs.amazon.com/sp-api (roles; tax & FBA
reports; RDT); shopify.dev; developer.woocommerce.com; docs.stripe.com;
e-justice.europa.eu (BRIS); idin.nl / itsme.
