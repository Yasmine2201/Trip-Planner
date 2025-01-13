<script setup lang="ts">
import TripForm from "~/components/TripForm.vue";

definePageMeta({
  title: 'navigation.create_trip',
  layout: false,
});
const { t } = useI18n();
</script>

<template>
  <NuxtLayout name="auth">
    <template #title>
      {{ t('navigation.create_trip') }}
    </template>
    <TripForm mode="create" />
  </NuxtLayout>
</template>
