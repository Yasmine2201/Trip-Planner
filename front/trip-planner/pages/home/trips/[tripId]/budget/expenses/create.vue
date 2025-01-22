<script setup lang="ts">
definePageMeta({
title: 'expense.add-expense',
requiresAuth: true,
layout: 'navigation'
});

</script>

<template>
  <ExpenseForm mode="create" />

</template>

<style scoped>

</style>