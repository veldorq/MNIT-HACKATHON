/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#0f766e",
        secondary: "#14b8a6",
        accent: "#0ea5e9",
        paper: "#f8fafc",
      },
      boxShadow: {
        soft: "0 14px 40px -20px rgba(15, 23, 42, 0.35)",
      },
    },
  },
  plugins: [],
};
