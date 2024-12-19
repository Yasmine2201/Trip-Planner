<template>
  <div class="bg-gray-100 dark:bg-gray-900">
    <UContainer class="flex flex-col space-y-3 min-h-screen sm:px-24">
      <Header class="mt-2 mb-3" />
      <div class="flex-1 flex items-center justify-center">
        <UCard class="auth-layout">
          <template #header>
            <h1 class="text-4xl font-bold text-primary text-center">
              <slot name="title"></slot>
            </h1>
          </template>
          <slot />
        </UCard>
      </div>
      <Footer class="mb-3" />
    </UContainer>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
  .auth-layout {
    min-width: max-content;
    flex-basis: 70%;
  }
</style>