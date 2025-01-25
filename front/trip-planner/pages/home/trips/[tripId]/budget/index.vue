<script setup lang="ts">
definePageMeta({
  title: 'budget.title',
  requiresAuth: true,
  layout: 'navigation'
});


const { t } = useI18n();
const router = useRouter();
const tripId = Number(useRoute().params.tripId);

</script>

<template>
  <PageTitle :name="t('budget.title')">
    <template v-slot:actions>
      <UButton @click="router.push(`/home/trips/${tripId}`)" icon="i-heroicons-arrow-uturn-left" class="mr-2" :title="t('misc.back')" color="gray" />
    </template>
  </PageTitle>
  <Expenses />
</template>