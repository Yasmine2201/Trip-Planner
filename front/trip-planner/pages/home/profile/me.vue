<script setup lang="ts">
import UserProfile from "~/components/UserProfile.vue";

definePageMeta({
  title: "profile.title",
  layout: "navigation",
  requiresAuth: true,
});

const { t } = useI18n();
const authStore = useAuthStore();


</script>

<template>
  <PageTitle :name="t('profile.title')">
    <template #actions>
      <UButton icon="i-heroicons-pencil-square" @click="$router.push('/home/profile/edit')">
        {{ t('profile.edit') }}
      </UButton>
    </template>
  </PageTitle>

  <UserProfile :user="authStore.user" />
</template>

<style scoped>

</style>