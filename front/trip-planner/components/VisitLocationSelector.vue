<script lang="ts" setup>
import {useI18n} from "vue-i18n";
import {type Location, type Page, type Trip} from "~/types";
import type {AsyncData} from "#app";
import LocationCard from "~/components/LocationCard.vue";
import L from "leaflet";

const {t} = useI18n();

const props = defineProps<{
  tripId: string;
}>();

class LocationsMap {
  private readonly map: L.Map;
  private circle: L.Circle;
  private viewPort: L.LatLngBounds;
  private readonly locationsLayer: L.LayerGroup;
  private isPopupDisplayed: boolean = false;
  private locationLayerMap: Map<number, L.CircleMarker> = new Map();

  constructor() {
    this.map = L.map("map").setView([trip.value.latitude, trip.value.longitude], 10);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(this.map);

    this.locationsLayer = L.layerGroup().addTo(this.map);
    this.circle = L.circle([trip.value.latitude, trip.value.longitude], {
      radius: radius.value * 1000,
      fillColor: 'black',
      fillOpacity: 0.15,
      color: 'black'
    }).addTo(this.map);
    this.viewPort = this.circle.getBounds();

    this.map.fitBounds(this.viewPort);
    this.updateLocations();

    this.map.on('moveend', this.updateLocations.bind(this));
  }

  setRadius(radius: number) {
    this.circle.setRadius(radius * 1000);
    this.viewPort = this.circle.getBounds();
    this.map.flyToBounds(this.viewPort);
  }

  getViewPort() {
    return this.viewPort;
  }

  showPopup() {
    if (!this.isPopupDisplayed) {
      this.isPopupDisplayed = true;
      L.popup()
          .setLatLng([trip.value.latitude, trip.value.longitude])
          .setContent(t('locations.popup.too-many-locations'))
          .openOn(this.map);
    }
  }

  hidePopup() {
    if (this.isPopupDisplayed) {
      this.isPopupDisplayed = false;
      this.map.closePopup();
    }
  }

  async updateLocations() {
    this.viewPort = this.map.getBounds();
    fetchLocations(1, true).then(data => {
      this.locationsLayer.clearLayers();
      this.locationLayerMap.clear();
      if (data.value.total_elements > viewPageSize) {
        this.showPopup();
      } else {
        this.hidePopup();
        this.displayLocations(data.value.data);
      }
    });
  }

  displayLocations(locations: Location[]) {
    locations?.forEach(location => {
      const marker = L.circleMarker([location.latitude, location.longitude], {
        radius: 5,
        color: 'orange',
        fillOpacity: 1
      })
          .bindPopup(location.name)
          .addTo(this.locationsLayer);
      this.locationLayerMap.set(location.location_id, marker);
    });
  }

  highlightLocation(location: Location, highlight: boolean) {
    if (selectedLocation.value?.location_id === location.location_id) {
      highlight = true;
    }
    this.locationLayerMap.get(location.location_id)?.setStyle({
      color: highlight ? 'blue' : 'orange'
    });
  }

  unhighlightAllLocations() {
    this.locationLayerMap.forEach(marker => {
      marker.setStyle({
        color: 'orange'
      });
    });
  }
}


const {data: trip}: AsyncData<Trip, any> = await useApiFetch<Trip>(`/trips/${props.tripId}`, {}, true);

const radius = ref(trip.value.radius);
const minBudget = ref(0);
const maxBudget = ref(1000);
const onlyPrices = ref(false);
const textSearch = ref(null) as Ref<string | null>;
const page = ref(1);
const pageSize = 5;
const viewPageSize = 100;

const locations = await fetchLocations();

let map: LocationsMap;
const selectedLocation = ref(null) as Ref<Location | null>;

async function fetchLocations(page: number = 1, useViewPort: boolean = false) {
  const params = {
    lat: trip.value.latitude,
    lon: trip.value.longitude,
    radius: radius.value,
    min_price: minBudget.value,
    max_price: maxBudget.value,
    search: textSearch.value,
    page: page,
    pageSize: pageSize,
    only_prices: onlyPrices.value
  };

  if (useViewPort && map) {
    params.min_lat = map.getViewPort().getSouth();
    params.max_lat = map.getViewPort().getNorth();
    params.min_lon = map.getViewPort().getWest();
    params.max_lon = map.getViewPort().getEast();
    params.pageSize = viewPageSize;
  }

  const {data: locations}: AsyncData<Page<Location>, any> = await useApiFetch<Location[]>(`/locations`, {
    params: params
  });

  return locations;
}

watch(page, async () => {
  const data = await fetchLocations(page.value);
  locations.value = data.value;
  map.unhighlightAllLocations();
});

watch(radius, async () => {
  if (map) {
    map.setRadius(radius.value);
  }
});

watch(selectedLocation, () => {
  if (selectedLocation.value) {
    map.unhighlightAllLocations();
    map.highlightLocation(selectedLocation.value, true);
  }
});

onMounted(() => {
  map = new LocationsMap();
  if (locations.value.total_elements > viewPageSize) {
    map.showPopup();
  } else {
    map.hidePopup();
    map.updateLocations();
  }
});

defineEmits<{
  onLocationSelected: (location: Location) => any
}>();

</script>

<template>

  <div id="wrapper">
    <div id="line0" class="flex flex-row">
      <div id="locations-list" class="w-2/5 mr-5">
        <div id="locations-list-header">
          <h1 class="text-primary font-semibold text-xl">{{ t('locations.titles.select-location') }}</h1>
        </div>
        <div id="list">
          <ul>
            <li v-for="location in locations.data" :key="location.id">
              <LocationCard :location :selected="selectedLocation?.location_id === location.location_id" class="my-2"
                            @mouseenter="map.highlightLocation(location, true)"
                            @mouseleave="map.highlightLocation(location, false)"
                            @onSelect="(l) => selectedLocation = l"
              />
            </li>
          </ul>
        </div>
        <UPagination v-model="page" :page-count="locations.elements_per_page" :total="locations.total_elements"
                     show-first show-last/>

      </div>
      <div id="map" class="w-3/5 rounded-3xl z-0">
      </div>
    </div>
    <div class="w-full mt-8 flex justify-end">
      <UButton :disabled="selectedLocation === null" color="primary" size="xl"
               @click="$emit('onLocationSelected', selectedLocation)">{{ t('form_visit.visit_create_button') }}
      </UButton>
    </div>
  </div>
</template>

<style scoped>


</style>
