<script setup lang="ts">
import { CheckResult } from "@/modules/checks/components/check-result";
import { useCreateCheck, useIdentifierDetection } from "@/modules/checks/composables";
import type { SmeCheck } from "@/modules/checks/types";

const emit = defineEmits<{
  created: [check: SmeCheck];
}>();

const { query, label, identifierType, ready, normalized } = useIdentifierDetection();
const { loading, error, result, submit } = useCreateCheck();

async function onSubmit() {
  if (!ready.value || loading.value) {
    return;
  }

  const check = await submit(normalized.value);
  if (check) {
    emit("created", check);
  }
}

function chipColor(): string {
  if (identifierType.value === "UNKNOWN") {
    return "negative";
  }
  return "positive";
}
</script>

<template>
  <q-card flat bordered class="q-pa-md">
    <q-card-section class="q-pa-none q-mb-md">
      <div class="text-h6">Новая проверка</div>
      <div class="text-caption text-grey-7">
        Введите ИНН или ОГРН — тип определится автоматически
      </div>
    </q-card-section>

    <q-form class="q-gutter-md" @submit.prevent="onSubmit">
      <q-input
        v-model="query"
        outlined
        dense
        label="ИНН или ОГРН"
        placeholder="Например, 4707048043"
        maxlength="32"
        inputmode="numeric"
        autocomplete="off"
        :disable="loading"
      >
        <template #append>
          <q-chip dense :color="chipColor()" text-color="white">
            {{ label }}
          </q-chip>
        </template>
      </q-input>

      <div>
        <q-btn
          type="submit"
          color="primary"
          unelevated
          :loading="loading"
          :disable="!ready"
          label="Проверить в реестре МСП"
          icon="search"
        />
      </div>

      <q-banner v-if="error" rounded class="bg-negative text-white">
        {{ error }}
      </q-banner>

      <CheckResult v-if="result" :check="result" />
    </q-form>
  </q-card>
</template>
