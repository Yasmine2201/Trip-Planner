<script setup lang="ts">
defineProps<{
  name: string,
  icon?: string,
}>();
</script>

<template>
  <div class="flex mb-5 gap-2 items-center text-primary-500">
    <UIcon v-if="icon" :name="icon" class="w-8 h-8" />
    <h3 class="text-3xl font-semibold text-gray-700 dark:text-gray-200">
      {{ name }}
    </h3>
    <div class="flex-1 flex justify-end gap-2">
      <slot name="actions" />
    </div>
  </div>
</template>

<style scoped>

</style>