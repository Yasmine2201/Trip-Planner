<script lang="ts" setup>

import {Notifications} from "~/types/notifications";
import {NotificationsList} from "#components";


const {t, locale} = useI18n();
const route = useRoute();
const toast = useToast();
const slideover = useSlideover();
const notificationsStore = useNotificationsStore();

const notifications = ref<Notifications[]>(await notificationsStore.fetchNotifications());

const getNotificationText = (content: string) => {
  const notification = JSON.parse(content);
  for (const key in notification.data) {
    if (isValidDate(notification.data[key]) && typeof(notification.data[key]) === 'string') {
      let date = new Date(notification.data[key]);
      notification.data[key] = date.toLocaleString([locale.value], { dateStyle: 'short', timeStyle: 'short' });
    }
  }

  return t(notification.message, notification.data);
}

watch(route, async () => {
  console.debug("updating notifications");
  let oldNotifications = notificationsStore.notifications;

  notifications.value = await notificationsStore.fetchNotifications();

  for (let notification of notifications.value) {
    if (!oldNotifications?.find((oldNotification) => oldNotification.notification_id === notification.notification_id) && !notification.is_read) {
      const notificationProps = getNotificationProps(JSON.parse(notification.content), t);

      toast.add({
        title: getNotificationText(notification.content),
        icon: notificationProps[notification.type].icon,
        color: 'primary',
        timeout: 2000
      });
    }
  }
});

const openNotificationSlideOver = () => {
  slideover.open(NotificationsList, {
    onClose: slideover.close
  });
};

const notificationsCount = computed(() => {
  console.debug("updating notifications count");
  return notifications?.value.filter((notification: Notification) => !notification.is_read).length ?? 0;
});

</script>

<template>
    <UChip :show="notificationsCount > 0" :text="notificationsCount" size="2xl">
      <UButton color="gray" icon="i-heroicons-bell" @click="openNotificationSlideOver"/>
    </UChip>
</template>
<style>

</style>