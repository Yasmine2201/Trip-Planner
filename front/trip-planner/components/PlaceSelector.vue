<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import L from "leaflet";
import { useI18n } from "vue-i18n";
import { type Location } from "~/types";

const { t } = useI18n();

const props = defineProps<{
  placeId: Number | null,
  filterData: { latitude: number, longitude: number, radius: number }
}>();

console.log(props);

// Lieux à afficher sur la carte : pour le moment différents endroits de paris
const places: Location[] = [
  { location_id: 1, name: "Tour Eiffel", latitude: 48.8584, longitude: 2.2945, description:"", prices:[]},
  { location_id: 2, name: "Louvre", latitude: 48.8606, longitude: 2.3376, description:"", prices:[]},
  { location_id: 3, name: "Notre-Dame", latitude: 48.8529, longitude: 2.3499, description:"", prices:[]},
  { location_id: 4, name: "Champs-Élysées", latitude: 48.8656, longitude: 2.3076, description:"", prices:[]},
  { location_id: 5, name: "Montmartre", latitude: 48.8867, longitude: 2.3431, description:"", prices:[]},
];

const selectedPlaceId = ref<Number | null>(props.placeId || null);
const mapContainer = ref<HTMLElement | null>(null);
let map: L.Map | null = null;
let markers: L.Marker[] = [];
let circle: L.Circle;

// Calculer les lieux filtrés selon la position et le rayon
const filteredPlaces = computed(() => {
  if (!props.filterData.radius) return places;

  return places.filter((place: Location) => {
    const distance = L.latLng(place.latitude, place.longitude).distanceTo(
        L.latLng(props.filterData.latitude, props.filterData.longitude)
    );
    return distance <= props.filterData.radius * 1000; // Rayon en mètres
  });
});

// Mettre à jour les marqueurs sur la carte
const updateMarkers = () => {
  // Supprimer les anciens marqueurs
  markers.forEach((marker) => marker.remove());
  markers = [];

  // Ajouter les nouveaux marqueurs
  markers = filteredPlaces.value.map((place: Location) => {
    return L.marker([place.latitude, place.longitude])
        .addTo(map!)
        .bindPopup(place.name);
  });
};

// Mettre à jour le cercle de rayon
const updateCircle = () => {
  // Supprimer l'ancien cercle s'il existe
  if (circle) {
    circle.remove();
  }

  // Ajouter un nouveau cercle
  circle = L.circle([props.filterData.latitude, props.filterData.longitude], {
    radius: props.filterData.radius * 1000,
  }).addTo(map!);
};

const selectPlace = (place: Location) => {
  console.log("Place selected:", place);
  selectedPlaceId.value = place.location_id;
};

onMounted(() => {
  if (mapContainer.value) {
    map = L.map(mapContainer.value).setView(
        [props.filterData.latitude, props.filterData.longitude],
        10
    );

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);

    // Initialiser les marqueurs et le cercle
    updateMarkers();
    updateCircle();

    // Redimensionner la carte après un court délai
    setTimeout(() => {
      map!.invalidateSize();
    }, 100);
  }
});

watch(filteredPlaces, () => {
  updateMarkers();
});

watch(() => props.filterData.radius, () => {
  updateCircle();
});

defineExpose({
  selectedPlaceId,
});
</script>

<template>
  <div class="place-selector">
    <h1 id="title">{{ t('PlaceSelect.title') }}</h1>
    <div ref="mapContainer" id="map" class="map-container-mapviewer"></div>
    <ul class="places-list">
      <li
          v-for="place in filteredPlaces"
          :key="place.location_id"
          @click="selectPlace(place)"
          class="place-item"
          :class="{ selected: selectedPlaceId && selectedPlaceId === place.location_id }"
      >
        {{ place.name }}
      </li>
    </ul>
  </div>
</template>

<style scoped>
.map-container-mapviewer {
  height: 400px;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.places-list {
  margin-top: 1rem;
  list-style: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.place-item {
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}

.place-item.selected {
  background-color: coral;
  color: white;
}

#title {
  font-size: 1.5rem;
  color: coral;
  text-align: center;
  font-weight: bold;
}
</style>
