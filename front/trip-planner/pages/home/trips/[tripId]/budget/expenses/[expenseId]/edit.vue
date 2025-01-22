<script setup lang="ts">
definePageMeta({
title: 'budget.edit-budget',
requiresAuth: true,
layout: 'navigation'
});

const route = useRoute();
const tripId = ref(route.params.tripId);
const expenseId = ref(route.params.expenseId);

const router = useRouter();

// Fetch the expense data from the API
const { data: expense, status, error } = await useApiFetch(`/trips/${tripId.value}/budget/expenses/${expenseId.value}`, {}, true);

const expenseData = Object.assign({}, expense.value ?? {});

</script>

<template>
  <ExpenseForm mode="edit" :expenseData="expenseData" />
</template>

<style scoped>

</style>