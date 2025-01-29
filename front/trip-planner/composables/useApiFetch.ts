import type { UseFetchOptions } from "#app";

export const useApiFetch = <T>(url: string, options: UseFetchOptions<T> = {}, redirect: boolean = false) => {
  const config = useRuntimeConfig();
  const authStore = useAuthStore();

  return useFetch<T>(
    url,
    {
      baseURL: config.public.apiBaseUrl,
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
      onResponseError: async ({ response}) => {
        if (response.status === 404 && redirect) {
          navigateTo('/notfound');
        } else if (response.status === 401) {
          await authStore.clearUser();
          navigateTo('/login');
        } else if (response.status === 403) {
          navigateTo('/forbidden');
        }
      },
      ...options as any,
    });
}