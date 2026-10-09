<script setup lang="ts">
import type { SmeCheck } from "@/modules/checks/types";

defineProps<{
  check: SmeCheck;
}>();
</script>

<template>
  <q-banner
    rounded
    class="q-mt-md"
    :class="check.is_sme ? 'bg-positive text-white' : 'bg-negative text-white'"
  >
    <template #avatar>
      <q-icon :name="check.is_sme ? 'verified' : 'highlight_off'" />
    </template>

    <div class="text-weight-bold">
      {{ check.is_sme ? "Субъект МСП" : "Не найден в реестре МСП" }}
      <q-badge v-if="check.from_cache" color="white" text-color="dark" class="q-ml-sm">
        из кэша (&lt; 5 мин)
      </q-badge>
    </div>

    <div v-if="check.company_name" class="q-mt-xs">{{ check.company_name }}</div>
    <div v-if="check.sme_category" class="q-mt-xs">Категория: {{ check.sme_category }}</div>
    <div class="q-mt-xs">
      ИНН: {{ check.inn || "—" }} · ОГРН: {{ check.ogrn || "—" }}
    </div>
  </q-banner>
</template>
