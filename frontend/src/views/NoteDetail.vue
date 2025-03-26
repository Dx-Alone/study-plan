<template>
  <div class="note-detail-container" :class="{ 'dark-mode': isDarkMode }">
    <div class="note-detail-header">
      <button class="back-button" @click="goBack">
        <span>&larr;</span> 返回
      </button>
      <div class="note-meta">
        <span class="note-id">笔记 #{{ note.id }}</span>
        <span class="note-date" v-if="note.created_at">{{ formatDate(note.created_at) }}</span>
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载笔记中...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
      <button @click="fetchNote">重试</button>
    </div>

    <div v-else class="note-content-container">
      <div class="markdown-content" v-html="renderedContent"></div>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked'
import axios from 'axios'

export default {
  name: 'NoteDetail',
  data() {
    return {
      note: {},
      loading: true,
      error: null,
      isDarkMode: localStorage.getItem('darkMode') === 'true'
    }
  },
  computed: {
    renderedContent() {
      if (!this.note.content) return ''
      return marked(this.note.content)
    }
  },
  created() {
    marked.setOptions({
      breaks: true,
      gfm: true,
      sanitize: false
    })
    
    this.fetchNote()
    
    // 监听暗黑模式变化
    window.addEventListener('storage', this.checkDarkMode)
  },
  unmounted() {
    window.removeEventListener('storage', this.checkDarkMode)
  },
  methods: {
    async fetchNote() {
      this.loading = true
      this.error = null
      
      try {
        const noteId = this.$route.params.noteId
        const response = await axios.get(`/api/notes/${noteId}/`)
        this.note = response.data
      } catch (err) {
        console.error('获取笔记失败:', err)
        this.error = '无法加载笔记，请稍后重试'
      } finally {
        this.loading = false
      }
    },
    goBack() {
      this.$router.back()
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      const dateStr = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`
      const timeStr = `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}`
      return `${dateStr} ${timeStr}`
    },
    checkDarkMode(e) {
      if (e.key === 'darkMode') {
        this.isDarkMode = e.newValue === 'true'
      }
    }
  }
}
</script>

<style scoped>
.note-detail-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  min-height: 80vh;
}

.dark-mode.note-detail-container {
  background-color: #1a202c;
  color: #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.note-detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 15px;
  margin-bottom: 20px;
  border-bottom: 1px solid #e2e8f0;
}

.dark-mode .note-detail-header {
  border-bottom-color: #4a5568;
}

.back-button {
  display: flex;
  align-items: center;
  background-color: #edf2f7;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  color: #4a5568;
  transition: background-color 0.2s;
}

.back-button:hover {
  background-color: #e2e8f0;
}

.dark-mode .back-button {
  background-color: #2d3748;
  color: #e2e8f0;
}

.dark-mode .back-button:hover {
  background-color: #4a5568;
}

.note-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 5px;
}

.note-id {
  font-size: 0.9rem;
  color: #718096;
}

.note-date {
  font-size: 0.85rem;
  color: #a0aec0;
}

.dark-mode .note-id {
  color: #a0aec0;
}

.dark-mode .note-date {
  color: #718096;
}

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top: 3px solid #4299e1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

.dark-mode .loading-spinner {
  border: 3px solid #4a5568;
  border-top: 3px solid #63b3ed;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.note-content-container {
  padding: 10px;
}

:deep(.markdown-content) {
  line-height: 1.6;
}

:deep(.markdown-content h1) {
  font-size: 2rem;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  color: #2d3748;
}

:deep(.markdown-content h2) {
  font-size: 1.5rem;
  margin-top: 1.4rem;
  margin-bottom: 0.9rem;
  color: #2d3748;
}

:deep(.markdown-content h3) {
  font-size: 1.3rem;
  margin-top: 1.3rem;
  margin-bottom: 0.8rem;
  color: #2d3748;
}

:deep(.markdown-content p) {
  margin: 1rem 0;
}

:deep(.markdown-content code) {
  background-color: #edf2f7;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: monospace;
  font-size: 0.9em;
}

:deep(.markdown-content pre) {
  background-color: #edf2f7;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
}

:deep(.markdown-content pre code) {
  background-color: transparent;
  padding: 0;
}

:deep(.markdown-content ul), 
:deep(.markdown-content ol) {
  padding-left: 2rem;
  margin: 1rem 0;
}

:deep(.markdown-content blockquote) {
  border-left: 4px solid #e2e8f0;
  padding-left: 1rem;
  color: #718096;
  margin: 1rem 0;
}

:deep(.markdown-content img) {
  max-width: 100%;
  margin: 1rem 0;
}

:deep(.markdown-content table) {
  border-collapse: collapse;
  width: 100%;
  margin: 1rem 0;
}

:deep(.markdown-content th),
:deep(.markdown-content td) {
  border: 1px solid #e2e8f0;
  padding: 0.5rem;
  text-align: left;
}

:deep(.markdown-content th) {
  background-color: #f7fafc;
}

/* 暗色模式样式 */
.dark-mode :deep(.markdown-content h1),
.dark-mode :deep(.markdown-content h2),
.dark-mode :deep(.markdown-content h3) {
  color: #e2e8f0;
}

.dark-mode :deep(.markdown-content code) {
  background-color: #2d3748;
}

.dark-mode :deep(.markdown-content pre) {
  background-color: #2d3748;
}

.dark-mode :deep(.markdown-content blockquote) {
  border-left-color: #4a5568;
  color: #a0aec0;
}

.dark-mode :deep(.markdown-content th),
.dark-mode :deep(.markdown-content td) {
  border-color: #4a5568;
}

.dark-mode :deep(.markdown-content th) {
  background-color: #2d3748;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .note-detail-container {
    padding: 15px;
    margin: 10px;
    width: auto;
  }
  
  .note-detail-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .note-meta {
    align-items: flex-start;
    margin-top: 10px;
  }
}
</style> 