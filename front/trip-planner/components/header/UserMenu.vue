<script setup lang="ts">
import type {User} from "~/types";

const {t} = useI18n();
const authStore = useAuthStore();
const $router = useRouter();

const { user } = defineProps<{ user: User | null }>();

console.log("User", user);
const profileItems = computed(() => [
  [{
    slot: 'name',
    disabled: true
  }], [{
    label: t('navigation.home'),
    icon: 'heroicons:home',
    click: () => $router.push("/home")
  },
  {
    label: t('navigation.profile'),
    icon: 'i-uil-user',
    click: () => $router.push("/home/profile/me")
  },{
    label: t('navigation.logout'),
    icon: 'i-uil-signout',
    click: logout
    }],
]);

const logout = async () => {
  await authStore.logout();
}
</script>

<template>
  <UDropdown :items="profileItems" :ui="{ item: { disabled: 'cursor-text select-text' } }" :popper="{ placement: 'bottom-start' }">
    <UAvatar icon="i-uil-user" size="sm" :src="user?.avatarImage?.url" class="object-scale-down"/>

    <template #name="{ item }">
      <div class="text-left">
        <p class="text-black dark:text-white font-bold truncate">{{ `${authStore.user?.firstname} ${authStore.user?.lastname?.toUpperCase()}` }}</p>
        <p class="text-sm text-gray-900 dark:text-gray-100 truncate">{{ authStore.user?.email }}</p>
      </div>
    </template>
    <template #item="{ item }">
      <span class="truncate">{{ item.label }}</span>
      <UIcon :name="item.icon" class="flex-shrink-0 h-4 w-4 text-gray-400 dark:text-gray-500 ms-auto"/>
    </template>
  </UDropdown>
</template>

<style scoped>

</style>