<script lang="ts" setup>
import type {Trip, Visit, VisitParticipation} from '~/types';
import type {AsyncData} from "#app";

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
const dataVisitParts = ref<VisitParticipation[]>(await $api(`/trips/${tripId}/visits/participations`, {
  params: { user_id: auth.user?.id }
}));

console.log("dataVisitParts:", dataVisitParts.value);
rows.value = rows.value ?? [];

const rowsWithParticipation = computed(() => {
  return rows.value.map(visit => {
    let participation = dataVisitParts.value.find(p => p.visit === visit.visit_id) || null;
    return { visit, participation };
  });
});
console.log("rowsWithParticipation:", rowsWithParticipation.value);

const sendParticipationChoice = async (visit: Visit, choice: string) => {
  const visitParticipation = {
    // visit_id: visit.visit_id,
    // user_id: auth.user?.id,
    status: choice
  };

  const { data, pending, error } = await useApiFetch<VisitParticipation | null>(`/trips/${tripId}/visits/${visit.visit_id}/participations`, {
    method: 'PUT',
    body: JSON.stringify(visitParticipation)
  });
  if (!error.value && data.value) {
    const participationIndex = dataVisitParts.value.findIndex(p => p.visit === visit.visit_id);

    if (participationIndex >= 0) {
      dataVisitParts.value[participationIndex] = { ...data.value };
    } else {
      dataVisitParts.value.push({ ...data.value });
    }

    // Forcer la mise à jour de la liste
    dataVisitParts.value = [...dataVisitParts.value];

    notifs.send_notif(t('misc.update'), true, t);
  } else {
    notifs.send_notif(t('misc.error'), false, t);
  }
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
      :rows="rowsWithParticipation"
      :sort
  >
    <template #name-data="{ row }">
      <NuxtLink :to="`/home/trips/${row.visit.trip_id}/visits/${row.visit.visit_id}`" class="font-semibold underline text-left">
        {{ row.visit.name }}
      </NuxtLink>
    </template>

    <template #start_date-data="{ row }">
      {{ new Date(row.visit.start_date).toLocaleString([locale], { dateStyle: 'long', timeStyle: 'short' }) }}
    </template>

    <template #end_date-data="{ row }">
      {{ new Date(row.visit.end_date).toLocaleString([locale], { dateStyle: 'long', timeStyle: 'short' }) }}
    </template>

    <template #participation-data="{ row }">
      <div class="flex space-x-2">
        <UButton
            icon="i-heroicons:check-circle-16-solid"
            size="xs"
            :color="row.participation?.status === 'accepted' ? 'green' : 'gray'"
            square
            variant="solid"
            @click="sendParticipationChoice(row.visit, 'accepted')"
        />
        <UButton
            icon="i-heroicons:no-symbol-16-solid"
            size="xs"
            :color="row.participation?.status === 'declined' ? 'red' : 'gray'"
            square
            variant="solid"
            @click="sendParticipationChoice(row.visit, 'declined')"
        />
      </div>
    </template>

    <template #actions-data="{ row }">
      <div class="flex space-x-2">
        <UButton
            :to="`/home/trips/${row.visit.trip_id}/visits/${row.visit.visit_id}`"
            color="gray"
            icon="i-heroicons-eye"
            size="xs"
            square
            variant="solid"
        />
        <UButton
            :to="`/home/trips/${row.visit.trip_id}/visits/${row.visit.visit_id}/edit`"
            color="primary"
            icon="i-heroicons-pencil-square"
            size="xs"
            square
            variant="solid"
        />
        <UButton
            color="red"
            icon="i-heroicons-trash"
            size="xs"
            square
            variant="solid"
            @click="deleteVisit(row.visit)"
        />
      </div>
    </template>
  </UTable>
</template>

<style scoped>
</style>
