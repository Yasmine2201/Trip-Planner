// plugins/api.client.js
export default defineNuxtPlugin(() => {
  const authStore = useAuthStore();

  const apiClient = $fetch.create({
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    credentials: "include",
    headers: {
      'Content-Type': 'application/json',
    },
    onResponseError: async ({ response}) => {
      if (response.status === 404) {
        navigateTo('/not-found');
      } else if (response.status === 401) {
        await authStore.clearUser();
        navigateTo('/login');
      }
    }
  });

  return {
    provide: {
      api: apiClient,
    },
  };
});
