<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup lang="ts">
  const { $router } = useNuxtApp();

  const getTitle = computed(() => {
    const pageName = $router.currentRoute.value.meta.title;
    return `${pageName} • TripPlanner`;
  });

  useHead({
    title: getTitle
  });
</script>
