<script setup lang="ts">
import {type EditProfilDto, editProfileSchema} from "~/schemas";
import type { FormSubmitEvent } from "#ui/types";

definePageMeta({
  title: "profile.title",
  requiresAuth: true,
});

const { t } = useI18n();
const authStore = useAuthStore();
const { $api } = useNuxtApp();

const form = ref();
const formError = ref('');
const submitting = ref(false);

const state = reactive({
  firstname: authStore.user.firstname,
  lastname: authStore.user.lastname,
  alias: authStore.user.alias,
  birthdate: authStore.user.birthdate,
  languages: authStore.user.languages?.split(',') ?? [],
  email: authStore.user.email,
  description: authStore.user.description
})

const onSubmit = async ({ data }: FormSubmitEvent<EditProfilDto>) => {
  submitting.value = true;
  console.log("Save with data: ", data);

  try {
    const user = {
      first_name: data.firstname,
      last_name: data.lastname,
      alias: data.alias,
      birthdate: data.birthdate,
      languages: data.languages.length ? data.languages.join(',') : null,
      description: data.description,
      user_id: authStore.user.id
    }

    await $api('/me', {
      method: 'PUT',
      body: JSON.stringify(user)
    });

    await authStore.refreshUser();

    navigateTo('/home/profile/me');

  } catch (e) {
    console.error(e);
    formError.value = 'errors.unknown-error';
  }

  submitting.value = false;
}

</script>

<template>
  <UForm :schema="editProfileSchema" :state="state" class="space-y-5" @submit="onSubmit" ref="form">
    <PageTitle :name="t('profile.title')">
      <template #actions>
        <UButton
            type="submit"
            color="primary"
            :loading="submitting"
            leading-icon="i-heroicons-check"
        >
          {{ t('misc.save') }}
        </UButton>
      </template>
    </PageTitle>

    <UCard class="h-full flex flex-col p-2">
      <div class="flex flex-wrap gap-6 mb-6">
        <UFormGroup :label="t('profile.first-name')" name="firstname" required class="flex-1 min-w-[420px]">
          <UInput v-model="state.firstname" />
        </UFormGroup>
        <UFormGroup :label="t('profile.last-name')" name="lastname" required class="flex-1 min-w-[420px]">
          <UInput v-model="state.lastname" />
        </UFormGroup>
      </div>

      <div class="flex flex-wrap gap-6 mb-6">
        <UFormGroup :label="t('profile.alias')" name="alias" required class="flex-1 min-w-[420px]">
          <UInput v-model="state.alias" />
        </UFormGroup>
        <UFormGroup :label="t('profile.birthdate')" name="birthdate" class="flex-1 min-w-[420px]">
          <UInput v-model="state.birthdate" type="date" />
        </UFormGroup>
      </div>

      <UFormGroup :label="t('profile.email')" name="email" required class="flex-1 min-w-[420px] mb-6">
        <UInput v-model="state.email" disabled />
      </UFormGroup>

      <UFormGroup :label="t('profile.languages')" name="languages" class="flex-1 min-w-[420px] mb-6">
        <LanguageSelector v-model="state.languages" ref="languageSelector" />
      </UFormGroup>

      <UFormGroup :label="t('profile.description')" name="description" class="flex-1 min-w-[420px]">
        <UTextarea v-model="state.description" autoresize :maxrows="10" />
      </UFormGroup>
    </UCard>

    <UAlert
        class="mb-4 w-full"
        v-if="formError !== ''"
        color="red"
        variant="outline"
        :title="t('errors.oops')"
        :description="t(formError)"
    />
  </UForm>
</template>

<style scoped>

</style>