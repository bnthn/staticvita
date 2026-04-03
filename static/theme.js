(function () {
  var KEY = "theme";
  var root = document.documentElement;

  function apply(theme) {
    root.dataset.theme = theme;
    var btn = document.getElementById("theme-toggle");
    if (btn) {
      btn.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
    }
  }

  function readStored() {
    try {
      var v = localStorage.getItem(KEY);
      if (v === "light" || v === "dark") return v;
    } catch (_) {}
    return null;
  }

  var theme = readStored();
  if (theme === null) {
    theme = window.matchMedia("(prefers-color-scheme: light)").matches
      ? "light"
      : "dark";
  }
  apply(theme);

  document.getElementById("theme-toggle")?.addEventListener("click", function () {
    theme = root.dataset.theme === "dark" ? "light" : "dark";
    try {
      localStorage.setItem(KEY, theme);
    } catch (_) {}
    apply(theme);
  });
})();
