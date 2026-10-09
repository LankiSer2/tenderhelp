<script setup lang="ts">
import { CheckForm, ChecksHistory } from "@/modules/checks/components";
import { useChecksHistory } from "@/modules/checks/composables";
import type { SmeCheck } from "@/modules/checks/types";

const { items, total, loading, error, refresh, prepend } = useChecksHistory();

async function onCreated(check: SmeCheck) {
  prepend(check);
  await refresh();
}
</script>

<template>
  <div class="page-shell">
    <header class="q-mb-xl text-white">
      <p class="brand-title">TenderHelp</p>
      <h1 class="text-h5 q-mt-none q-mb-sm">Проверка субъекта МСП</h1>
      <p class="lead-text">
        Введите ИНН или ОГРН — приложение определит тип идентификатора и сверит его с реестром
        rmsp.nalog.ru.
      </p>
    </header>

    <div class="q-gutter-y-md">
      <CheckForm @created="onCreated" />
      <ChecksHistory
        :items="items"
        :total="total"
        :loading="loading"
        :error="error"
      />
    </div>
  </div>
</template>
