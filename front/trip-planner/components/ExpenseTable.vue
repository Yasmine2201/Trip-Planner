<script setup lang="ts">
import {type Expense} from "~/types";
import { CategoryValues } from "~/schemas/expense";

interface Props {
  expenses: Expense[],
  tripId: number,
  displayVisit?: boolean,
  categoryFilter?: string,
  selectable?: boolean,
}

const props = defineProps<Props>();
const { tripId, categoryFilter: categoryQuery = undefined, displayVisit = true, selectable = false } = props;

const expenses = defineModel<Expense[]>('expenses');
const selected = defineModel<Expense[]>('selected');

const { t } = useI18n();
const { $api } = useNuxtApp();
const toast = useToast();
const route = useRoute();
const router = useRouter();

if (selected.value == undefined && selectable) {
  selected.value = [];
} else if (!selectable) {
  selected.value = undefined;
}

const columns = computed(() => {
  const col = [
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
      key: 'visit',
      label: t('expense.visit'),
    },
    {key: 'actions'}
  ].filter(column => column.key !== 'visit' || displayVisit);
  console.debug(col, displayVisit);
  return col;
});

const categoryOptions = computed(() => [
  { label: t('misc.all'), value: '' },
  ...Object.values(CategoryValues).map(value => ({
    label: getCategoryLabel(value),
    value: value,
  }))
]);

// Methods
const getCategoryLabel = (category: string) => t(`expense.categories.${category.toLowerCase()}`);

const deleteExpense = async (expenseId: number) => {
  const {status} = await useApiFetch(`/trips/${tripId}/budget/expenses/${expenseId}`, {
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

const convertPlannedToReal = async (expense: Expense) => {
  const sentData = JSON.stringify(
      {
        name: expense.name,
        category: expense.category,
        planned_amount: expense.planned_amount,
        actual_amount: expense.planned_amount,
      }
  )

  await $api(`/trips/${tripId}/budget/expenses/${expense.expense_id}`, {
    method: 'PUT',
    body: sentData
  });

  expenses.value = expenses.value.map((e) => {
    if (e.expense_id === expense.expense_id) {
      e.actual_amount = e.planned_amount;
    }
    return e;
  });
};

// Category filter
const selectedCategory = reactive({value: categoryQuery ?? ''});

const filteredExpenses = computed(() => {
  if (!selectedCategory.value) return expenses.value;
  else {
    return expenses.value.filter(expense => expense.category === selectedCategory.value);
  }
});

</script>

<template>

  <div class="flex justify-between mb-5">
    <div class="flex-1">
      <slot name="caption" />
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
      :empty-state="{ icon: 'i-heroicons-circle-stack-20-solid', label: t('misc.no-items') }"
  >
    <template #name-data="{ row }">
      <UTooltip :ui="{
                          strategy: 'override',
                          base: '[@media(pointer:coarse)]:hidden max-h-96 px-2 py-1 text-xs font-normal relative overflow-hidden',
                          con
        }">
        <span class="font-semibold underline text-left">{{ row.name }}</span>

        <template #text>
          <p class="font-bold">{{ t('expense.description') }}:</p>
          <p class="whitespace-pre-line">{{ row.description }}</p>
        </template>
      </UTooltip>

    </template>

    <template #planned_amount-data="{ row }">
      <div v-if="row.planned_amount" class="flex justify-between">
        <span>{{ row.planned_amount?.toLocaleString(undefined, {minimumFractionDigits: 2}) }} €</span>
        <UButton
            v-if="row.actual_amount == null"
            color="gray"
            icon="i-heroicons-arrow-right"
            size="2xs"
            square
            variant="solid"
            @click="convertPlannedToReal(row)" />
      </div>
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

    <template #visit-data="{ row }" v-if="displayVisit" >
      <p v-if="row.visit == null"> {{ t('misc.not-defined') }} </p>
      <p v-else>
        <UTooltip>
          <a :href="`/home/trips/${tripId}/visits/${row.visit?.visit_id}`" class="underline">{{ row.visit.name }}</a>
          <template #text>
            <span>{{ t('expense.visit-tooltip') }}</span>
          </template>
        </UTooltip>
      </p>
    </template>

    <template #actions-data="{ row }">
      <div class="flex space-x-2 items-center">
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