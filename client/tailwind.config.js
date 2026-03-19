/** @type {import("tailwindcss").Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#eef8ff",
          100: "#d9efff",
          500: "#1177cc",
          600: "#0a5ea6",
          700: "#084c85",
        },
        accent: "#f2a93b",
        surface: "#f7f4ed",
        ink: "#1f2937",
      },
      fontFamily: {
        sans: ["Be Vietnam Pro", "system-ui", "sans-serif"],
      },
      boxShadow: {
        panel: "0 18px 45px rgba(17, 119, 204, 0.12)",
      },
    },
  },
  plugins: [],
};