<script lang="ts" setup>

import type {AsyncData} from "#app";
import type {Image, User} from "~/types";

definePageMeta({
  title: "profile.title",
  layout: "navigation",
  requiresAuth: true,
});

const {t} = useI18n();
const route = useRoute();
const router = useRouter();

type UserDto = {
  user_id: string;
  alias: string;
  first_name: string;
  profile_picture: Image | null;
  description: string | null;
  languages: string | null;
};

const {data: userDto}: AsyncData<UserDto, any> = await useApiFetch(`/users/${route.params.userId}`, {}, true);
const user = computed(() => ({
  id: userDto.value.user_id,
  alias: userDto.value.alias,
  firstname: userDto.value.first_name,
  avatarImage: userDto.value.profile_picture,
  description: userDto.value.description,
  languages: userDto.value.languages,
} as Partial<User>));

</script>

<template>
  <PageTitle :name="t('profile.title')">
    <template #actions>
      <UButton :title="t('misc.back')" class="mr-2" color="gray" icon="i-heroicons-arrow-uturn-left"
               @click="$router.back()"/>
    </template>
  </PageTitle>

  <UserProfile :user/>
</template>

<style scoped>

</style>