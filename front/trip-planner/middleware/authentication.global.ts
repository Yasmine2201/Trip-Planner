export default defineNuxtRouteMiddleware(to => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth !== true && !authStore.isAuthenticated) {
    return;
  }

  if (!authStore.isAuthenticated) {
    return navigateTo('/login');
  }
});