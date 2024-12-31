<template>
  <div class="bg-gray-100 dark:bg-gray-900" flex>
    <UContainer class="flex flex-col space-y-3 min-h-screen sm:px-24">
      <Header class="mt-2 mb-3"/>
      <div class="flex-1 h-full flex flex-row pt-4">
        <div class="xl:w-1/5 lg:w-1/4 sm:w-1/3 h-full mr-4">
          <NavigationMenu class="h-full" />
        </div>
        <div class="xl:w-4/5 lg:w-3/4 sm:w-2/3">
          <NuxtPage />
        </div>
      </div>
      <Footer class="mb-3" />
    </UContainer>
  </div>
</template>

<script setup lang="ts">
</script>