<script lang="ts" setup>

import {ref} from "vue";
import type {PublicUser, Trip} from "~/types/";
import type {AsyncData} from "#app";

const {t} = useI18n();
definePageMeta({
  title: 'navigation.share-trip',
  requiresAuth: true,
  layout: 'navigation'
});

const route = useRoute();
const tripId = Number(route.params.tripId);

const {data: trip}: AsyncData<Trip, any> = await useApiFetch(`/trips/${tripId}`);
const members = ref<PublicUser[]>(trip.value.members);

const isOwner = (user: PublicUser) => user.user_id === trip.value.owner_id;

</script>

<template>

  <div class="flex justify-between items-center mb-10">
    <h1 class="text-xl mb-0">{{ t('share.headline') }}</h1>
    <InvitationForm/>
  </div>

  <ul class="space-y-2 h-full overflow-y-auto">
    <UCard v-for="member in members" :key="member.user_id" class="border border-gray-200 dark:border-gray-700">
      <div class="flex justify-between items-center">
        <div class="flex items-center gap-4">
          <UAvatar :src="member.profile_picture?.url" class="mr-3 object-scale-down" icon="i-uil-user" size="lg"/>
          <div>
            <div class="space-x-6 flex items-center"><span class="text-lg text-primary-500">{{ member.first_name }}</span>
              <UBadge v-if="isOwner(member)" color="primary" size="xs" variant="soft">{{ t('share.owner') }}</UBadge>
            </div>
            <span class="text-sm text-gray-500">{{ member.alias }}</span>
          </div>
        </div>
        <div class="space-x-2 mr-2">
          <UTooltip :title="t('share.see-profile')">
            <UButton
                :to="`/home/profile/${member.user_id}`"
                color="primary"
                icon="i-heroicons-eye"
                size="sm"
                square
                variant="solid"
            />
          </UTooltip>
        </div>
      </div>
    </UCard>
  </ul>
</template>

<style scoped>

</style>