<template>
  <div class="phase-content active" id="overview">
    <div class="phase-header">
      <h2>2025考研备考总览</h2>
      <div class="phase-date">2025年4月-12月</div>
    </div>

    <p>这个备考计划将引导你从基础入门到考前冲刺，分为六个阶段，每个阶段有明确的学习目标和方法。</p>

    <div class="subject-cards">
      <div class="subject-card" v-for="(phase, index) in phases" :key="index">
        <h3>第{{ phase.number }}阶段：{{ phase.name }}</h3>
        <p>{{ phase.date_range }}</p>
        <p>{{ phase.description }}</p>
      </div>
    </div>

    <div class="tip-box">
      <h4>备考建议</h4>
      <p>保持良好的学习习惯和健康的生活方式，合理安排学习时间，定期复习，保持自信和良好心态。</p>
    </div>

    <button class="print-btn" @click="$emit('print')">打印计划</button>
  </div>
</template>

<script>
export default {
  name: 'PlanOverview',
  props: {
    phases: Array
  },
  emits: ['print']
}
</script>
