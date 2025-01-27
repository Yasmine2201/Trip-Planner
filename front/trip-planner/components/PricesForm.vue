<script lang="ts" setup>
import type {Expense, LocationPrice} from "~/types";
import type {ExpenseDto} from "~/schemas/expense";
import type {FormSubmitEvent} from "#ui/types";

interface Props {
  tripId: number;
  visitId: number;
  prices: LocationPrice[];
}

type PriceLine = LocationPrice & { quantity: number };

type PriceForm = PriceLine[];

const {tripId, visitId, prices} = defineProps<Props>();

const priceLines = reactive<PriceLine[]>(prices.map((price) => ({...price, quantity: 0})));
const totalPrice = computed(() => {
  let total = 0;
  for (const price of priceLines) {
    total += price.price * price.quantity;
  }
  return total;
});

const emits = defineEmits<{
  onSave: (prices: PriceForm) => void
}>();

const { $api } = useNuxtApp();
const { t } = useI18n();

const columns = computed(() => [
  {
    key: 'price_name',
    label: t('locations.price.name'),
  },
  {
    key: 'price',
    label: t('locations.price.price'),
    direction: 'desc' as const
  },
  {
    key: 'inputs',
    label: t('visits.display.price-quantity')
  }
]);

const onSubmit = async ({ data }: FormSubmitEvent<PriceForm>) => {
  emits('onSave', data);
};

</script>

<template>
  <UForm :state="priceLines" @submit="onSubmit">
    <UTable :columns="columns"
            :empty-state="{ icon: 'i-heroicons-circle-stack-20-solid', label: t('locations.price.no-prices') }"
            :rows="priceLines"
            class="w-full border border-gray-300 dark:border-gray-700 rounded-lg mb-4"
    >
      <template #price_name-data="{ row }">
        <UTooltip
            :text="row.description ?? t('locations.price.no-description')"
            :ui="tooltipUi">
          <span class="mr-2 text-blue-600">&#9432;</span>
        </UTooltip>
        <span class="text-gray-600 dark:text-gray-300">{{ row.price_name }}</span>
      </template>
      <template #price-data="{ row }">
        <span class="text-gray-600 dark:text-gray-300">{{ row.price.toLocaleString(undefined, {minimumFractionDigits: 2}) }} €</span>
      </template>
      <template #inputs-data="{ row }">
        <UInput
            v-model="row.quantity"
            :label="t('visits.display.price-quantity')"
            :placeholder="t('visits.display.price-quantity')"
            type="number"
            class="w-24"
            min="0">
          <template #trailing>
            <span class="text-gray-500 dark:text-gray-400 text-xs">€</span>
          </template>
        </UInput>
      </template>
    </UTable>

    <div class="flex justify-between items-center mb-4">
      <span>{{ t('visits.display.total-price') }}</span>
      <span class="text-lg ml-2">{{ totalPrice.toLocaleString(undefined, {minimumFractionDigits: 2}) }} €</span>
    </div>
    <UButton block color="primary" type="submit">{{ t('misc.save') }}</UButton>
  </UForm>
</template>

<style scoped>

</style>
