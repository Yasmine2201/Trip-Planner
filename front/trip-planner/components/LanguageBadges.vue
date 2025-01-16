<script setup lang="ts">
const props = defineProps<{
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

const languagesText = computed(() => {
    return props.languages
        ?.split(',')
        .map(lang => lang.trim())
        .map(lang => languagesDict.value[lang])
        .sort()
  }
);

const generateRandomColor = (isDark: boolean): string => {
  const dark = isDark ? "dark:" : "";
  const colors = [
    `${dark}bg-blue-500 ${dark}text-white`,
    `${dark}bg-green-500 ${dark}text-white`,
    `${dark}bg-yellow-500 ${dark}text-white`,
    `${dark}bg-red-500 ${dark}text-white`,
    `${dark}bg-indigo-500 ${dark}text-white`,
    `${dark}bg-purple-500 ${dark}text-white`,
    `${dark}bg-pink-500 ${dark}text-white`,
    `${dark}bg-gray-500 ${dark}text-white`,
    `${dark}bg-orange-500 ${dark}text-white`,
    `${dark}bg-cyan-500 ${dark}text-white`,
    `${dark}bg-rose-500 ${dark}text-white`,
    `${dark}bg-emerald-500 ${dark}text-white`,
    `${dark}bg-fuchsia-500 ${dark}text-white`,
    `${dark}bg-amber-500 ${dark}text-white`,
    `${dark}bg-lime-500 ${dark}text-white`,
    `${dark}bg-teal-500 ${dark}text-white`,
    `${dark}bg-sky-500 ${dark}text-white`,
    `${dark}bg-violet-500 ${dark}text-white`,
    `${dark}bg-cyan-500 ${dark}text-white`,
    isDark ? `${dark}bg-white ${dark}text-black` : `${dark}bg-black ${dark}text-white`,
  ];
  return colors[Math.floor(Math.random() * colors.length)];
}

</script>

<template>
  <div class="flex gap-1 flex-wrap" v-if="props.languages">
    <template v-for="language in languagesText">
      <UBadge :ui="{ rounded: 'rounded-full' }" class="text-xs" :class="generateRandomColor(false) + ' ' + generateRandomColor(true)" >{{ language }} </UBadge>
    </template>
  </div>
</template>

<style scoped>

</style>