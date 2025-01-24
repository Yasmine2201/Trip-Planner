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

const locationSelected = (location: Location) => {
  visitData.location = location;
  step.value = 1;
}

const goBack = () => {
  if (step.value === 1) {
    router.back();
  } else {
    step.value = 1;
  }
}

</script>

<template>
  <PageTitle :name="t('navigation.modify_visit')">
    <template v-slot:actions>
      <UButton @click="goBack()" icon="i-heroicons-arrow-uturn-left" class="mr-2" :title="t('misc.back')" color="gray" />
    </template>
  </PageTitle>
  <VisitLocationSelector v-if="step === 2" :tripId="tripId" @onLocationSelected="locationSelected"/>
  <VisitForm v-if="step === 1" mode="modify" :visitData="visitData" @changeLocation="step = 2" />
</template>
