<template>
  <div class="app" :class="{ 'dark-mode': darkMode }">
    <div class="note-detail-header">
      <div class="container">
        <div class="back-link">
          <router-link to="/">« 返回计划</router-link>
        </div>
        <h1>笔记详情</h1>
        <div class="note-date" v-if="note">{{ formatDate(note.created_at) }}</div>
        <button class="theme-toggle header-theme-toggle" @click="toggleTheme">
          {{ darkMode ? '🌙' : '☀️' }}
        </button>
      </div>
    </div>

    <div class="container">
      <div class="note-detail-content" v-if="note">
        <div :class="getMarkdownClass()" v-html="renderedContent"></div>
      </div>
      <div class="note-loading" v-else>
        <p>加载笔记中...</p>
      </div>
    </div>

    <div class="theme-controls-corner">
      <div class="md-theme-selector">
        <label for="md-theme">Markdown主题:</label>
        <select id="md-theme" v-model="mdTheme">
          <option value="github">GitHub</option>
          <option value="vue">Vue文档</option>
          <option value="academic">学术</option>
        </select>
      </div>
    </div>

    <footer class="footer">
      <div class="container">
        <p>2025考研复习计划 | JCY</p>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from 'axios'
import { marked } from 'marked'

export default {
  name: 'NoteDetail',
  props: {
    phaseId: String,
    noteId: String
  },
  data() {
    return {
      note: null,
      darkMode: false,
      mdTheme: 'github' // 默认使用GitHub主题
    }
  },
  computed: {
    renderedContent() {
      if (!this.note) return ''
      try {
        return marked(this.note.content)
      } catch (error) {
        console.error('Markdown渲染失败:', error)
        return this.note.content
      }
    }
  },
  created() {
    // 加载主题偏好
    this.darkMode = localStorage.getItem('darkMode') === 'true'
    
    // 加载Markdown主题偏好
    const savedMdTheme = localStorage.getItem('markdown-theme')
    if (savedMdTheme) {
      this.mdTheme = savedMdTheme
    }
    
    // 加载笔记
    this.loadNote()
  },
  watch: {
    mdTheme(newTheme) {
      localStorage.setItem('markdown-theme', newTheme)
    }
  },
  methods: {
    getMarkdownClass() {
      return `markdown-${this.mdTheme}`
    },
    loadNote() {
      // 从本地存储获取笔记
      const notesJson = localStorage.getItem(`notes-${this.phaseId}`)
      if (notesJson) {
        const notes = JSON.parse(notesJson)
        this.note = notes.find(note => note.id.toString() === this.noteId)
        
        if (!this.note) {
          console.error(`找不到笔记: phaseId=${this.phaseId}, noteId=${this.noteId}`)
        }
      }
      
      // 也尝试从服务器获取（如果实现了API）
      this.fetchNoteFromServer()
    },
    fetchNoteFromServer() {
      // 可选：从服务器获取笔记
      // 如API接口尚未实现可忽略
      axios.get(`/api/notes/${this.noteId}/`)
        .then(response => {
          // 如果本地没有找到笔记，使用服务器返回的数据
          if (!this.note) {
            this.note = response.data
          }
        })
        .catch(error => {
          console.error('从服务器获取笔记失败 (使用本地数据):', error)
        })
    },
    toggleTheme() {
      this.darkMode = !this.darkMode
      localStorage.setItem('darkMode', this.darkMode)
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

<style scoped>
.note-detail-header {
  background-color: #4a5568;
  color: white;
  padding: 20px 0;
  margin-bottom: 20px;
}

.dark-mode .note-detail-header {
  background-color: #2d3748;
}

.back-link {
  margin-bottom: 15px;
}

.back-link a {
  color: #fff;
  text-decoration: none;
}

.back-link a:hover {
  text-decoration: underline;
}

.note-date {
  font-size: 0.9em;
  color: #cbd5e0;
  margin-top: 5px;
}

.note-detail-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.dark-mode .note-detail-content {
  background: #2d3748;
  color: #f7fafc;
}

.header-theme-toggle {
  position: absolute;
  right: 20px;
  top: 20px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: white;
}

.theme-controls {
  display: none; /* 隐藏原来的控制区 */
}

.theme-controls-corner {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 100;
  background-color: rgba(74, 85, 104, 0.9);
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  transition: opacity 0.3s;
}

.dark-mode .theme-controls-corner {
  background-color: rgba(45, 55, 72, 0.9);
}

.theme-controls-corner .md-theme-selector {
  margin: 0;
  display: flex;
  align-items: center;
}

.theme-controls-corner label {
  color: white;
  margin-right: 8px;
  white-space: nowrap;
}

.theme-controls-corner select {
  background-color: #2d3748;
  color: white;
  border: 1px solid #4a5568;
  border-radius: 4px;
  padding: 5px 10px;
  min-width: 100px;
}

.dark-mode .theme-controls-corner select {
  background-color: #1a202c;
  border-color: #2d3748;
}

.note-loading {
  text-align: center;
  padding: 40px;
}
</style> 