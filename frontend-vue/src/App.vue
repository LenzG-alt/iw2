<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <!-- RouterView es donde se inyectan tus páginas (Login o Dashboard) -->
  <RouterView />
</template>

<style>
/* Estilos globales básicos si quieres */
body {
  font-family: sans-serif;
  margin: 0;
  background-color: #f3f4f6;
}
</style>