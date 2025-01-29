<script setup lang="ts">
import type {Invitation} from "~/types/invitation";

definePageMeta({
  title: "navigation.invitations",
  layout: "navigation",
  requiresAuth: true,
});

const {t, locale} = useI18n();
const router = useRouter();

const invitations = ref<Invitation[]>([]);

const invitationsReponse = await useApiFetch<Invitation[]>(`/invitations`)
invitations.value = invitationsReponse.data.value ?? [];

console.log(invitations.value);
const handleAccept = async (invitationId: number) => {
  const {data, status} = await useApiFetch(`/invitations/${invitationId}`, {
    method: 'PUT',
    body: JSON.stringify({
      status: true
    })
  });
  if (status.value === 'success') {
    invitations.value = invitations.value.filter((invitation) => invitation.trip_invitation_id !== invitationId);
    router.push(`/home/trips/${data.value.trip.trip_id}`);
  }

}

const handleDecline = async (invitationId: number) => {
  const {data, status} = await useApiFetch(`/invitations/${invitationId}`, {
    method: 'PUT',
    body: JSON.stringify({
      status: false
    })
  });
  if (status.value === 'success') {
    invitations.value = invitations.value.filter((invitation) => invitation.trip_invitation_id !== invitationId);
  }
}

</script>


<template>

  <ul class="space-y-4 max-h-96 overflow-y-auto">
    <transition-group name="invitation" tag="div" class="flex flex-col gap-2">
      <li v-for="invitation in invitations" :key="invitation.trip_invitation_id"
          class="flex justify-between items-center p-2 bg-white dark:bg-gray-800
          border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700">
        <div class="flex items-center">
          <UTooltip :title="invitation.sender.alias">
            <UAvatar icon="i-uil-user" size="sm" :src="invitation.sender.profile_picture?.url" class="mr-3"/>
          </UTooltip>
          <div>
            <div>
              <span class="font-bold text-primary"> {{ invitation.sender.first_name }}&nbsp;</span>
              <span> {{ t('share.invitation') }}&nbsp;</span>
              <UTooltip
                  :title="`${t('share.from')} ${new Date(invitation.trip.start_date).toLocaleDateString([locale], {dateStyle: 'full'})} ${t('share.to')} ${new Date(invitation.trip.end_date).toLocaleDateString([locale], {dateStyle: 'full'})}`">
                <span class="font-bold text-primary">{{ invitation.trip.trip_name }}&nbsp;</span>
              </UTooltip>
            </div>
          </div>
        </div>
        <div class="space-x-2 mr-2">
          <UTooltip :title="t('share.accept-invitation')">
            <UButton
                color="green"
                icon="i-heroicons-check"
                size="xs"
                square
                variant="solid"
                @click="handleAccept(invitation.trip_invitation_id)"
            />
          </UTooltip>
          <UTooltip :title="t('share.decline-invitation')">
            <UButton
                color="red"
                icon="i-heroicons-x-mark"
                size="xs"
                square
                variant="solid"
                @click="handleDecline(invitation.trip_invitation_id)"
            />
          </UTooltip>
        </div>
      </li>
    </transition-group>
  </ul>


</template>

<style scoped>
.invitation-enter-active, .invitation-leave-active {
  transition: all 0.5s ease;
}

.invitation-enter, .invitation-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}
</style>