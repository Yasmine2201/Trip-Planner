<script setup lang="ts">
definePageMeta({
title: 'budget.edit-budget',
requiresAuth: true,
layout: 'navigation'
});

const { t } = useI18n();
const router = useRouter();
const route = useRoute();

const tripId = ref(route.params.tripId);
const expenseId = ref(route.params.expenseId);

// Fetch the expense data from the API
const { data: expense, status, error } = await useApiFetch(`/trips/${tripId.value}/budget/expenses/${expenseId.value}`, {}, true);

const expenseData = Object.assign({}, expense.value ?? {});

</script>

<template>
  <PageTitle :name="t('expense.edit-expense')">
    <template v-slot:actions>
      <UButton @click="router.back()" icon="i-heroicons-arrow-uturn-left" class="mr-2" :title="t('misc.back')" color="gray" />
    </template>
  </PageTitle>
  <ExpenseForm mode="edit" :expenseData="expenseData" />
</template>

<style scoped>

</style>