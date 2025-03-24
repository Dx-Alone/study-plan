<template>
  <div class="app" :class="{ 'dark-mode': darkMode }">
    <plan-header :dark-mode="darkMode" @toggle-theme="toggleTheme" :countdown-days="countdownDays" />

    <div class="container">
      <tab-navigation :active-tab="activeTab" @change-tab="changeTab" />

      <plan-overview v-if="activeTab === 'overview'" :phases="phases" @print="printPlan" />

      <phase-detail v-else :phase="getActivePhase()" :activePhaseId="activeTab" :notes="notes[activeTab]"
        @save-note="saveNote" @post-note="postNote" @clear-note="clearNote" @clear-history="clearHistory" />
    </div>

    <footer class="footer">
      <div class="container">
        <p>2025考研复习计划 | JCY</p>
        <button v-if="activeTab !== 'overview'" class="reset-notes-btn" @click="resetAllNotes">重置所有笔记</button>
      </div>
    </footer>
  </div>
</template>

<script>
import PlanHeader from './components/PlanHeader.vue'
import TabNavigation from './components/TabNavigation.vue'
import PlanOverview from './components/PlanOverview.vue'
import PhaseDetail from './components/PhaseDetail.vue'
import axios from 'axios'
import emitter from './utils/eventBus'

