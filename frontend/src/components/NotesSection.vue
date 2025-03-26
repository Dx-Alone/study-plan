<template>
  <div class="notes-area">
    <h4>个人笔记</h4>
    <textarea :id="`${phaseId}-notes`" v-model="noteContent" placeholder="添加你的笔记和调整计划..."></textarea>

    <div class="notes-actions">
      <button class="clear-note-btn" @click="clearNote">清除</button>
      <button class="save-note-btn" @click="saveNote">保存</button>
      <button class="post-note-btn" @click="postNote">发送</button>
      
      <div class="file-upload-container">
        <label for="file-upload" class="file-upload-btn">
          <span class="file-icon">📄</span> 上传文件
        </label>
        <input 
          type="file" 
          id="file-upload" 
          accept=".txt,.md" 
          @change="handleFileUpload"
          ref="fileInput"
          style="display: none;"
        >
      </div>
    </div>

    <div class="file-status" v-if="fileStatus.show">
      <div class="file-status-content" :class="{ 'file-error': fileStatus.isError }">
        {{ fileStatus.message }}
        <button class="file-status-close" @click="fileStatus.show = false">×</button>
      </div>
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
        <div class="note-item-wrapper" v-for="note in notes" :key="note.id">
          <div class="note-item-container">
            <router-link
              :to="`/note/${phaseId}/${note.id}`"
              class="note-item-card"
            >
              <div class="note-item">
                <div class="note-item-header">
                  <span class="note-date">{{ formatDate(note.created_at) }}</span>
                </div>
                <div class="note-item-preview">
                  {{ truncateText(note.content, 100) }}
                </div>
                <div class="view-note">查看全文 »</div>
              </div>
            </router-link>
            <div class="note-controls">
              <button class="delete-note-btn" @click="deleteNote(note.id)">
                <span class="delete-icon">🗑️</span>
              </button>
            </div>
          </div>
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
  emits: ['save-note', 'post-note', 'clear-note', 'clear-history', 'delete-note'],
  data() {
    return {
      noteContent: '',
      statusVisible: false,
      statusMessage: '笔记已保存!',
      fileStatus: {
        show: false,
        message: '',
        isError: false
      }
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
    emitter.on('note-posted', this.handleNotePosted)
    emitter.on('note-failed', this.handleNoteFailed)
    emitter.on('note-deleted', this.handleNoteDeleted)
    emitter.on('notes-refreshed', this.handleNotesRefreshed)
  },
  unmounted() {
    // 移除事件监听
    emitter.off('note-posted', this.handleNotePosted)
    emitter.off('note-failed', this.handleNoteFailed)
    emitter.off('note-deleted', this.handleNoteDeleted)
    emitter.off('notes-refreshed', this.handleNotesRefreshed)
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
    handleNotePosted({ phaseId }) {
      if (phaseId === this.phaseId) {
        this.statusMessage = '笔记已发送!'
        this.showStatus()
        
        // 添加延时以确保新笔记已被添加到DOM
        setTimeout(() => {
          this.scrollToBottom()
        }, 100)
      }
    },
    
    handleNoteFailed({ phaseId }) {
      if (phaseId === this.phaseId) {
        this.statusMessage = '发送失败!'
        this.showStatus()
      }
    },
    
    handleNoteDeleted({ phaseId, noteId }) {
      if (phaseId === this.phaseId) {
        this.statusMessage = '笔记已删除!'
        this.showStatus()
        console.log(`笔记删除成功: phaseId=${phaseId}, noteId=${noteId}`)
        
        // 强制更新组件，确保删除后的视图更新
        this.$forceUpdate()
      }
    },
    
    handleNotesRefreshed({ phaseId }) {
      if (phaseId === this.phaseId) {
        console.log(`收到笔记刷新事件: phaseId=${phaseId}`)
        this.$forceUpdate()
      }
    },

    deleteNote(noteId) {
      if (confirm('确定要删除此笔记吗？此操作不可恢复。')) {
        console.log(`从NotesSection发出删除请求: phaseId=${this.phaseId}, noteId=${noteId} (类型: ${typeof noteId})`)
        
        // 显示临时删除状态
        this.statusMessage = '正在删除笔记...'
        this.showStatus()
        
        // 确保noteId是字符串格式，明确传递phaseId和noteId
        this.$emit('delete-note', this.phaseId, noteId.toString())
      }
    },
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
    handleFileUpload(event) {
      const file = event.target.files[0]
      if (!file) return
      
      // 验证文件类型
      const allowedTypes = ['.txt', '.md']
      const fileExt = file.name.substring(file.name.lastIndexOf('.')).toLowerCase()
      
      if (!allowedTypes.includes(fileExt)) {
        this.showFileStatus('不支持的文件类型，仅支持 .txt 和 .md 文件', true)
        this.$refs.fileInput.value = '' // 清空文件输入
        return
      }
      
      // 读取文件
      const reader = new FileReader()
      
      reader.onload = (e) => {
        try {
          const content = e.target.result
          
          // 直接发送文件内容作为笔记
          this.$emit('post-note', `## ${file.name}\n\n${content}`)
          this.showFileStatus(`文件 "${file.name}" 已作为新笔记发送`, false)
        } catch (error) {
          console.error('文件解析错误:', error)
          this.showFileStatus('无法解析文件内容，请检查文件格式', true)
        }
      }
      
      reader.onerror = () => {
        this.showFileStatus('读取文件失败，请重试', true)
      }
      
      reader.readAsText(file)
      
      // 清空文件输入，允许重复选择同一文件
      this.$refs.fileInput.value = ''
    },
    showFileStatus(message, isError = false) {
      this.fileStatus = {
        show: true,
        message,
        isError
      }
      
      // 5秒后自动隐藏
      setTimeout(() => {
        this.fileStatus.show = false
      }, 5000)
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
    },
    truncateText(text, maxLength) {
      if (!text) return '';
      if (text.length <= maxLength) return text;
      return text.substring(0, maxLength) + '...';
    }
  }
}
</script>

