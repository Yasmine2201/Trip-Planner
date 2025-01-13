<script setup lang="ts">
import TripForm from "~/components/TripForm.vue";
import type {Trip} from "~/types";

const { t } = useI18n();
const { $api } = useNuxtApp();

definePageMeta({
  title: 'navigation.modify_trip',
  layout: false,
});

const route = useRoute()
const tripId = route.params.trip_id;
console.log("tripId:", tripId);

// Charge les données du voyage depuis l'API
const { data: row, status } = await useApiFetch<Trip>(`/trips/${tripId}`);
const tripData = Object.assign({}, row.value ?? {});
console.log("tripData:", tripData, tripData.trip_name);

</script>

<template>
  <NuxtLayout name="auth">
    <template #title>
      {{ t('navigation.modify_trip') }}
    </template>
    <TripForm mode="modify" :tripData="tripData" />
  </NuxtLayout>
</template>
