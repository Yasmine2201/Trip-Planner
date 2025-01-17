<script setup lang="ts">
import TripForm from "~/components/TripForm.vue";
import type {Trip} from "~/types";

const { t } = useI18n();

definePageMeta({
  title: 'navigation.modify_trip',
  layout: 'navigation',
  requiresAuth: true,
});

const route = useRoute()
const tripId = route.params.tripId;
console.log("tripId:", tripId);

// Charge les données du voyage depuis l'API
const { data: row, status } = await useApiFetch<Trip>(`/trips/${tripId}`);
const tripData = Object.assign({}, row.value ?? {});
console.log("tripData:", tripData, tripData.trip_name);

</script>

<template>
  <PageTitle :name="t('modify_trip.title')" />
  <TripForm mode="modify" :tripData="tripData" />
</template>
