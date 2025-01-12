<script setup lang="ts">
import {NotificationType} from "~/types/notifications";
import { useI18n } from 'vue-i18n';
import {ref} from "vue";

definePageMeta({
title: 'trip_home.trip_details',
requiresAuth: true,
layout: 'navigation'
});

const { t } = useI18n();
const route = useRoute();
const router = useRouter();

const notificationId = ref(route.params.notificationId);
const { data: notificationData } = await useApiFetch<Notification[]>(`/notifications/${notificationId.value}`);
const  selectedNotification = ref<Notification | null>(notificationData.value || null);

const handleReadNotification = async (notificationId: number) => {
  const response = await useApiFetch(`/notifications/${notificationId}`, {
    method: 'PUT',
  });
  selectedNotification.value = response.data.value;
}

const handleDeleteNotification = async (notificationId: number) => {
  try {
    await useApiFetch(`/notifications/${notificationId}`, {
    method: 'DELETE'
  });

  selectedNotification.value = null;

  }

  catch (error) {
    console.error('Error deleting notification :', error);
  }

}
</script>

<template>
  <div>
    <transition-group name="notification" tag="div">
      <UNotification
        v-if="selectedNotification"
        :title="selectedNotification.type"
        :close-button="false"
        :icon="NotificationType[selectedNotification.type as keyof typeof NotificationType]"
        :color="selectedNotification.is_read ? 'gray' : 'primary'"
        :description="selectedNotification.content"
        :timeout="0"
        :actions="[
            {
            label: selectedNotification.is_read ? t('notifications.read') : t('notifications.mark-as-read'),
            icon: selectedNotification.is_read ? 'i-heroicons-check' : 'mdi:hand-pointing-up',
            color: selectedNotification.is_read ? 'gray' : 'primary',
            click: () => handleReadNotification(selectedNotification.notification_id)
            },
            {
              label: t('core.enter'),
              icon: 'memory:arrow-up-right',
              click: () => router.push('/home')
            },
            {
              label: t('core.delete'),
              icon: 'i-heroicons-trash',
              click: () => handleDeleteNotification(selectedNotification.notification_id)
            }
        ]"
      />
      <div v-else>
        {{ t('notifications.deleted') }}
      </div>
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