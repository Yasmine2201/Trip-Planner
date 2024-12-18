<template>
  <div class="bg-gray-100 dark:bg-gray-900">
    <UContainer class="flex flex-col space-y-3 min-h-screen sm:px-24">
      <AuthenticatedHeader class="mt-2 mb-3" />
      <div class="flex-1">
        <NuxtPage />
      </div>
      <Footer class="mb-3" />
    </UContainer>
  </div>
</template>

<script setup lang="ts">
</script>