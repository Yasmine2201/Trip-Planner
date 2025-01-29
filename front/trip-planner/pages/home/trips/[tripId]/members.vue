<script setup lang="ts">

import {ref} from "vue";
import type {PublicUser} from "~/types/invitation";

const {t} = useI18n();
definePageMeta({
  title: 'navigation.share-trip',
  requiresAuth: true,
  layout: 'navigation'
});

const route = useRoute();
const tripId = ref(route.params.tripId);

const members = ref<PublicUser[]>([]);
const membersResponse = await useApiFetch<PublicUser[]>(`/trips/${tripId.value}/members`);
members.value = membersResponse.data.value ?? [];

</script>

<template>

  <div class="flex justify-between items-center mb-10">
    <h1 class="text-xl mb-0">{{ t('share.headline') }}</h1>
    <InvitationForm/>
  </div>

  <ul class="space-y-4 max-h-96 overflow-y-auto">
    <UCard v-for="member in members" :key="member.user_id" class="border border-gray-200 dark:border-gray-700">
      <div class="flex justify-between items-center">
        <div class="flex items-center">
          <UAvatar icon="i-uil-user" size="sm" :src="member.profile_picture?.url" class="mr-3"/>
          <div>
            <span class="text-lg text-primary-500">{{ member.first_name }}</span>
            <br>
            <span class="text-sm text-gray-500">{{ member.alias }}</span>
          </div>
        </div>
        <div class="space-x-2 mr-2">
          <UTooltip :title="t('share.see-profile')">
            <UButton
                color="primary"
                icon="i-heroicons-eye"
                size="sm"
                square
                variant="solid"
                :to="`/home/profile/${member.user_id}`"
            />
          </UTooltip>
<!--          <UTooltip :title="t('share.delete-from-trip')">-->
<!--            <UButton-->
<!--                color="red"-->
<!--                icon="i-heroicons-trash"-->
<!--                size="sm"-->
<!--                square-->
<!--                variant="solid"-->
<!--            />-->
<!--          </UTooltip>-->
        </div>
      </div>
    </UCard>
  </ul>


</template>


<style scoped>

</style>