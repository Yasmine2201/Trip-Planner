<script lang="ts" setup>
import type {Expense} from "~/types/expense";

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
const categoryQuery = route.query?.category as string | undefined;
const expenses = ref<Expense[]>([]);
const expensesResponse = await useApiFetch<Expense[]>(`/trips/${tripId.value}/budget/expenses`);
expenses.value = expensesResponse.data.value ?? [];

const selected = ref([]) as Ref<Expense[]>;
const anySelected = computed(() => selected.value?.length >= 1);

const deleteExpense = async (expenseId: number) => {

  const {status} = await useApiFetch(`/trips/${tripId.value}/budget/expenses/${expenseId}`, {
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

  <ExpenseTable
      :tripId="tripId"
      :expenses="expenses"
      :selectable="true"
      :display-visit="true"
      :categoryFilter="categoryQuery"
      v-model="selected"
  >
  </ExpenseTable>
</template>

<style scoped>
</style>