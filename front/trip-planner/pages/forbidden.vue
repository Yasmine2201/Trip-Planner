<script setup lang="ts">
definePageMeta({
  title: 'errors.page-not-found'
});

const { t } = useI18n();
const auth = useAuthStore();
</script>

<template>
  <div class="flex flex-col items-center gap-6">
    <h1 class="text-primary font-semibold text-4xl mt-6">{{ t('errors.page-forbidden') }}</h1>
    <UButton
        :to="auth.isAuthenticated ? '/home' : '/'"
        color="primary"
        icon="i-heroicons-home"
        :label="t('errors.go-home')"
        size="md"
        square
        variant="solid"
    />
  </div>
</template>

<style scoped>

</style>