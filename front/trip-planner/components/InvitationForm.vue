<script setup lang="ts">
import {invitationSchema} from "~/schemas/invitation";
import {ref} from "vue";


const {t} = useI18n();
const toast = useToast();
const state = reactive({alias: ''});

const route = useRoute();
const tripId = ref(route.params.tripId);

const formError = ref('');
const onSubmit = async () => {

  formError.value = '';
  const {data: users, error} = await useApiFetch(`/users`);
  console.log('Users:', users);
  console.log("error", error)
  if (error.value) {
    formError.value = 'errors.unknown-error';
  } else {
    const aliasExists = computed(() => users.value.some((user: any) => user.alias === state.alias));
    if (aliasExists.value) {
      const {data: invitation, error} = await useApiFetch(`/trips/${tripId.value}/invitations?alias=${state.alias}`, {
        method: 'POST'
      });
      if (error.value) {
        if (error.value.statusCode === 400) formError.value = 'errors.already-invited';
        else formError.value = 'errors.unknown-error';
      } else {
        toast.add({
          title: t('notifications.type.invitation-created'),
          description: t('notifications.content.invitation-created'),
          icon: 'i-heroicons-check-badge',
          color: "green",
          timeout: 2000,
        })
        isOpen.value = false;
      }

    } else formError.value = 'errors.alias-not-exists';

  }
}
const isOpen = ref(false);
</script>

<template>
  <div class="space-y-3">
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

        <UForm :schema="invitationSchema" :state="state" @submit="onSubmit">
          <UFormGroup :label="t('share.alias')" name="alias" class="mb-4" required>
            <UInput v-model="state.alias" :placeholder="t('share.placeholder')"/>
            <template #error="{ error }">
              <span>{{ t(error) }}</span>
            </template>
          </UFormGroup>
          <UAlert
              v-if="formError !== ''"
              :description="t(formError)"
              :title="t('errors.oops')"
              class="mb-4 w-full"
              color="red"
              variant="outline"/>
          <UButton type="submit" color="primary" block>{{ t('misc.save') }}</UButton>
        </UForm>

      </UCard>
    </UModal>

  </div>
</template>

<style scoped>

</style>