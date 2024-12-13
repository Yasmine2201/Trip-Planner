<script setup lang="ts">
  const { locale, locales, setLocale } = useI18n();

  const selected = ref(locales.value.find((l) => l.code === locale.value));

  const switchLocale = (code: string) => {
    setLocale(code);
    selected.value = locales.value.find((l) => l.code === code);
  };
</script>

<template>
  <USelectMenu
      v-model="locale"
      :options="locales"
      option-attribute="name"
      value-attribute="code"
      @change="switchLocale"
      class="w-32"
  >
    <template #leading>
      <UIcon :name="selected.icon" />
    </template>
  </USelectMenu>
</template>

<style scoped>

</style>