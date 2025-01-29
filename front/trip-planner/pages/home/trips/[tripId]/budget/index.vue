<script lang="ts" setup>
import {ref} from "vue";
import type {BudgetDto} from "~/schemas/expense";
import type {AsyncData} from "#app";

definePageMeta({
  title: 'budget.title',
  requiresAuth: true,
  layout: 'navigation'
});


const route = useRoute();
const router = useRouter();
const tripId = ref(route.params.tripId);
const {t} = useI18n();

// API calls
const {data: declaredBudget}: AsyncData<number, any> = await useApiFetch<number>(`/trips/${tripId.value}/budget`);
const {data: expenses}: AsyncData<Expense[], any> = await useApiFetch<Expense[]>(`/trips/${tripId.value}/budget/expenses`);

// Tab items
const tabItems = computed(() => [{
  key: 'previsional',
  label: t('budget.forecasted-expenses'),
  predicate: (expense: Expense) => expense.planned_amount
}, {
  key: 'effective',
  label: t('budget.effective-expenses'),
  predicate: (expense: Expense) => expense.actual_amount
}]);

// Computed values and Refs
const selectedTabIndex = ref(0);
const isBudgetModalOpen = ref(false);

const amountPredicate = computed(() => tabItems.value[selectedTabIndex.value].predicate);
const remainingBudget = computed(() => {
  const totalExpenses = expenses.value.reduce((acc, expense) => acc + amountPredicate.value(expense), 0)
  return declaredBudget.value - totalExpenses
});

const remainingColorClass = computed(() => {
  const ratio = (remainingBudget.value / declaredBudget.value) * 100;

  switch (true) {
    case ratio > 30:
      return 'text-green-500 dark:text-green-400'
    case ratio > 15:
      return 'text-primary dark:text-primary'
    default:
      return 'text-red-500 dark:text-red-400'
  }
});

const refreshBudget = (budgetData: BudgetDto) => {
  declaredBudget.value = budgetData.budget;
  isBudgetModalOpen.value = false;
}
</script>

<template>
  <PageTitle :name="t('budget.title')">
    <template v-slot:actions>
      <UButton :title="t('misc.back')" class="mr-2" color="gray"
               icon="i-heroicons-arrow-uturn-left" @click="router.push(`/home/trips/${tripId}`)"/>
    </template>
  </PageTitle>

  <UTabs :items="tabItems" v-model="selectedTabIndex"/>
  <UCard>
    <UModal v-model="isBudgetModalOpen" prevent-close>
      <UCard>
        <PageTitle :name="t('budget.edit-budget')">
          <template #actions>
            <UButton class="-my-1" color="gray" icon="i-heroicons-x-mark-20-solid" variant="ghost"
                     @click="isBudgetModalOpen = false"/>
          </template>
        </PageTitle>
        <BudgetForm :budgetData="declaredBudget" @onSave="refreshBudget"/>
      </UCard>
    </UModal>

    <template #header>
      <div class="h-8 header flex">
        <!--left -->
        <div class="flex-1 flex flex-col justify-center items-center">
          <div class="text-sm">{{ t('budget.initial-budget') }}
          </div>
          <div>
            <span class="text-lg text-primary">{{ declaredBudget }} €</span>
          </div>
        </div>
        <!--right -->
        <div class="flex-1 flex flex-col justify-center items-center space-y-1">
          <div class="text-sm">{{ t('budget.remaining-budget') }}</div>
          <div :class="remainingColorClass" class="text-lg">{{ remainingBudget }} €</div>
        </div>
      </div>
    </template>

    <ExpensesChart :expenses :predicate="amountPredicate" />

    <template #footer>
      <div class="h-8 footer flex justify-center space-x-8 px-12">

        <UButton
            :label="t('budget.edit-budget')"
            class="flex-1 flex items-center justify-center"
            color="primary"
            icon="material-symbols-light:box-edit"
            size="md"
            square
            variant="solid"
            @click="isBudgetModalOpen = true"
        />
        <UButton
            :label="t('budget.manage-expenses')"
            class="flex-1 flex items-center justify-center"
            color="red"
            icon="material-symbols:analytics"
            size="md"
            square
            variant="solid"
            @click="$router.push(`/home/trips/${tripId}/budget/expenses`)"
        />
      </div>
    </template>
  </UCard>
</template>