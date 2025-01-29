<script setup lang="ts">
const auth = useAuthStore();
const isAuthenticated = computed(() => auth.isAuthenticated);
</script>

<template>
  <div class="flex justify-between items- w-full">
    <HeaderLogo :logo-link="isAuthenticated ? '/home' : '/'"/>

    <HeaderMenu/>

    <div class="flex items-center justify-end gap-4">
      <div class="flex items-center justify-end gap-4" v-if="isAuthenticated">
        <HeaderNotifications />
        <HeaderUserMenu :user="auth.user"/>
        <div class="w-0 h-10 border" />
      </div>

      <HeaderLocaleSwitcher/>
      <HeaderThemeSwitcher />
    </div>
  </div>
</template>