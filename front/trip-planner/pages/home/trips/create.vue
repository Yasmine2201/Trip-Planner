<script setup lang="ts">
import TripForm from "~/components/TripForm.vue";

definePageMeta({
  title: 'navigation.create_trip',
  layout: "navigation",
  requiresAuth: true,
});
const { t } = useI18n();
</script>

<template>
  <TripForm mode="create" />
</template>
