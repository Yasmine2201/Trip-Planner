<script setup lang="ts">

import {type BudgetDto, budgetSchema} from "~/schemas/expense";
import type {FormSubmitEvent} from "#ui/types";
import {ref} from "vue";
import {FetchError} from "ofetch";
import {number} from "zod";


const props = defineProps({
  budgetData: {type: number, default: 0},
})

const {$api} = useNuxtApp();
const {t} = useI18n();
const route = useRoute();
const tripId = ref(route.params.tripId);

const state = reactive({
  budget: props.budgetData
});

const formError = ref('');
const onSubmit = async ({data}: FormSubmitEvent<BudgetDto>) => {
  try {
    const sentData = JSON.stringify(
        {
          budget: data.budget
        }
    )
    await $api(`/trips/${tripId.value}/budget`, {
      method: 'PUT',
      body: sentData
    });
    navigateTo(`/home/trips/${tripId.value}/budget`);
  } catch (error) {
    if (error instanceof FetchError) {
      if (error.response.status === 400) formError.value = 'errors.sent-invalid-data';
    } else formError.value = 'errors.unknown-error';
  }

}

</script>

<template>
  <UForm :schema="budgetSchema" :state="state" @submit="onSubmit">
    <UFormGroup :label="t('budget.title')" class="w-1/2" name="budget" required>
      <UInput v-model="state.budget" :placeholder="t('budget.edit-budget')" type="number">
        <template #trailing>
          <span class="text-gray-500 dark:text-gray-400 text-xs">€</span>
        </template>
      </UInput>
      <template #error="{ error }">
        <span>{{ t(error) }}</span>
      </template>
    </UFormGroup>
    <UAlert
        v-if="formError !== ''"
        :description="t(formError)"
        :title="t('errors.oops')"
        class="mb-4 w-full"
        color="red"
        variant="outline"
    />
  </UForm>
</template>

<style scoped>

</style>