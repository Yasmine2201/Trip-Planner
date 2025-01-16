<script setup lang="ts">

const { t } = useI18n();

const model = defineModel<Array<string>>({
  required: true,
});

const languagesKeys = [
  "ar", "bn", "cs", "da", "de", "el", "en", "es", "fa", "fi",
  "fr", "gu", "he", "hi", "hr", "hu", "id", "it", "ja", "jv",
  "ko", "ml", "mr", "ms", "nl", "no", "pa", "pl", "pt", "ro",
  "ru", "sv", "ta", "te", "th", "tr", "uk", "ur", "vi", "zh",
  "af", "sq", "bg", "et", "lv", "lt", "sk", "sl", "sr", "sw"
];

const getLanguageLabel = (lang: string) => t(`language.${lang}`);

const languagesOptions = computed(() =>
    languagesKeys.map(lang => {
      return { id: lang, label: getLanguageLabel(lang) };
    }).sort((a, b) => a.label.localeCompare(b.label))
);

</script>

<template>
  <USelectMenu
      :options="languagesOptions"
      multiple
      v-model="model"
      value-attribute="id"
      searchable
      :searchable-placeholder="t('misc.search')"
      :ui-menu="{
        option: {
          selected: 'bg-gray-100 dark:bg-gray-900'
        }, default: {
          optionEmpty: { label: t('misc.no-results', { query: '{query}' }) }
        } }"
  >
    <template #label>
      <span v-if="model.length && model !== ['']" class="truncate">{{ model.map(getLanguageLabel).sort().join(", ") }}</span>
      <span v-else>{{ t('misc.select-value') }}</span>
    </template>
  </USelectMenu>
</template>

<style scoped>

</style>