<template>
  <div class="phase-content active" :id="activePhaseId" v-if="phase" :key="componentKey">
    <div class="phase-header">
      <h2>第{{ phase.number }}阶段：{{ phase.name }}</h2>
      <div class="phase-date">{{ phase.date_range }}</div>
    </div>

    <p>{{ phase.description }}</p>

    <div class="subject-cards">
      <subject-card v-for="subject in phase.subjects" :key="subject.id" :subject="subject" />
    </div>

    <div class="tip-box">
      <h4>阶段要点</h4>
      <p>{{ getTipContent() }}</p>
    </div>

    <notes-section :phase-id="activePhaseId" :notes="notes" ref="notesSection"
      @save-note="(content) => $emit('save-note', activePhaseId, content)" 
      @post-note="(content) => $emit('post-note', activePhaseId, content)"
      @clear-note="() => $emit('clear-note', activePhaseId)" 
      @clear-history="() => $emit('clear-history', activePhaseId)" 
      @delete-note="(noteId) => $emit('delete-note', activePhaseId, String(noteId))" />
  </div>
</template>

<script>
import SubjectCard from './SubjectCard.vue'
import NotesSection from './NotesSection.vue'
import emitter from '../utils/eventBus'

export default {
  name: 'PhaseDetail',
  components: {
    SubjectCard,
    NotesSection
  },
  props: {
    phase: Object,
    activePhaseId: String,
    notes: Array
  },
  data() {
    return {
      componentKey: 0 // 用于强制刷新组件
    }
  },
  emits: ['save-note', 'post-note', 'clear-note', 'clear-history', 'delete-note'],
  mounted() {
    console.log(`PhaseDetail mounted for phase ${this.activePhaseId}, notes:`, this.notes)
    
    // 监听笔记刷新事件，强制刷新组件
    emitter.on('notes-refreshed', this.handleNotesRefreshed)
  },
  unmounted() {
    emitter.off('notes-refreshed', this.handleNotesRefreshed)
  },
  updated() {
    console.log(`PhaseDetail updated for phase ${this.activePhaseId}, notes:`, this.notes)
  },
  methods: {
    handleNotesRefreshed({ phaseId }) {
      if (phaseId === this.activePhaseId) {
        console.log("笔记刷新事件触发组件刷新")
        this.refreshComponent()
      }
    },
    refreshComponent() {
      // 递增componentKey，强制Vue重新渲染整个组件
      this.componentKey += 1
      console.log("组件刷新，新的key:", this.componentKey)
      
      // 确保组件刷新后，也触发子组件更新
      this.$nextTick(() => {
        if (this.$refs.notesSection) {
          console.log("强制更新NotesSection组件")
          this.$refs.notesSection.$forceUpdate()
        }
      })
    },
    getTipContent() {
      // 根据不同阶段返回不同的提示内容
      const tips = {
        phase1: '建立规律的学习习惯，每天固定学习时间，不求速度但求稳定进步。记得做好笔记，建立知识体系框架。',
        phase2: '这阶段重在全面系统学习，打好基础。做好笔记和知识归纳，定期回顾前面内容，防止遗忘。适当增加做题量，但以理解为主。',
        phase3: '这阶段注重深化理解和真题训练，开始形成系统的答题思路和方法。保持刷题量的同时，要注意总结和反思，找出自己的薄弱环节。',
        phase4: '这阶段重点在于查漏补缺，强化实战能力。通过模拟测试找出自己的不足，有针对性地加强训练。注意总结各类题型的解题策略。',
        phase5: '这阶段重点提升解题效率和准确性，通过限时训练强化考试应对能力。注意总结经验，优化解题策略，保持良好心态。',
        phase6: '准备考试用品（准考证、身份证、文具等），熟悉考场位置和交通路线，调整作息，保证充足睡眠，保持积极心态，相信自己的努力。'
      }
      return tips[this.activePhaseId] || ''
    }
  }
}
</script>