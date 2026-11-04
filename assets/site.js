// Covers: play the hover clip (video or gif) on hover; on touch screens, play whichever cover
// is mostly on screen. Clips load only when first needed, so the page stays light.
(function () {
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var covers = Array.prototype.slice.call(document.querySelectorAll(".cover.has-motion"));
  if (!covers.length) return;

  function motionOf(cover) { return cover.querySelector(".motion"); }

  function load(m) {
    if (m.dataset.src) { m.src = m.dataset.src; delete m.dataset.src; }
  }

  function play(cover) {
    if (reduce) return;
    var m = motionOf(cover); load(m);
    cover.classList.add("playing");
    if (m.tagName === "VIDEO") { var p = m.play(); if (p && p.catch) p.catch(function () {}); }
  }

  function stop(cover) {
    var m = motionOf(cover);
    cover.classList.remove("playing");
    if (m.tagName === "VIDEO") m.pause();
  }

  var canHover = window.matchMedia("(hover: hover)").matches;
  if (canHover) {
    covers.forEach(function (c) {
      c.addEventListener("pointerenter", function () { play(c); });
      c.addEventListener("pointerleave", function () { stop(c); });
      c.addEventListener("focus", function () { play(c); });
      c.addEventListener("blur", function () { stop(c); });
    });
  } else if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { e.intersectionRatio >= 0.6 ? play(e.target) : stop(e.target); });
    }, { threshold: [0, 0.6, 1] });
    covers.forEach(function (c) { io.observe(c); });
  }
})();

// Email: written as text so it survives bots and link-blocking; click copies it.
(function () {
  document.querySelectorAll(".email").forEach(function (el) {
    el.style.cursor = "copy";
    el.title = "Click to copy";
    el.addEventListener("click", function () {
      var v = el.dataset.email;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(v).then(function () { el.textContent = "Copied"; setTimeout(function () { el.textContent = v; }, 1200); });
      }
    });
  });
})();
