<script setup lang="ts">
const { t } = useI18n();

// The logic for fetching the notifications will be added later
const notificationItems = computed(() => [
  // [{
  //   label : t('notifications.none'),
  // }]
]);
</script>

<template>
  <UDropdown :items="notificationItems" :popper="{ placement: 'bottom-start' }">
    <UChip :text ="notificationItems.length" size="2xl" :show="notificationItems.length > 0">
      <UButton icon="i-heroicons-bell" color="gray"/>
    </UChip>
  </UDropdown>
</template>

<style scoped>

</style>