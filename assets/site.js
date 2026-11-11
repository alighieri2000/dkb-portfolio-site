// Covers: play the hover clip (video or gif) on hover; on touch screens, play whichever cover
// is mostly on screen. Clips load only when first needed, so the page stays light.
(function () {
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var covers = Array.prototype.slice.call(document.querySelectorAll(".cover.has-motion"));
  if (!covers.length || reduce) return;

  function motionOf(cover) { return cover.querySelector(".motion"); }

  // Move the clip's address into place the first time it is needed. `preload` says whether the
  // browser should start fetching right away ("auto") or wait for play() ("none").
  function load(m, preload) {
    if (m.dataset.src) {
      m.src = m.dataset.src; delete m.dataset.src;
      if (m.tagName === "VIDEO") {
        m.muted = true; m.playsInline = true;
        if (preload) m.preload = preload;
        m.load();
      }
    }
  }

  // Covers whose video refused to start on its own (iPhone Low Power Mode, "Auto-Play Video
  // Previews" turned off, some Android data savers). The first tap on the page counts as
  // permission, so they are retried then.
  var blocked = [];

  function play(cover) {
    var m = motionOf(cover); load(m);
    cover.dataset.wants = "1";
    if (m.tagName !== "VIDEO") { cover.classList.add("playing"); return; }
    var p = m.play();
    if (p && p.catch) p.catch(function () { if (blocked.indexOf(cover) < 0) blocked.push(cover); });
  }

  function stop(cover) {
    var m = motionOf(cover);
    delete cover.dataset.wants;
    cover.classList.remove("playing");
    if (m.tagName === "VIDEO") m.pause();
  }

  covers.forEach(function (c) {
    var m = motionOf(c);
    if (m.tagName !== "VIDEO") return;
    // Reveal the clip only once frames are actually arriving, so a slow or refused video never
    // hides the still behind an empty box.
    m.addEventListener("playing", function () { if (c.dataset.wants) c.classList.add("playing"); });
    m.addEventListener("waiting", function () { c.classList.remove("playing"); });
    m.addEventListener("pause", function () { c.classList.remove("playing"); });
  });

  function retryBlocked() {
    if (!blocked.length) return;
    blocked.splice(0).forEach(function (c) { if (c.dataset.wants) play(c); });
  }
  ["touchend", "pointerup", "keydown"].forEach(function (ev) {
    document.addEventListener(ev, retryBlocked, { passive: true });
  });

  var canHover = window.matchMedia("(hover: hover)").matches;
  if (canHover) {
    covers.forEach(function (c) {
      c.addEventListener("pointerenter", function () { play(c); });
      c.addEventListener("pointerleave", function () { stop(c); });
      c.addEventListener("focus", function () { play(c); });
      c.addEventListener("blur", function () { stop(c); });
    });
  } else if ("IntersectionObserver" in window) {
    // Start fetching a clip while its cover is still a screen away, so it is buffered by the time
    // it scrolls into view; play at 60% visible, pause when it leaves.
    var warm = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { load(motionOf(e.target), "auto"); warm.unobserve(e.target); }
      });
    }, { rootMargin: "100% 0px" });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { e.intersectionRatio >= 0.6 ? play(e.target) : stop(e.target); });
    }, { threshold: [0, 0.6, 1] });
    covers.forEach(function (c) { warm.observe(c); io.observe(c); });
  }
})();

// Clips inside a write-up: play silently while on screen, pause when scrolled past. The
// controls stay available for sound or scrubbing, and a clip someone pauses by hand stays paused.
(function () {
  var clips = Array.prototype.slice.call(document.querySelectorAll(".gallery video.clip"));
  if (!clips.length || !("IntersectionObserver" in window)) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  clips.forEach(function (v) {
    v.muted = true; v.playsInline = true;
    v.addEventListener("pause", function () { if (!v.dataset.auto) v.dataset.manual = "1"; delete v.dataset.auto; });
    v.addEventListener("play", function () { if (!v.dataset.auto) delete v.dataset.manual; delete v.dataset.auto; });
  });

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      var v = e.target;
      if (v.dataset.manual) return;
      if (e.intersectionRatio >= 0.5) {
        if (v.paused) { v.dataset.auto = "1"; var p = v.play(); if (p && p.catch) p.catch(function () { delete v.dataset.auto; }); }
      } else if (!v.paused) {
        v.dataset.auto = "1"; v.pause();
      }
    });
  }, { threshold: [0, 0.5, 1] });
  clips.forEach(function (v) { io.observe(v); });
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
