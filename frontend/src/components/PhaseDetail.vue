<template>
  <div class="phase-content active" :id="activePhaseId" v-if="phase">
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
      @save-note="saveNote" @post-note="postNote"
      @clear-note="clearNote" @clear-history="clearHistory" />
  </div>
</template>

<script>
import SubjectCard from './SubjectCard.vue'
import NotesSection from './NotesSection.vue'

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
  emits: ['save-note', 'post-note', 'clear-note', 'clear-history'],
  mounted() {
    console.log(`PhaseDetail mounted for phase ${this.activePhaseId}, notes:`, this.notes)
  },
  updated() {
    console.log(`PhaseDetail updated for phase ${this.activePhaseId}, notes:`, this.notes)
  },
  methods: {
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
    },
    saveNote(content) {
      this.$emit('save-note', this.activePhaseId, content)
    },
    postNote(content) {
      this.$emit('post-note', this.activePhaseId, content)
    },
    clearNote() {
      this.$emit('clear-note', this.activePhaseId)
    },
    clearHistory() {
      this.$emit('clear-history', this.activePhaseId)
    }
  }
}
</script>
