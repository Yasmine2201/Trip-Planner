<script lang="ts" setup>
import {useI18n} from 'vue-i18n';
import type {Trip} from '~/types';
import MapViewer from "~/components/MapViewer.vue";
import type {AsyncData} from "#app";

definePageMeta({
  title: 'trip_home.trip_details',
  requiresAuth: true,
  layout: 'navigation'
});
const {t, locale} = useI18n();
const route = useRoute();
const router = useRouter();
const toast = useToast();
const user = useAuthStore().user;

const tripId = ref(route.params.tripId);
const { data: trip, status, error }: AsyncData<Trip, any> = await useApiFetch<Trip>(`/trips/${tripId.value}`);

if (status.value === 'error' && error.value.statusCode === 404) {
  router.push('/notfound');
}

const town = ref('');
const country = ref('');

const getLocationDetails = async (trip: Trip) => {

  try {
    const response = await useFetch(
        `https://nominatim.openstreetmap.org/reverse?lat=${trip.latitude}&lon=${trip.longitude}&format=json&addressdetails=1`
    );

    const address = response.data.value.address;

    town.value = address.village ?? address.town ?? address.city ?? address.municipality ?? address.county ?? address.state ?? address.region ?? "";
    country.value = address.country ?? address.continent ?? "";
  } catch (error) {
    console.error('Error fetching location details:', error);
  }
};


onMounted(async () => {
  await getLocationDetails(trip.value as Trip)
});

const deleteTrip = async (tripId: number) => {
  const { status } = await useApiFetch(`/trips/${tripId}`, {
    method: 'DELETE'
  });

  if (status.value === 'success') {
    router.push('/home');
    toast.add({
      title: t('misc.delete'),
      description: t('misc.success'),
      icon: 'i-heroicons-check-badge',
      color: "green",
      timeout: 2000
    });
  } else {
    toast.add({
      title: t('misc.delete'),
      description: t('misc.error'),
      icon: 'i-heroicons-x-circle',
      color: "red",
      timeout: 2000
    });
  }
};

const formatDate = (date: string | null) => {
  if (!date) {
    return '';
  }
  return new Date(date).toLocaleDateString([locale.value], { dateStyle: 'full' });
};

</script>

<template>
  <div class="overflow-x-auto">
    <PageTitle :name="t('trip_home.trip_details')">
      <template #actions>
        <UButton @click="router.push(`/home/`)" icon="i-heroicons-arrow-uturn-left" class="mr-2" :title="t('misc.back')" color="gray" />
        <div class="flex gap-2" v-if="trip.owner_id === user.id">
          <UButton
              :to="`/home/trips/${trip.trip_id}/edit`"
              color="primary"
              icon="i-heroicons-pencil-square"
              :label="t('misc.edit')"
              size="md"
              square
              variant="solid"
          />
          <ConfirmationDropdown @confirm="deleteTrip(trip.trip_id)">
            <UButton
                color="red"
                icon="i-heroicons-trash"
                :label="t('misc.delete')"
                size="md"
                square
                variant="solid"
            />
          </ConfirmationDropdown>
        </div>
      </template>
    </PageTitle>

    <div class="flex space-x-3 mb-4 justify-end">

    </div>
    <table class="table-auto border-collapse w-full bg-white dark:bg-gray-800 shadow-md rounded-lg">

      <tbody>
      <tr>
        <th class="w-48"></th>
        <th></th>
      </tr>
      <!-- Nom du voyage -->
      <tr class="border-t dark:border-gray-700">
        <td class="px-6 py-4 text-gray-800 dark:text-gray-100 text-sm font-medium">
          {{ t('create_trip.trip_name') }}
        </td>
        <td class="px-6 py-4 text-gray-700 dark:text-gray-300 text-sm">
          {{ trip?.trip_name }}
        </td>
      </tr>
      <!-- Date de début -->
      <tr class="border-t dark:border-gray-700">
        <td class="px-6 py-4 text-gray-800 dark:text-gray-100 text-sm font-medium">
          {{ t('create_trip.trip_start_date') }}
        </td>
        <td class="px-6 py-4 text-gray-700 dark:text-gray-300 text-sm">
          {{ formatDate(trip.start_date) }}
        </td>
      </tr>
      <!-- Date de fin -->
      <tr class="border-t dark:border-gray-700">
        <td class="px-6 py-4 text-gray-800 dark:text-gray-100 text-sm font-medium">
          {{ t('create_trip.trip_end_date') }}
        </td>
        <td class="px-6 py-4 text-gray-700 dark:text-gray-300 text-sm">
          {{ formatDate(trip.end_date) }}
        </td>
      </tr>
      <!-- Localisation -->
      <tr class="border-t dark:border-gray-700">
        <td class="px-6 py-4 text-gray-800 dark:text-gray-100 text-sm font-medium">
          {{ t('create_trip.trip_location') }}
        </td>
        <td class="px-6 py-4 text-gray-700 dark:text-gray-300 text-sm">
          {{ town && country ? town + ', ' : '' }}{{ country }}
          {{ (town || country) && trip.latitude && trip.longitude ? ' ; ' : '' }}
          {{ trip.latitude && trip.longitude ? '(' + trip.latitude.toFixed(2) + '°, ' + trip.longitude.toFixed(2) + '°)' : '' }}
        </td>
      </tr>

      <!-- Placeholder for map or location -->
      <tr class="border-t dark:border-gray-700">
        <td class="px-6 py-4 text-gray-800 dark:text-gray-100 text-sm font-medium">
          {{ t('create_trip.trip_map') }}
        </td>
        <td class="px-6 py-4 text-gray-700 dark:text-gray-300 text-sm">
          <MapViewer
              v-if="trip.latitude && trip.longitude && trip.radius"
              :lat="trip.latitude"
              :lon="trip.longitude"
          ></MapViewer>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>