<style scoped>
/* 保留原有样式 */
/* ... existing code ... */

/* 笔记项布局调整 */
.note-item-wrapper {
  position: relative;
  margin-bottom: 15px;
}

.note-item-container {
  display: flex;
  align-items: stretch;
}

.note-item-card {
  display: block;
  text-decoration: none;
  color: inherit;
  flex: 1;
}

.note-controls {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-left: 10px;
}

.delete-note-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #f56565;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  transition: background-color 0.2s, transform 0.2s;
}

.delete-note-btn:hover {
  background-color: #e53e3e;
  transform: scale(1.1);
}

.dark-mode .delete-note-btn {
  background-color: #c53030;
}

.dark-mode .delete-note-btn:hover {
  background-color: #9b2c2c;
}

/* 文件上传相关样式 */
.notes-actions {
  display: flex;
  margin-bottom: 15px;
  align-items: center;
  flex-wrap: wrap;
}

.file-upload-container {
  margin-left: auto;
}

.file-upload-btn {
  display: inline-flex;
  align-items: center;
  background-color: #4a5568;
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.file-upload-btn:hover {
  background-color: #2d3748;
}

.dark-mode .file-upload-btn {
  background-color: #2d3748;
}

.dark-mode .file-upload-btn:hover {
  background-color: #1a202c;
}

.file-icon {
  margin-right: 5px;
}

.file-status {
  margin-bottom: 15px;
}

.file-status-content {
  background-color: #e6fffa;
  border-left: 4px solid #38b2ac;
  color: #234e52;
  padding: 10px 15px;
  border-radius: 4px;
  font-size: 0.9rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.file-status-content.file-error {
  background-color: #fff5f5;
  border-left-color: #f56565;
  color: #c53030;
}

.dark-mode .file-status-content {
  background-color: #234e52;
  border-left-color: #38b2ac;
  color: #e6fffa;
}

.dark-mode .file-status-content.file-error {
  background-color: #742a2a;
  border-left-color: #f56565;
  color: #fff5f5;
}

.file-status-close {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: inherit;
  padding: 0 0 0 10px;
}

/* 添加笔记卡片样式 */
.note-item {
  background-color: white;
  border-radius: 5px;
  padding: 12px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.dark-mode .note-item {
  background-color: #2d3748;
  color: #e2e8f0;
}

.note-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.note-item-header {
  border-bottom: 1px solid #edf2f7;
  padding-bottom: 8px;
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
}

.dark-mode .note-item-header {
  border-bottom-color: #4a5568;
}

.note-date {
  font-size: 0.8rem;
  color: #718096;
}

.dark-mode .note-date {
  color: #a0aec0;
}

.note-item-preview {
  text-align: left;
  font-size: 0.9rem;
  margin-bottom: 8px;
  line-height: 1.4;
  color: #4a5568;
  max-height: 60px;
  overflow: hidden;
}

.dark-mode .note-item-preview {
  color: #e2e8f0;
}

.view-note {
  text-align: right;
  font-size: 0.8rem;
  color: #4299e1;
}

.dark-mode .view-note {
  color: #63b3ed;
}
</style>
