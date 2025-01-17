<script setup lang="ts">
import {Notifications} from "~/types";

const {data: notifications} = await useApiFetch<Notifications[]>(`/notifications`);

const { t } = useI18n();

const deleteNotification = (id: number) => {
  notifications.value = notifications.value.filter((notification) => notification.notification_id !== id);
}

</script>

<template>
  <USlideover>
    <UCard
        class="flex flex-col flex-1"
        :ui="{
                body: { base: 'flex-1' },
                ring: '',
                divide: 'divide-y divide-gray-100 dark:divide-gray-800'
            }"
    >
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="text-base font-semibold leading-6 text-gray-900 dark:text-white">
            {{ t('notifications.title') }}
          </h3>
          <UButton
              color="gray"
              variant="ghost"
              icon="i-heroicons-x-mark-20-solid"
              class="-my-1"
              @click="$emit('close')"
          />
        </div>
      </template>

      <transition-group name="notification" tag="div" class="flex flex-col gap-2">
        <NotificationCard
            v-if="notifications && notifications.length > 0"
            v-for="(notification, index) in notifications"
            v-model="notifications[index]"
            @delete="deleteNotification"
            :id="`notification-${notification.notification_id}`"
            :can-close="false"
            @navigate="$emit('close')"
        />
        <p v-else>
          {{ t('notifications.no-notifications') }}
        </p>
      </transition-group>
    </UCard>
  </USlideover>
</template>
<style scoped>
</style>