<script setup lang="ts">
const links = [
  [
    {
      label: 'Home',
      to: '/'
    },
    {
      label: 'About',
      to: '/about'
    }
  ],
  [
    {
      label: 'Login',
      to: '/login'
    },
    {
      label: 'Register',
      to: '/register'
    }
    ],
];
</script>

<template>
  <UHorizontalNavigation class="flex-grow" :links />
</template>