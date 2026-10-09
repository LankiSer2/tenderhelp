<script setup lang="ts">
</script>

<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-secondary text-white">
      <q-toolbar>
        <q-toolbar-title>TenderHelp</q-toolbar-title>
        <q-btn flat dense round icon="fact_check" to="/" aria-label="Проверки" />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page>
        <router-view />
      </q-page>
    </q-page-container>
  </q-layout>
</template>
