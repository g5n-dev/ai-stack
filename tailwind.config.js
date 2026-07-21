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
        "primary-dim": "#4db6ac",
        "deep-navy": "#060a14",
        "muted-teal": "#26a69a",
        "off-white": "#d1d5db",
        "terminal-bg": "#0a111a",
        "las-vegas-orange": "#d97706",
        error: "#ef4444",
        "glitch-pink": "#ec4899",
        "surface-dark": "#111f1f",
        "surface-border": "#203a3a"
      },
      backgroundImage: {
        "grid-pattern":
          "linear-gradient(to right, #152626 1px, transparent 1px), linear-gradient(to bottom, #152626 1px, transparent 1px)"
      },
      animation: {
        "glitch-1": "glitch-anim-1 2.5s infinite linear alternate-reverse",
        "glitch-2": "glitch-anim-2 3s infinite linear alternate-reverse",
        "pulse-fast": "pulse 0.5s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        scanline: "scanline 8s linear infinite",
        shake: "shake 0.5s cubic-bezier(.36,.07,.19,.97) both"
      },
      keyframes: {
        "glitch-anim-1": {
          "0%": { clipPath: "inset(20% 0 80% 0)" },
          "20%": { clipPath: "inset(60% 0 10% 0)" },
          "40%": { clipPath: "inset(40% 0 50% 0)" },
          "60%": { clipPath: "inset(80% 0 5% 0)" },
          "80%": { clipPath: "inset(10% 0 70% 0)" },
          "100%": { clipPath: "inset(30% 0 50% 0)" }
        },
        "glitch-anim-2": {
          "0%": { clipPath: "inset(10% 0 60% 0)" },
          "20%": { clipPath: "inset(80% 0 5% 0)" },
          "40%": { clipPath: "inset(40% 0 10% 0)" },
          "60%": { clipPath: "inset(10% 0 80% 0)" },
          "80%": { clipPath: "inset(50% 0 20% 0)" },
          "100%": { clipPath: "inset(30% 0 40% 0)" }
        },
        scanline: {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100%)" }
        },
        shake: {
          "10%, 90%": { transform: "translate3d(-1px, 0, 0)" },
          "20%, 80%": { transform: "translate3d(2px, 0, 0)" },
          "30%, 50%, 70%": { transform: "translate3d(-4px, 0, 0)" },
          "40%, 60%": { transform: "translate3d(4px, 0, 0)" }
        }
      },
      fontFamily: {
        display: ["var(--site-font-sans)"],
        mono: ["var(--site-font-mono)"]
      }
    }
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography")
  ]
};
