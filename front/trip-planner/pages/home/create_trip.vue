<script setup lang="ts">

import LocationSelector from "~/components/LocationSelector.vue";
import type { FormSubmitEvent } from "#ui/types";
import type { CreateTripDto } from '~/schemas';
import { createTripSchema } from '~/schemas';

const { t } = useI18n();
const { $api } = useNuxtApp();

definePageMeta({
  title: 'navigation.create_trip',
  layout: false
});

const state = reactive({
  tripName: '',
  latitude: -1,
  longitude: -1,
  radius: -1,
  start_date: '',
  end_date: '',
});

const locationSelector = ref(null);
const form = ref();
const formError = ref('');
const submitting = ref(false);

const updateLocation = () => {
  state.latitude = locationSelector.value.selectedLat ? locationSelector.value.selectedLat : state.latitude;
  state.longitude = locationSelector.value.selectedLng ? locationSelector.value.selectedLng : state.longitude;
  state.radius = locationSelector.value.radius ? locationSelector.value.radius : state.radius;
};

onMounted(() => {
  // On récupère la référence du composant LocationSelector
  updateLocation();
});

const onSubmit = async ({ data }: FormSubmitEvent<CreateTripDto>) => {
  updateLocation();
  // update les data avec le nouvel état
  Object.assign(data, state);
  console.log("New trip data: ", data);
  submitting.value = true;
  formError.value = '';


  try {
    await $api('/trips', {
      method: 'POST',
      body: JSON.stringify(
          {
            trip_name: data.tripName,
            latitude: data.latitude,
            longitude: data.longitude,
            radius: data.radius,
            start_date: data.start_date,
            end_date: data.end_date,
          },
      ),
    });
    navigateTo('/home');
  } catch (error) {
    formError.value = 'errors.unknown-error';
  }
  submitting.value = false;

};
</script>

<template>
  <NuxtLayout name="auth">
    <template #title>
      {{ t('navigation.create_trip') }}
    </template>

    <UForm :schema="createTripSchema" :state="state" class="space-y-5" @submit="onSubmit" ref="form">
      <UFormGroup
          :label="t('create_trip.trip_name')"
          name="tripName"
          required
      >
        <UInput
            v-model="state.tripName"
            placeholder="MyTrip"
        />

        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>

      <UFormGroup
          :label="t('create_trip.trip_start_date')"
          name="start_date"
          required
      >
        <UInput
            v-model="state.start_date"
            type="date"
        />
        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>

      <UFormGroup
          :label="t('create_trip.trip_end_date')"
          name="end_date"
          required
      >
        <UInput
            v-model="state.end_date"
            type="date"
        />
        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>

      <LocationSelector ref="locationSelector" class="w-full h-96"/>

      <UAlert
          class="mb-4 w-full"
          v-if="formError !== ''"
          color="red"
          variant="outline"
          :title="t('errors.oops')"
          :description="t(formError)"
      />

      <div class="flex justify-center">
        <UButton
            type="submit"
            color="primary"
            class="w-1/2 flex justify-center"
            :loading="submitting"
        >
          {{ t('create_trip.trip_create_button') }}
        </UButton>
      </div>
    </UForm>
  </NuxtLayout>
</template>
