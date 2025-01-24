<script setup lang="ts">

import type {Trip, Visit} from '~/types';
import type {AsyncData} from "#app";

definePageMeta({
  title: 'visits.list.title',
  requiresAuth: true,
  layout: 'navigation'
});

const route = useRoute();
const { t } = useI18n();
const toast = useToast();

const tripId = route.params.tripId as number;
const { data: trip }: AsyncData<Trip, any> = await useApiFetch<Trip>(`/trips/${tripId}`, {}, true);

// const toast = useToast();
//
const sort = ref({
  column: 'start_date',
  direction: 'desc'
})

const columns = computed(() => [
  {
    key: 'name',
    label: t('visits.fields.name'),
    sortable: true
  },
  {
    key: 'location.name',
    label: t('visits.fields.location_name'),
  },
  {
    key: 'start_date',
    label: t('visits.fields.start_date'),
    sortable: true,
    direction: 'desc' as const
  },
  {
    key: 'end_date',
    label: t('visits.fields.end_date'),
    sortable: true,
    direction: 'desc' as const
  },
  {
    key: 'actions',
  }
]);

const { data: rows, status }: AsyncData<Visit[], any> = await useApiFetch<Visit[]>(`/trips/${tripId}/visits`);
const computedRows = computed(() => rows.value ?? []);

const deleteVisit = async (visit: Visit) => {
  const { status } = await useApiFetch(`/trips/${visit.trip_id}/visits/${visit.visit_id}`, {
    method: 'DELETE'
  });

  if (status.value === "success") {
    rows.value = rows.value.filter((v) => v.visit_id !== visit.visit_id);
    toast.add({
      title: t('misc.delete'),
      description: t('misc.success'),
      icon: 'i-heroicons-check-badge',
      color: "green",
      timeout: 2000,
    });
  } else {
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
  <PageTitle :name="t('visits.list.title')">
    <template #actions>
      <UButton
          icon="i-entypo:add-to-list"
          size="sm"
          color="primary"
          variant="solid"
          :label="t('visits.list.add')"
          :to='`/home/trips/${tripId}/visits/create`'
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
    <template #name-data="{ row }">
      <NuxtLink :to="`/home/trips/${row.trip_id}/visits/${row.visit_id}`" class="font-semibold underline text-left">{{ row.name }}</NuxtLink>
    </template>

    <template #start_date-data="{ row }">
      {{ new Date(row.start_date).toLocaleString([], {dateStyle: 'full' ,timeStyle: 'short'}) }}
    </template>

    <template #end_date-data="{ row }">
      {{ new Date(row.end_date).toLocaleString([], {dateStyle: 'full' ,timeStyle: 'short'})  }}
    </template>

    <template #actions-data="{ row }">
      <div class="flex space-x-2">
        <UButton
            icon="i-heroicons-eye"
            size="xs"
            color="gray"
            square
            variant="solid"
            :to="`/home/trips/${row.trip_id}/visits/${row.visit_id}`"
        />
        <UButton
            icon="i-heroicons-pencil-square"
            size="xs"
            color="primary"
            square
            variant="solid"
            :to="`/home/trips/${row.trip_id}/visits/${row.visit_id}/edit`"
        />
        <UButton
            icon="i-heroicons-trash"
            size="xs"
            color="red"
            square
            variant="solid"
            @click="deleteVisit(row)"
        />
      </div>
    </template>
  </UTable>
</template>

<style scoped>

</style>