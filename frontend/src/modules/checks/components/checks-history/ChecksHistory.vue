<script setup lang="ts">
import type { SmeCheck } from "@/modules/checks/types";
import ChecksHistoryItem from "./ChecksHistoryItem.vue";

defineProps<{
  items: SmeCheck[];
  total: number;
  loading: boolean;
  error?: string | null;
}>();
</script>

<template>
  <q-card flat bordered>
    <q-card-section class="row items-center justify-between">
      <div class="text-h6">История проверок</div>
      <q-badge color="primary">{{ total }}</q-badge>
    </q-card-section>

    <q-separator />

    <q-card-section v-if="loading" class="text-grey-7">
      <q-spinner color="primary" size="28px" class="q-mr-sm" />
      Загрузка…
    </q-card-section>

    <q-banner v-else-if="error" rounded class="bg-negative text-white q-ma-md">
      {{ error }}
    </q-banner>

    <q-card-section v-else-if="items.length === 0" class="text-grey-7">
      Проверок пока нет
    </q-card-section>

    <q-list v-else separator>
      <ChecksHistoryItem v-for="item in items" :key="item.id" :item="item" />
    </q-list>
  </q-card>
</template>
