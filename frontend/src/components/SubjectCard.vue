<template>
  <div class="subject-card">
    <h3>{{ subject.name }}</h3>
    <ul class="task-list">
      <li v-for="task in subject.tasks" :key="task.id">
        <input type="checkbox" class="task-checkbox" :id="getTaskId(task.id)" @change="saveTaskState"
          :checked="isTaskChecked(task.id)">
        {{ task.description }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'SubjectCard',
  props: {
    subject: Object
  },
  methods: {
    getTaskId(taskId) {
      return `task-${taskId}`
    },
    isTaskChecked(taskId) {
      const id = this.getTaskId(taskId)
      return localStorage.getItem(id) === 'true'
    },
    saveTaskState(event) {
      const checkbox = event.target
      localStorage.setItem(checkbox.id, checkbox.checked)
    }
  }
}
</script>
