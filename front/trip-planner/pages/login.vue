<script setup lang="ts">
  console.log("HEY")
  const { data } = await useFetch("http://localhost:8000/auth/");
</script>

<template>
  <div class="text-primary">
    {{ data }}
  </div>
</template>

<style scoped>

</style>