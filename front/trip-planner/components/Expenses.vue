<script setup lang="ts">

import { ref, onMounted, onBeforeUnmount } from 'vue';
import {
  Chart,
  DoughnutController,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';
import type {Expense} from "~/types/expense";
const route = useRoute();
const tripId = ref(route.params.tripId);
const { t } = useI18n();

// API cals
const declaredBudget = ref<number>(0);
const expenses = ref<Expense[]>([]);

const budgetResponse = await useApiFetch<number>(`/trips/${tripId.value}/budget`);
declaredBudget.value = budgetResponse.data.value ?? 0;

const expensesResponse = await useApiFetch<Expense[]>(`/trips/${tripId.value}/budget/expenses`);
expenses.value = expensesResponse.data.value ?? [];

// Computed values
const totalExpenses = computed(() => expenses.value.reduce((acc, expense) => acc + expense.actual_amount, 0));
const remainingBudget = computed(() => declaredBudget.value - totalExpenses.value);
const ratio = computed(() => (remainingBudget.value / declaredBudget.value) * 100);
const presentCategories = computed(() => Array.from(new Set(expenses.value.map((expense: Expense) => expense.category))).sort());
const groupedExpenses = computed(() => {
  const colors = [
    'rgba(54, 162, 235, 0.8)', //Accommodation
    'rgba(255, 99, 132, 0.8)', //Activities
    'rgba(255, 206, 86, 0.8)', //Food
    'rgba(201, 203, 207, 0.8)', //Others
    'rgba(75, 192, 192, 0.8)', //Transport
  ];

  return presentCategories.value.map((category: string, index: number) => {
    const total = expenses.value
      .filter((expense: Expense) => expense.category === category)
      .reduce((sum: number, expense: Expense) => sum + expense.actual_amount, 0);
    return { category, total, backgroundColor: colors[index % colors.length] };
  });
});

const color = computed(() => {
  switch (true) {
    case ratio.value > 50: return 'text-green-500 dark:text-green-400'
    case ratio.value > 30: return 'text-primary dark:text-primary'
    default: return 'text-red-500 dark:text-red-400'
  }
})

// Register components for the doughnut chart
Chart.register(DoughnutController, ArcElement, Tooltip, Legend);

// Ref for the chart canvas
const chartCanvas = ref(null);
let chartInstance : Chart | null = null;

// Data for the donut chart
const chartData = {
  labels: groupedExpenses.value.map((expense) => t(`budget.${expense.category.toLowerCase()}`)),
  datasets: [
    {
      label: t('budget.expenses'),
      data: groupedExpenses.value.map((expense) => expense.total),
      backgroundColor: groupedExpenses.value.map((expense) => expense.backgroundColor),
      hoverOffset: 15, // Makes segments expand on hover
    },
  ],
};
// Options for the donut chart
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    tooltip: {
      enabled: true,
      callbacks: {
         label: function (tooltipItem) {
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
};

onMounted(() => {
  if (chartCanvas.value) {
    chartInstance = new Chart(chartCanvas.value, {
      type: 'doughnut', // Specify the type as "doughnut"
      data: chartData,
      options: chartOptions,
    });
  }
});

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});
</script>

<template>
  <UCard>
     <template #header>
      <div class="h-8 header flex">
      <!--left -->
        <div class="flex-1 flex flex-col justify-center items-center">
          <div class="text-sm">{{ t('budget.initial-budget') }}</div>
          <div class="text-lg text-primary">{{declaredBudget}} € </div>
        </div>
        <!--right -->
        <div class="flex-1 flex flex-col justify-center items-center space-y-1">
           <div class="text-sm">{{ t('budget.remaining-budget') }}</div>
            <div class="text-lg" :class="color">{{remainingBudget}} € </div>
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
            @click="$router.push(`/home/trips/${tripId}/budget/edit`)"
            color="primary"
            icon="material-symbols-light:box-edit"
            :label="declaredBudget === 0 ? t('budget.declare-budget') : t('budget.edit-budget')"
            size="md"
            square
            variant="solid"
            class = "flex-1 flex items-center justify-center"
        />
        <UButton
            @click="$router.push(`/home/trips/${tripId}/budget/expenses`)"
            color="red"
            icon="material-symbols:analytics"
            :label="t('budget.manage-expenses')"
            size="md"
            square
            variant="solid"
            class = "flex-1 flex items-center justify-center"
        />
      </div>

    </template>
  </UCard>
</template>

<style scoped>
</style>