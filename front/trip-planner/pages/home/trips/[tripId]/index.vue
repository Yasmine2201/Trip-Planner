<script lang="ts" setup>
import {onMounted, ref} from 'vue';
import {useI18n} from 'vue-i18n';
import type {Trip} from '~/types';

definePageMeta({
  title: 'trip_home.trip_details',
  requiresAuth: true,
  layout: 'navigation'
});
const {t} = useI18n();
const route = useRoute();

const tripId = ref(route.params.tripId);
const trip = ref<Trip | null>(null)

const town = ref('');
const country = ref('');

const getLocationDetails = async (trip: Trip) => {

  try {
    const response = await useFetch(
        `https://nominatim.openstreetmap.org/reverse?lat=${trip.latitude}&lon=${trip.longitude}&format=json&addressdetails=1`
    );

    const address = response.data.value.address;

    town.value = address.city ?? address.town ?? "";
    country.value = address.country;
  } catch (error) {
    console.error('Error fetching location details:', error);
  }
};


onMounted(async () => {

  const tripResponse = await useApiFetch<Trip>(`/trips/${tripId.value}`);
  trip.value = tripResponse.data.value;

  if (trip.value) {
    await getLocationDetails(trip.value);
  } else {
    console.error('Trip not found');
  }
});

const deleteTrip = async (tripId: number) => {
  // TODO: Implement delete trip functionality
}

</script>

<template>
  <div class="overflow-x-auto">
    <PageTitle :name="t('trip_home.trip_details')">
      <template #actions>
        <UButton
            :to="`/home/trips/${trip?.trip_id}/edit`"
            color="primary"
            icon="i-heroicons-pencil-square"
            :label="t('misc.edit')"
            size="md"
            square
            variant="solid"
        />
        <UButton
            @click="deleteTrip(trip?.trip_id)"
            color="red"
            icon="i-heroicons-trash"
            :label="t('misc.delete')"
            size="md"
            square
            variant="solid"
        />
      </template>
    </PageTitle>

    <div class="flex space-x-3 mb-4 justify-end">

    </div>
    <table class="table-auto border-collapse w-full bg-white dark:bg-gray-800 shadow-md rounded-lg">

      <tbody>
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
          {{ trip?.start_date }}
        </td>
      </tr>
      <!-- Date de fin -->
      <tr class="border-t dark:border-gray-700">
        <td class="px-6 py-4 text-gray-800 dark:text-gray-100 text-sm font-medium">
          {{ t('create_trip.trip_end_date') }}
        </td>
        <td class="px-6 py-4 text-gray-700 dark:text-gray-300 text-sm">
          {{ trip?.end_date }}
        </td>
      </tr>
      <!-- Localisation -->
      <tr class="border-t dark:border-gray-700">
        <td class="px-6 py-4 text-gray-800 dark:text-gray-100 text-sm font-medium">
          {{ t('create_trip.trip_location') }}
        </td>
        <td class="px-6 py-4 text-gray-700 dark:text-gray-300 text-sm">
          {{ town }}, {{ country }} ({{ trip?.latitude.toFixed(2) }}°, {{ trip?.longitude.toFixed(2) }}°)
        </td>
      </tr>

      <!-- Placeholder for map or location -->
      <tr class="border-t dark:border-gray-700">
        <td class="px-6 py-4 text-gray-800 dark:text-gray-100 text-sm font-medium">
          {{ t('create_trip.trip_map') }}
        </td>
        <td class="px-6 py-4 text-gray-700 dark:text-gray-300 text-sm">
          <TripMap
              v-if="trip?.latitude && trip?.longitude && trip?.radius"
              :lat="trip.latitude"
              :lon="trip.longitude"
          ></TripMap>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>




