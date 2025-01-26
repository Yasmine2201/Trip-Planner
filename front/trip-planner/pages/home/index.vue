<script setup lang="ts">

import type { Trip } from '~/types';

definePageMeta({
  title: 'navigation.home',
  requiresAuth: true,
  layout: 'navigation'
});

const { t, locale } = useI18n();
const toast = useToast();

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
  const { status } = await useApiFetch(`/trips/${tripId}`, {
    method: 'DELETE'
  });
  if (status.value === 'success') {
    rows.value = rows.value.filter((trip) => trip.trip_id !== tripId);
    toast.add({
      title: t('misc.deletion'),
      description: t('misc.success'),
      icon: 'i-heroicons-check-badge',
      color: "green",
      timeout: 2000,
    });
  }
  else {
    toast.add({
      title: t('misc.deletion'),
      description: t('misc.error'),
      icon: 'i-heroicons-x-circle',
      color: "red",
      timeout: 2000,
    });
  }
}
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
  <UTable
      :columns
      :sort
      :rows="computedRows"
      :loading="status === 'pending'"
      :loading-state="{ icon: 'i-heroicons-arrow-path-20-solid', label: t('misc.loading') }"
      :progress="{ color: 'primary', animation: 'carousel' }"
      :empty-state="{ icon: 'i-heroicons-circle-stack-20-solid', label: t('misc.no-items') }"
  >
    <template #trip_name-data="{ row }">
      <NuxtLink :to="`/home/trips/${row.trip_id}`">{{ row.trip_name }}</NuxtLink>
    </template>

    <template #start_date-data="{ row }">
      {{ new Date(row.start_date).toLocaleDateString([locale], { dateStyle: 'full' }) }}
    </template>

    <template #end_date-data="{ row }">
      {{ new Date(row.end_date).toLocaleDateString([locale], { dateStyle: 'full' }) }}
    </template>

    <template #actions-data="{ row }">
      <div class="flex space-x-2">
        <UButton
            icon="i-heroicons-eye"
            size="xs"
            color="gray"
            square
            variant="solid"
            :to="`/home/trips/${row.trip_id}`"
        />
        <UButton
            icon="i-heroicons-pencil-square"
            size="xs"
            color="primary"
            square
            variant="solid"
            :to="`/home/trips/${row.trip_id}/edit`"
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