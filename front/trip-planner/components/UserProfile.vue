<script setup lang="ts">
import type { User } from "~/types";

const { user } = defineProps<{
  user: Partial<User> | null;
}>();

const { t } = useI18n();

const age = computed(() => {
  if (!user?.birthdate) return null;
  const birthdate = new Date(user.birthdate);
  const ageDifMs = Date.now() - birthdate.getTime();
  const ageDate = new Date(ageDifMs);
  return Math.abs(ageDate.getUTCFullYear() - 1970);
});

</script>

<template>
  <div class="flex flex-row gap-4 mt-12">
    <div class="flex-col flex-1 basis-1/4">
      <UCard class="h-full">
        <div>
          <img v-if="user.avatarImage" :src="user.avatarImage?.url" alt="Profile picture" class="w-64 h-64 rounded-2xl object-cover" />
          <img v-else src="/public/static/img/empty-avatar.webp" alt="Empty profile picture" class="w-64 aspect-1 rounded-2xl" />
        </div>

        <div class="m-4">
          <p class="text-primary text-xl font-semibold mt-6">
            {{ `${user.firstname} ${user.lastname?.toUpperCase() ?? ''}` }}
          </p>
          <p class="text-gray-500 dark:text-gray-400 text-md font-light">
            {{ user.alias }}
          </p>
          <p class="h-4 text-lg mt-5 mb-10">
            <span v-if="age"><span class="font-semibold">{{ t('profile.age') }}:</span> {{ age }} </span>
          </p>
          <p>
            <LanguageBadges :languages="user.languages ?? undefined" />
          </p>
        </div>

      </UCard>
    </div>

    <div class="flex-col flex-1 basis-3/4">
      <UCard class="h-full">
        <div class="flex flex-row gap-4">
          <div class="flex-1">
            <h3 class="text-2xl font-semibold text-primary-500">{{ t('profile.informations') }}</h3>
            <div class="flex flex-col gap-2 mt-4">
              <p class="text-lg font-semibold">{{ t('profile.alias') }}</p>
              <p class="text-lg">{{ user.alias }}</p>
              <p class="text-lg font-semibold" v-if="user.email">{{ t('profile.email') }}</p>
              <p class="text-lg" v-if="user.email">{{ user.email }}</p>
              <p class="text-lg font-semibold" v-if="user.birthdate">{{ t('profile.birthdate') }}</p>
              <p class="text-lg" v-if="user.birthdate">{{ user.birthdate ? new Date(user.birthdate).toLocaleDateString() : t('profile.not-filled') }}</p>
              <p class="text-lg font-semibold">{{ t('profile.description') }}</p>
              <p class="text-lg overflow-y-auto h-48">{{ user.description ?? t('profile.not-filled') }}</p>
            </div>
          </div>
        </div>
      </UCard>
    </div>
  </div>
</template>

<style scoped>

</style>