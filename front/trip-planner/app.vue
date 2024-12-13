<template>
  <div>
    {{ data }}
  </div>
</template>

<script lang="ts" setup>
console.log("HEY")
const { data } = await useFetch("http://localhost:8000/auth/");
</script>
