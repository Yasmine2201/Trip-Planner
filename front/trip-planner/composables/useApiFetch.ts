export function useApiFetch<T>(url: string, options: RequestInit = {}): ReturnType<typeof useFetch<T>> {
  const config = useRuntimeConfig();
  const authStore = useAuthStore();

  return useFetch<T>(url,
    {
      baseURL: config.public.apiBaseUrl,
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
      ...options,
      onResponseError: async ({ response}) => {
        if (response.status === 404) {
          navigateTo('/not-found');
        } else if (response.status === 401) {
          await authStore.clearUser();
          navigateTo('/login');
        }
      }
    });
}