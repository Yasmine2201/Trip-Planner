<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup lang="ts">
  const { $router } = useNuxtApp();
  const { t } = useI18n();

  const getTitle = computed(() => {
    const pageName = $router.currentRoute.value.meta.title;
    // console.log("PAGE: ", pageName);
    return `${t(pageName)} • TripPlanner`;
  });

  useHead({
    title: getTitle
  });
</script>
