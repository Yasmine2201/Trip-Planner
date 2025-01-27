<script setup lang="ts">
import type {AsyncData} from "#app";
import type {Visit, Expense} from "~/types";

definePageMeta({
  title: 'navigation.visit_details',
  layout: 'navigation',
  requiresAuth: true,
});

const { t, locale } = useI18n();
const route = useRoute();
const router = useRouter();
const toast = useToast();

const tripId = Number(route.params.tripId);
const visitId = Number(route.params.visitId);

const { data: visit }: AsyncData<Visit, any> = await useApiFetch<Visit>(`/trips/${tripId}/visits/${visitId}`, {}, true);

const { data: expenses }: AsyncData<Expense[], any> = await useApiFetch<Expense[]>(`/trips/${tripId}/budget/expenses`);
expenses.value = expenses.value.filter((expense) => expense.visit?.visit_id === visitId);

const formatDate = (date: string) => {
  return new Date(date).toLocaleString([locale.value], { dateStyle: 'full', timeStyle: 'short' });
}

const deleteVisit = async () => {
  const {status} = await useApiFetch(`/trips/${tripId}/visits/${visitId}`, {
    method: 'DELETE'
  });

  if (status.value === "success") {
    toast.add({
      title: t('misc.delete'),
      description: t('misc.success'),
      icon: 'i-heroicons-check-badge',
      color: "green",
      timeout: 2000,
    });
    router.push(`/home/trips/${tripId}/visits`);
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
  <PageTitle :name="t('navigation.visit_details')">
    <template v-slot:actions>
      <UButton icon="i-heroicons-arrow-uturn-left" class="mr-2" :title="t('misc.back')" color="gray" @click="$router.back()" />
      <UButton
          :to="`/home/trips/${tripId}/visits/${visitId}/edit`"
          color="primary"
          icon="i-heroicons-pencil-square"
          :label="t('misc.edit')"
          size="md"
          square
          variant="solid"
      />
      <UButton
          @click="deleteVisit()"
          color="red"
          icon="i-heroicons-trash"
          :label="t('misc.delete')"
          size="md"
          square
          variant="solid"
      />
    </template>
  </PageTitle>

  <UCard>
    <template #header>
      <h2 class="text-xl font-bold text-primary">{{ visit.name }}</h2>
      <p class="pt-4">{{ t('visits.display.dates', { start: formatDate(visit.start_date), end: formatDate(visit.end_date) }) }}</p>
    </template>

    <LocationDetails :location="visit.location" class="" />

    <UDivider class="mt-6" />

    <div class="pt-6">
      <ExpenseTable
        :tripId="tripId"
        :expenses="expenses"
        :displayVisit="false"
        >
        <template #caption>
          <div class="flex justify-between items-center mr-2">
            <h2 class="text-lg font-semibold">{{ t('budget.expenses') }}</h2>
            <div>
              <UButton
                  color="gray"
                  icon="material-symbols:attach-money"
                  :label="t('budget.add-expense')"
                  size="sm"
                  :to="`/home/trips/${tripId}/budget/expenses/create?visit_id=${visitId}`"
                  class="mr-2"
              />
              <UButton
                  color="primary"
                  :label="t('visits.display.fill-prices')"
                  size="sm"
                  icon="material-symbols:add-shopping-cart"
              />
            </div>
          </div>
        </template>
      </ExpenseTable>
    </div>

  </UCard>

</template>

<style scoped>

</style>