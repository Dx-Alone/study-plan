<template>
  <div class="notes-area">
    <h4>个人笔记</h4>
    <textarea :id="`${phaseId}-notes`" v-model="noteContent" placeholder="添加你的笔记和调整计划..."></textarea>

    <div class="notes-actions">
      <button class="clear-note-btn" @click="clearNote">清除</button>
      <button class="save-note-btn" @click="saveNote">保存</button>
      <button class="post-note-btn" @click="postNote">发送</button>
    </div>

    <div class="save-status" :id="`${phaseId}-save-status`" :class="{ visible: statusVisible }">
      {{ statusMessage }}
    </div>

    <div class="notes-history">
      <div class="notes-history-title">
        <h4>历史笔记</h4>
        <button class="clear-history-btn" @click="clearHistory">清空历史</button>
      </div>

      <div :id="`${phaseId}-notes-history`" class="notes-history-content">
        <div class="note-item" v-for="note in notes" :key="note.id">
          <div class="note-item-header">
            <span>{{ formatDate(note.created_at) }}</span>
          </div>
          <!-- 调试信息，在生产环境中应移除 -->
          <pre v-if="false" style="font-size: 0.7rem; color: #999;">ID: {{ note.id }}, Phase: {{ note.phase_id }}</pre>
          <div class="note-item-content">{{ note.content }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import emitter from '../utils/eventBus'

export default {
  name: 'NotesSection',
  props: {
    phaseId: String,
    notes: Array
  },
  emits: ['save-note', 'post-note', 'clear-note', 'clear-history'],
  data() {
    return {
      noteContent: '',
      statusVisible: false,
      statusMessage: '笔记已保存!'
    }
  },
  created() {
    // 加载草稿
    const savedNote = localStorage.getItem(`${this.phaseId}-draft`)
    if (savedNote) {
      this.noteContent = savedNote
    }

    console.log(`NotesSection created for phase ${this.phaseId}, notes:`, this.notes)

    // 添加事件监听
    emitter.on('note-posted', ({ phaseId }) => {
      if (phaseId === this.phaseId) {
        this.statusMessage = '笔记已发送!'
        this.showStatus()
        
        // 添加延时以确保新笔记已被添加到DOM
        setTimeout(() => {
          this.scrollToBottom()
        }, 100)
      }
    })

    emitter.on('note-failed', ({ phaseId }) => {
      if (phaseId === this.phaseId) {
        this.statusMessage = '发送失败!'
        this.showStatus()
      }
    })
  },
  unmounted() {
    // 移除事件监听
    emitter.off('note-posted')
    emitter.off('note-failed')
  },
  watch: {
    notes: {
      handler(newNotes) {
        console.log(`Notes updated for phase ${this.phaseId}:`, newNotes)
        if (newNotes && newNotes.length > 0) {
          // 当笔记更新时，滚动到底部
          this.$nextTick(() => {
            this.scrollToBottom()
          })
        }
      },
      deep: true
    }
  },
  methods: {
    saveNote() {
      this.$emit('save-note', this.noteContent)

      this.statusMessage = '笔记已保存!'
      this.showStatus()
    },
    postNote() {
      if (this.noteContent.trim() === '') {
        alert('笔记内容不能为空！')
        return
      }

      const content = this.noteContent
      this.noteContent = ''
      
      this.$emit('post-note', content)
      this.statusMessage = '正在发送...'
      this.showStatus()
    },
    scrollToBottom() {
      const historyContent = document.querySelector(`#${this.phaseId}-notes-history`)
      if (historyContent) {
        historyContent.scrollTop = historyContent.scrollHeight
      }
    },
    clearNote() {
      this.noteContent = ''
      this.$emit('clear-note')
    },
    clearHistory() {
      this.$emit('clear-history')
    },
    showStatus() {
      this.statusVisible = true
      setTimeout(() => {
        this.statusVisible = false
      }, 3000)
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      const dateStr = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`
      const timeStr = `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
      return `${dateStr} ${timeStr}`
    }
  }
}
</script>
