<script setup lang="ts">
const colorMode = useColorMode();

const isDark = computed({
  get() {
    return colorMode.value === 'dark';
  },
  set() {
    colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark';
  }
});
</script>

<template>
  <div class="flex w-full justify-center">
    <NuxtLink to="/" class="flex items-center mr-3">
      <img
          src="/public/static/img/logo.png"
          alt="Logo TripPlanner"
          class="w-16 ml-1 mr-1"
      />
      <span class="text-primary text-xl ml-2 font-semibold">TripPlanner</span>
    </NuxtLink>

    <div class="flex-grow mx-8 content-center">
      <AnonymousMenu/>
    </div>

    <div class="flex items-center space-x-2 gap-4">
      <UButton
          :icon="isDark ? 'i-heroicons-moon-20-solid' : 'i-heroicons-sun-20-solid'"
          color="gray"
          size="xl"
          variant="ghost"
          aria-label="Theme"
          square
          @click="isDark = !isDark"
      />
    </div>
  </div>
</template>