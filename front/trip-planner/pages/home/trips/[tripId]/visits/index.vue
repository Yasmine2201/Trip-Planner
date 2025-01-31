<script lang="ts" setup>
import type {Trip, Visit, VisitParticipation} from '~/types';
import type {AsyncData} from "#app";
import type {H3Error} from "h3";

definePageMeta({
  title: 'visits.list.title',
  requiresAuth: true,
  layout: 'navigation'
});

const {t, locale} = useI18n();
const route = useRoute();
const router = useRouter();
const auth = useAuthStore();
const notifs = useNotificationsStore();
const {$api} = useNuxtApp();

const tripId = route.params.tripId as number;

const sort = ref({
  column: 'start_date',
  direction: 'desc'
});

const columns = computed(() => [
  { key: 'name', label: t('visits.fields.name'), sortable: true },
  { key: 'location.name', label: t('visits.fields.location_name') },
  { key: 'start_date', label: t('visits.fields.start_date'), sortable: true },
  { key: 'end_date', label: t('visits.fields.end_date'), sortable: true },
  { key: 'participation', label: t('visits.fields.participation') },
  { key: 'actions' }
]);

const {data: rows, status}: AsyncData<Visit[], any> = await useApiFetch<Visit[]>(`/trips/${tripId}/visits`);
rows.value = rows.value
    ?.map(
        visit => ({
        ...visit,
        participations: visit.participations.filter(p => p.user.user_id === auth.user?.id)
      })
    ).filter(visit => visit.participations.length > 0)
    ?? [];

const sendParticipationChoice = async (visit: Visit, choice: string) => {

  const { error }: AsyncData<null, H3Error> = await useApiFetch(`/trips/${tripId}/visits/${visit.visit_id}/participations/${auth.user.id}`, {
    method: 'PUT',
    body: JSON.stringify({ status: choice })
  });

  if (error.value) {
    notifs.send_notif(t('misc.error'), false, t);
    return;
  }
  rows.value = rows.value.map(v => {
    if (v.visit_id === visit.visit_id) {
      v.participations[0].status = choice;
    }
    return v;
  });

  notifs.send_notif(t('misc.update'), true, t);
};

const deleteVisit = async (visit: Visit) => {
  const { status } = await useApiFetch(`/trips/${visit.trip_id}/visits/${visit.visit_id}`, {
    method: 'DELETE'
  });

  if (status.value === "success") {
    rows.value = rows.value.filter(v => v.visit_id !== visit.visit_id);
    notifs.send_notif(t('misc.delete'), true, t);
  } else {
    notifs.send_notif(t('misc.deletion_error'), false, t);
  }
};
</script>

<template>
  <PageTitle :name="t('visits.list.title')">
    <template #actions>
      <UButton :title="t('misc.back')" class="mr-2" color="gray"
               icon="i-heroicons-arrow-uturn-left" @click="router.push(`/home/trips/${tripId}`)" />
      <UButton
          :label="t('visits.list.add')"
          :to='`/home/trips/${tripId}/visits/create`'
          color="primary"
          icon="i-entypo:add-to-list"
          size="sm"
          variant="solid"
      />
    </template>
  </PageTitle>
  <UTable
      :columns
      :empty-state="{ icon: 'i-heroicons-circle-stack-20-solid', label: t('misc.no-items') }"
      :loading="status === 'pending'"
      :loading-state="{ icon: 'i-heroicons-arrow-path-20-solid', label: t('misc.loading') }"
      :progress="{ color: 'primary', animation: 'carousel' }"
      :rows
      :sort
  >
    <template #name-data="{ row }">
      <NuxtLink :to="`/home/trips/${tripId}/visits/${row.visit_id}`" class="font-semibold underline text-left">
        {{ row.name }}
      </NuxtLink>
    </template>

    <template #start_date-data="{ row }">
      {{ new Date(row.start_date).toLocaleString([locale], { dateStyle: 'long', timeStyle: 'short' }) }}
    </template>

    <template #end_date-data="{ row }">
      {{ new Date(row.end_date).toLocaleString([locale], { dateStyle: 'long', timeStyle: 'short' }) }}
    </template>

    <template #participation-data="{ row }">
      <div class="flex space-x-2">
        <UButton
            icon="i-heroicons:check-circle-16-solid"
            size="xs"
            :color="row.participations[0]?.status === 'accepted' ? 'green' : 'gray'"
            square
            variant="solid"
            @click="sendParticipationChoice(row, 'accepted')"
        />
        <UButton
            icon="i-heroicons:no-symbol-16-solid"
            size="xs"
            :color="row.participations[0]?.status === 'declined' ? 'red' : 'gray'"
            square
            variant="solid"
            @click="sendParticipationChoice(row, 'declined')"
        />
      </div>
    </template>

    <template #actions-data="{ row }">
      <div class="flex space-x-2">
        <UButton
            :to="`/home/trips/${tripId}/visits/${row.visit_id}`"
            color="gray"
            icon="i-heroicons-eye"
            size="xs"
            square
            variant="solid"
        />
        <UButton
            :to="`/home/trips/${tripId}/visits/${row.visit_id}/edit`"
            color="primary"
            icon="i-heroicons-pencil-square"
            size="xs"
            square
            variant="solid"
        />
        <ConfirmationDropdown @confirm="deleteVisit(row)">
          <UButton
              color="red"
              icon="i-heroicons-trash"
              size="xs"
              square
              variant="solid"
          />
        </ConfirmationDropdown>
      </div>
    </template>
  </UTable>
</template>

<style scoped>
</style>
