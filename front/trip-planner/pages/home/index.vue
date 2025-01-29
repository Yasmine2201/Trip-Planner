<script setup lang="ts">

import type { Trip } from '~/types';
import type {AsyncData} from "#app";

definePageMeta({
  title: 'navigation.home',
  requiresAuth: true,
  layout: 'navigation'
});

const { t, locale } = useI18n();

const { data: rows }: AsyncData<Trip[], any> = await useApiFetch<Trip[]>('/trips');

</script>

<template>
  <PageTitle :name="t('navigation.my-trips')">
    <template #actions>
      <UButton
          icon="i-entypo:add-to-list"
          size="sm"
          color="primary"
          variant="solid"
          :label="t('navigation.create_trip')"
          to="/home/trips/create"
      />
    </template>
  </PageTitle>
  <TripTable v-model:trips="rows" />
</template>

<style scoped>

</style>