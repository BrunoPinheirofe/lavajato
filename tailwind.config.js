/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // 💡 IMPORTANTE: Inclua todos os templates Jinja2
    "./templates/**/*.html", // Escaneia todos os arquivos .html dentro de 'templates/'
    "./*.py",                 // Se você usa classes do Tailwind em strings no Python (raro, mas bom incluir)
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}