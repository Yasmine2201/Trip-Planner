<script setup lang="ts">

import type {Location, Trip, Visit} from "~/types";
import {createVisitSchema} from "~/schemas";

const props = defineProps<{
  mode: string, // "create" ou "modify"
  visitData: Partial<Visit>, // Données de la visite
}>();
const { t } = useI18n();
const { $api } = useNuxtApp();

// Fonction pour convertir une date timestampz en format YYYY-MM-DDTHH:MM
const formatDateForInput = (dateString: string | undefined): string => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toISOString().slice(0, 16); // Format YYYY-MM-DDTHH:MM
};

const state = reactive({
  name: props.visitData.name || '',
  start_date: formatDateForInput(props.visitData.start_date) || '',
  end_date: formatDateForInput(props.visitData.end_date) || '',
  trip_id: props.visitData.trip_id || null,
  location_id: props.visitData.location?.location_id || null,
});

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
    await $api(endpoint, {
      method,
      body: JSON.stringify(data),
    });
    navigateTo(`/home/trips/${data.trip_id}/visits`);
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

    <MapViewer v-if="verify_map_has_place()" :lat="visitData.location?.latitude ?? 0" :lon="visitData.location?.longitude ?? 0"/>

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
