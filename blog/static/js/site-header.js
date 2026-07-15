(() => {
  "use strict";

  const clock = document.querySelector("[data-site-clock]");
  const latency = document.querySelector("[data-site-latency]");
  const header = document.querySelector("[data-site-header]");
  const menuButton = document.querySelector("[data-site-menu-button]");
  const navigation = document.getElementById("site-header-navigation");

  if (header && menuButton && navigation && menuButton.dataset.siteMenuReady !== "true") {
    menuButton.dataset.siteMenuReady = "true";

    const closeMenu = ({ restoreFocus = false } = {}) => {
      header.dataset.siteMenuOpen = "false";
      menuButton.setAttribute("aria-expanded", "false");
      menuButton.setAttribute("aria-label", "打开主导航");
      if (restoreFocus) menuButton.focus();
    };

    const openMenu = () => {
      header.dataset.siteMenuOpen = "true";
      menuButton.setAttribute("aria-expanded", "true");
      menuButton.setAttribute("aria-label", "关闭主导航");
      navigation.querySelector("a")?.focus();
    };

    menuButton.addEventListener("click", () => {
      if (header.dataset.siteMenuOpen === "true") closeMenu();
      else openMenu();
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && header.dataset.siteMenuOpen === "true") {
        closeMenu({ restoreFocus: true });
      }
    });

    document.addEventListener("click", (event) => {
      if (header.dataset.siteMenuOpen === "true" && !header.contains(event.target)) {
        closeMenu();
      }
    });

    window.matchMedia("(min-width: 901px)").addEventListener("change", (event) => {
      if (event.matches) closeMenu();
    });
  }

  if (latency) {
    const navigationTiming = performance.getEntriesByType("navigation")[0];
    const requestLatency = navigationTiming
      ? Math.max(0, Math.round(navigationTiming.responseStart - navigationTiming.requestStart))
      : null;
    latency.textContent = Number.isFinite(requestLatency) ? `${requestLatency}ms` : "—";
  }

  if (!clock || clock.dataset.siteClockReady === "true") return;

  clock.dataset.siteClockReady = "true";
  let timer = 0;

  function renderTime() {
    const now = new Date();
    const pad = (value) => String(value).padStart(2, "0");
    const display = [
      now.getFullYear(),
      pad(now.getMonth() + 1),
      pad(now.getDate()),
    ].join("-") + ` ${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;

    clock.dateTime = now.toISOString();
    clock.textContent = display;
  }

  function stopClock() {
    if (!timer) return;
    window.clearInterval(timer);
    timer = 0;
  }

  function startClock() {
    stopClock();
    renderTime();
    if (!document.hidden) timer = window.setInterval(renderTime, 1000);
  }

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) stopClock();
    else startClock();
  });

  startClock();
})();
