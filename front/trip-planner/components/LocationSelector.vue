<script setup lang="ts">
import { ref } from 'vue';

const markerPosition = ref([48.8566, 2.3522]); // Position par défaut (Paris)
const radius = ref(5); // Rayon en kilomètres

// Fonction qui met à jour la position du marqueur
const onMarkerDragEnd = (e: any) => {
  markerPosition.value = [e.latlng.lat, e.latlng.lng];
};
</script>

<template>
  <div class="location-selector">
    <div id="map-wrap" style="height: 400px;">
      <client-only>
        <l-map :zoom="13" :center="markerPosition">
          <!-- Calque de tuiles OpenStreetMap -->
          <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          <!-- Marqueur draggable -->
          <l-marker :lat-lng="markerPosition" @dragend="onMarkerDragEnd" />
          <!-- Cercle pour le rayon -->
          <l-circle :lat-lng="markerPosition" :radius="radius * 1000" color="blue" fillOpacity="0.3" />
        </l-map>
      </client-only>
    </div>

    <div class="inputs mt-4 space-y-3">
      <div>
        <label for="latitude">Latitude</label>
        <UInput
            id="latitude"
            v-model="markerPosition[0]"
            readonly
        />
      </div>
      <div>
        <label for="longitude">Longitude</label>
        <UInput
            id="longitude"
            v-model="markerPosition[1]"
            readonly
        />
      </div>
      <div>
        <label for="radius">Rayon (km)</label>
        <UInput
            id="radius"
            type="number"
            v-model="radius"
            placeholder="Rayon en km"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.map-container {
  height: 400px;
  width: 100%;
}
</style>
