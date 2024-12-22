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
  <PageTitle :name="t('profile.title')" />

  <div class="flex flex-row gap-4">
    <div class="flex-col flex-1 basis-1/4">
      <UCard>
        <div class="flex justify-center">
          <img :src="authStore.user.avatarImage" alt="Logo TripPlanner" class="w-64 h-64 rounded-2xl" />
        </div>

        <div class="m-4">
          <p class="text-primary text-xl font-semibold">
            {{ `${authStore.user.firstname} ${authStore.user.lastname?.toUpperCase()}` }}
          </p>
          <p class="text-gray-500 dark:text-gray-400 text-md font-light mb-3">
            {{ authStore.user.email }}
          </p>
          <p class="h-4 text-lg">
            <span v-if="age"><span class="font-semibold">{{ t('profile.age') }}:</span> {{ age }} </span>
          </p>
          <p>
            <template>
              <LanguageBadges :languages="authStore.user.languages" />
              {{ authStore.user.languages }}
            </template>
          </p>
        </div>

      </UCard>
    </div>

    <div class="flex-col flex-1 basis-3/4">
      <UCard class="">
        text
      </UCard>
    </div>
  </div>
</template>

<style scoped>

</style>