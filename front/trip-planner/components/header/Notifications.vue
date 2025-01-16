<script setup lang="ts">

import {NotificationType} from "~/types/notifications";
import {ref} from "vue";

const { t } = useI18n();
const router = useRouter();

const { data: notificationsData } = await useApiFetch<Notification[]>(`/notifications`);
const  notifications = ref<Notification | null>(notificationsData.value || null);

const maxDisplayCount = 3;
const notificationItems = computed(() => [
    notifications.value ? notifications.value.map(
        (notification: Notification) => ({
              class: notification.is_read ? 'text-gray-500 dark:text-gray-400' : 'text-primary-500 dark:text-primary-400 font-extrabold',
              label: notification.content,
              icon: NotificationType[notification.type as keyof typeof NotificationType],
              iconClass: notification.is_read ? 'text-gray-500 dark:text-gray-400' : 'text-primary-500 dark:text-primary-400',
              click: () => router.push({
                path: '/home/notifications/' + notification.notification_id
              })
            })
    ) : []
]);
const displayedNotifications =  computed(() => {
  if (!notifications.value) {
    return [];
  }
  const limitedNotifications = notificationItems.value.flat().slice(0, maxDisplayCount);
  limitedNotifications.push({
    label: t('notifications.view-all'),
    class: 'text-primary-500 dark:text-primary-400 font-extrabold',
    icon: 'i-heroicons-eye',
    iconClass: 'text-primary-500 dark:text-primary-400',
    click: () => router.push('/home/notifications')
  });
  return [limitedNotifications];
});

const notificationCount = computed(() =>
  notifications.value ? notifications.value.filter((notification: Notification) => !notification.is_read).length : 0
);


</script>

<template>

  <UDropdown :items = "displayedNotifications" :popper="{ placement: 'bottom-start' }">
  <UButton icon="i-heroicons-bell" color="gray"/>
    <UChip :text ="notificationCount" size="2xl" :show="notificationItems.length > 0">
    </UChip>
  </UDropdown>
</template>
<style>

</style>