// plugins/api.client.js
export default defineNuxtPlugin(() => {
  const apiClient = $fetch.create({
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  return {
    provide: {
      api: apiClient,
    },
  };
});
