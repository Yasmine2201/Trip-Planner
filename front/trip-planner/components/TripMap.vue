<script setup lang="ts">

import { onMounted, nextTick } from 'vue';
import L from 'leaflet';

const { t } = useI18n();
const props = defineProps({
  lat: {
    type: Number,
    required: true,
  },
  lon: {
    type: Number,
    required: true,
  }
});

onMounted(() => {
  nextTick(() => {
    const mapElement = document.getElementById('map');
    if (mapElement) {
      const map = L.map(mapElement).setView([props.lat, props.lon], 13);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
      }).addTo(map);

      L.marker([props.lat, props.lon]).addTo(map).bindPopup(t("trip_home.trip_location_info")).openPopup();
    }
  });
});
</script>

<template>
  <div class="map-container">
    <div id="map" class="map"></div>
  </div>
</template>

<style scoped>
.map-container {
  height: 400px;
  width: 100%;
  position: relative;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.map {
  width: 100%;
  height: 100%;
}
</style>
