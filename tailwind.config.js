/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./blog/themes/terminal-theme/layouts/**/*.html",
    "./blog/static/js/**/*.js"
  ],
  safelist: Array.from({ length: 101 }, (_, value) => `w-[${value}%]`),
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: "#4db6ac",
        "deep-navy": "#060a14",
        "muted-teal": "#26a69a",
        "off-white": "#d1d5db",
        "terminal-bg": "#0a111a",
        "las-vegas-orange": "#d97706"
      },
      fontFamily: {
        display: [
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "sans-serif"
        ],
        mono: [
          "ui-monospace",
          "SFMono-Regular",
          "Menlo",
          "Monaco",
          "Consolas",
          "Liberation Mono",
          "Courier New",
          "monospace"
        ]
      }
    }
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography")
  ]
};
