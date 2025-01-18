<script setup lang="ts">
definePageMeta({
title: 'budget.title',
requiresAuth: true,
layout: 'navigation'
});
const { t } = useI18n();

const budgetItems = [{
  label: t('budget.debts-and-credits'),
  icon: 'material-symbols:account-balance-wallet',
  content: t('budget.debts-and-credits-description'),
  component: 'DebtsAndCredits'
}, {
  label: t('budget.expenses'),
  icon: 'solar:banknote-2-linear',
  content: t('budget.expenses-description'),
  component: 'Expenses'
}]

</script>

<template>
  <UTabs :items="budgetItems">
    <template #item ="{item}">
      <Expenses v-if="item.component === 'Expenses'" />
      <DebtsAndCredits v-if="item.component === 'DebtsAndCredits'" />
    </template>
  </UTabs>

</template>