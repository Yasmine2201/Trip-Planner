export function useApiFetch<T>(url: string, options: RequestInit = {}) {
  const config = useRuntimeConfig();
  const auth = useAuthStore();

  return useFetch<T>(url, {
      baseURL: config.public.apiBaseUrl,
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
      ...options,
    onResponseError: async (error) => {
      if (error.response && error.response.status === 401) {
        return auth.refreshToken().then(() => {
          return useFetch<T>(url, {
            baseURL: config.public.apiBaseUrl,
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
              ...(options.headers || {}),
            },
            ...options
          });
        }).catch(() => {
          return Promise.reject('Token refresh failed');
        });
      }
    }
  });
}