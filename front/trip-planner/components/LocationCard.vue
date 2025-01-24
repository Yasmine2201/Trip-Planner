<script lang="ts" setup>
import type {Location} from "~/types";

const props = defineProps<{
  location: Location,
  selected: boolean
}>();

const {t} = useI18n();

const minPrice = ref(undefined) as Ref<number | undefined>;
const maxPrice = ref(undefined) as Ref<number | undefined>;

if (props.location.prices.length > 0) {
  minPrice.value = Math.min(...props.location.prices.map(p => p.price));
  maxPrice.value = Math.max(...props.location.prices.map(p => p.price));
}

const priceRange = computed(() => {
  if (minPrice.value === undefined && maxPrice.value === undefined) {
    return t('locations.price_range.unknown');
  }

  let priceRange = '';
  priceRange += minPrice.value === undefined ? 'xxx' : minPrice.value.toLocaleString(undefined, {minimumFractionDigits: 2}) + '€';
  priceRange += '-';
  priceRange += maxPrice.value === undefined ? 'xxx' : maxPrice.value.toLocaleString(undefined, {minimumFractionDigits: 2}) + '€';
  return priceRange;
});

defineEmits<{
  onSelect: (location: Location) => Location
}>();

</script>

<template>
  <UCard :ui="{ body: { padding: 'p-0 sm:p-0' } }" class="w-full overflow-hidden p-0" :class="selected ? 'bg-gray-100 dark:bg-gray-800' : ''">
    <div class="flex items-center">
      <div class="flex-shrink-0 h-24 w-24">
        <img :src="location.pictures.length > 0 ? location.pictures[0].url : '/static/img/placeholder.jpg'"
             alt="Location image"
             class="h-24 w-24 object-cover">
      </div>
      <div class="ml-4 flex-1">
        <UTooltip :text="location.description">
          <div class="text-sm font-medium text-gray-900 dark:text-gray-100">{{ location.name }}</div>
        </UTooltip>
        <div class="text-sm text-gray-500 dark:text-gray-400">{{ priceRange }}</div>
        <div class="flex justify-center">
          <UButton class="min-w-24" color="primary"
                   @click="$emit('onSelect', location)"
                   :disabled="selected">
            <span class="w-full text-center">{{ t('misc.select') }}</span>
          </UButton>
        </div>
      </div>
    </div>
  </UCard>
</template>

<style scoped>

</style>