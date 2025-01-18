<script setup lang="ts">
definePageMeta({
title: 'budget.expenses',
requiresAuth: true,
layout: 'navigation'
});
const { t } = useI18n();

const items = [
  {
    id: 1,
    name: 'Toto',
  },
  {
    id: 2,
    name: 'Tata',
  }
]
</script>

<template>
  <div class ="flex justify-end mb-4">
   <UButton
    @click=""
    color="primary"
    icon="material-symbols:add-shopping-cart"
    :label="t('budget.add-expense')"
    size="md"
    square
    variant="solid"/>
  </div>

  <UTable :rows="items" />
</template>

<style scoped>

</style>