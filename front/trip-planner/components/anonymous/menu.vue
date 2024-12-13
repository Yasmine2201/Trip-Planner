<script setup lang="ts">
const links = [
  [
    {
      label: 'Accueil',
      to: '/'
    },
    {
      label: 'À propos',
      to: '/about'
    }
  ],
  [
    {
      label: 'Se connecter',
      to: '/login'
    },
    {
      label: 'Créer un compte',
      to: '/register'
    }
    ],
];
</script>

<template>
  <UHorizontalNavigation class="flex-grow" :links />
</template>