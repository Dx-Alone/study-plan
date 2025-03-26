import mitt from 'mitt'

/**
 * 全局事件总线，用于跨组件通信
 * 支持的事件类型:
 * - note-posted: { phaseId: string } - 笔记发送成功时触发
 * - note-failed: { phaseId: string } - 笔记发送失败时触发
 * - note-deleted: { phaseId: string, noteId: string } - 笔记删除成功时触发
 * - notes-refreshed: { phaseId: string } - 笔记列表刷新时触发
 */
const emitter = mitt()

export default emitter 