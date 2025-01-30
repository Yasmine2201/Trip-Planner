<script setup lang="ts">
const { t } = useI18n();
const auth = useAuthStore();

const isAuthenticated = computed(() => auth.isAuthenticated);

const links = computed(() => ([
  [
  ],
  isAuthenticated.value ? [] : [
    {
      label: t('navigation.login'),
      to: '/login'
    },
    {
      label: t('navigation.register'),
      to: '/register'
    }
  ]
]));
</script>

<template>
  <div class="flex-grow mx-8 content-center">
    <UHorizontalNavigation class="flex-grow" :links />
  </div>
</template>