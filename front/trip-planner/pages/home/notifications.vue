<script setup lang="ts">

const t = useI18n();
definePageMeta({
title: 'notifications',
requiresAuth: true,
layout: 'navigation'
});

const { data: notifications } = await useApiFetch<Notification[]>('/notifications');

</script>

<template>
  <div>
    <UNotification
      v-for="notification in notifications"
      :key="notification"
      :title="notification.type"
      :description="notification.content"
       :timeout="0"
    />
  </div>
</template>
