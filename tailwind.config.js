/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html",],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')({
      charts: true,
  }),
  // ... other plugins
  ],
}

module.exports = {

  content: [
      "./node_modules/flowbite/**/*.js"
  ]

}

