/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'pixel-black': '#000000',
        'pixel-white': '#FFFFFF',
        'pixel-gray': '#808080',
        'pixel-light-gray': '#C0C0C0',
      },
      fontFamily: {
        'pixel': ['"Press Start 2P"', 'monospace'],
        'mono': ['monospace'],
      },
    },
  },
  plugins: [],
}

