<script setup lang="ts">

import type { FormSubmitEvent } from "#ui/types";
import type { RegisterDto } from "~/schemas";
import { registerSchema } from "~/schemas";
import { FetchError } from "ofetch";

const { t } = useI18n();
const { $api } = useNuxtApp();

definePageMeta({
  title: 'auth.register-title',
  layout: false
});

const state = reactive({
  firstName: '',
  lastName: '',
  alias: '',
  birthdate: '',
  email: '',
  password: '',
  confirmPassword: ''
});

const form = ref();
const formError = ref('');
const submitting = ref(false);

const onSubmit = async ({ data }: FormSubmitEvent<RegisterDto>) => {
  submitting.value = true;
  formError.value = '';

  try {
    const sentData = JSON.stringify({
      firstName: data.firstName,
      lastName: data.lastName,
      alias: data.alias,
      birthdate: data.birthdate,
      emial: data.email,
      password: data.password
    });

    await $api('/auth/register', {
      method: 'POST',
      body: sentData
    })

    $router.push({path: '/login'});

  } catch (error) {
    if (error instanceof FetchError) {
      if (error.response.status === 400) {
        if (error.statusText === 'EMAIL_ALREADY_EXISTS') {
          formError.value = 'errors.already-have-account';
        } else if (error.statusText === 'PASSWORD_REJECTED') {
          formError.value = 'erros.password-rejected';
        } else if (error.statusText === 'INVALID_FORM') {
          formError.value = 'erros.invalid-form';
        }

        state.password = '';
        state.confirmPassword = '';
      } else {
        formError.value = 'errors.unknown-error';
      }
    }
  } finally {
    submitting.value = false;
  }
};

</script>

<template>
  <NuxtLayout name="auth">
    <template #title>
      {{ t('auth.register-title') }}
    </template>

    <UForm :schema="registerSchema" :state="state" class="space-y-3" @submit="onSubmit" ref="form">
      <UFormGroup
          :label="t('auth.first-name')"
          name="firstName"
          required
      >
        <UInput
            v-model="state.firstName"
            placeholder="John"
        />
        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>

      <UFormGroup
          :label="t('auth.last-name')"
          name="lastName"
          required
      >
        <UInput
            v-model="state.lastName"
            placeholder="Doe"
        />
        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>

      <UFormGroup
          :label="t('auth.alias')"
          name="alias"
          required
      >
        <UInput
            v-model="state.alias"
            placeholder="johndoe123"
        />
        <template #help>
          <span>{{ t('auth.alias-help') }}</span>
        </template>

        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>

      <UFormGroup
          :label="t('auth.birthdate')"
          name="birthdate"
      >
        <UInput
            v-model="state.birthdate"
            type="date"
        />
        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>

      <UFormGroup
          :label="t('auth.email')"
          name="email"
          required
      >
        <UInput
            v-model="state.email"
            placeholder="youremail@example.com"
        />
        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>

      <UFormGroup
          :label="t('auth.password')"
          name="password"
          required
      >
        <UInput
            v-model="state.password"
            type="password"
            placeholder="********"
        />
        <template #error="{ error }">
          <span>{{ t(error) }}</span>
        </template>
      </UFormGroup>

      <UFormGroup
          :label="t('auth.confirm-password')"
          name="confirmPassword"
          required
      >
        <UInput
            v-model="state.confirmPassword"
            type="password"
            placeholder="********"
        />
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

      <div class="flex justify-center">
        <UButton
            type="submit"
            color="primary"
            class="w-1/2 flex justify-center"
            :loading="submitting"
        >
          {{ t('auth.register-button') }}
        </UButton>
      </div>
    </UForm>

    <NuxtLink to="/login" class="text-center block mt-4 text-blue-600">
      {{ t('auth.already-have-account') }}
    </NuxtLink>
  </NuxtLayout>
</template>

<style scoped>
</style>
