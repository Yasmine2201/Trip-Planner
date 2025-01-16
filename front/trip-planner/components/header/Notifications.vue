<script lang="ts" setup>

import {NotificationType, Notifications} from "~/types/notifications";
import {NotificationsList} from "#components";

const {t} = useI18n();
const route = useRoute();
const toast = useToast();
const slideover = useSlideover();

const {data: notificationsData} = await useApiFetch<Notifications[]>(`/notifications`);
const notifications = reactive<Notifications | null>(notificationsData.value || null);

const getNotificationText = (content: string) => {
  const notification = JSON.parse(content);
  return t(notification.message, notification.data);
}

watch(route, async () => {
  let oldNotifications = notifications.value;

  const {data: notificationsData} = await useApiFetch<Notifications[]>(`/notifications`);
  notifications.value = notificationsData.value;

  for (let notification of notifications.value) {
    if (!oldNotifications?.find((oldNotification) => oldNotification.notification_id === notification.notification_id) && !notification.is_read) {
      console.log('new notification', notification);
      toast.add({
        title: getNotificationText(notification.content),
        icon: NotificationType[notification.type as keyof typeof NotificationType],
        color: 'primary',
        duration: 2000
      });
    }
  }
});

const openNotificationSlideOver = () => {
  slideover.open(NotificationsList, {
    onClose: slideover.close
  });
};

</script>

<template>
    <UChip :show="notifications?.length > 0" :text="notifications.value?.filter((notification: Notification) => !notification.is_read).length ?? 0" size="2xl">
      <UButton color="gray" icon="i-heroicons-bell" @click="openNotificationSlideOver"/>
    </UChip>
</template>
<style>

</style>