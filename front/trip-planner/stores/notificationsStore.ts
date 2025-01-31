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

    send_notif(title: string, status: boolean, t: any) {
      const toast = useToast();
      if (status) {
        toast.add({
          title: title,
          description: t('misc.success'),
          icon: 'i-heroicons-check-badge',
          color: "green",
          timeout: 2000,
        });
      }
      else {
        toast.add({
          title: title,
          description: t('misc.error'),
          icon: 'i-heroicons-x-circle',
          color: "red",
          timeout: 2000,
        });
      }
    }
  },
});