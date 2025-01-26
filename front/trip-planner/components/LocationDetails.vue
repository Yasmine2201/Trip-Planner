<script lang="ts" setup>
import {type Location} from "~/types";

const props = defineProps<{
  location: Location;
}>();

const {t} = useI18n();

const columns = [
  {
    key: 'price_name',
    label: t('locations.price.name'),
  },
  {
    key: 'price',
    label: t('locations.price.price'),
    direction: 'desc' as const
  }
];

const tooltipUi = {
  strategy: 'override',
  base: '[@media(pointer:coarse)]:hidden max-h-96 px-2 py-1 text-xs font-normal relative',
}

</script>

<template>
  <div class="w-full max-h-64 flex gap-6">
    <div class="basis-1/3 grow flex flex-col gap-6 h-64">
      <h2 class="font-semibold text-lg">{{ location.name }}</h2>
      <UCarousel v-if="location.pictures.length > 0" v-slot="{ item }" :items="location.pictures"
                 :ui="{ item: 'basis-full justify-center items-start', container: 'bg-gray-800' }" arrows
                 class="rounded-lg overflow-hidden object-cover border border-gray-300 dark:border-gray-700"
                 indicators>
        <img :src="item.url" alt="item.name" class="h-52 object-contain rounded-lg" draggable="false">
      </UCarousel>
      <img v-else alt="Location image placeholder" class="w-full object-contain flex-1" draggable="false"
           src="/static/img/placeholder.jpg">
    </div>
    <div class="basis-2/3 grow flex flex-col">
      <MapViewer :lat="location.latitude" :lon="location.longitude" :popup="false" class="w-fullz-0"/>
    </div>
  </div>
  <div class="flex flex-row gap-6 mt-6">
    <div class="grow basis-3/5">
      <h3 class="font-semibold text-lg mb-2">{{ t('locations.description') }}</h3>
      <p>{{ location.description }}</p>
    </div>
    <div class="grow basis-2/5">
      <UTable :columns="columns"
              :empty-state="{ icon: 'i-heroicons-circle-stack-20-solid', label: t('locations.price.no-prices') }"
              :rows="location.prices"
              class="w-full border border-gray-300 dark:border-gray-700 rounded-lg"
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
      </UTable>
    </div>
  </div>
</template>

<style scoped>

</style>