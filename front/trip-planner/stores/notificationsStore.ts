import type {Notifications} from "~/types";

export const useNotificationsStore = defineStore('notifications', {
  persist: true,

  state: () => ({
    notifications: [] as Notifications[],
  }),

  actions: {
    async fetchNotifications(): Promise<Notifications[]> {
      const { $api } = useNuxtApp();

      try {
        this.notifications = await $api('/notifications');
        return this.notifications;
      } catch (error) {
        console.error(error);
        throw error;
      }
    },
  },
});