/* ignasia Consulting — main.js */
(function () {
  'use strict';

  // Sticky header on scroll
  var header = document.getElementById('header');
  var onScroll = function () {
    if (!header) return;
    if (window.scrollY > 12) header.classList.add('scrolled');
    else header.classList.remove('scrolled');
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile nav toggle
  var toggle = document.getElementById('navToggle');
  var links = document.getElementById('navLinks');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        links.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Reveal on scroll — progressive enhancement with guaranteed fallback
  var reveals = document.querySelectorAll('.reveal');
  function revealAll() {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }
  if ('IntersectionObserver' in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0, rootMargin: '0px 0px 0px 0px' });
    reveals.forEach(function (el) { io.observe(el); });
    // Reveal anything already in viewport immediately
    requestAnimationFrame(function () {
      reveals.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.top < (window.innerHeight || 800)) el.classList.add('in');
      });
    });
    // Hard fallback: reveal everything after 2s regardless of observer
    setTimeout(revealAll, 2000);
    // Also reveal on full load (covers slow-rendering cases)
    window.addEventListener('load', function () { setTimeout(revealAll, 300); });
  } else {
    revealAll();
  }

  // Preselect service from ?service= query param
  try {
    var params = new URLSearchParams(window.location.search);
    var svc = params.get('service');
    if (svc) {
      var sel = document.getElementById('service');
      if (sel) {
        var opt = Array.prototype.find.call(sel.options, function (o) { return o.value === svc; });
        if (opt) opt.selected = true;
      }
    }
  } catch (e) {}

  // Contact form: FormSubmit (posts to info@ignasia.in, redirects to thank-you page)
  var form = document.getElementById('contactForm');
  if (form) {
    // FormSubmit _next needs an absolute URL — set it from current origin
    var next = document.getElementById('nextUrl');
    if (next) next.value = window.location.origin + window.location.pathname.replace(/contact\.html.*/, '') + 'thank-you.html';
    // Allow native form submission to FormSubmit; no JS interception needed.
    // First-ever submission triggers a one-time confirmation email to info@ignasia.in.
  }
})();
