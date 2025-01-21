<script setup lang="ts">
definePageMeta({
title: 'expense.add-expense',
requiresAuth: true,
layout: false
});

</script>

<template>
  <ExpenseForm mode="create" />

</template>

<style scoped>

</style>