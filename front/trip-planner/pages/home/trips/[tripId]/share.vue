<script setup lang="ts">

import {ref} from "vue";

definePageMeta({
  title: 'navigation.share-trip',
  requiresAuth: true,
  layout: 'navigation'
});
const props = defineProps({
  invitationLink: {type: String, default: ''}
})
const {t} = useI18n();
const toast = useToast();


/* to be deleted later */
const friends = [
  {
    id: 1,
    name: 'John Doe',
    avatar: 'https://randomuser.me/api/portraits/men/1.jpg',
    alias: 'johnny'
  },
  {
    id: 2,
    name: 'Jane Smith',
    avatar: 'https://randomuser.me/api/portraits/women/2.jpg',
    alias: 'jane'
  },
  {
    id: 3,
    name: 'Alice Johnson',
    avatar: 'https://randomuser.me/api/portraits/women/3.jpg',
    alias: 'alice'
  },
]
const invitationLink = ref('');
const handleInvitationCreated = (link: string) => {
  invitationLink.value = link;
  console.log('Invitation link received from child:', link);
};
const copyToClipboard = () => {
  navigator.clipboard.writeText(invitationLink.value).then(() => {
    toast.add({
      title: t('misc.copied'),
      icon: 'i-heroicons-check-badge',
      color: "green",
      timeout: 2000,
    });
  });
};
const isOpen = ref(false);
watch(isOpen, (newVal) => {
  if (!newVal) {
    invitationLink.value = '';
  }
});
</script>

<template>

  <div class="flex justify-between items-center mb-10">
    <h1 class="text-xl mb-0">{{ t('share.headline') }}</h1>
    <div>
      <UButton icon="i-heroicons-envelope" :label="t('share.invite')" size="sm" color="primary" variant="solid"
               @click="isOpen = true"/>
      <UModal v-model="isOpen">
        <UCard :ui="{ ring: '', divide: 'divide-y divide-gray-100 dark:divide-gray-800' }">
          <PageTitle :name="t('share.invite')">
            <template #actions>
              <UButton color="gray" variant="ghost" icon="i-heroicons-x-mark-20-solid" class="-my-1"
                       @click="isOpen = false"/>
            </template>
          </PageTitle>

          <InvitationForm @invitation-created="handleInvitationCreated"/>
          <template #footer v-if="invitationLink">
            <div class="flex justify-between items-center">
              <span>{{ t('share.link') }}:</span>
              <div class="space-x-1">
                <span class="text-white">{{ invitationLink }}</span>
                <UButton
                    icon="material-symbols:content-copy"
                    @click="copyToClipboard"
                    size="xs" color="primary"
                    variant="solid"/>
              </div>

            </div>
          </template>

        </UCard>
      </UModal>

    </div>
  </div>
  <ul class="space-y-4 max-h-96 overflow-y-auto">
    <li v-for="friend in friends" :key="friend.id"
        class="flex justify-between items-center p-2 border border-gray-700 rounded-lg hover:bg-gray-800 ">
      <div class="flex items-center">
        <img :src="friend.avatar" alt="Avatar" class="w-10 h-10 rounded-full mr-3">
        <div>
          <span class="text-lg text-primary-500">{{ friend.name }}</span>
          <br>
          <span class="text-sm text-gray-500">{{ friend.alias }}</span>
        </div>
      </div>
      <div class="space-x-2 mr-2">
        <UTooltip :title="t('share.see-profile')">
          <UButton
              color="primary"
              icon="i-heroicons-eye"
              size="xs"
              square
              variant="solid"
          />
        </UTooltip>
        <UTooltip :title="t('share.delete-from-trip')">
          <UButton
              color="red"
              icon="i-heroicons-trash"
              size="xs"
              square
              variant="solid"
          />
        </UTooltip>
      </div>
    </li>
  </ul>


</template>


<style scoped>

</style>