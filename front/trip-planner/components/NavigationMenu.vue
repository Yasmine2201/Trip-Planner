<script setup lang="ts">
const { t } = useI18n();
const authStore = useAuthStore();

const links = computed(() => {
  return [[
    {
      label: t('navigation.profile'),
      icon: "i-uil-user",
      to: "/home/profile/me"
    }
  ], [
    {
      label: t('navigation.my-trips'),
      icon: "material-symbols:trip-outline",
      to: "/home"
    },
    {
      label: t('navigation.last-trip'),
      icon: "heroicons:clock",
      to: "/home/last-trip"
    },
    {
      label: t('navigation.new-trip'),
      icon: "heroicons:plus",
      to: '/home/new-trip'
    }
  ],[{
    label: t('navigation.logout'),
    icon: "i-uil-signout",
    click: logout
  }
  ]];
});

const logout = async () => {
  await authStore.logout();
}

</script>

<template>
  <UVerticalNavigation
    :links="links"
    class="nav"
    :ui="{
      active: 'text-primary-500 dark:text-primary-400 font-medium',
      inactive: 'text-gray-500 dark:text-gray-400 font-normal',
    }"
  />
</template>

<style scoped>
.nav {
  padding: 1rem;
  height: 100%;
  box-shadow: 2px 1px 2px rgba(0, 0, 0, 0.1);
}
</style>