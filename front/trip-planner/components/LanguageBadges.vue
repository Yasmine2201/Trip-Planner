<script setup lang="ts">
defineProps<{
  languages?: string,
}>();

const { t } = useI18n();

const languagesKeys = [
  "ar", "bn", "cs", "da", "de", "el", "en", "es", "fa", "fi",
  "fr", "gu", "he", "hi", "hr", "hu", "id", "it", "ja", "jv",
  "ko", "ml", "mr", "ms", "nl", "no", "pa", "pl", "pt", "ro",
  "ru", "sv", "ta", "te", "th", "tr", "uk", "ur", "vi", "zh",
  "af", "sq", "bg", "et", "lv", "lt", "sk", "sl", "sr", "sw"
];

const languagesDict = computed(() =>
    Object.fromEntries(languagesKeys.map(lang => [lang, t(`language.${lang}`)]))
);

const languagesText = computed(() =>
    languages?.split(',').map(lang => languagesDict.value[lang])
);

const generateRandomColor = (): string => {
  const colors = [
    "bg-blue-500 text-white",
    "bg-green-500 text-white",
    "bg-yellow-500 text-black",
    "bg-red-500 text-white",
    "bg-indigo-500 text-white",
    "bg-purple-500 text-white",
    "bg-pink-500 text-white",
    "bg-gray-500 text-white",
    "bg-black text-white",
  ];
  return colors[Math.floor(Math.random() * colors.length)];
}

</script>

<template>
  <div class="flex gap-2" v-if="languages">
    <template v-for="language in languagesText">
      <UBadge :ui="{ rounded: 'rounded-full' }" :color="generateRandomColor()" >{{ language }}</UBadge>
    </template>
  </div>
</template>

<style scoped>

</style>