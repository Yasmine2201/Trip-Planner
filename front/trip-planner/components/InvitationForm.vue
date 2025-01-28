<script setup lang="ts">
import {invitationSchema} from "~/schemas/invitation";
import {ref} from "vue";


const {t} = useI18n();
const toast = useToast();
const state = reactive({alias: ''});
const invitationLink = ref('');

const route = useRoute();
const tripId = ref(route.params.tripId);

const formError = ref('');
const emit = defineEmits(['invitation-created']);
const onSubmit = async () => {

  formError.value = '';
  invitationLink.value = '';
  const {data: users, error} = await useApiFetch(`/users`);
  console.log('Users:', users);
  console.log("error", error)
  if (error.value) {
    formError.value = 'errors.unknown-error';
  }

  else {
    const aliasExists = computed(() => users.value.some((user: any) => user.alias === state.alias));
    if (aliasExists.value) {
      const {data: invitation, error} = await useApiFetch(`/trips/${tripId.value}/invitations?alias=${state.alias}`, {
        method: 'POST'
      });
      if (error.value) {
        if (error.value.statusCode === 400) formError.value = 'errors.already-invited';
        else formError.value = 'errors.unknown-error';
      }
      else {
        const invitationData: Object = invitation.value;
         invitationLink.value = `localhost:3000/invitations/${invitationData.trip_invitation_id}`;
        emit('invitation-created', invitationLink.value);
        toast.add({
          title: t('notifications.type.invitation-created'),
          description: t('notifications.content.invitation-created'),
          icon: 'i-heroicons-check-badge',
          color: "green",
          timeout: 2000,
        })
        console.log('Invitation link:', invitationLink.value);
      }
    }
    else formError.value = 'errors.alias-not-exists';

  }
}

</script>

<template>
  <div class="space-y-3">
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
          variant="outline"
      />
      <UButton type="submit" color="primary" block>{{ t('misc.save') }}</UButton>
    </UForm>


  </div>
</template>

<style scoped>

</style>