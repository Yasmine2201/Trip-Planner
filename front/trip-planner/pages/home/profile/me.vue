<script setup lang="ts">
definePageMeta({
  title: "profile.title"
});

const { t } = useI18n();
const authStore = useAuthStore();

const age = computed(() => {
  if (!authStore.user?.birthdate) return null;
  const birthdate = new Date(authStore.user.birthdate);
  const ageDifMs = Date.now() - birthdate.getTime();
  const ageDate = new Date(ageDifMs);
  return Math.abs(ageDate.getUTCFullYear() - 1970);
});

</script>

<template>
  <PageTitle :name="t('profile.title')">
    <template #actions>
      <UButton icon="i-heroicons-pencil-square" @click="$router.push('/home/profile/edit')">
        {{ t('profile.edit') }}
      </UButton>
    </template>
  </PageTitle>

  <div class="flex flex-row gap-4 mt-12">
    <div class="flex-col flex-1 basis-1/4">
      <UCard class="h-full">
        <div class="flex justify-center">
          <img v-if="authStore.user.avatarImage" :src="authStore.user.avatarImage" alt="Profile picture" class="w-64 h-64 rounded-2xl" />
          <img v-else src="/public/static/img/empty-avatar.webp" alt="Empty profile picture" class="w-64 h-64 rounded-2xl" />
        </div>

        <div class="m-4">
          <p class="text-primary text-xl font-semibold mt-6">
            {{ `${authStore.user.firstname} ${authStore.user.lastname?.toUpperCase()}` }}
          </p>
          <p class="text-gray-500 dark:text-gray-400 text-md font-light">
            {{ authStore.user.alias }}
          </p>
          <p class="h-4 text-lg mt-5 mb-10">
            <span v-if="age"><span class="font-semibold">{{ t('profile.age') }}:</span> {{ age }} </span>
          </p>
          <p>
            <LanguageBadges :languages="authStore.user.languages" />
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
              <p class="text-lg">{{ authStore.user.firstname }}</p>
              <p class="text-lg font-semibold">{{ t('profile.email') }}</p>
              <p class="text-lg">{{ authStore.user.email }}</p>
              <p class="text-lg font-semibold">{{ t('profile.birthdate') }}</p>
              <p class="text-lg">{{ authStore.user.birthdate ? new Date(authStore.user.birthdate).toLocaleDateString() : t('profile.not-filled') }}</p>
              <p class="text-lg font-semibold">{{ t('profile.description') }}</p>
              <p class="text-lg overflow-y-auto h-48">{{ authStore.user.description ?? t('profile.not-filled') }}</p>
            </div>
          </div>
        </div>
      </UCard>
    </div>
  </div>
</template>

<style scoped>

</style>