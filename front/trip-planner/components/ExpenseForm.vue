<script lang="ts" setup>
import {useI18n} from "vue-i18n";
import {computed, reactive, ref} from "vue";
import {CategoryValues, type ExpenseDto, expenseSchema} from "~/schemas/expense";
import {Expense} from "~/types";
import type {FormSubmitEvent} from "#ui/types";
import {FetchError} from "ofetch";
import type {AsyncData} from "#app";

const props = defineProps<{
  mode: string,
  expenseData?: Expense
}>();


const {t} = useI18n();
const {$api} = useNuxtApp();
const route = useRoute();
const tripId = ref(route.params.tripId);
const visitIdStr = route.query?.visit_id as string | undefined;
const visitId = visitIdStr ? parseInt(visitIdStr) : undefined;

const getCategoryLabel = (category: string) => t(`expense.categories.${category.toLowerCase()}`);

const categoryOptions = computed(() => Object.values(CategoryValues).map(value => ({
      label: getCategoryLabel(value),
      value: value,
    }))
);

const visitOptions = ref([]);
const { data: visits }: AsyncData<Visit[], any> = await useApiFetch(`/trips/${tripId.value}/visits`)
visits.value = visits.value ?? [];
visitOptions.value = visits.value.map((visit) => ({
  label: visit.name,
  value: visit.visit_id,
}));


const default_state = {
  category: props.expenseData?.category || undefined,
  name: props.expenseData?.name || undefined,
  description: props.expenseData?.description || '',
  planned_amount: props.expenseData?.planned_amount || undefined,
  actual_amount: props.expenseData?.actual_amount || undefined,
  visit_id: props.expenseData?.visit?.visit_id || visitId,
};

const state = reactive(Object.assign({}, default_state));

const formError = ref('');

const onSubmit = async ({data}: FormSubmitEvent<ExpenseDto>) => {
  try {
    const sentData = JSON.stringify(
        {
          category: data.category,
          name: data.name,
          description: data.description,
          planned_amount: data.planned_amount,
          actual_amount: data.actual_amount,
          is_shared: false,
          visit_id: data.visit_id,
        }
    )
    if (props.mode === 'edit') {
      await $api(`/trips/${tripId.value}/budget/expenses/${props.expenseData.expense_id}`, {
        method: 'PUT',
        body: sentData
      });
    } else {
      await $api(`/trips/${tripId.value}/budget/expenses`, {
        method: 'POST',
        body: sentData
      });
    }

    navigateTo(`/home/trips/${tripId.value}/budget/expenses` as any);

  } catch (error) {
    if (error instanceof FetchError) {
      if (error.response.status === 400) formError.value = 'errors.sent-invalid-data';
    } else formError.value = 'errors.unknown-error';
  }
}

async function resetForm() {
  Object.assign(state, default_state);
  formError.value = '';
}
</script>

<template>
  <UForm :schema="expenseSchema" :state="state" class="space-y-5" @submit="onSubmit">
    <div class="flex w-full justify-between gap-8">
      <UFormGroup class="flex-1" :label="t('expense.name')" name="name" required>
        <UInput v-model="state.name" :placeholder="t('expense.placeholders.enter-name')"/>
        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>

      <UFormGroup :label="t('expense.category')" class="flex-1" name="category" required>
        <USelectMenu v-model="state.category" :options="categoryOptions" value-attribute="value">
          <template #label>
            <span v-if="state.category" class="truncate">{{ getCategoryLabel(state.category) }}</span>
            <span v-else class="text-gray-400 dark:text-gray-500">{{ t('expense.placeholders.select-category') }}</span>
          </template>
        </USelectMenu>
        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>
    </div>

    <UFormGroup :label="t('expense.description')" name="description">
      <UTextarea v-model="state.description" :placeholder="t('expense.placeholders.enter-description')" resize
                 rows="10"/>
      <template #error="{ error }">
        <span>{{ t(error) }}</span>
      </template>
    </UFormGroup>

    <div class="flex w-full justify-between gap-8">
      <UFormGroup :label="t('expense.planned-amount')" class="flex-1" name="planned_amount">
        <UInput v-model="state.planned_amount" :placeholder="t('expense.placeholders.enter-planned-amount')"
                type="number">
          <template #trailing>
            <span class="text-gray-500 dark:text-gray-400 text-xs">€</span>
          </template>
        </UInput>
        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>

      <UFormGroup :label="t('expense.actual-amount')" class="flex-1" name="actual_amount">
        <UInput v-model="state.actual_amount" :placeholder="t('expense.placeholders.enter-actual-amount')"
                type="number">
          <template #trailing>
            <span class="text-gray-500 dark:text-gray-400 text-xs">€</span>
          </template>
        </UInput>
        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>
    </div>

    <UFormGroup :label="t('expense.visit')" name="visit_id">
      <UInputMenu v-model="state.visit_id" :options="visitOptions" :placeholder="t('expense.placeholders.select-visit')"
                  value-attribute="value" />
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

    <div class="flex justify-center space-x-4">
      <UButton class="w-1/3 justify-center text-center" color="primary" type="submit">
        {{ t(props.mode === 'edit' ? 'expense.edit-expense' : 'expense.add-expense' as string) }}
      </UButton>
      <UButton class="w-1/3 justify-center text-center" color="gray" type="button" @click="resetForm">
        {{ t('misc.reinitialize') }}
      </UButton>
    </div>

  </UForm>
</template>

<style scoped>
</style>