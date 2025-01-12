<script setup lang="ts">

import {NotificationType} from "~/types/notifications";

const { t } = useI18n();
const router = useRouter();

const { data: notifications } = await useApiFetch<Notification[]>('/notifications');

const maxDisplayCount = 3;
const notificationItems = computed(() => [

    notifications.value.map(
        (notification: Notification) => ({
              class: notification.is_read ? 'text-gray-500 dark:text-gray-400' : 'text-primary-500 dark:text-primary-400 font-extrabold',
              label: notification.content,
              icon: NotificationType[notification.type as keyof typeof NotificationType],
              iconClass: notification.is_read ? 'text-gray-500 dark:text-gray-400' : 'text-primary-500 dark:text-primary-400',
              click: () => router.push({
                path: '/home/notifications/'
              })
            })
    )
]);
const displayedNotifications =  computed(() => {
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
  notifications.value.filter((notification : Notification) => !notification.is_read).length
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