import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vite.dev/config/
export default defineConfig({
  base: process.env.NODE_ENV === 'production' ? '/boh/' : '/',
  plugins: [svelte()],
  server: {
    cors: {
      origin: process.env.NODE_ENV === "production" ? "https://araujosemacento.github.io*" : "http://localhost/*",
      methods: ['GET', 'POST', 'PUT'],
      allowedHeaders: ['Content-Type', 'Authorization']
    }
  }
})
