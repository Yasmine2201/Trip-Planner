<script setup lang="ts">
import type {Trip} from "~/types";
import {onMounted, ref} from "vue";

const { t } = useI18n();
const router = useRouter();
definePageMeta({
  title: 'navigation.last-trip',
  layout: 'navigation'
});

const lastTrip = ref<Trip | null>(null);
onMounted(async () => {

  const tripResponse = await useApiFetch<Trip>(`/trips/last`);
  lastTrip.value = tripResponse.data.value;

  router.push(`/home/trips/${lastTrip.value?.trip_id}`);

});

</script>
<template>

</template>



