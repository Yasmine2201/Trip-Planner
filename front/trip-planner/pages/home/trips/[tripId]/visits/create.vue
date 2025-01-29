<script lang="ts" setup>
import VisitForm from "~/components/VisitForm.vue";
import type {Location, Visit} from "~/types";

definePageMeta({
  title: 'navigation.create_visit',
  layout: "navigation",
  requiresAuth: true,
});

const {t} = useI18n();

const route = useRoute();
const router = useRouter();
const tripId = Number(route.params.tripId);
const visit = {
  trip_id: tripId
} as Partial<Visit>

onBeforeMount(() => {
  if (!tripId) {
    router.push('/home');
  }
});

const step = ref(1);
const pageTitle = computed(() => {
  return `${t('navigation.create_visit')} (${step.value}) : ${step.value === 1 ? t('locations.titles.select-location') : t('visits.title.finalize')}`;
});

const locationSelected = (location: Location) => {
  visit.location = location;
  step.value = 2;
}

const goBack = () => {
  if (step.value === 1) {
    router.back();
  } else {
    step.value = 1;
  }
}
</script>

<template>
  <PageTitle :name="pageTitle">
    <template v-slot:actions>
      <UButton :title="t('misc.back')" class="mr-2" color="gray" icon="i-heroicons-arrow-uturn-left"
               @click="goBack()"/>
    </template>
  </PageTitle>
  <VisitLocationSelector v-if="step === 1" :tripId="tripId" @onLocationSelected="locationSelected"/>
  <VisitForm v-if="step === 2" mode="create" :visit-data="visit" @changeLocation="step = 1" />
</template>
