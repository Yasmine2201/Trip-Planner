<script setup lang="ts">
import VisitForm from "~/components/VisitForm.vue";

definePageMeta({
  title: 'navigation.create_visit',
  layout: "navigation",
  requiresAuth: true,
});

const { t } = useI18n();

const route = useRoute();
const router = useRouter();
const tripId = Number(route.params.tripId);
</script>

<template>
  <PageTitle :name="t('navigation.create_visit')">
    <template v-slot:actions>
      <UButton @click="router.back()" icon="i-heroicons-arrow-uturn-left" class="mr-2" :title="t('misc.back')" color="gray" />
    </template>
  </PageTitle>
  <VisitForm :trip_id=tripId mode="create" />
</template>
