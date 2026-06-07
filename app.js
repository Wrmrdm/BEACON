/* [BRAND] — subtle scroll reveals + sticky nav state.
   Progressive enhancement only: without JS, all content is visible. */
(function () {
  "use strict";

  // Signal that JS is available (CSS uses .no-js as a fallback safeguard).
  document.documentElement.classList.remove("no-js");

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- sticky nav: add a state once the page has scrolled ---- */
  var nav = document.querySelector("[data-nav]");
  if (nav) {
    var onScroll = function () {
      if (window.scrollY > 8) {
        nav.setAttribute("data-scrolled", "");
      } else {
        nav.removeAttribute("data-scrolled");
      }
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---- scroll reveals ---- */
  var revealables = Array.prototype.slice.call(
    document.querySelectorAll("[data-reveal]")
  );

  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealables.forEach(function (el) { el.classList.add("is-visible"); });
    return;
  }

  var observer = new IntersectionObserver(
    function (entries, obs) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        // gentle stagger for sibling groups
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
})();
