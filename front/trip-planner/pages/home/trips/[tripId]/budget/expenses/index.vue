<script lang="ts" setup>
import type {Expense} from "~/types/expense";
import {ref} from "vue";

definePageMeta({
  title: 'budget.expenses',
  requiresAuth: true,
  layout: 'navigation'
});
const {t} = useI18n();
const toast = useToast();
const route = useRoute();
const tripId = ref(route.params.tripId);
const router = useRouter();

const expenses = ref<Expense[]>([]);
const expensesResponse = await useApiFetch<Expense[]>(`/trips/${tripId.value}/budget/expenses`);
expenses.value = expensesResponse.data.value ?? [];

const columns = computed(() => [
  {
    key: 'select'
  },
  {
    key: 'name',
    label: t('expense.name'),
    sortable: true,
  },
  {
    key: 'planned_amount',
    label: t('expense.planned-amount-short'),
    sortable: true
  },
  {
    key: 'actual_amount',
    label: t('expense.actual-amount-short'),
    sortable: true
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

const getCategoryLabel = (category: string) => t(`expense.categories.${category.toLowerCase()}`);

const selected = ref<Expense[]>([]);
const anySelected = computed(() => selected.value?.length >= 1);

const deleteExpense = async (expenseId: number) => {

  const { status } = await useApiFetch(`/trips/${tripId.value}/budget/expenses/${expenseId}`, {
    method: 'DELETE'
  });

  if (status.value === 'success') {
    expenses.value = expenses.value.filter((expense) => expense.expense_id !== expenseId);
    toast.add({
      title: t('misc.deletion'),
      description: t('misc.success'),
      icon: 'i-heroicons-check-badge',
      color: "green",
      timeout: 2000,
    });
  } else {
    toast.add({
      title: t('misc.deletion'),
      description: t('misc.error'),
      icon: 'i-heroicons-x-circle',
      color: "red",
      timeout: 2000,
    });
  }
};

const deleteAllSelected = async () => {
  selected.value?.forEach((expense: Expense) => {
    deleteExpense(expense.expense_id);
  });
  selected.value = [];
};

</script>

<template>
  <PageTitle :name="t('budget.expenses')" />

  <div class="flex justify-between mb-10">
    <UButton
        :disabled="!anySelected"
        :label="t('expense.delete-selected')"
        :title="t('expense.delete-many-tooltip')"
        color="red"
        icon="material-symbols:delete"
        size="xs"
        variant="solid"
        @click="deleteAllSelected"
    />

    <div class="flex w-1/2 space-x-5 px-5">
      <UButton
          :label="t('expense.add-expense-group')"
          class="w-1/2 justify-center"
          color="primary"
          icon="material-symbols:cards-star-outline"
          size="xs"
          square
          variant="solid"
          @click=""/>
      <UButton
          :label="t('budget.add-expense')"
          class="w-1/2 justify-center"
          color="primary"
          icon="material-symbols:add-shopping-cart"
          size="xs"
          square
          variant="solid"
          @click="$router.push(`/home/trips/${tripId}/budget/expenses/create`)"/>
    </div>
  </div>

  <UTable
      v-model="selected"
      :columns="columns"
      :rows="expenses"
  >
    <template #name-data="{ row }">
      <UTooltip >
        <span class="font-semibold underline text-left">{{ row.name }}</span>

        <template #text>
          <p class="font-bold">{{ t('expense.description') }}:</p>
          <p>{{ row.description }}</p>
        </template>
      </UTooltip>

    </template>

    <template #planned_amount-data="{ row }">
      <span v-if="row.planned_amount">{{ row.planned_amount?.toLocaleString(undefined, { minimumFractionDigits: 2 }) }} €</span>
      <span v-else>-</span>
    </template>

    <template #actual_amount-data="{ row }">
      <span v-if="row.actual_amount">{{ row.actual_amount?.toLocaleString(undefined, { minimumFractionDigits: 2 }) }} €</span>
      <span v-else>-</span>
    </template>

    <template #category-data="{ row }">
      <span>{{ getCategoryLabel(row.category) }}</span>
    </template>

    <template #expense_group-data="{ row }">
      <p v-if="row.expense_group == null"> {{ t('misc.not-defined') }} </p>
    </template>

    <template #actions-data="{ row }">
      <div class="flex space-x-2 items-center">
        <div class="mr-4 pt-1">
          <UTooltip v-if="row.is_shared" :title="t('expense.yes')">
            <UIcon color="gray" name="ic:sharp-people-alt" class="w-5 h-5 aspect-1"/>
          </UTooltip>
          <UTooltip v-else :title="t('expense.no')">
            <UIcon color="gray" name="material-symbols-light:person-rounded" class="w-5 h-5 aspect-1"/>
          </UTooltip>
        </div>
        <UButton
            icon="i-heroicons-pencil-square"
            size="xs"
            color="primary"
            square
            variant="solid"
            :to="`/home/trips/${tripId}/budget/expenses/${row.expense_id}/edit`"
        />
        <UButton
            icon="i-heroicons-trash"
            size="xs"
            color="red"
            square
            variant="solid"
            @click="deleteExpense(row.expense_id)"
        />
      </div>
    </template>
  </UTable>
</template>

<style scoped>
</style>