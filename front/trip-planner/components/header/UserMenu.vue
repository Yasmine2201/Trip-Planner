<script setup lang="ts">
const { t } = useI18n();
const authStore = useAuthStore();
const $router = useRouter();

const profileItems = computed(() => [
  [
    {
      label: t('navigation.profile'),
      icon: 'i-uil-user',
      click: () => { $router.push("/profile") }
    },
    // {
    //   label: t('profile.preferences'),
    //   icon: 'i-heroicons-cog',
    // },
    {
      label: t('navigation.logout'),
      icon: 'i-uil-signout',
      click: logout
    }
  ],
  // [
  //   {
  //     label: t('profile.help-support'),
  //     icon: 'i-heroicons-question-mark-circle',
  //     click: () => {
  //       console.log('Help')
  //     },
  //   },
  //   {
  //     label: t('profile.delete-account'),
  //     icon: 'i-heroicons-trash',
  //     click: () => {
  //       console.log('Delete')
  //     }
  //   }
  // ],
]);

const logout = async () => {
  await authStore.logout();
}
</script>

<template>
  <UDropdown :items="profileItems" :popper="{ placement: 'bottom-start' }">
    <UAvatar icon="i-uil-user" size="md"/>
  </UDropdown>
</template>

<style scoped>

</style>