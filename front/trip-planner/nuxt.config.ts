// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  ssr: false,

  modules: ['@nuxt/ui', '@nuxtjs/i18n', '@pinia/nuxt'],

  i18n: {
    locales: [
      {
        code: 'en',
        name: 'English',
        file: 'en.json',
        icon: 'circle-flags:us'
      },
      {
        code: 'fr',
        name: 'Français',
        file: 'fr.json',
        icon: 'circle-flags:fr'
      }
    ],

    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'i18n_redirected',
      redirectOn: 'root'
    },

    strategy: 'no_prefix'
  },

  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.API_BASE_URL || 'http://127.0.0.1:8000/api',
    },
  }
})