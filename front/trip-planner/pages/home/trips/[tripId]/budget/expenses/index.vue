<script lang="ts" setup>
import type {Expense} from "~/types/expense";
import {CategoryValues} from "~/schemas/expense";

definePageMeta({
  title: 'budget.expenses',
  requiresAuth: true,
  layout: 'navigation'
});
const {t} = useI18n();
const toast = useToast();
const route = useRoute();
const router = useRouter();

const tripId = ref(route.params.tripId);
const categoryQuery = route.query?.category;
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

// Filter
const categoryOptions = computed(() => [
  {label: t('misc.all'), value: ''},
  ...Object.values(CategoryValues).map(value => ({
    label: getCategoryLabel(value),
    value: value,
  }))
]);
const selectedCategory = reactive({value: categoryQuery ?? ''});
const filteredExpenses = computed(() => {
  if (!selectedCategory.value) return expenses.value;
  else {
    return expenses.value.filter(expense => expense.category === selectedCategory.value);
  }
});
const selectMenuClass = computed(() => {
  return selectedCategory.value ? 'primary' : '';
});

// Delete all selected
const deleteAllSelected = async () => {
  selected.value?.forEach((expense: Expense) => {
    deleteExpense(expense.expense_id);
  });
  selected.value = [];
};

</script>

<template>
  <PageTitle :name="t('budget.expenses')">
    <template #actions>
      <UButton :title="t('misc.back')" class="mr-2" color="gray" icon="i-heroicons-arrow-uturn-left"
               @click="router.back()"/>
      <UButton
          :disabled="!anySelected"
          :label="t('expense.delete-selected')"
          :title="t('expense.delete-many-tooltip')"
          class="min-w-48 justify-center"
          color="red"
          icon="material-symbols:delete"
          size="xs"
          variant="solid"
          @click="deleteAllSelected"
      />
      <UButton
          :label="t('budget.add-expense')"
          class="min-w-48 justify-center"
          color="primary"
          icon="material-symbols:add-shopping-cart"
          size="xs"
          square
          variant="solid"
          @click="$router.push(`/home/trips/${tripId}/budget/expenses/create`)"/>
    </template>
  </PageTitle>

  <div class="flex justify-between mb-5">
    <div class="flex w-1/2 space-x-5 px-5">

    </div>
    <UFormGroup>
      <USelectMenu
          v-model="selectedCategory.value"
          :color="selectedCategory.value ? 'primary' : 'gray'"
          :options="categoryOptions"
          :placeholder="t('expense.placeholders.filter-by-category')"
          class="min-w-48"
          icon="fa6-solid:filter"
          value-attribute="value"
      />
    </UFormGroup>
  </div>

  <UTable
      v-model="selected"
      :columns="columns"
      :rows="filteredExpenses"
  >
    <template #name-data="{ row }">
      <UTooltip>
        <span class="font-semibold underline text-left">{{ row.name }}</span>

        <template #text>
          <p class="font-bold">{{ t('expense.description') }}:</p>
          <p>{{ row.description }}</p>
        </template>
      </UTooltip>

    </template>

    <template #planned_amount-data="{ row }">
      <span v-if="row.planned_amount">{{
          row.planned_amount?.toLocaleString(undefined, {minimumFractionDigits: 2})
        }} €</span>
      <span v-else>-</span>
    </template>

    <template #actual_amount-data="{ row }">
      <span v-if="row.actual_amount">{{
          row.actual_amount?.toLocaleString(undefined, {minimumFractionDigits: 2})
        }} €</span>
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
            <UIcon class="w-5 h-5 aspect-1" color="gray" name="ic:sharp-people-alt"/>
          </UTooltip>
          <UTooltip v-else :title="t('expense.no')">
            <UIcon class="w-5 h-5 aspect-1" color="gray" name="material-symbols-light:person-rounded"/>
          </UTooltip>
        </div>
        <UButton
            :to="`/home/trips/${tripId}/budget/expenses/${row.expense_id}/edit`"
            color="primary"
            icon="i-heroicons-pencil-square"
            size="xs"
            square
            variant="solid"
        />
        <UButton
            color="red"
            icon="i-heroicons-trash"
            size="xs"
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