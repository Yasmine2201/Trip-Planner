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

const tripId = Number(route.params.tripId);
const visitId = Number(route.params.visitId);

const { data: visit }: AsyncData<Visit, any> = await useApiFetch<Visit>(`/trips/${tripId}/visits/${visitId}`, {}, true);

const { data: expenses }: AsyncData<Expense[], any> = await useApiFetch<Expense[]>(`/trips/${tripId}/budget/expenses`);
expenses.value = expenses.value.filter((expense) => expense.visit?.visit_id === visitId);

const formatDate = (date: string) => {
  return new Date(date).toLocaleString([locale.value], { dateStyle: 'full', timeStyle: 'short' });
}

</script>

<template>
  <PageTitle :name="t('navigation.visit_details')">
    <template v-slot:actions>
      <UButton icon="i-heroicons-arrow-uturn-left" class="mr-2" :title="t('misc.back')" color="gray" @click="$router.back()" />
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
          <h2 class="text-lg font-semibold">{{ t('budget.expenses') }}</h2>
        </template>
      </ExpenseTable>
    </div>

  </UCard>

</template>

<style scoped>

</style>