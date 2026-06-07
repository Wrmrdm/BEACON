/* [BRAND] dashboard — demo data + interactions.
   Static, self-contained; no backend. */
(function () {
  "use strict";
  document.documentElement.classList.remove("no-js");

  /* ---------------- demo data ---------------- */
  // Germany registration sequence — company is ~halfway.
  var STEPS = [
    {
      n: "01", status: "done", title: "Onboarding completed",
      meta: "20 minutes",
      detail: "We captured Bloomwell's structure, catalogue, sales volumes, and where stock sits: a German fulfilment centre via Amazon FBA."
    },
    {
      n: "02", status: "done", title: "Tax position assessed",
      meta: "OSS + local DE",
      detail: "Stock held in Germany makes those sales domestic, so OSS can't cover them — a local German VAT registration is required. Belgian distance sales stay on OSS."
    },
    {
      n: "03", status: "done", title: "Documents collected",
      meta: "4 documents",
      detail: "KvK extract, Dutch VAT certificate, articles of association, and director ID — gathered and verified for the German filing."
    },
    {
      n: "04", status: "done", title: "Power of attorney signed",
      meta: "Finanzamt Kleve",
      detail: "Authorises [BRAND] to file and correspond with Finanzamt Kleve, the office that centrally handles Netherlands-resident businesses."
    },
    {
      n: "05", status: "active", title: "German VAT registration submitted",
      meta: "Submitted 18 days ago",
      detail: "The Fragebogen zur steuerlichen Erfassung is with Finanzamt Kleve. We're awaiting your Steuernummer — typically 4–8 weeks for a foreign applicant. We'll chase if it stalls."
    },
    {
      n: "06", status: "active", title: "ELSTER certificate setup",
      meta: "Awaiting your confirmation",
      detail: "Your organisational certificate for Germany's electronic filing portal is being created. We need you to confirm a few company details — see Needs you."
    },
    {
      n: "07", status: "pending", title: "USt-IdNr issued",
      meta: "After Steuernummer",
      detail: "Your EU VAT identification number is requested from the Bundeszentralamt für Steuern once the Steuernummer is granted. It's the number that goes on invoices and intra-EU trade."
    },
    {
      n: "08", status: "pending", title: "Verpackungsgesetz (LUCID) registration",
      meta: "Before first DE sale",
      detail: "Packaging law, separate from VAT, but a precondition for selling to German consumers. We register you in LUCID and arrange the dual-system contract. Without it, marketplaces can suspend listings."
    },
    {
      n: "09", status: "active", title: "German invoice & withdrawal templates",
      meta: "In legal review",
      detail: "A German-law invoice template with the correct VAT wording, plus a Widerrufsbelehrung (withdrawal notice). Drafted; awaiting your approval — see Needs you."
    },
    {
      n: "10", status: "pending", title: "First Umsatzsteuervoranmeldung",
      meta: "Scheduled",
      detail: "Your first advance VAT return via ELSTER, due the 10th of the following month. New registrations file monthly for the first two years; we prepare and submit each one."
    }
  ];

  var TASKS = [
    {
      title: "Confirm your ELSTER organisational details",
      meta: "Needed to finish step 6 · 2 min",
      cta: "Review"
    },
    {
      title: "Approve the German invoice template",
      meta: "Needed to finish step 9 · 3 min",
      cta: "Open"
    }
  ];

  var DEADLINES = [
    { title: "NL BTW return", sub: "Q2 2026 · Belastingdienst", due: "31 Jul", tone: "ok" },
    { title: "OSS return", sub: "Q2 2026 · covers BE distance sales", due: "31 Jul", tone: "ok" },
    { title: "German advance return", sub: "Begins once Steuernummer issued", due: "—", tone: "muted" }
  ];

  var FILINGS = [
    { name: "BTW return", market: "NL", period: "Q1 2026", due: "30 Apr 2026", status: "filed" },
    { name: "OSS return", market: "EU", period: "Q1 2026", due: "30 Apr 2026", status: "filed" },
    { name: "BTW return", market: "NL", period: "Q2 2026", due: "31 Jul 2026", status: "scheduled" },
    { name: "OSS return", market: "EU", period: "Q2 2026", due: "31 Jul 2026", status: "scheduled" },
    { name: "Umsatzsteuervoranmeldung", market: "DE", period: "Monthly (Y1–2)", due: "After registration", status: "pending" }
  ];

  var TEMPLATES = [
    { title: "German invoice (Rechnung)", sub: "VAT wording, mandatory fields, reverse-charge note", status: "active", tag: "In review" },
    { title: "Withdrawal notice (Widerrufsbelehrung)", sub: "Statutory 14-day consumer withdrawal", status: "active", tag: "In review" },
    { title: "OSS-compliant invoice", sub: "Cross-border B2C, destination VAT rates", status: "done", tag: "Ready" },
    { title: "Dutch invoice (factuur)", sub: "BTW-compliant, bilingual NL/EN", status: "done", tag: "Ready" }
  ];

  var FEED = [
    { tag: "DE", when: "2 days ago", title: "Packaging obligation flagged", body: "Selling to German consumers triggers a LUCID registration. Added to your sequence as step 8." },
    { tag: "EU", when: "1 week ago", title: "OSS threshold cleared", body: "Your cross-border B2C sales passed €10,000, so destination VAT now applies. OSS is handling it — no action needed." },
    { tag: "DE", when: "2 weeks ago", title: "Standard rate confirmed", body: "German standard VAT of 19% mapped to your skincare catalogue. No reduced-rate items detected." },
    { tag: "NL", when: "3 weeks ago", title: "Q1 returns filed", body: "Dutch BTW and OSS returns for Q1 2026 submitted and confirmed received." }
  ];

  /* ---------------- helpers ---------------- */
  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }
  var STATUS_LABEL = { done: "Done", active: "In progress", pending: "Pending", scheduled: "Scheduled" };

  /* ---------------- render: overview timeline (preview) ---------------- */
  var tl = document.querySelector("[data-timeline-preview]");
  if (tl) {
    STEPS.forEach(function (s) {
      var li = el("li", "db-tl db-tl--" + s.status);
      li.innerHTML =
        '<span class="db-tl__node" aria-hidden="true"></span>' +
        '<div class="db-tl__body">' +
          '<p class="db-tl__title">' + s.title + "</p>" +
          '<p class="db-tl__meta">' + STATUS_LABEL[s.status] + " · " + s.meta + "</p>" +
        "</div>";
      tl.appendChild(li);
    });
  }

  /* ---------------- render: tasks ---------------- */
  var tasksEl = document.querySelector("[data-tasks]");
  if (tasksEl) {
    TASKS.forEach(function (t) {
      var li = el("li", "db-task");
      li.innerHTML =
        '<div><p class="db-task__title">' + t.title + "</p>" +
        '<p class="db-task__meta">' + t.meta + "</p></div>" +
        '<button class="db-task__cta" type="button">' + t.cta + "</button>";
      tasksEl.appendChild(li);
    });
    tasksEl.addEventListener("click", function (e) {
      var btn = e.target.closest(".db-task__cta");
      if (!btn) return;
      btn.textContent = "Opened";
      btn.disabled = true;
    });
  }

  /* ---------------- render: deadlines ---------------- */
  var dlEl = document.querySelector("[data-deadlines]");
  if (dlEl) {
    DEADLINES.forEach(function (d) {
      var li = el("li", "db-deadline");
      li.innerHTML =
        '<div><p class="db-deadline__title">' + d.title + "</p>" +
        '<p class="db-deadline__sub">' + d.sub + "</p></div>" +
        '<span class="db-deadline__due db-deadline__due--' + d.tone + '">' + d.due + "</span>";
      dlEl.appendChild(li);
    });
  }

  /* ---------------- render: full steps (accordion) ---------------- */
  var stepsEl = document.querySelector("[data-steps]");
  if (stepsEl) {
    STEPS.forEach(function (s, i) {
      var item = el("div", "db-step db-step--" + s.status);
      var btnId = "step-btn-" + i, panelId = "step-panel-" + i;
      item.innerHTML =
        '<button class="db-step__head" id="' + btnId + '" aria-expanded="' +
          (s.status === "active" ? "true" : "false") +
          '" aria-controls="' + panelId + '" type="button">' +
          '<span class="db-step__num">' + s.n + "</span>" +
          '<span class="db-step__main">' +
            '<span class="db-step__title">' + s.title + "</span>" +
            '<span class="db-step__meta">' + s.meta + "</span>" +
          "</span>" +
          '<span class="db-pill db-pill--' + s.status + '">' + STATUS_LABEL[s.status] + "</span>" +
          '<span class="db-step__chev" aria-hidden="true">⌄</span>' +
        "</button>" +
        '<div class="db-step__panel" id="' + panelId + '" role="region" aria-labelledby="' + btnId +
          '"' + (s.status === "active" ? "" : " hidden") + '>' +
          "<p>" + s.detail + "</p>" +
        "</div>";
      stepsEl.appendChild(item);
    });
    stepsEl.addEventListener("click", function (e) {
      var head = e.target.closest(".db-step__head");
      if (!head) return;
      var panel = document.getElementById(head.getAttribute("aria-controls"));
      var open = head.getAttribute("aria-expanded") === "true";
      head.setAttribute("aria-expanded", String(!open));
      if (open) panel.hidden = true; else panel.hidden = false;
    });
  }

  /* ---------------- render: filings table ---------------- */
  var filingsEl = document.querySelector("[data-filings]");
  if (filingsEl) {
    FILINGS.forEach(function (f) {
      var tr = el("tr");
      tr.innerHTML =
        "<td>" + f.name + "</td>" +
        '<td><span class="db-tag">' + f.market + "</span></td>" +
        "<td>" + f.period + "</td>" +
        "<td>" + f.due + "</td>" +
        '<td><span class="db-pill db-pill--' + statusToPill(f.status) + '">' + cap(f.status) + "</span></td>";
      filingsEl.appendChild(tr);
    });
  }
  function statusToPill(s) {
    return s === "filed" ? "done" : s === "scheduled" ? "planned" : "pending";
  }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

  /* ---------------- render: templates ---------------- */
  var tplEl = document.querySelector("[data-templates]");
  if (tplEl) {
    TEMPLATES.forEach(function (t) {
      var card = el("article", "db-doc");
      card.innerHTML =
        '<div class="db-doc__icon" aria-hidden="true">¶</div>' +
        '<div class="db-doc__body"><p class="db-doc__title">' + t.title + "</p>" +
        '<p class="db-doc__sub">' + t.sub + "</p></div>" +
        '<span class="db-pill db-pill--' + t.status + '">' + t.tag + "</span>";
      tplEl.appendChild(card);
    });
  }

  /* ---------------- render: monitoring feed ---------------- */
  var feedEl = document.querySelector("[data-feed]");
  if (feedEl) {
    FEED.forEach(function (f) {
      var li = el("li", "db-feed__item");
      li.innerHTML =
        '<span class="db-feed__tag">' + f.tag + "</span>" +
        '<div class="db-feed__body"><div class="db-feed__row">' +
          '<p class="db-feed__title">' + f.title + "</p>" +
          '<span class="db-feed__when">' + f.when + "</span></div>" +
        '<p class="db-feed__text">' + f.body + "</p></div>";
      feedEl.appendChild(li);
    });
  }

  /* ---------------- panel switching ---------------- */
  var navBtns = Array.prototype.slice.call(document.querySelectorAll(".db-nav__item"));
  var panels = Array.prototype.slice.call(document.querySelectorAll("[data-panel-body]"));

  function show(name) {
    panels.forEach(function (p) {
      var match = p.getAttribute("data-panel-body") === name;
      p.classList.toggle("is-active", match);
      p.hidden = !match;
    });
    navBtns.forEach(function (b) {
      b.classList.toggle("is-active", b.getAttribute("data-panel") === name);
    });
    var main = document.getElementById("db-main");
    if (main) main.scrollTo ? main.scrollTo(0, 0) : (main.scrollTop = 0);
  }

  navBtns.forEach(function (b) {
    b.addEventListener("click", function () { show(b.getAttribute("data-panel")); });
  });
  document.addEventListener("click", function (e) {
    var go = e.target.closest("[data-goto]");
    if (go) show(go.getAttribute("data-goto"));
  });
})();
