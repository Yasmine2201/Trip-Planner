<script setup lang="ts">
definePageMeta({
title: 'expense.add-expense',
requiresAuth: true,
layout: 'navigation'
});

const {t} = useI18n();
const router = useRouter();

</script>

<template>
  <PageTitle :name="t('expense.add-expense')">
    <template v-slot:actions>
      <UButton @click="router.back()" icon="i-heroicons-arrow-uturn-left" class="mr-2" :title="t('misc.back')" color="gray" />
    </template>
  </PageTitle>
  <ExpenseForm mode="create" />
</template>

<style scoped>

</style>