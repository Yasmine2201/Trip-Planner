<script setup lang="ts">

import {NotificationType} from "~/types/notifications";
import { useI18n } from 'vue-i18n';
import {ref} from "vue";

const {t} = useI18n();
const router = useRouter();
definePageMeta({
title: 'notifications',
requiresAuth: true,
layout: 'navigation'
});
const { data: notificationsData } = await useApiFetch<Notification[]>(`/notifications`);
const  notifications = ref<Notification | null>(notificationsData.value || null);

const handleReadNotification = async (notificationId: number) => {
   if (!notifications.value) {
      return;
    }
  try {
   await useApiFetch(`/notifications/${notificationId}`, {
      method: 'PUT',
    });
    notifications.value = notifications.value.map(notification => {
      if (notification.notification_id === notificationId) {
        notification.is_read = true;
      }
      return notification;
    })
  }
  catch (error) {
    console.error('Error marking notification read :', error);
  }
}

const handleDeleteNotification = async (notificationId: number) => {
  if (!notifications.value) {
    return;
  }

  try{
    await useApiFetch(`/notifications/${notificationId}`, {
    method: 'DELETE'
  });
  notifications.value = notifications.value.filter(notification => notification.notification_id !== notificationId);
  }

  catch (error) {
    console.error('Error deleting notification :', error);
  }

}

</script>

<template>
  <div>
    <transition-group name="notification" tag="div">
      <UNotification v-if = "notifications"
      v-for="notification in notifications"
      :key="notification"
      :title="notification.type"
      :close-button="false"

      :actions="[
          {
          label: notification.is_read ? t('notifications.read') : t('notifications.mark-as-read'),
          icon: notification.is_read ? 'i-heroicons-check' : 'mdi:hand-pointing-up' ,
          color: notification.is_read ? 'gray': 'primary',
          click: () => handleReadNotification(notification.notification_id)
          },
          {
            label: t('core.enter'),
            icon: 'memory:arrow-up-right',
            click: () => router.push('/home')

          },
          {
            label: t('core.delete'),
            icon: 'i-heroicons-trash',
            click: () => handleDeleteNotification(notification.notification_id)
          }
      ]"
      :icon = "NotificationType[notification.type as keyof typeof NotificationType]"
      :color="notification.is_read ? 'gray' : 'primary'"
      :description="notification.content"
      :timeout="0"
    />
      <p v-else>
        {{ t('notifications.no-notifications') }}
      </p>

       </transition-group>
  </div>

</template>
<style scoped>
.notification-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}
.notification-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
