<script setup lang="ts">
definePageMeta({
  title: 'app.name'
});

useRouter().push(useAuthStore().isAuthenticated ? '/home' : '/login');
</script>

<template>

</template>

<style scoped>

</style>