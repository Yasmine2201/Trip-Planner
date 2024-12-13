<script setup lang="ts">

import type {FormSubmitEvent} from "#ui/types";
import { z } from 'zod';

const { t } = useI18n();

definePageMeta({
  title: 'Login',
  layout: false
});

const schema = z.object({
  email: z.string().email(t('login.error.emailInvalid')),
  password: z.string().nonempty(t('login.error.passwordRequired'))
});

type LoginDto = z.infer<typeof schema>;

const state = reactive({
  email: '',
  password: ''
});

const form = ref();
const submitting = ref(false);

const onSubmit = async ({ data }: FormSubmitEvent<LoginDto>) => {
  submitting.value = true;
  console.log(data);
  submitting.value = false;
};

</script>

<template>
  <NuxtLayout name="auth">
    <template #title>
      {{ t('login.title') }}
    </template>

    <UForm :schema :state class="space-y-3" @submit="onSubmit" ref="form">
      <UFormGroup
        :label="t('login.email')"
        name="email"
        required
      >
        <UInput
            v-model="state.email"
            placeholder="youremail@example.com"
        />
      </UFormGroup>

      <UFormGroup
        :label="t('login.password')"
        name="password"
        required
      >
        <UInput
            v-model="state.password"
            type="password"
            placeholder="********"
        />
      </UFormGroup>

      <div class="flex justify-center">
        <UButton
            type="submit"
            color="primary"
            class="w-1/2 flex justify-center"
            :loading="submitting"
        >
          Log in
        </UButton>
      </div>

    </UForm>
    <NuxtLink to="/register" class="text-center block mt-4 text-blue-600">
      Don't have an account? Register here.
    </NuxtLink>
  </NuxtLayout>
</template>

<style scoped>

</style>