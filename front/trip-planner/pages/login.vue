<script setup lang="ts">

import type {FormSubmitEvent} from "#ui/types";
import type {LoginDto} from "~/schemas";
import { loginSchema } from '~/schemas';

const { t } = useI18n();
const auth = useAuthStore();

definePageMeta({
  title: 'Login',
  layout: false
});

const state = reactive({
  email: '',
  password: ''
});

const form = ref();
const submitting = ref(false);

const onSubmit = async ({ data }: FormSubmitEvent<LoginDto>) => {
  submitting.value = true;
  await auth.login(data.email, data.password);
  submitting.value = false;
};

</script>

<template>
  <NuxtLayout name="auth">
    <template #title>
      {{ t('auth.login-title') }}
    </template>

    <UForm :schema="loginSchema" :state class="space-y-3" @submit="onSubmit" ref="form">
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
          <span>{{ $t(error) }}</span>
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
          <span>{{ $t(error) }}</span>
        </template>
      </UFormGroup>

      <div class="flex justify-center">
        <UButton
            type="submit"
            color="primary"
            class="w-1/2 flex justify-center"
            :loading="submitting"
        >
          {{  t('auth.login-button') }}
        </UButton>
      </div>

    </UForm>
    <NuxtLink to="/register" class="text-center block mt-4 text-blue-600">
      {{ t('auth.no-account-yet') }}
    </NuxtLink>
  </NuxtLayout>
</template>

<style scoped>

</style>