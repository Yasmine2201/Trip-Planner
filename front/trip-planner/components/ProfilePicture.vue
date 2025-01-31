<script setup lang="ts">

import type {User} from "~/types";

const props = defineProps<{
  user: Partial<User>;
  canEdit: boolean;
}>();
const authStore = useAuthStore();

const userImageUrl = ref<string | null>(props.user?.avatarImage?.url || null);

const fileInput = ref<HTMLInputElement | null>(null);
const updatePorfilePicture = () => {
  fileInput.value?.click();
};

const onFileChange = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file && file.type === 'image/png') {
    console.log('File', file);
    const formData = new FormData();
    formData.append('image', file, file.name);

    const {data: response} = await useApiFetch('/images', {
      method: 'POST',
      body: formData,
      headers: {accept: 'application/json'},
    })

    // edit user
    const userPayload = {
      first_name: props.user?.firstname,
      last_name: props.user?.lastname,
      alias: props.user?.alias,
      birthdate: props.user?.birthdate,
      languages: props.user?.languages,
      description: props.user?.description,
      user_id: props.user?.id,
      profile_picture: response.value.image_id,
    }

    const {data: userResponse} = await useApiFetch('/me', {
      method: 'PUT',
      body: JSON.stringify(userPayload)
    });
    await authStore.refreshUser();
    console.log('User response', userResponse);
    userImageUrl.value = userResponse.value.profile_picture.url;
  }
}


</script>

<template>
  <div v-if="props.canEdit">
    <nuxt-img v-if="userImageUrl" :src="userImageUrl" alt="Profile picture"
              class="w-64 h-64 rounded-2xl object-cover"/>
    <nuxt-img v-else src="https://wallpapers.com/images/hd/funny-frog-pictures-4ad8ns1kjheffr5w.jpg"
              alt="Empty profile picture" class="w-64 aspect-1 rounded-2xl"/>

    <!-- Edit Button -->
    <input type="file" @change="onFileChange" accept="image/png" ref="fileInput" style="display: none;"/>
    <UButton
        icon="i-heroicons-pencil-square"
        @click="updatePorfilePicture"
        class="absolute bottom-2 right-2 bg-black/50 text-white p-2 rounded-full dark:bg-white/50 dark:text-black"
    />
  </div>
  <nuxt-img v-else :src="userImageUrl" alt="Profile picture" class="w-64 h-64 rounded-2xl object-cover"/>

</template>

<style scoped>

</style>