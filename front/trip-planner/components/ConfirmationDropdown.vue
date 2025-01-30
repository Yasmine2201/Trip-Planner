<script setup lang="ts">

const emit = defineEmits<{
  confirm: () => void
}>();

const { t } = useI18n();
const isOpen = ref(false);

const handleConfirm = () => {
  isOpen.value = false;
  emit('confirm');
}

</script>

<template>
  <UPopover v-model:open="isOpen" :ui="{
    rounded: 'rounded-2xl',
    base: 'px-6 py-4 flex flex-col items-center gap-2',
  }">
    <slot />

    <template #panel>
      <span class="text-black dark:text-white text-base">{{ t('misc.ask-confirmation') }} :</span>
      <div class="flex items-center justify-center gap-4">
        <UTooltip :title="t('misc.confirm')">
          <UButton
              color="green"
              icon="i-heroicons-check"
              size="xs"
              square
              class="rounded-full"
              variant="solid"
              @click="handleConfirm"
          />
        </UTooltip>
        <UTooltip :title="t('misc.cancel')">
          <UButton
              color="red"
              icon="i-heroicons-x-mark"
              size="xs"
              square
              class="rounded-full"
              variant="solid"
              @click="isOpen = false"
          />
        </UTooltip>
      </div>
    </template>
  </UPopover>
</template>

<style scoped>

</style>