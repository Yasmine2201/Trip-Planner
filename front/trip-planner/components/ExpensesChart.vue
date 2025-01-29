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
import {CategoryValues} from "~/schemas/expense";

const props = defineProps<{
  expenses: Expense[];
  predicate: (expense: Expense) => number;
}>();

const expenses = props.expenses;
const predicate = toRefs(props).predicate;

const route = useRoute();
const router = useRouter();
const tripId = ref(route.params.tripId);
const {t} = useI18n();


// Chart
const allCategories = Object.values(CategoryValues).sort();

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
    const total = expenses
        .filter((expense: Expense) => expense.category === category)
        .reduce((sum: number, expense: Expense) => sum + predicate.value(expense), 0);
    return {category, total, backgroundColor: colors[index % colors.length]};
  });
});
console.log("grouped expenses", groupedExpenses.value);

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

</script>

<template>
  <div class="h-100">

    <div v-if="expenses.length === 0" class="flex items-center justify-center h-full">
      <p>{{ t('expense.no-expenses') }}</p>
    </div>

    <div v-else class="chart-container">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </div>
</template>

<style scoped>
</style>