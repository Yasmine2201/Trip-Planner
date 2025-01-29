<script setup lang="ts">
import TripForm from "~/components/TripForm.vue";

definePageMeta({
  title: 'navigation.create_trip',
  layout: "navigation",
  requiresAuth: true,
});
const { t } = useI18n();
const router = useRouter();
</script>

<template>
  <PageTitle :name="t('navigation.create_trip')">
    <template v-slot:actions>
      <UButton @click="router.back()" icon="i-heroicons-arrow-uturn-left" class="mr-2" :title="t('misc.back')" color="gray" />
    </template>
  </PageTitle>
  <TripForm mode="create" />
</template>
