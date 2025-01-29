<script setup lang="ts">
import type {Trip} from "~/types";

const { t } = useI18n();
const authStore = useAuthStore();

const route = useRoute();
const router = useRouter();
const selectedTripId = computed(() => route.params.tripId);
const path = computed(() => route.path);

const links = computed(() => {
  const baseLinks = [
    [
      {
        label: t('navigation.profile'),
        icon: "i-uil-user",
        to: "/home/profile/me",
      },
      {
      label: t('navigation.invitations'),
      icon: 'ic:outline-markunread-mailbox',
      to: "/home/invitations"
    }
    ],
    [
      {
        label: t('navigation.my-trips'),
        icon: "material-symbols:trip-outline",
        to: "/home",

      },
      {
        label: t('navigation.last-trip'),
        icon: "heroicons:clock",
        click: navigateToLastTrip,
        active: route.path === '/home/trips/last'
      },
      {
        label: t('navigation.new-trip'),
        icon: "heroicons:plus",
        to: '/home/trips/create',
      }
    ]

  ];

  if (selectedTripId.value) {
    baseLinks.push([
      {
        label: t('trip_home.trip_details'),
        icon: "icon-park-twotone:acceleration",
        to: `/home/trips/${selectedTripId.value}`
      },
      {
        label: t('trip_home.visits'),
        icon: "icon-park-twotone:beach-umbrella",
        to: `/home/trips/${selectedTripId.value}/visits`
      },
      {
        label: t('trip_home.budget'),
        icon: "material-symbols:currency-exchange",
        to: `/home/trips/${selectedTripId.value}/budget`
      },
      {
        label: t('trip_home.share'),
        icon: "ic:baseline-people-alt",
        to: `/home/trips/${selectedTripId.value}/members`
      }
    ]);
  }

  baseLinks.push([
    {
      label: t('navigation.logout'),
      icon: "i-uil-signout",
      click: logout
    }
  ]);

  return baseLinks;
});


const logout = async () => {
  await authStore.logout();
};

const navigateToLastTrip = async () => {
  const tripResponse = await useApiFetch<Trip>(`/trips/last`);
  const lastTripId = tripResponse.data.value?.trip_id;

  if (!lastTripId) {
    return;
  }

  router.push(`/home/trips/${lastTripId}`);
};

</script>

<template>
  <UVerticalNavigation
    :links="links"
    class="nav border-r border-gray-300 dark:border-gray-700"
    :ui="{
      active: 'text-primary-500 dark:text-primary-400 font-medium',
      inactive: 'text-gray-500 dark:text-gray-400 font-normal',
    }"
  />
</template>

<style scoped>
.nav {
  padding: 1rem;
  height: 100%;
}
</style>