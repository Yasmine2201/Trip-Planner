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
const { data: row, status, error } = await useApiFetch<Visit>(`/trips/${tripId.toString()}/visits/${visitId.toString()}`, {}, true);

const visitData = Object.assign({}, row.value ?? {});

const step = ref(1);
const pageTitle = computed(() => {
  return `${t('navigation.modify_visit')} (${step.value}) : ${step.value === 1 ? t('locations.titles.select-location') : t('visits.title.finalize')}`;
});
const locationSelected = (location: Location) => {
  visitData.location = location;
  step.value = 2;
}

</script>

<template>
  <PageTitle :name="pageTitle">
    <template v-slot:actions>
      <UButton @click="router.back()" icon="i-heroicons-arrow-uturn-left" class="mr-2" :title="t('misc.back')" color="gray" />
    </template>
  </PageTitle>
  <VisitLocationSelector v-if="step === 1" :tripId="tripId" :selectedLocation="visitData.location" @onLocationSelected="locationSelected"/>
  <UButton v-if="step === 2" @click="step = 1" class="mr-2 mb-4" color="orange" icon="i-heroicons-arrow-uturn-left"> {{ t('modify_visit.return_to_step1') }} </UButton>
  <VisitForm v-if="step === 2" mode="modify" :visitData="visitData" />
</template>
