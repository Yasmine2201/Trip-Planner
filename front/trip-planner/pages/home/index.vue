<script setup lang="ts">

import type { Trip } from '~/types';

definePageMeta({
  title: 'navigation.home',
  requiresAuth: true,
  layout: 'navigation'
});

const { t } = useI18n();

const sort = ref({
  column: 'start_date',
  direction: 'desc'
})

const columns = computed(() => [
  {
    key: 'trip_name',
    label: t('trips.name'),
    sortable: true
  },
  {
    key: 'start_date',
    label: t('trips.start'),
    sortable: true,
    direction: 'desc' as const
  },
  {
    key: 'end_date',
    label: t('trips.end'),
    sortable: true,
    direction: 'desc' as const
  },
  {
    key: 'actions',
  }
]);

const { data: rows, status } = await useApiFetch<Trip[]>('/trips');
const computedRows = computed(() => rows.value ?? []);

const deleteTrip = async (tripId: number) => {
  // TODO: Implement delete trip functionality
  console.log('Deleting trip with id:', tripId);
}
</script>

<template>
  <h1 class="font-semibold text-primary-600 dark:text-primary-400">{{ t('trips.triplist-title') }}</h1>

  <UTable
      :columns
      :sort
      :rows="computedRows"
      :loading="status === 'pending'"
      :loading-state="{ icon: 'i-heroicons-arrow-path-20-solid', label: t('misc.loading') }"
      :progress="{ color: 'primary', animation: 'carousel' }"
      :empty-state="{ icon: 'i-heroicons-circle-stack-20-solid', label: 'misc.no-items' }"
  >
    <template #trip_name-data="{ row }">
      <NuxtLink :to="`/home/trip/${row.trip_id}`">{{ row.trip_name }}</NuxtLink>
    </template>

    <template #start_date-data="{ row }">
      {{ new Date(row.start_date).toLocaleDateString() }}
    </template>

    <template #end_date-data="{ row }">
      {{ new Date(row.end_date).toLocaleDateString() }}
    </template>

    <template #actions-data="{ row }">
      <div class="flex space-x-2">
        <UButton
            icon="i-heroicons-eye"
            size="xs"
            color="gray"
            square
            variant="solid"
            :to="`/home/trip/${row.trip_id}`"
        />
        <UButton
            icon="i-heroicons-pencil-square"
            size="xs"
            color="primary"
            square
            variant="solid"
            :to="`/home/trip/${row.trip_id}/edit`"
        />
        <UButton
            icon="i-heroicons-trash"
            size="xs"
            color="red"
            square
            variant="solid"
            @click="deleteTrip(row.trip_id)"
        />
      </div>
    </template>
  </UTable>
</template>


<style scoped>

</style>