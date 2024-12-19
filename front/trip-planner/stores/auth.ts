import type {User} from "~/types";

export const useAuthStore = defineStore('auth', {
  persist: true,

  state: () => ({
    user: null as User | null,
    isAuthenticated: false,
  }),

  actions: {
    async login(email: string, password: string): Promise<void> {
      const { $api } = useNuxtApp();

      const data = await $api('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });

      console.log(data);

      this.user = data.user;
      this.isAuthenticated = true;

      navigateTo('/home');
    },

    async logout() {
      const { $api } = useNuxtApp();

      try {
        await $api('/auth/logout', {method: 'POST'});

      } finally {
        this.user = null;
        this.isAuthenticated = false;
        navigateTo('/login');
      }
    },
  }
});