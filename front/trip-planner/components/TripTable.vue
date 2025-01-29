<script setup lang="ts">

import type { Trip } from '~/types';
import type {ModelRef} from "vue";

definePageMeta({
  title: 'navigation.home',
  requiresAuth: true,
  layout: 'navigation'
});

const trips: ModelRef<Trip[]> = defineModel<Trip[]>('trips', {
  required: true
}) as ModelRef<Trip[]>;

const tripRows = computed(() => trips.value.map((trip) => ({
  ...trip,
  isOwner: trip.owner_id === authStore.user.id
})));

const { t, locale } = useI18n();
const toast = useToast();
const authStore = useAuthStore();

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

const deleteTrip = async (tripId: number) => {
  const { status } = await useApiFetch(`/trips/${tripId}`, {
    method: 'DELETE'
  });
  if (status.value === 'success') {
    trips.value = trips.value.filter((trip) => trip.trip_id !== tripId);
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

const leaveTrip = async (tripId: number) => {
  const { status } = await useApiFetch(`/trips/${tripId}/leave`, {
    method: 'POST'
  });
  if (status.value === 'success') {
    trips.value = trips.value.filter((trip) => trip.trip_id !== tripId);
    toast.add({
      title: t('trips.leave'),
      description: t('misc.success'),
      icon: 'i-heroicons-check-badge',
      color: "green",
      timeout: 2000,
    });
  }
  else {
    toast.add({
      title: t('trips.leave'),
      description: t('misc.error'),
      icon: 'i-heroicons-x-circle',
      color: "red",
      timeout: 2000,
    });
  }
}
</script>

<template>
  <UTable
      :columns
      :sort
      :rows="tripRows"
      :loading-state="{ icon: 'i-heroicons-arrow-path-20-solid', label: t('misc.loading') }"
      :progress="{ color: 'primary', animation: 'carousel' }"
      :empty-state="{ icon: 'i-heroicons-circle-stack-20-solid', label: t('misc.no-items') }"
  >
    <template #trip_name-data="{ row }">
      <NuxtLink :to="`/home/trips/${row.trip_id}`" class="font-semibold underline text-left">{{ row.trip_name }}</NuxtLink>
      <UBadge v-if="row.isOwner" color="primary" size="xs" variant="soft" class="ml-6">{{ t('share.owner') }}</UBadge>
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
            v-if="row.isOwner"
            icon="i-heroicons-trash"
            size="xs"
            color="red"
            square
            variant="solid"
            @click="deleteTrip(row.trip_id)"
        />
        <UButton
          v-if="!row.isOwner"
          icon="i-heroicons-arrow-right-start-on-rectangle-20-solid"
          size="xs"
          color="red"
          square
          variant="solid"
          @click="leaveTrip(row.trip_id)" />
      </div>
    </template>
  </UTable>
</template>

<style scoped>

</style>