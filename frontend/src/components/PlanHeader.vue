<template>
  <header class="header">
    <div class="container">
      <h1>2025考研复习计划</h1>
      <p>系统化备考指南，分阶段精准学习</p>
      <div class="countdown">距离考试还有: {{ countdownDays }}天</div>
      <button class="theme-toggle" @click="$emit('toggle-theme')">
        {{ darkMode ? '☀️' : '🌙' }}
      </button>
    </div>
  </header>
</template>

<script>
export default {
  name: 'PlanHeader',
  props: {
    darkMode: Boolean,
    countdownDays: Number
  },
  emits: ['toggle-theme']
}
</script>