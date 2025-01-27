<script setup lang="ts">

import { useI18n } from "vue-i18n";
import { useNuxtApp } from "#app";
import {createTripSchema} from "~/schemas";

const props = defineProps({
  mode: { type: String, required: true }, // "create" ou "modify"
  tripData: { type: Object, default: () => ({}) }, // Données du voyage en mode "modify"
});

const { t } = useI18n();
const { $api } = useNuxtApp();

const state = reactive({
  trip_name: props.tripData.trip_name || '',
  latitude: props.tripData.latitude || null,
  longitude: props.tripData.longitude || null,
  radius: props.tripData.radius || null,
  start_date: props.tripData.start_date || '',
  end_date: props.tripData.end_date || '',
});

const locationSelector = ref(null);
const form = ref();
const formError = ref('');
const submitting = ref(false);

const updateLocation = () => {
  state.latitude = locationSelector.value?.selectedLat || state.latitude;
  state.longitude = locationSelector.value?.selectedLng || state.longitude;
  state.radius = locationSelector.value?.radius || state.radius;
};

const getLocation = () => {
  return {
    latitude: state.latitude,
    longitude: state.longitude,
    radius: state.radius,
  };
};

onMounted(() => {
  updateLocation();
});

// Type ModifyTripDto inapplicable here
const onSubmit = async ({ data }: any) => {
  updateLocation();
  Object.assign(data, state);
  console.log("data submitted:", data);

  submitting.value = true;
  formError.value = '';

  const endpoint = props.mode === "create" ? '/trips' : `/trips/${props.tripData.trip_id}`;
  const method = props.mode === "create" ? 'POST' : 'PUT';
  if (props.mode === "modify") {
    data.trip_id = props.tripData.trip_id;
  }

  try {
    await $api(endpoint, {
      method,
      body: JSON.stringify(data),
    });
    navigateTo('/home');
  } catch (error) {
    formError.value = 'errors.unknown-error';
  }
  submitting.value = false;
};
</script>

<template>
  <UForm :schema="createTripSchema" :state="state" class="space-y-5" @submit="onSubmit" ref="form">
    <UFormGroup :label="t('create_trip.trip_name')" name="trip_name" required>
      <UInput v-model="state.trip_name" :placeholder="t('create_trip.trip_name_placeholder')" />
      <template #error="{ error }">
        <span>{{ t(error) }}</span>
      </template>
    </UFormGroup>

    <UFormGroup :label="t('create_trip.trip_start_date')" name="start_date" required>
      <UInput v-model="state.start_date" type="date" />
      <template #error="{ error }">
        <span>{{ t(error) }}</span>
      </template>
    </UFormGroup>

    <UFormGroup :label="t('create_trip.trip_end_date')" name="end_date" required>
      <UInput v-model="state.end_date" type="date" />
      <template #error="{ error }">
        <span>{{ t(error) }}</span>
      </template>
    </UFormGroup>

    <TripLocationSelector ref="locationSelector" class="w-full h-96" :locationData="getLocation()" />

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
        {{ props.mode === "create" ? t('create_trip.trip_create_button') : t('modify_trip.trip_modify_button') }}
      </UButton>
    </div>
  </UForm>
</template>
