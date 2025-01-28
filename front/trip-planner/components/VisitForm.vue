<script setup lang="ts">

import type {Visit, Trip} from "~/types";
import {createVisitSchema} from "~/schemas";
import LocationDetails from "~/components/LocationDetails.vue";
import type {AsyncData} from "#app";
import {getDateTimeString, getLater, getHoursFromTimestamp} from "~/utils/date";

const props = defineProps<{
  mode: string, // "create" ou "modify"
  visitData: Partial<Visit>, // Données de la visite
}>();

defineEmits<{
  changeLocation: () => void
}>();

const { t } = useI18n();
const { $api } = useNuxtApp();

const { data: trip }: AsyncData<Trip, any> = await useApiFetch(`trips/${props.visitData.trip_id}`);
const start = new Date(trip.value.start_date);
start.setHours(10);
let visitDuration = 2;
const end = getLater(start, 0, visitDuration);


// Fonction pour convertir une date timestampz en format YYYY-MM-DDTHH:MM
const formatDateForInput = (dateString: string | undefined): string => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toISOString().slice(0, 16); // Format YYYY-MM-DDTHH:MM
};

const state = reactive({
  name: props.visitData.name || '',
  start_date: formatDateForInput(props.visitData.start_date) || getDateTimeString(start),
  end_date: formatDateForInput(props.visitData.end_date) || getDateTimeString(end),
  trip_id: props.visitData.trip_id || null,
  location_id: props.visitData.location?.location_id || null,
});

function onStartChange(value: string) {
  state.end_date = getDateTimeString(getLater(value, 0, visitDuration));
}

function onEndChange(value: string) {
  const startTime = new Date(state.start_date).getTime();
  const endTime = new Date(value).getTime();
  if (endTime > startTime) {
    visitDuration = getHoursFromTimestamp(endTime - startTime);
  }
}

const verify_map_has_place = () => {
  return props.mode != "modify" || props.visitData.location?.location_id !== null;
}

const form = ref();
const formError = ref('');
const submitting = ref(false);

const onSubmit = async ({ data }: any) => {
  Object.assign(data, state);
  console.log("data submitted:", data);

  submitting.value = true;
  formError.value = '';

  const endpoint = `trips/${data.trip_id}` + (props.mode === "create" ? '/visits' : `/visits/${props.visitData.visit_id}`);
  const method = props.mode === "create" ? 'POST' : 'PUT';
  if (props.mode === "modify") {
    data.visit_id = props.visitData.visit_id;
  }

  try {
    const visit = await $api(endpoint, {
      method,
      body: JSON.stringify(data),
    });
    navigateTo(`/home/trips/${data.trip_id}/visits/${visit.visit_id}`);
  } catch (error) {
    formError.value = t('errors.unknown-error');
  }
  submitting.value = false;
};


</script>

<template>
  <UForm :schema="createVisitSchema" class="space-y-5" :state="state" @submit="onSubmit" ref="form"> <!-- :schema="createVisitSchema" -->
    <UFormGroup :label="t('form_visit.visit_name')" name="name" required>
      <UInput v-model="state.name" placeholder="Visit Name" />
      <template #error="{ error }">
        <span>{{ t(error) }}</span>
      </template>
    </UFormGroup>

    <div class="flex flex-col sm:flex-row gap-2">
      <div class="flex-1">
        <UFormGroup :label="t('form_visit.visit_start_date')" name="start_date" required>
          <UInput v-model="state.start_date" type="datetime-local" @change="onStartChange" />
          <template #error="{ error }">
            <span>{{ t(error) }}</span>
          </template>
        </UFormGroup>
      </div>
      <div class="flex-1">
        <UFormGroup :label="t('form_visit.visit_end_date')" name="end_date" required>
          <UInput v-model="state.end_date" type="datetime-local" @change="onEndChange" />
          <template #error="{ error }">
            <span>{{ t(error) }}</span>
          </template>
        </UFormGroup>
      </div>
    </div>

    <UCard>
      <template #header>
      <div class="w-full flex flex-row items-center justify-between">
        <span class="font-semibold text-xl">{{ t('form_visit.location') }}</span>
        <UButton @click="$emit('changeLocation')">
          {{ t('form_visit.change_location') }}
        </UButton>
      </div>
      </template>

      <LocationDetails v-if="visitData.location" :location="visitData.location" />
      <span v-else>{{ t('form_visit.no_location') }}</span>
    </UCard>

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
