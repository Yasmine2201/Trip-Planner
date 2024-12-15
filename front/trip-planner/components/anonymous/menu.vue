<script setup lang="ts">
const { t } = useI18n();

const links = computed(() => ([
  [
    {
      label: t('navigation.about'),
      to: '/about'
    }
  ],
  [
    {
      label: t('navigation.login'),
      to: '/login'
    },
    {
      label: t('navigation.register'),
      to: '/register'
    }
    ],
]));
</script>

<template>
  <UHorizontalNavigation class="flex-grow" :links />
</template>