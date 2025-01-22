<script setup lang="ts">
import type {Expense} from "~/types/expense";
import {ref} from "vue";

definePageMeta({
title: 'budget.expenses',
requiresAuth: true,
layout: 'navigation'
});
const { t } = useI18n();
const toast = useToast();
const route = useRoute();
const tripId = ref(route.params.tripId);
const router = useRouter();

const expenses = ref<Expense[]>([]);
const expensesResponse = await useApiFetch<Expense[]>(`/trips/${tripId.value}/budget/expenses`);
expenses.value = expensesResponse.data.value ?? [];

const columns = computed(() => [
  {
  key: 'name',
  label: t('expense.name'),
  sortable: true
  },
  {
    key: 'description',
    label: t('expense.description'),
  },
    {
    key: 'planned_amount',
    label: t('expense.planned-amount'),
    sortable: true
  },
  {
    key: 'actual_amount',
    label: t('expense.actual-amount'),
    sortable: true
  },
  {
    key: 'is_shared',
    label: t('expense.is-shared'),

  },
  {
    key: 'category',
    label: t('expense.category'),
    sortable: true
  },
  {
    key: 'expense_group',
    label: t('expense.expense-group'),
  },
  {key: 'actions'}
]);

const actionItems = (row) => [
    [
  {
    label: t('misc.edit'),
    icon: 'i-heroicons-pencil',
    class: 'bg-primary-500 text-white dark:bg-primary dark:text-black mb-2',
    iconClass: 'text-white dark:text-black',
    click: () => router.push(`/home/trips/${tripId.value}/budget/expenses/${row.expense_id}/edit`)
  },
  {
    label: t('misc.delete'),
    icon : 'i-heroicons-trash',
    class: 'bg-red-500 text-white dark:bg-red-400 dark:text-black',
    iconClass: 'text-white dark:text-black',
    click: () =>  deleteExpense(row.expense_id)
  }
  ]
]
const selected = ref([]);
const anySelected = computed(() => selected.value.length >= 1);

const deleteExpense = async (expenseId: number) => {
  try {
    await useApiFetch(`/trips/${tripId.value}/budget/expenses/${expenseId}`, {
      method: 'DELETE'
    });
    expenses.value = expenses.value.filter((expense) => expense.expense_id !== expenseId);
    toast.add({
      title: t('misc.deletion'),
      description: t('misc.success'),
      icon: 'i-heroicons-check-badge',
      color: "green",
      timeout: 2000,
    });
  } catch (error) {
    toast.add({
      title: t('misc.delete'),
      description: t('misc.error'),
      icon: 'i-heroicons-x-circle',
      color: "red",
      timeout: 2000,
    });
  }
};
const deleteAllSelected = async () => {
  selected.value.forEach((expense : Expense) => {
    deleteExpense(expense.expense_id);
  });
  selected.value = [];
};

</script>

<template>
    <div class="flex justify-between mb-10">
        <UButton
          @click="deleteAllSelected"
          :title="t('expense.delete-many-tooltip')"
          color="red"
          icon="material-symbols:delete"
          :label="t('expense.delete-selected')"
          size="xs"
          variant="solid"
          :disabled="!anySelected"
          />

      <div class="flex">
        <UButton
          @click=""
          color="primary"
          icon="material-symbols:cards-star-outline"
          :label="t('expense.add-expense-group')"
          size="xs"
          square
          variant="solid"
          class = "mr-2"/>
      <UButton
        @click="$router.push(`/home/trips/${tripId}/budget/expenses/create`)"
        color="primary"
        icon="material-symbols:add-shopping-cart"
        :label="t('budget.add-expense')"
        size="xs"
        square
        variant="solid"/>
    </div>
  </div>

  <UTable
      v-model="selected"
      :rows="expenses"
      :columns="columns">
    <template #is_shared-data="{ row }">
        <UButton v-if="row.is_shared" icon="ic:sharp-people-alt" color="gray" size="sm" :title="t('expense.yes')" />
        <UButton v-else icon="material-symbols-light:person-rounded" color="gray" size="sm" :title="t('expense.no')"/>
    </template>
    <template #actions-data="{row}">
      <UDropdown :items="actionItems(row)" >
        <UButton color="gray" variant="ghost" icon="i-heroicons-ellipsis-horizontal-20-solid" size="sm" square/>
      </UDropdown>
    </template>
    <template #expense_group-data="{ row }">
    <p v-if="row.expense_group == null"> {{t('misc.not-defined') }} </p>
    </template>

  </UTable>


</template>

<style scoped>
</style>