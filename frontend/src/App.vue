<template>
  <div style="font-family: system-ui; padding: 2rem; max-width: 720px; margin: auto;">
    <h1>RHorizon Frontend</h1>
    <section>
      <button @click="refresh" style="padding: .5rem 1rem; border-radius: .5rem; border: 1px solid #ddd;">Refresh</button>
      <pre v-if="hello" style="background: #f7f7f7; padding: 1rem; border-radius: .5rem; overflow:auto;">{{ hello }}</pre>
      <pre v-if="health" style="background: #f7f7f7; padding: 1rem; border-radius: .5rem; overflow:auto;">{{ health }}</pre>
    </section>
    <section style="margin-top: 1.5rem;">
      <h2>Items</h2>
      <form @submit.prevent="addItem">
        <input v-model="newItem" placeholder="Item name" />
        <button type="submit">Add</button>
      </form>
      <ul>
        <li v-for="it in items" :key="it.id">{{ it.id }} - {{ it.name }} ({{ it.created_at }})</li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getHello, getHealth } from './api.js'

const hello = ref(null)
const health = ref(null)
const items = ref([])
const newItem = ref("")

async function refresh() {
  hello.value = await getHello()
  health.value = await getHealth()
  const res = await fetch(`/api/items`)
  items.value = await res.json()
}

async function addItem() {
  if (!newItem.value.trim()) return
  await fetch(`/api/items`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({name: newItem.value})
  })
  newItem.value = ""
  await refresh()
}

onMounted(refresh)
</script>
