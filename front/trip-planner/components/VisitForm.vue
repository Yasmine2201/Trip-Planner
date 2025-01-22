<script setup lang="ts">
import PlaceSelector from "~/components/PlaceSelector.vue";
import type { FormSubmitEvent } from "#ui/types";
import type {Trip, Location} from "~/types";
import {createVisitSchema} from "~/schemas";

const props = defineProps({
  mode: { type: String, required: true }, // "create" ou "modify"
  visitData: { type: Object, default: () => ({}) }, // Données de la visite en mode "modify"
  trip_id: { type: String, required: true },
});
console.log("tripId:", props.trip_id);
const { t } = useI18n();
const { $api } = useNuxtApp();

const state = reactive({
  name: props.visitData.name || '',
  start_date: props.visitData.start_date || '',
  end_date: props.visitData.end_date || '',
  place: props.visitData.place || null,
  trip_id: props.trip_id || null,
});

// Charge les données du voyage depuis l'API
const { data: row, status, error } = await useApiFetch<Trip>(`/trips/${state.trip_id}`);
if (status.value === 'error' && error.value?.statusCode === 404) {
  console.log("WARNING : trip not found");
}

const tripData: Trip = Object.assign({}, row.value ?? {}) as Trip;
const getTripLocation = () => {
  return {
    latitude: tripData.latitude || 0,
    longitude: tripData.longitude || 0,
    radius: tripData.radius || 0,
  };
};


// placeSelector est de type Location
const placeSelector = ref(null);
const form = ref();
const formError = ref('');
const submitting = ref(false);

const updatePlace = () => {
  state.place = placeSelector.value?.selectedPlace || state.place;
};

const onSubmit = async ({ data }: any) => {
  updatePlace();
  Object.assign(data, state);
  console.log("data submitted:", data);

  submitting.value = true;
  formError.value = '';

  const endpoint = props.mode === "create" ? '/visits' : `/visits/${props.visitData.visit_id}`;
  const method = props.mode === "create" ? 'POST' : 'PUT';
  if (props.mode === "modify") {
    data.visit_id = props.visitData.visit_id;
  }

  try {
    await $api(endpoint, {
      method,
      body: JSON.stringify(data),
    });
    navigateTo('/home');
  } catch (error) {
    formError.value = t('errors.unknown-error');
  }
  submitting.value = false;
};
</script>

<template>
  <UForm :schema="createVisitSchema" class="space-y-5" :state="state" @submit="onSubmit" ref="form">
    <UFormGroup :label="t('form_visit.visit_name')" name="name" required>
      <UInput v-model="state.name" placeholder="Visit Name" />
      <template #error="{ error }">
        <span>{{ t(error) }}</span>
      </template>
    </UFormGroup>

    <UFormGroup :label="t('form_visit.visit_start_date')" name="start_date" required>
      <UInput v-model="state.start_date" type="datetime-local" />
      <template #error="{ error }">
        <span>{{ t(error) }}</span>
      </template>
    </UFormGroup>

    <UFormGroup :label="t('form_visit.visit_end_date')" name="end_date" required>
      <UInput v-model="state.end_date" type="datetime-local" />
      <template #error="{ error }">
        <span>{{ t(error) }}</span>
      </template>
    </UFormGroup>

    <PlaceSelector ref="placeSelector" class="w-full" :placeData="state.place" :filterData="getTripLocation()"/>

    <UAlert
        v-if="formError !== ''"
        class="mb-4 w-full"
        color="red"
        variant="outline"
        :title="t('errors.oops')"
        :description="t(formError)"
    />

    <div class="flex justify-center">
      <UButton type="submit" color="primary" class="w-1/2 flex justify-center" :loading="submitting">
        {{ props.mode === "create" ? t('form_visit.visit_create_button') : t('form_visit.visit_modify_button') }}
      </UButton>
    </div>
  </UForm>
</template>
