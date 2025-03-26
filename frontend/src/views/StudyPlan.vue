<template>
  <div class="study-plan-container">
    <div class="welcome-section">
      <h2>欢迎使用学习计划笔记系统</h2>
      <p>这是一个简单的笔记系统，可以帮助你记录和管理学习过程中的笔记和想法。</p>
      
      <div v-if="localMode" class="local-mode-alert">
        <p>⚠️ 正在使用本地模式，笔记将仅保存在您的浏览器中</p>
        <button @click="reconnectServer" class="retry-button">重试连接</button>
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载笔记中...</p>
    </div>

    <div v-else-if="error && notes.length === 0" class="error-container">
      <p>{{ error }}</p>
      <button @click="fetchNotesFromServer" class="retry-button">重试</button>
    </div>

    <notes-section 
      v-else
      phaseId="study-notes" 
      :notes="notes" 
      @save-note="saveNote"
      @post-note="postNote"
      @clear-note="clearNote"
      @clear-history="clearHistory" />
  </div>
</template>

<script>
import NotesSection from '../components/NotesSection.vue'
import axios from 'axios'
import emitter from '../utils/eventBus'

export default {
  name: 'StudyPlan',
  components: {
    NotesSection
  },
  data() {
    return {
      notes: [],
      loading: true,
      error: null,
      localMode: false // 本地模式，当后端API不可用时使用
    }
  },
  created() {
    // 从本地存储加载笔记
    this.loadNotesFromLocalStorage()
    
    // 从服务器获取笔记
    this.fetchNotesFromServer().catch(err => {
      console.warn('使用本地模式:', err.message)
      this.localMode = true
    }).finally(() => {
      this.loading = false
    })
  },
  methods: {
    loadNotesFromLocalStorage() {
      try {
        const notesJson = localStorage.getItem('study-notes')
        if (notesJson) {
          this.notes = JSON.parse(notesJson)
        }
      } catch (error) {
        console.error('加载本地笔记失败:', error)
      }
    },
    
    saveNotesToLocalStorage() {
      try {
        localStorage.setItem('study-notes', JSON.stringify(this.notes))
      } catch (error) {
        console.error('保存笔记到本地失败:', error)
      }
    },
    
    fetchNotesFromServer() {
      this.loading = true
      this.error = null
      
      return axios.get('/api/notes/recent/1/')
        .then(response => {
          this.notes = response.data
          this.saveNotesToLocalStorage()
          this.localMode = false
        })
        .catch(error => {
          console.error('获取笔记失败:', error)
          this.error = '无法从服务器获取笔记，使用本地模式'
          // 不抛出错误，允许继续使用本地笔记
          throw error
        })
    },
    
    saveNote(content) {
      // 保存笔记草稿到本地存储
      localStorage.setItem('study-notes-draft', content)
    },
    
    postNote(content) {
      // 创建新笔记对象
      const newNote = {
        id: Date.now(), // 临时ID
        content: content,
        created_at: new Date().toISOString(),
        phase_id: 1
      }
      
      // 添加到本地列表
      this.notes.unshift(newNote)
      
      // 保存到本地存储
      this.saveNotesToLocalStorage()
      
      // 发送到服务器
      axios.post('/api/notes/create/', {
        content: content,
        phase_id: 1
      })
        .then(response => {
          // 更新本地笔记ID
          const serverNote = response.data
          newNote.id = serverNote.id
          this.saveNotesToLocalStorage()
          
          // 发出成功事件
          emitter.emit('note-posted', { phaseId: 'study-notes' })
        })
        .catch(error => {
          console.error('发送笔记失败:', error)
          emitter.emit('note-failed', { phaseId: 'study-notes' })
        })
    },
    
    clearNote() {
      localStorage.removeItem('study-notes-draft')
    },
    
    clearHistory() {
      if (confirm('确定要清空所有历史笔记吗？此操作不可恢复。')) {
        // 清空本地存储
        localStorage.removeItem('study-notes')
        
        // 清空内存中的笔记
        this.notes = []
        
        // 清空服务器笔记
        axios.get('/api/notes/delete_all/1/')
          .then(() => {
            console.log('服务器笔记清空成功')
          })
          .catch(error => {
            console.error('清空服务器笔记失败:', error)
          })
      }
    },
    reconnectServer() {
      this.loading = true
      this.error = null
      
      this.fetchNotesFromServer().finally(() => {
        this.loading = false
      })
    }
  }
}
</script>

<style scoped>
.study-plan-container {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.welcome-section {
  margin-bottom: 30px;
  text-align: center;
  padding: 20px;
  background-color: #f0f9ff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.dark-mode .welcome-section {
  background-color: #2d3748;
}

h2 {
  color: #3182ce;
  margin-bottom: 10px;
}

.dark-mode h2 {
  color: #63b3ed;
}

p {
  color: #4a5568;
  line-height: 1.6;
}

.dark-mode p {
  color: #e2e8f0;
}

.local-mode-alert {
  background-color: #ffedf2;
  border: 1px solid #f56565;
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 20px;
}

.retry-button {
  background-color: #3182ce;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.retry-button:hover {
  background-color: #2b6cb0;
}

.loading-container {
  text-align: center;
  padding: 20px;
}

.loading-spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top: 4px solid #3182ce;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  text-align: center;
  padding: 20px;
  background-color: #fff5f5;
  border: 1px solid #f56565;
  border-radius: 4px;
  margin-bottom: 20px;
}

.error-container p {
  color: #f56565;
  margin-bottom: 10px;
}
</style> 