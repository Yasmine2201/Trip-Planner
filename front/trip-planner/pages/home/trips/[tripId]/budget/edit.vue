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

// Fetch the budget data from the API
const { data: budget}= await useApiFetch(`/trips/${tripId.value}/budget`);
const budgetData = budget.value ?? {};

</script>

<template>

  <BudgetForm :budgetData="budgetData" />
</template>

<style scoped>

</style>