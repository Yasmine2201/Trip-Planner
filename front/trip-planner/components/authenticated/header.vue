<script setup lang="ts">
const colorMode = useColorMode();
const { t } = useI18n();
const isDark = computed({
  get() {
    return colorMode.value === 'dark';
  },
  set() {
    colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark';
  }
});
// The logic for handling click events will be added later
const profileItems = [
    [{
    label: t('profile.personal-info'),
    icon: 'i-uil-user',
    click: () => {
      console.log('Edit')
    }
  }, {
    label: t('profile.preferences'),
    icon: 'i-heroicons-cog',
  }], [{
    label: t('profile.help-support'),
    icon: 'i-heroicons-question-mark-circle',
    click: () => {
      console.log('Help')
    }
  }],
  [
    {
    label: t('profile.logout'),
    icon: 'i-uil-signout',
    click: () => {
      console.log('Logout')
    }
  },
    {
    label: t('profile.delete-account'),
    icon: 'i-heroicons-trash',
    click: () => {
      console.log('Delete')
    }
  }]
];
// The logic for fetching the notifications will be added later
const notificaionItems = [
    [{
    label : t('profile.no-notifications'),
    }]
];
</script>

<template>
  <div class="flex justify-between items- w-full">
    <NuxtLink to="/" class="flex items-center mr-3">
      <img
          src="/public/static/img/logo.png"
          alt="Logo TripPlanner"
          class="w-16 ml-1 mr-1"
      />
      <span class="text-primary text-xl ml-2 font-semibold">TripPlanner</span>
    </NuxtLink>

    <div class="flex items-center justify-end gap-16">
      <!-- the logic for chip text will be added later -->
      <UDropdown :items="notificaionItems" :popper="{ placement: 'bottom-start' }">
        <UChip text ="0" size="2xl">
          <UButton icon="i-heroicons-bell" color="gray"/>
        </UChip>
      </UDropdown>

      <UDropdown :items="profileItems" :popper="{ placement: 'bottom-start' }">
        <UAvatar icon="i-uil-user" size="md"/>
      </UDropdown>

      <LocaleSwitcher/>
      <UButton
          :icon="isDark ? 'i-heroicons-moon-20-solid' : 'i-heroicons-sun-20-solid'"
          color="gray"
          size="xl"
          variant="ghost"
          aria-label="Theme"
          square
          @click="isDark = !isDark"
      />
    </div>

  </div>
</template>