import type { User } from "~/types";

export const useAuthStore = defineStore('auth', {
  persist: true,

  state: () => ({
    user: null as User,
    isAuthenticated: false,
  }),

  actions: {
    async login(email: string, password: string): Promise<boolean> {
      const { $api } = useNuxtApp();

      try {
        const data = await $api('/auth/login', {
          method: 'POST',
          body: JSON.stringify({ email, password }),
        });
        this.user = {
          id: data.user_id,
          alias: data.alias,
          firstname: data.first_name,
          lastname: data.last_name,
          email: data.email,
          birthdate: data.birthdate,
          avatarImage: data.profile_picture?.url,
          description: data.description,
          languages: data.languages
        }
        this.isAuthenticated = true;
        navigateTo('/home');
        return true;

      } catch (error) {
        return false;
      }
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

    async refreshUser() {
      const { $api } = useNuxtApp();

      if (!this.isAuthenticated) {
        return;
      }

      try {
        const data = await $api('/me');
        this.user = {
          id: data.user_id,
          alias: data.alias,
          firstname: data.first_name,
          lastname: data.last_name,
          email: data.email,
          birthdate: data.birthdate,
          avatarImage: data.profile_picture?.url,
          description: data.description,
          languages: data.languages
        }
        this.isAuthenticated = true;
      } catch (error) {
        this.user = null;
        this.isAuthenticated = false;
        navigateTo('/login');
      }
    }
  }
});