export default {
  name: 'App',
  components: {
    PlanHeader,
    TabNavigation,
    PlanOverview,
    PhaseDetail
  },
  data() {
    return {
      darkMode: false,
      activeTab: 'overview',
      countdownDays: 365,
      phases: [],
      notes: {}
    }
  },
  created() {
    // 加载主题偏好
    this.darkMode = localStorage.getItem('darkMode') === 'true'

    // 计算倒计时
    this.updateCountdown()
    setInterval(this.updateCountdown, 86400000) // 每天更新一次

    // 从API获取数据
    this.fetchPhases()
  },
  methods: {
    resetAllNotes() {
      if (confirm('确定要重置所有笔记数据吗？此操作将清除所有已保存的笔记，不可恢复。')) {
        // 清除所有阶段的笔记
        for (let i = 1; i <= 6; i++) {
          const phaseId = `phase${i}`
          localStorage.removeItem(`notes-${phaseId}`)
          localStorage.removeItem(`${phaseId}-draft`)
          
          // 清空内存中的笔记
          if (this.notes && this.notes[phaseId]) {
            this.notes[phaseId] = []
          }
        }
        
        // 刷新页面
        alert('所有笔记已重置，将刷新页面。')
        window.location.reload()
      }
    },
    toggleTheme() {
      this.darkMode = !this.darkMode
      localStorage.setItem('darkMode', this.darkMode)
    },
    changeTab(tabId) {
      this.activeTab = tabId

      // 如果切换到非概览标签，加载对应阶段的笔记
      if (tabId !== 'overview') {
        this.fetchNotes(tabId)
      }
    },
    updateCountdown() {
      const examDate = new Date("2025-12-20T00:00:00")
      const now = new Date()
      const diff = examDate - now
      this.countdownDays = Math.floor(diff / (1000 * 60 * 60 * 24))
    },
    fetchPhases() {
      axios.get('/api/phases/')
        .then(response => {
          this.phases = response.data
        })
        .catch(error => {
          console.error('获取阶段数据失败:', error)
        })
    },
    fetchNotes(phaseId) {
      // 从本地存储加载笔记
      const localNotes = this.loadNotesFromLocalStorage(phaseId)
      if (localNotes) {
        console.log(`Loaded notes for ${phaseId} from local storage:`, localNotes)
        this.notes[phaseId] = localNotes
      } else {
        // 没有本地缓存时，初始化为空数组
        this.notes[phaseId] = []
      }
      
      // 尝试从服务器获取最新笔记（可选）
      this.fetchNotesFromServer(phaseId)
    },
    
    // 新增方法：从服务器获取笔记
    fetchNotesFromServer(phaseId) {
      const phase = this.phases.find(p => p.number === parseInt(phaseId.replace('phase', '')))
      if (!phase) return
      
      axios.get(`/api/phases/${phase.id}/notes/`)
        .then(response => {
          console.log(`Got notes from server for ${phaseId}:`, response.data)
          // 可以选择将服务器数据与本地数据合并，这里简单起见不做处理
        })
        .catch(error => {
          console.error(`获取阶段${phaseId}笔记从服务器失败 (使用本地缓存):`, error)
        })
    },
    
    // 新增方法：从localStorage加载笔记
    loadNotesFromLocalStorage(phaseId) {
      const notesJson = localStorage.getItem(`notes-${phaseId}`)
      const notes = notesJson ? JSON.parse(notesJson) : null
      
      // 验证笔记对象结构
      if (notes) {
        this.validateNotes(phaseId, notes)
      }
      
      return notes
    },
    
    // 新增方法：验证笔记对象结构
    validateNotes(phaseId, notes) {
      if (!Array.isArray(notes)) {
        console.error(`笔记格式错误：notes 不是数组`, notes)
        return false
      }
      
      let hasIssue = false
      
      notes.forEach((note, index) => {
        if (!note.content) {
          console.error(`笔记[${index}]缺少content属性:`, note)
          hasIssue = true
        } else if (typeof note.content !== 'string') {
          console.error(`笔记[${index}]的content不是字符串:`, note.content)
          hasIssue = true
        }
      })
      
      if (hasIssue) {
        console.log(`有问题的笔记数据:`, notes)
      }
      
      return !hasIssue
    },
    
    // 新增方法：保存笔记到localStorage
    saveNotesToLocalStorage(phaseId, notes) {
      localStorage.setItem(`notes-${phaseId}`, JSON.stringify(notes))
    },
    
    // 新增方法：发送笔记到服务器（作为备份）
    sendNoteToServer(phaseId, content) {
      axios.post(`/api/phases/${phaseId}/notes/`, { content: content })
        .then(response => {
          console.log('Note saved to server:', response.data)
        })
        .catch(error => {
          console.error('保存笔记到服务器失败 (但已保存到本地):', error)
        })
    },
    clearNote(phaseId) {
      localStorage.removeItem(`${phaseId}-draft`)
    },
    clearHistory(phaseId) {
      if (confirm('确定要清空所有历史笔记吗？此操作不可恢复。')) {
        // 清空本地存储
        localStorage.removeItem(`notes-${phaseId}`)
        
        // 清空内存中的笔记
        if (this.notes && this.notes[phaseId]) {
          this.notes[phaseId] = []
          // 强制更新视图
          this.$forceUpdate()
        }
        
        // 也删除服务器上的笔记（可选）
        this.clearServerNotes(phaseId)
      }
    },
    
    // 新增方法：从服务器清除笔记
    clearServerNotes(phaseId) {
      const phase = this.phases.find(p => p.number === parseInt(phaseId.replace('phase', '')))
      if (!phase) return
      
      // 获取该阶段所有笔记
      axios.get(`/api/phases/${phase.id}/notes/`)
        .then(response => {
          const notes = response.data
          // 删除所有笔记
          const deletePromises = notes.map(note =>
            axios.delete(`/api/phases/${phase.id}/notes/${note.id}/`)
          )
  
          Promise.all(deletePromises)
            .then(() => {
              console.log(`清空服务器上阶段${phaseId}的所有笔记成功`)
            })
            .catch(error => {
              console.error('清空服务器笔记失败:', error)
            })
        })
        .catch(error => {
          console.error(`获取服务器笔记失败:`, error)
        })
    },
    printPlan() {
      window.print()
    },
    getActivePhase() {
      if (this.activeTab === 'overview') return null
      return this.phases.find(phase => phase.number === parseInt(this.activeTab.replace('phase', '')))
    },
    saveNote(phaseId, content) {
      // 仅在本地保存草稿，不发送到服务器
      localStorage.setItem(`${phaseId}-draft`, content)
    },
    postNote(phaseId, content) {
      // 检查phaseId是否有效
      const phase = this.phases.find(p => p.number === parseInt(phaseId.replace('phase', '')))
      if (!phase) {
        console.error('Invalid phase ID:', phaseId)
        alert('发送笔记失败: 无效的阶段ID')
        emitter.emit('note-failed', { phaseId })
        return
      }

      console.log(`Posting note for phase ${phaseId} (ID: ${phase.id}): "${content}"`)

      // 确保本地存储有初始化
      let localNotes = this.loadNotesFromLocalStorage(phaseId) || []
      
      // 创建新笔记对象
      const newNote = {
        id: Date.now(), // 使用时间戳作为临时ID
        content: content, // 确保这里存储的是具体内容
        created_at: new Date().toISOString(),
        phase_id: phase.id // 存储数字ID，不是字符串"phase1"
      }
      
      // 添加到本地存储
      localNotes.unshift(newNote)
      this.saveNotesToLocalStorage(phaseId, localNotes)

      // 更新内存中的笔记
      if (!this.notes) {
        this.notes = {}
      }
      
      this.notes[phaseId] = localNotes
      
      // 强制更新视图
      this.$forceUpdate()
      
      console.log(`Updated notes for ${phaseId}:`, this.notes[phaseId])

      // 清除草稿
      localStorage.removeItem(`${phaseId}-draft`)
      
      // 发送成功事件
      emitter.emit('note-posted', { phaseId })
      
      // 同时发送到后端（可选，用于备份）
      this.sendNoteToServer(phaseId, content)
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
