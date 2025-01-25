<script lang="ts" setup>

import {onBeforeUnmount, onMounted, ref} from 'vue';
import {
  ArcElement,
  Chart,
  type ChartDataset,
  type ChartOptions,
  DoughnutController,
  Legend,
  Tooltip,
} from 'chart.js';
import type {Expense} from "~/types/expense";
import {type BudgetDto, CategoryValues} from "~/schemas/expense";

const route = useRoute();
const router = useRouter();
const tripId = ref(route.params.tripId);
const {t} = useI18n();

// API calls
const declaredBudget = ref<number>(0);
const expenses = ref<Expense[]>([]);

const budgetResponse = await useApiFetch<number>(`/trips/${tripId.value}/budget`);
declaredBudget.value = budgetResponse.data.value ?? 0;

const expensesResponse = await useApiFetch<Expense[]>(`/trips/${tripId.value}/budget/expenses`);
expenses.value = expensesResponse.data.value ?? [];

// Computed values
const isOpen = ref(false);
const totalExpenses = computed(() => expenses.value.reduce((acc, expense) => acc + expense.actual_amount, 0));
const remainingBudget = computed(() => declaredBudget.value - totalExpenses.value);
const ratio = computed(() => (remainingBudget.value / declaredBudget.value) * 100);
const allCategories = Object.values(CategoryValues).sort();
console.log("all categories", allCategories);
const groupedExpenses = computed(() => {
  const colors = [
    'rgba(54, 162, 235, 0.8)', //Accommodation
    'rgba(165, 42, 42, 0.8)', //Activities
    'rgba(255, 0, 0, 0.8)', //Food
    'rgba(201, 203, 207, 0.8)', //Others
    'rgba(150, 20, 90, 0.8)', //Shopping
    'rgba(75, 192, 192, 0.8)', //Transport
    'rgba(255, 165, 0, 0.8)' //Visit
  ];

  return allCategories.map((category: string, index: number) => {
    const total = expenses.value
        .filter((expense: Expense) => expense.category === category)
        .reduce((sum: number, expense: Expense) => sum + expense.actual_amount, 0);
    return {category, total, backgroundColor: colors[index % colors.length]};
  });
});
console.log("grouped expenses", groupedExpenses.value);

const color = computed(() => {
  switch (true) {
    case ratio.value > 50:
      return 'text-green-500 dark:text-green-400'
    case ratio.value > 30:
      return 'text-primary dark:text-primary'
    default:
      return 'text-red-500 dark:text-red-400'
  }
})

// Register components for the doughnut chart
Chart.register(DoughnutController, ArcElement, Tooltip, Legend);

// Ref for the chart canvas
const chartCanvas = ref(null);
let chartInstance: Chart<"doughnut", number[], string> | null = null;

// Data for the donut chart

const chartData: ComputedRef<ChartDataset<"doughnut", number[]>> = computed(() => ({
  labels: groupedExpenses.value.map((expense) => t(`budget.${expense.category.toLowerCase()}`)),
  datasets: [
    {
      label: t('budget.expenses'),
      data: groupedExpenses.value.map((expense) => expense.total),
      backgroundColor: groupedExpenses.value.map((expense) => expense.backgroundColor),
      hoverOffset: 15, // Makes segments expand on hover

    },
  ],
}));

// Options for the donut chart
const chartOptions: ComputedRef<ChartOptions<"doughnut">> = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    tooltip: {
      enabled: true,
      callbacks: {
        label: function (tooltipItem: any) {
          const data = tooltipItem.dataset.data[tooltipItem.dataIndex];
          return `${data} €`;
        },
      },
    },
    legend: {
      display: true,
      position: 'top',
    },
  },
  onClick: (event, elements) => {
    if (elements.length > 0) {
      const category = groupedExpenses.value[elements[0].index].category;
      router.push(`/home/trips/${tripId.value}/budget/expenses?category=${category}`);
    }
  }
}));

onMounted(() => {
  if (chartCanvas.value) {
    chartInstance = new Chart<"doughnut", number[], string>(chartCanvas.value, {
      type: "doughnut",
      data: chartData.value,
      options: chartOptions.value,
    });
  }
});

watch(chartData, () => {
  if (chartInstance) {
    chartInstance.data = chartData.value;
    chartInstance.update();
  }
});

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});

const refreshBudget = (budgetData: BudgetDto) => {
  declaredBudget.value = budgetData.budget;
  isOpen.value = false;
}
</script>

<template>
  <UCard>
    <UModal v-model="isOpen" prevent-close>
      <UCard>
        <PageTitle :name="t('budget.edit-budget')">
          <template #actions>
            <UButton color="gray" variant="ghost" icon="i-heroicons-x-mark-20-solid" class="-my-1" @click="isOpen = false" />
          </template>
        </PageTitle>
        <BudgetForm :budgetData="declaredBudget" @onSave="refreshBudget" />
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
          <div :class="color" class="text-lg">{{ remainingBudget }} €</div>
        </div>
      </div>
    </template>

    <div class="h-100">

      <div v-if="expenses.length === 0" class="flex items-center justify-center h-full">
        <p>{{ t('expense.no-expenses') }}</p>
      </div>

      <div v-else class="chart-container">
        <canvas ref="chartCanvas"></canvas>
      </div>
    </div>


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
            @click="isOpen = true"
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

<style scoped>
</style>