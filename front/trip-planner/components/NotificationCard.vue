<script setup lang="ts">
import {Notifications} from "~/types/notifications";
import getNotificationProps from "~/utils/getNotificationProps";

const {t, locale} = useI18n();
const router = useRouter();

const notification = defineModel<Notifications>({
  required: true,
});

interface Props {
  canClose: boolean
}

const props = withDefaults(defineProps<Props>(), {
  canClose: false
});

const emit = defineEmits<{
  delete: [id: number],
  navigate,
}>();

const closeButton = props.canClose ? {
  icon: 'i-heroicons-x-mark-20-solid',
  color: 'gray',
  variant: 'link',
  padded: false
} : null;

const content = JSON.parse(notification.value.content);

const getNotificationText = (content: string) => {
  const notification = JSON.parse(content);
  for (const key in notification.data) {
    if (isValidDate(notification.data[key]) && typeof(notification.data[key]) === 'string') {
      let date = new Date(notification.data[key]);
      notification.data[key] = date.toLocaleString([locale.value], {dateStyle: 'long', timeStyle: 'short'});
    }
  }

  return t(notification.message, notification.data);
}

const getActions = () => {
  return [
    {
      label: notification.value.is_read ? t('notifications.read') : t('notifications.mark-as-read'),
      icon: notification.value.is_read ? 'i-heroicons-check' : 'mdi:hand-pointing-up' ,
      color: notification.value.is_read ? 'gray': 'primary',
      click: handleReadNotification
    },
    {
      label: t('misc.see'),
      icon: 'memory:arrow-up-right',
      click: () => { router.push(typeProps[notification.value.type].link()); emit('navigate'); }
    },
    {
      label: t('misc.delete'),
      icon: 'i-heroicons-trash',
      click: handleDeleteNotification
    }
  ]
}

const typeProps = getNotificationProps(content, t);

const handleReadNotification = async () => {
  try {
    await useApiFetch(`/notifications/${notification.value.notification_id}`, {
      method: 'PUT',
    });
    notification.value.is_read = true;
  } catch (error) {
    console.error('Error marking notification read :', error);
  }
}

const handleDeleteNotification = async () => {
  try {
    await useApiFetch(`/notifications/${notification.value.notification_id}`, {
      method: 'DELETE'
    });

    emit('delete', notification.value.notification_id);
  } catch (error) {
    console.error('Error deleting notification :', error);
  }
}
</script>

<template>
  <UNotification
                 :key="notification"
                 :actions="getActions(notification)"
                 :close-button
                 :color="notification.is_read ? 'gray' : 'primary'"
                 :description="getNotificationText(notification.content)"
                 :icon="typeProps[notification.type].icon"
                 :timeout="0"
                 :title="typeProps[notification.type].label"
  />
</template>

<style scoped>

</style>