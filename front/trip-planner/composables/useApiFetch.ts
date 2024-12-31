export function useApiFetch<T>(url: string, options: RequestInit = {}): ReturnType<useFetch<T>> {
  const config = useRuntimeConfig();
  return useFetch<T>(url, {
      baseURL: config.public.apiBaseUrl,
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
      ...options,
  });
}