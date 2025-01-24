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
  <PageTitle :name="t('budget.edit-budget')">
    <template v-slot:actions>
      <UButton @click="router.back()" icon="i-heroicons-arrow-uturn-left" class="mr-2" :title="t('misc.back')" color="gray" />
    </template>
  </PageTitle>
  <BudgetForm :budgetData="budgetData" />
</template>

<style scoped>

</style>