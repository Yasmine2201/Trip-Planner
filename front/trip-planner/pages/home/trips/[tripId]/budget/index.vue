<script setup lang="ts">
definePageMeta({
  title: 'budget.title',
  requiresAuth: true,
  layout: 'navigation'
});
const {t} = useI18n();

const budgetItems = computed(() =>
  [
    {
      label: t('budget.expenses'),
      icon: 'solar:banknote-2-linear',
      content: t('budget.expenses-description'),
      component: 'Expenses'
    },
    {
      label: t('budget.debts-and-credits'),
      icon: 'material-symbols:account-balance-wallet',
      content: t('budget.debts-and-credits-description'),
      component: 'DebtsAndCredits'
    }
  ]
);

</script>

<template>
  <UTabs :items="budgetItems">
    <template #item="{item}">
      <DebtsAndCredits v-if="item.component === 'DebtsAndCredits'"/>
      <Expenses v-if="item.component === 'Expenses'"/>
    </template>
  </UTabs>

</template>