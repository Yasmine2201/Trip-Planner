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
  private blockUpdate: boolean = false;

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
    if (this.blockUpdate) {
      this.blockUpdate = false;
      return;
    }

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
    if (this.isPopupDisplayed) {
      this.locationsLayer.clearLayers();
      if (highlight) {
        L.circleMarker([location.latitude, location.longitude], {
          radius: 5,
          color: 'blue',
          fillOpacity: 1
        }).addTo(this.locationsLayer);
        this.moveMapToLocation(location);
      }
      return;
    }

    const marker = this.locationLayerMap.get(location.location_id);
    marker?.setStyle({
      color: highlight ? 'blue' : 'orange'
    });
    if (highlight) {
      marker?.bringToFront();
    }
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

  const {data: locations}: AsyncData<Page<Location>, any> = await useApiFetch(`/locations`, {
    params: params
  });

  return locations;
}

function updateLocations() {
  fetchLocations(page.value).then(data => {
    locations.value = data.value;
    map.updateLocations();
  });
}

watch(page, async () => {
  const data = await fetchLocations(page.value);
  locations.value = data.value;
  map.unhighlightAllLocations();
});

watch(radius, async () => {
  if (map) {
    map.setRadius(radius.value);
    updateLocations();
  }
});

watch(minBudget, async () => {
  updateLocations();
});

watch(maxBudget, async () => {
  updateLocations();
});

watch(onlyPrices, async () => {
  updateLocations();
});

watch(textSearch, async (text) => {
  setTimeout(() => {
    if (text === textSearch.value) {
      updateLocations();
    }
  }, 500);
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
    <div id="filters" class="w-full mb-6">
      <UInput v-model="textSearch" placeholder="Search..." trailing-icon="i-heroicons-magnifying-glass"/>
      <div class="flex flex-row gap-4 mt-2">
        <div class="flex-1">
          <label for="radius">{{ t('locations.labels.radius') }}</label>
          <UInput id="radius" v-model="radius" placeholder="Radius" type="number"/>
        </div>
        <div class="flex-1">
          <label for="minBudget">{{ t('locations.labels.min-budget') }}</label>
          <UInput v-model="minBudget" placeholder="Min budget" type="number"/>
        </div>
        <div class="flex-1">
          <label for="maxBudget">{{ t('locations.labels.max-budget') }}</label>
          <UInput v-model="maxBudget" placeholder="Max budget" type="number"/>
        </div>
        <div class="flex-1">
          <label for="onlyPrices">{{ t('locations.labels.only-prices') }}</label><br>
          <UToggle id="onlyPrices" v-model="onlyPrices" class="mt-2"/>
        </div>
      </div>
    </div>
    <div id="line0" class="flex flex-row min-h-48">
      <div id="locations-list" class="w-2/5 mr-5">
        <div id="locations-list-header">
          <h1 class="text-primary font-semibold text-xl">{{ t('locations.titles.select-location') }}</h1>
        </div>
        <div id="list" class="min-h-524px">
          <ul>
            <li v-for="location in locations.data" :key="location.id">
              <LocationCard :location class="my-2"
                            @mouseenter="map.highlightLocation(location, true)"
                            @mouseleave="map.highlightLocation(location, false)"
                            @onSelect="(l) => $emit('onLocationSelected', l)"
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
  </div>
</template>

<style scoped>
.min-h-524px {
  min-height: 524px;
}

</style>
