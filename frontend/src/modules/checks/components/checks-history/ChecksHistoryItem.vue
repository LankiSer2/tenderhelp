<script setup lang="ts">
import type { SmeCheck } from "@/modules/checks/types";
import { formatDateTime } from "@/modules/checks/utils";

defineProps<{
  item: SmeCheck;
}>();
</script>

<template>
  <q-item>
    <q-item-section>
      <q-item-label class="row items-center q-gutter-xs">
        <span class="text-weight-bold">{{ item.identifier }}</span>
        <q-chip dense size="sm" color="secondary" text-color="white">
          {{ item.identifier_type }}
        </q-chip>
        <q-chip
          dense
          size="sm"
          :color="item.is_sme ? 'positive' : 'negative'"
          text-color="white"
        >
          {{ item.is_sme ? "МСП" : "не МСП" }}
        </q-chip>
        <q-chip v-if="item.from_cache" dense size="sm" outline color="grey-7">
          кэш
        </q-chip>
      </q-item-label>

      <q-item-label v-if="item.company_name" caption>
        {{ item.company_name }}
      </q-item-label>
      <q-item-label caption>
        {{ item.sme_category || "категория не указана" }} · {{ formatDateTime(item.created_at) }}
      </q-item-label>
    </q-item-section>
  </q-item>
</template>
