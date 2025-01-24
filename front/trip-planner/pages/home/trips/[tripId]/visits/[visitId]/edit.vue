<script setup lang="ts">
import VisitForm from "~/components/VisitForm.vue";
import type { Visit } from "~/types";

const { t } = useI18n();

definePageMeta({
  title: 'navigation.modify_visit',
  layout: 'navigation',
  requiresAuth: true,
});

const route = useRoute();
const router = useRouter();
const visitId = Number(route.params.visitId);
const tripId = Number(route.params.tripId);

// Charge les données de la visite depuis l'API
const { data: row, status, error } = await useApiFetch<Visit>(`/visits/${visitId}`);
if (status.value === 'error' && error.value.statusCode === 404) {
  router.push('/notfound');
}
const visitData = Object.assign({}, row.value ?? {});
</script>

<template>
  <PageTitle :name="t('navigation.modify_visit')">
    <template v-slot:actions>
      <UButton @click="router.back()" icon="i-heroicons-arrow-uturn-left" class="mr-2" :title="t('misc.back')" color="gray" />
    </template>
  </PageTitle>
  <VisitForm mode="modify" :visitData="visitData" :trip_id="tripId" />
</template>
