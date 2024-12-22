<script setup lang="ts">
defineProps<{
  logoLink: string,
}>();
</script>

<template>
  <NuxtLink :to="logoLink" class="flex items-center mr-3">
    <img
        src="/public/static/img/logo.png"
        alt="Logo TripPlanner"
        class="w-16 ml-1 mr-1"
    />
    <span class="text-primary text-xl ml-2 font-semibold">TripPlanner</span>
  </NuxtLink>
</template>

<style scoped>

</style>