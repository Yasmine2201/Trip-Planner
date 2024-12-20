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
  <UButton
      :icon="isDark ? 'i-heroicons-moon-20-solid' : 'i-heroicons-sun-20-solid'"
      color="gray"
      size="xl"
      variant="ghost"
      aria-label="Theme"
      square
      @click="isDark = !isDark"
  />
</template>

<style scoped>

</style>