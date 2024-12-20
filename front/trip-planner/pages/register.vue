<script setup lang="ts">

import type { FormSubmitEvent } from "#ui/types";
import type { RegisterDto } from "~/schemas";
import type { Error } from "~/types";
import { registerSchema } from "~/schemas";
import { FetchError } from "ofetch";

const { t } = useI18n();
const { $api } = useNuxtApp();

definePageMeta({
  title: 'auth.register-title',
  layout: false,
  middleware: 'anonymous'
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
    if (data.birthdate === '') {
      data.birthdate = null;
    } else {
      data.birthdate = new Date(data.birthdate).toDateString("yyyy-MM-dd");
    }

    const sentData = JSON.stringify({
      first_name: data.firstName,
      last_name: data.lastName,
      alias: data.alias,
      birthdate: data.birthdate,
      email: data.email,
      password: data.password
    });

    await $api('/auth/register', {
      method: 'POST',
      body: sentData
    })

    navigateTo('/login');

  } catch (error) {
    if (error instanceof FetchError) {
      console.log(error.response._data)
      if (error.response.status === 400) {
        const err: Error = error.response._data;
        switch (err.error_code) {
          case 'validation_failed':
            formError.value = 'errors.invalid-form'
            break;
          case 'user_already_exists':
            formError.value = 'errors.email-already-exists'
            break;
          case 'weak_password':
            formError.value = 'errors.password-rejected'
            break;
          default:
            formError.value = 'errors.unknown-error'
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
