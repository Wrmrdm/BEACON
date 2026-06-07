/* BEACON — interactions:
   - sticky nav state
   - subtle scroll reveals
   - live obligations configurator
   Progressive enhancement: without JS, all content is visible. */
(function () {
  "use strict";

  document.documentElement.classList.remove("no-js");

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------- sticky nav ---------------- */
  var nav = document.querySelector("[data-nav]");
  if (nav) {
    var onScroll = function () {
      if (window.scrollY > 8) nav.setAttribute("data-scrolled", "");
      else nav.removeAttribute("data-scrolled");
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------------- scroll reveals ---------------- */
  var revealables = Array.prototype.slice.call(
    document.querySelectorAll("[data-reveal]")
  );

  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealables.forEach(function (el) { el.classList.add("is-visible"); });
  } else {
    var observer = new IntersectionObserver(
      function (entries, obs) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var el = entry.target;
          var siblings = Array.prototype.slice.call(
            el.parentNode.querySelectorAll(":scope > [data-reveal]")
          );
          var idx = siblings.indexOf(el);
          el.style.transitionDelay = (idx > 0 ? Math.min(idx, 6) * 70 : 0) + "ms";
          el.classList.add("is-visible");
          obs.unobserve(el);
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.12 }
    );
    revealables.forEach(function (el) { observer.observe(el); });
  }

  /* ---------------- obligations configurator ---------------- */
  var cfg = document.querySelector("[data-configurator]");
  if (!cfg) return;

  var listEl = cfg.querySelector("[data-cfg-list]");
  var countEl = cfg.querySelector("[data-cfg-count]");

  function read(name) {
    return Array.prototype.slice
      .call(cfg.querySelectorAll('input[name="' + name + '"]'))
      .filter(function (i) { return i.checked; })
      .map(function (i) { return i.value; });
  }

  function compute() {
    var markets = read("market");                 // ["BE","DE"]
    var stock = read("stock");                     // ["DE",...]
    var over = read("threshold")[0] === "over";
    var has = function (arr, v) { return arr.indexOf(v) !== -1; };
    var items = [];

    // NL baseline — always
    items.push({
      tag: "NL", region: "nl",
      title: "Dutch BTW returns continue",
      detail: "Your home registration with the Belastingdienst stays the base for everything — quarterly returns, unchanged."
    });

    if (!markets.length) {
      items.push({
        tag: "—", region: "muted",
        title: "Select a market to see what it triggers",
        detail: "Add Belgium or Germany above to map the obligations that follow."
      });
      return items;
    }

    // EU distance-selling threshold + OSS
    if (over) {
      items.push({
        tag: "EU", region: "eu",
        title: "Charge destination-country VAT",
        detail: "You've passed the EU-wide €10,000 distance-selling threshold, so each customer's country rate applies — not the Dutch rate."
      });
      items.push({
        tag: "EU", region: "eu",
        title: "Register for the One-Stop-Shop (OSS) in NL",
        detail: "One quarterly OSS return through the Belastingdienst covers cross-border B2C distance sales, instead of a return in every country."
      });
    } else {
      items.push({
        tag: "EU", region: "eu",
        title: "Keep charging Dutch VAT for now",
        detail: "Under the €10,000 threshold you can still apply NL VAT to cross-border B2C sales. We watch the line and flag it before you cross it."
      });
    }

    // GERMANY
    if (has(markets, "DE")) {
      if (has(stock, "DE")) {
        items.push({
          tag: "DE", region: "de",
          title: "Local German VAT registration required",
          detail: "You hold stock in Germany, so OSS doesn't cover those sales. Register with Finanzamt Kleve, which handles NL-resident businesses."
        });
        items.push({
          tag: "DE", region: "de",
          title: "USt-IdNr and ELSTER setup",
          detail: "Your German VAT ID via the Bundeszentralamt für Steuern, plus an ELSTER certificate so returns can be filed electronically."
        });
        items.push({
          tag: "DE", region: "de",
          title: "Monthly advance VAT returns",
          detail: "Umsatzsteuervoranmeldung via ELSTER — monthly for the first two years — plus an annual return and EC sales lists for any B2B."
        });
      } else if (over) {
        items.push({
          tag: "DE", region: "de",
          title: "German sales reported via OSS",
          detail: "While you hold no stock in Germany, distance sales there go through your NL OSS return — no separate German VAT registration needed yet."
        });
      }
      items.push({
        tag: "DE", region: "de",
        title: "Verpackungsgesetz (LUCID) registration",
        detail: "Required before selling packaged goods to German consumers, independent of VAT. Without it, marketplaces can suspend your listings."
      });
    }

    // BELGIUM
    if (has(markets, "BE")) {
      if (has(stock, "BE")) {
        items.push({
          tag: "BE", region: "be",
          title: "Local Belgian VAT (BTW/TVA) registration",
          detail: "Stock in Belgium means a local registration; OSS won't cover sales shipped from Belgian inventory."
        });
        items.push({
          tag: "BE", region: "be",
          title: "Periodic returns via Intervat",
          detail: "Belgium's filing portal — monthly or quarterly depending on turnover. We prepare and submit each one."
        });
      } else if (over) {
        items.push({
          tag: "BE", region: "be",
          title: "Belgian sales reported via OSS",
          detail: "With no stock in Belgium, distance sales there are covered by your NL OSS return — no Belgian registration required yet."
        });
      }
    }

    return items;
  }

  function render() {
    var items = compute();
    listEl.innerHTML = "";
    items.forEach(function (it, i) {
      var li = document.createElement("li");
      li.className = "cfg-item cfg-item--" + it.region;
      li.style.setProperty("--i", i);
      li.innerHTML =
        '<span class="cfg-item__tag">' + it.tag + "</span>" +
        '<div class="cfg-item__body">' +
        '<p class="cfg-item__title">' + it.title + "</p>" +
        '<p class="cfg-item__detail">' + it.detail + "</p>" +
        "</div>";
      listEl.appendChild(li);
    });
    var n = items.length;
    countEl.textContent = n + (n === 1 ? " item" : " items");
  }

  cfg.addEventListener("change", render);
  render();
})();
