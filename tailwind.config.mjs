import daisyui from "daisyui";

module.exports = {
  content: [
    "./src/**/*.{astro,html,js,svelte,ts}",
    "./components/**/*.{astro,html,js,svelte,ts}",
  ],
  theme: {
    extend: {},
  },
  plugins: [daisyui],
};
