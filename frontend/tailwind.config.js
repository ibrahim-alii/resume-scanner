/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cream: '#fff1db',
        peach: '#fbd9a2',
        text: '#000000',
      },
      borderRadius: {
        'retro': '8px',
        'box': '12px',
      },
      fontFamily: {
        'retro': ['Georgia', 'serif'],
      },
    },
  },
  plugins: [],
}
