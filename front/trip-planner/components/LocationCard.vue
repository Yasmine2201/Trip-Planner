<script lang="ts" setup>
import type {Location} from "~/types";

const props = defineProps<{
  location: Location
}>();

const {t} = useI18n();

const minPrice = ref(undefined) as Ref<number | undefined>;
const maxPrice = ref(undefined) as Ref<number | undefined>;

const priceRange = computed(() => {
  console.log(`Compute price range for ${props.location.name}: ${props.location.prices}`)
  if (props.location.prices.length > 0) {
    minPrice.value = Math.min(...props.location.prices.map(p => p.price));
    maxPrice.value = Math.max(...props.location.prices.map(p => p.price));
  } else {
    minPrice.value = undefined;
    maxPrice.value = undefined;
  }

  console.log(`minPrice: ${minPrice.value}, maxPrice: ${maxPrice.value}`);

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
  <UCard :ui="{ body: { padding: 'p-0 sm:p-0' } }"
         class="w-full overflow-hidden p-0 h-24 hover:bg-gray-200 hover:dark:bg-gray-800"
         @click="$emit('onSelect', location)"
  >
    <div class="flex">
      <div class="flex-shrink-0 h-24 w-24">
        <img :src="location.pictures.length > 0 ? location.pictures[0].url : '/static/img/placeholder.jpg'"
             alt="Location image"
             class="h-24 w-24 object-scale-down">
      </div>
      <div class="ml-4 flex-1 px-3 py-3">

        <div class="text-sm font-medium text-gray-900 dark:text-gray-100">{{ location.name }}</div>
        <div class="text-sm text-gray-500 dark:text-gray-400">{{ priceRange }}</div>
        <UTooltip :popper="{ placement: 'top' }" :text="location.description"
                  :ui="{
                          strategy: 'override',
                          base: '[@media(pointer:coarse)]:hidden max-h-96 px-2 py-1 text-xs font-normal relative',
        }">
          <div class="text-xs text-gray-500 dark:text-gray-400 h-8 overflow-hidden">{{ location.description }}</div>
        </UTooltip>
      </div>
    </div>
  </UCard>
</template>

<style scoped>

</style>