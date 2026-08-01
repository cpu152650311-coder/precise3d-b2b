/* site.js — mobile nav toggle + dropdowns (ems-3dp.com) */
(function () {
  'use strict';

  /* 1. MOBILE HAMBURGER — toggles .open on .nav-main */
  var toggle = document.querySelector('.mobile-toggle');
  var nav = document.querySelector('.nav-main');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.classList.toggle('active', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    /* close menu when a link inside is clicked */
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        nav.classList.remove('open');
        toggle.classList.remove('active');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* 2. NAV DROPDOWNS — click toggles (touch friendly), close others, close on outside click */
  var dropdowns = document.querySelectorAll('.nav-dropdown');
  dropdowns.forEach(function (dd) {
    var trigger = dd.querySelector('.nav-dropdown-toggle');
    if (!trigger) return;
    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      var isOpen = dd.classList.contains('open');
      /* close all */
      dropdowns.forEach(function (d) { d.classList.remove('open'); });
      if (!isOpen) dd.classList.add('open');
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav-dropdown')) {
      dropdowns.forEach(function (d) { d.classList.remove('open'); });
    }
  });
})();
