<template>
  <div class="location-selector">
    <h1 id="title">{{ t('LocationSelect.place') }}</h1>
    <div id="map" class="map-container"></div>
    <div class="controls">
      <div class="control-item">
        <span class="label">{{ t('LocationSelect.latitude') }}:</span>
        <span class="value">{{ selectedLat.toFixed(4) }}</span>
      </div>
      <div class="control-item">
        <span class="label">{{ t('LocationSelect.longitude') }}:</span>
        <span class="value">{{ selectedLng.toFixed(4) }}</span>
      </div>
      <div class="control-item">
        <label class="label">
          {{ t('LocationSelect.radius') }}:
        </label>
        <input
            type="number"
            v-model="radius"
            @input="updateRadius"
            min="1"
            class="radius-input"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import L from "leaflet";

const { t } = useI18n();

const selectedLat = ref(48.8566); // Par défaut : Paris
const selectedLng = ref(2.3522);
const radius = ref(10); // Rayon par défaut (en km)

let map: L.Map;
let marker: L.Marker;
let circle: L.Circle;

const updateRadius = () => {
  if (circle) {
    circle.setRadius(radius.value * 1000);
  }
};

onMounted(() => {
  map = L.map("map").setView([selectedLat.value, selectedLng.value], radius.value);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  marker = L.marker([selectedLat.value, selectedLng.value], { draggable: true }).addTo(map);
  circle = L.circle([selectedLat.value, selectedLng.value], { radius: radius.value * 1000 }).addTo(map);

  marker.on("dragend", (event) => {
    const position = marker.getLatLng();
    selectedLat.value = position.lat;
    selectedLng.value = position.lng;
    circle.setLatLng(position);
  });

  map.on("click", (event: L.LeafletMouseEvent) => {
    const { lat, lng } = event.latlng;
    selectedLat.value = lat;
    selectedLng.value = lng;
    marker.setLatLng([lat, lng]);
    circle.setLatLng([lat, lng]);
  });

  // Assurez-vous que la carte est bien redimensionnée
  setTimeout(() => {
    map.invalidateSize();
  }, 100); // Délai pour permettre au DOM de finir de se rendre
});

watch([selectedLat, selectedLng], () => {
  if (circle) {
    circle.setLatLng([selectedLat.value, selectedLng.value]);
  }
});

defineExpose({
  selectedLat,
  selectedLng,
  radius,
});
</script>

<style>
.map-container {
  height: 400px;
  width: 100%;
  position: relative;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.location-selector {
  height: 100%;
  width: 100%;
  border: 1px solid coral;
  padding: 0 1rem 1rem 1rem;

}

.controls {
  margin-top: 1rem;
  display: grid;
  gap: 0.5rem;
  align-items: center;
}

.control-item {
  display: flex;
  align-items: center;
}

.label {
  font-weight: bold;
  margin-right: 0.5rem;
}

.value {
  color: #333;
}

.radius-input {
  width: 5rem;
  margin-left: 0.5rem;
  text-align: left;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 0.25rem;
}

#title {
  font-size: 1.5rem;
  color: coral;
  text-align: center;
  font-weight: bold;
}
</style>
