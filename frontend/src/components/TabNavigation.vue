<template>
  <div class="nav-tabs">
    <button v-for="tab in tabs" :key="tab.id" class="nav-tab" :class="{ active: activeTab === tab.id }"
      @click="$emit('change-tab', tab.id)" :data-phase="tab.id">
      {{ tab.name }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'TabNavigation',
  props: {
    activeTab: String
  },
  emits: ['change-tab'],
  data() {
    return {
      tabs: [
        { id: 'overview', name: '总览' },
        { id: 'phase1', name: '第一阶段' },
        { id: 'phase2', name: '第二阶段' },
        { id: 'phase3', name: '第三阶段' },
        { id: 'phase4', name: '第四阶段' },
        { id: 'phase5', name: '第五阶段' },
        { id: 'phase6', name: '第六阶段' },
      ]
    }
  }
}
</script>
