<script setup lang="ts">
import {useI18n} from "vue-i18n";
import {ref, reactive, computed} from "vue";
import {CategoryValues, type ExpenseDto, expenseSchema} from "~/schemas/expense";
import type {FormSubmitEvent} from "#ui/types";
import {FetchError} from "ofetch";

const props = defineProps({
  mode: {type: String, required: true},
  expenseData: {type: Object, default: () => ({})},
});

const {t} = useI18n();
const {$api} = useNuxtApp();
const route = useRoute();
const tripId = ref(route.params.tripId);

const categoryOptions = computed(() => Object.values(CategoryValues).map(value => ({
      label: t(`expense.categories.${value.toLowerCase()}`),
      value: value,
    }))
);

const state = reactive({
  category: props.expenseData.category || undefined,
  name: props.expenseData.name || undefined,
  description: props.expenseData.description || undefined,
  planned_amount: props.expenseData.planned_amount || undefined,
  actual_amount: props.expenseData.actual_amount || undefined,
  is_shared: props.expenseData.is_shared || undefined,
  expense_group: props.expenseData.expense_group || undefined,
});

const formError = ref('');

const onSubmit = async ({data}: FormSubmitEvent<ExpenseDto>) => {
  try {
    if (data.planned_amount === undefined) {
      data.planned_amount = null;
    }
    if (data.expense_group === undefined) {
      data.expense_group = null;
    }
    if (data.description === undefined) {
      data.description = null;
    }
    const sentData = JSON.stringify(
        {
          category: data.category,
          name: data.name,
          description: data.description,
          planned_amount: data.planned_amount,
          actual_amount: data.actual_amount,
          is_shared: data.is_shared,
          expense_group: data.expense_group,
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

    navigateTo(`/home/trips/${tripId.value}/budget/expenses`);

  } catch (error) {
    if (error instanceof FetchError) {
      if (error.response.status === 400) formError.value = 'errors.sent-invalid-data';
    } else formError.value = 'errors.unknown-error';
  }
}

async function resetForm() {
  Object.assign(state, {
    category: '',
    name: '',
    description: '',
    planned_amount: undefined,
    actual_amount: undefined,
    is_shared: undefined,
    expense_group: '',
  });
  formError.value = '';
}
</script>

<template>
  <NuxtLayout name="auth">
    <template #title>
      {{ t(props.mode === 'edit' ? 'expense.edit-expense' : 'expense.add-expense') }}
    </template>

    <UForm :schema="expenseSchema" :state="state" class="space-y-5" @submit="onSubmit">
      <UFormGroup name="category" :label="t('expense.category')" required>
        <USelectMenu v-model="state.category" :options="categoryOptions" value-attribute="value"
                     :placeholder="t('expense.placeholders.select-category')"/>
        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>

      <UFormGroup name="name" label="Name" required>
        <UInput v-model="state.name" :placeholder="t('expense.placeholders.enter-name')"/>
        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>

      <UFormGroup name="description" :label="t('expense.description')">
        <UTextarea v-model="state.description" :placeholder="t('expense.placeholders.enter-description')"/>
        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>

      <UFormGroup name="planned_amount" :label="t('expense.planned-amount')">
        <UInput v-model="state.planned_amount" type="number"
                :placeholder="t('expense.placeholders.enter-planned-amount')"/>
        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>

      <UFormGroup name="actual_amount" :label="t('expense.actual-amount')" required>
        <UInput v-model="state.actual_amount" type="number"
                :placeholder="t('expense.placeholders.enter-actual-amount')"/>
        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>

      <UFormGroup name="is_shared" :label="t('expense.is-shared')" required>
        <UCheckbox v-model="state.is_shared" :checked="false"/>
        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>

      <UFormGroup name="expense_group" :label="t('expense.expense-group')">
        <UInput v-model="state.expense_group" :placeholder="t('expense.placeholders.select-expense-group')"/>
        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>

      <UAlert
          class="mb-4 w-full"
          v-if="formError !== ''"
          color="red"
          variant="outline"
          :title="t('errors.oops')"
          :description="t(formError)"
      />

      <div class="flex justify-center space-x-4">
        <UButton type="submit" color="primary" class="w-1/3 justify-center text-center">
          {{ t(props.mode === 'edit' ? 'expense.edit-expense' : 'expense.add-expense') }}
        </UButton>
        <UButton type="button" color="gray" class="w-1/3 justify-center text-center" @click="resetForm">
          {{ t('misc.reinitialize') }}
        </UButton>
      </div>

    </UForm>
  </NuxtLayout>
</template>

<style scoped>
</style>