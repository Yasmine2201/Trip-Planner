<script setup lang="ts">

import type {Trip, TripInvitation} from '~/types';

definePageMeta({
  title: 'navigation.tripInvitations',
  requiresAuth: true,
  layout: 'navigation'
});

const { t } = useI18n();
const toast = useToast();

const sort = ref({
  column: 'trip_name',
  direction: 'desc'
})

const columns = computed(() => [
  {
    key: 'trip_name',
    label: t('trips.name'),
    sortable: true
  },
  {
    key: 'user_email',
    label: t('profile.email'),
    sortable: true
  },
  {
    key: 'actions',
  }
]);

const { data: rows, status } = await useApiFetch<TripInvitation[]>('/trips/invitations');
const computedRows = computed(() => rows.value ?? []);

function send_notif(title: String, status: Boolean) {
  if (status) {
    toast.add({
      title: title,
      description: t('misc.success'),
      icon: 'i-heroicons-check-badge',
      color: "green",
      timeout: 2000,
    });
  }
  else {
    toast.add({
      title: title,
      description: t('misc.error'),
      icon: 'i-heroicons-x-circle',
      color: "red",
      timeout: 2000,
    });
  }
}

const AcceptTripInvitation = async (tripInvitationId: number) => {
  const { status } = await useApiFetch(`/trips/invitations/${tripInvitationId}`, {
    method: 'POST'
  });
  if (status === 'success') {
    rows.value = rows.value.filter((trip_invit) => trip_invit.tripInvitationId !== tripInvitationId);
  }
  send_notif(t('misc.deletion'), status === 'success')
}

const RefuseTripInvitation = async (tripInvitationId: number) => {
  const { status } = await useApiFetch(`/trips/invitations/${tripInvitationId}`, {
    method: 'DELETE'
  });
  if (status === 'success') {
    rows.value = rows.value.filter((trip_invit) => trip_invit.tripInvitationId !== tripInvitationId);
  }
  send_notif(t('misc.deletion'), status === 'success')
}
</script>

<template>
  <PageTitle :name="t('navigation.tripInvitations')">
    <template #actions>
      <UButton
          icon="i-entypo:add-to-list"
          size="sm"
          color="primary"
          variant="solid"
          :label="t('navigation.create_trip_invitation')"
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
      <NuxtLink :to="`/home/trips/${row.trip.trip_id}`">{{ row.trip.trip_name }}</NuxtLink>
    </template>

    <template #user_name-data="{ row }">{{ row.user.email }}</template>


    <template #actions-data="{ row }">
      <div class="flex space-x-2">
        <UButton
            icon="i-heroicons:check-circle-16-solid"
            size="xs"
            color="green"
            square
            variant="solid"
            @click="AcceptTripInvitation(row.trip_id)"
        />
        <UButton
            icon="i-heroicons:no-symbol-16-solid"
            size="xs"
            color="red"
            square
            variant="solid"
            @click="RefuseTripInvitation(row.trip_id)"
        />
      </div>
    </template>
  </UTable>
</template>

<style scoped>

</style>