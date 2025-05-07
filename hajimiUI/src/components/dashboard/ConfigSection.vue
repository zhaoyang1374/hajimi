<script setup>
import { useDashboardStore } from '../../stores/dashboard'
import { ref, computed, watch } from 'vue'
import BasicConfig from './config/BasicConfig.vue'
import FeaturesConfig from './config/FeaturesConfig.vue'
import VersionInfo from './config/VersionInfo.vue'
import VertexConfig from './config/VertexConfig.vue'

const dashboardStore = useDashboardStore()
const isExpanded = ref(true)

// 配置项解释
const configExplanations = {
  maxRequestsPerMinute: '限制每个IP每分钟可以发送的最大请求数量，防止API被滥用',
  maxRequestsPerDayPerIp: '限制每个IP每天可以发送的最大请求数量，防止API被滥用',
  currentTime: '当前服务器时间，用于同步和调试',
  fakeStreaming: '是否启用假流式响应，模拟流式返回效果',
  fakeStreamingInterval: '假流式响应的间隔时间（秒），控制返回速度',
  randomString: '是否启用随机字符串生成，用于伪装请求',
  randomStringLength: '随机字符串的长度，用于伪装请求',
  concurrentRequests: '默认并发请求数量，控制同时处理的请求数',
  increaseConcurrentOnFailure: '请求失败时增加的并发数，提高成功率',
  maxConcurrentRequests: '最大并发请求数量，防止系统过载',
  localVersion: '当前系统版本号',
  remoteVersion: '远程仓库最新版本号',
  hasUpdate: '是否有可用更新',
  searchMode: '是否启用联网搜索功能',
  searchPrompt: '联网搜索提示',
  enableVertexExpress: '是否启用Vertex Express模式',
  vertexExpressApiKey: 'Vertex Express API密钥'
}

// 显示解释的工具提示
const showTooltip = ref(false)
const tooltipText = ref('')
const tooltipPosition = ref({ x: 0, y: 0 })

function showExplanation(text, event) {
  tooltipText.value = text
  tooltipPosition.value = {
    x: event.clientX,
    y: event.clientY
  }
  showTooltip.value = true
}

function hideTooltip() {
  showTooltip.value = false
}

// 获取折叠图标类
const getFoldIconClass = (isVisible) => {
  return isVisible ? 'fold-icon rotated' : 'fold-icon'
}

// 编辑配置相关状态
const editingConfig = ref(null)
const editValue = ref('')
const editPassword = ref('')
const showPasswordInput = ref(false)
const editError = ref('')
const hasAuthenticated = ref(false)

// 打开编辑对话框
function openEditDialog(configKey, currentValue) {
  editingConfig.value = configKey
  editValue.value = currentValue
  editError.value = ''
  
  // 如果已经认证过，不需要再次输入密码
  if (!hasAuthenticated.value) {
    showPasswordInput.value = true
  } else {
    showPasswordInput.value = false
  }
}

// 关闭编辑对话框
function closeEditDialog() {
  editingConfig.value = null
  editValue.value = ''
  editPassword.value = ''
  showPasswordInput.value = false
  editError.value = ''
}

// 保存配置
async function saveConfig() {
  if (!editingConfig.value) return
  
  try {
    // 如果需要密码验证
    if (showPasswordInput.value) {
      if (!editPassword.value) {
        editError.value = '请输入密码'
        return
      }
    }
    
    // 根据配置项类型进行类型转换
    let value = editValue.value
    if (editingConfig.value === 'vertexExpressApiKey') {
      // API Key 保持为字符串类型
      value = String(editValue.value)
    } else if (typeof dashboardStore.config[editingConfig.value] === 'boolean') {
      value = editValue.value === 'true' || editValue.value === true
    } else if (typeof dashboardStore.config[editingConfig.value] === 'number') {
      value = Number(editValue.value)
      if (isNaN(value)) {
        editError.value = '请输入有效的数字'
        return
      }
    }
    
    // 调用API更新配置
    await dashboardStore.updateConfig(
      editingConfig.value, 
      value, 
      showPasswordInput.value ? editPassword.value : undefined
    )
    
    // 更新本地状态
    dashboardStore.config[editingConfig.value] = value
    
    // 如果输入了密码，标记为已认证
    if (showPasswordInput.value) {
      hasAuthenticated.value = true
    }
    
    // 关闭对话框
    closeEditDialog()
  } catch (error) {
    editError.value = error.message || '保存失败'
  }
}

// 获取配置项显示值
function getConfigDisplayValue(key) {
  const value = dashboardStore.config[key]
  if (typeof value === 'boolean') {
    return value ? '启用' : '禁用'
  }
  return value
}

// 获取配置项类型
function getConfigType(key) {
  const value = dashboardStore.config[key]
  // 特殊处理布尔值配置项
  if (key === 'fakeStreaming' || key === 'enableVertexExpress' || key === 'randomString' || key === 'searchMode') {
    return 'boolean'
  }
  // 特殊处理 API Key 配置项
  if (key === 'vertexExpressApiKey') {
    return 'string'
  }
  return typeof value
}

// 监听数据刷新，重置认证状态
watch(() => dashboardStore.isRefreshing, (newValue, oldValue) => {
  if (oldValue === true && newValue === false) {
    // 数据刷新完成，重置认证状态
    hasAuthenticated.value = false
  }
})
</script>

<template>
  <div class="info-box">
    <!-- Vertex模式只显示版本信息和Vertex配置 -->
    <div v-if="dashboardStore.status.enableVertex">
      <VertexConfig :openEditDialog="openEditDialog" :getConfigDisplayValue="getConfigDisplayValue" />
      <VersionInfo />
    </div>
    
    <!-- 非Vertex模式显示环境配置和折叠内容 -->
    <div v-else>
      <h3 class="section-title fold-header" @click="isExpanded = !isExpanded">
        ⚙️ 环境配置
        <span :class="getFoldIconClass(isExpanded)">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </span>
      </h3>
      
      <!-- 默认显示的简略配置 -->
      <div v-if="!isExpanded" class="stats-grid">
        <div class="stat-card">
          <div class="stat-value">{{ dashboardStore.config.maxRequestsPerMinute }}</div>
          <div class="stat-label">每分钟请求限制</div>
          <button class="edit-btn" @click="openEditDialog('maxRequestsPerMinute', dashboardStore.config.maxRequestsPerMinute)">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
            </svg>
          </button>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ dashboardStore.config.concurrentRequests }}</div>
          <div class="stat-label">并发请求数</div>
          <button class="edit-btn" @click="openEditDialog('concurrentRequests', dashboardStore.config.concurrentRequests)">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
            </svg>
          </button>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ dashboardStore.config.currentTime }}</div>
          <div class="stat-label">当前服务器时间</div>
        </div>
      </div>
      
      <!-- 展开后显示的所有配置项 -->
      <transition name="fold">
        <div v-if="isExpanded" class="fold-content">
          <!-- 基本配置 -->
          <BasicConfig :openEditDialog="openEditDialog" />
          
          <!-- 功能配置 -->
          <FeaturesConfig :openEditDialog="openEditDialog" :getConfigDisplayValue="getConfigDisplayValue" />
          
          <!-- 版本信息 -->
          <VersionInfo />
        </div>
      </transition>
    </div>
    
    <!-- 工具提示 -->
    <div class="tooltip" v-if="showTooltip" :style="{ left: tooltipPosition.x + 'px', top: tooltipPosition.y + 'px' }" @mouseleave="hideTooltip">
      {{ tooltipText }}
    </div>
    
    <!-- 编辑对话框 -->
    <div class="edit-dialog" v-if="editingConfig">
      <div class="edit-dialog-content">
        <h3>编辑配置</h3>
        <div class="edit-field">
          <label>{{ configExplanations[editingConfig] }}</label>
          
          <!-- 布尔值选择 -->
          <div v-if="getConfigType(editingConfig) === 'boolean'" class="boolean-selector">
            <label class="boolean-option">
              <input type="radio" v-model="editValue" :value="true"> 启用
            </label>
            <label class="boolean-option">
              <input type="radio" v-model="editValue" :value="false"> 禁用
            </label>
          </div>
          
          <!-- 数字输入 -->
          <input 
            v-else-if="getConfigType(editingConfig) === 'number'" 
            type="number" 
            v-model="editValue"
            min="1"
            class="edit-input"
          >
          
          <!-- 字符串输入 -->
          <template v-else-if="getConfigType(editingConfig) === 'string'">
            <!-- 特殊处理searchPrompt，使用textarea -->
            <textarea
              v-if="editingConfig === 'searchPrompt'"
              v-model="editValue"
              class="edit-input text-area"
              rows="4"
              placeholder="请输入联网搜索提示"
            ></textarea>
            <!-- API Key输入使用password类型 -->
            <input 
              v-else-if="editingConfig === 'vertexExpressApiKey'"
              type="password" 
              v-model="editValue"
              class="edit-input"
              placeholder="请输入新的 Vertex Express API Key"
            >
            <!-- 其他字符串使用普通input -->
            <input 
              v-else
              type="text" 
              v-model="editValue"
              class="edit-input"
            >
          </template>
          
          <!-- 密码输入 -->
          <div v-if="showPasswordInput" class="password-field">
            <label>请输入密码</label>
            <input 
              type="password" 
              v-model="editPassword"
              class="edit-input"
              placeholder="请输入密码"
            >
          </div>
          
          <!-- 错误提示 -->
          <div v-if="editError" class="edit-error">
            {{ editError }}
          </div>
        </div>
        
        <div class="edit-actions">
          <button class="cancel-btn" @click="closeEditDialog">取消</button>
          <button class="save-btn" @click="saveConfig">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.info-box {
  background-color: var(--card-background);
  border: 1px solid var(--card-border);
  border-radius: var(--radius-xl);
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.info-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: var(--gradient-primary);
  opacity: 0.8;
}

/* 移动端优化 - 减小外边距 */
@media (max-width: 768px) {
  .info-box {
    margin-bottom: 12px;
    padding: 15px 10px;
    border-radius: var(--radius-lg);
  }
}

@media (max-width: 480px) {
  .info-box {
    margin-bottom: 8px;
    padding: 12px 8px;
    border-radius: var(--radius-md);
  }
}

.section-title {
  color: var(--color-heading);
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 10px;
  margin-bottom: 20px;
  transition: all 0.3s ease;
  position: relative;
  font-weight: 600;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 50px;
  height: 2px;
  background: var(--gradient-primary);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-top: 15px;
  margin-bottom: 20px;
}

/* 移动端优化 - 保持三栏但减小间距 */
@media (max-width: 768px) {
  .stats-grid {
    gap: 8px;
  }
}

.stat-card {
  background-color: var(--stats-item-bg);
  padding: 10px 15px;
  border-radius: var(--radius-lg);
  text-align: center;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  border: 1px solid var(--card-border);
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: var(--gradient-secondary);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
  border-color: var(--button-primary);
}

.stat-card:hover::before {
  opacity: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: var(--button-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: all 0.3s ease;
  margin-bottom: 5px;
  position: relative;
  display: inline-block;
}

.stat-label {
  font-size: 14px;
  color: var(--color-text);
  margin-top: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: all 0.3s ease;
  opacity: 0.8;
}

.stat-card:hover .stat-label {
  opacity: 1;
  color: var(--color-heading);
}

/* 编辑按钮样式 */
.edit-btn {
  position: absolute;
  top: 5px;
  right: 5px;
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  opacity: 0.5;
  transition: all 0.3s ease;
  padding: 4px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}

.edit-btn:hover {
  opacity: 1;
  transform: scale(1.1) rotate(15deg);
  background-color: var(--color-background-mute);
  color: var(--button-primary);
}

/* 编辑对话框样式 */
.edit-dialog {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.edit-dialog-content {
  background-color: var(--card-background);
  border-radius: var(--radius-xl);
  padding: 25px;
  width: 90%;
  max-width: 400px;
  box-shadow: var(--shadow-xl);
  position: relative;
  overflow: hidden;
  animation: dialogAppear 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes dialogAppear {
  0% {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.edit-dialog-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: var(--gradient-primary);
}

.edit-dialog-content h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: var(--color-heading);
  font-size: 1.3rem;
  position: relative;
  padding-bottom: 10px;
}

.edit-dialog-content h3::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 40px;
  height: 2px;
  background: var(--gradient-primary);
}

.edit-field {
  margin-bottom: 20px;
}

.edit-field label {
  display: block;
  margin-bottom: 8px;
  color: var(--color-text);
  font-size: 14px;
  line-height: 1.5;
}

.edit-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background-color: var(--color-background);
  color: var(--color-text);
  font-size: 14px;
  transition: all 0.3s ease;
}

.edit-input:focus {
  outline: none;
  border-color: var(--button-primary);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
}

.text-area {
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
  line-height: 1.5;
}

.boolean-selector {
  display: flex;
  gap: 15px;
  margin-top: 12px;
}

.boolean-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: var(--radius-md);
  background-color: var(--stats-item-bg);
  transition: all 0.3s ease;
  border: 1px solid var(--color-border);
}

.boolean-option:hover {
  background-color: var(--color-background-mute);
  transform: translateY(-2px);
}

.boolean-option input[type="radio"] {
  accent-color: var(--button-primary);
}

.password-field {
  margin-top: 15px;
  position: relative;
}

.password-field label {
  margin-bottom: 8px;
  display: block;
}

.edit-error {
  color: #ef4444;
  font-size: 12px;
  margin-top: 8px;
  padding-left: 5px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.edit-error::before {
  content: '⚠️';
  font-size: 14px;
}

.edit-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.cancel-btn, .save-btn {
  padding: 10px 18px;
  border-radius: var(--radius-md);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.cancel-btn {
  background-color: var(--button-secondary);
  border: 1px solid var(--color-border);
  color: var(--button-secondary-text);
}

.save-btn {
  background: var(--gradient-primary);
  border: none;
  color: white;
  box-shadow: var(--shadow-sm);
}

.cancel-btn:hover {
  background-color: var(--button-secondary-hover);
  transform: translateY(-2px);
}

.save-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* 工具提示样式 */
.tooltip {
  position: fixed;
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 8px 12px;
  border-radius: var(--radius-md);
  font-size: 12px;
  max-width: 250px;
  z-index: 1000;
  pointer-events: none;
  transform: translate(-50%, -100%);
  margin-top: -10px;
  box-shadow: var(--shadow-lg);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: tooltipAppear 0.2s ease;
}

@keyframes tooltipAppear {
  0% {
    opacity: 0;
    transform: translate(-50%, -90%);
  }
  100% {
    opacity: 1;
    transform: translate(-50%, -100%);
  }
}

/* 移动端优化 - 更紧凑的卡片 */
@media (max-width: 768px) {
  .stat-card {
    padding: 8px 8px;
  }
  
  .stat-value {
    font-size: 16px;
  }
  
  .stat-label {
    font-size: 12px;
    margin-top: 2px;
  }
  
  .edit-btn {
    top: 3px;
    right: 3px;
    padding: 2px;
  }
  
  .edit-dialog-content {
    padding: 20px;
  }
  
  .boolean-selector {
    flex-direction: column;
    gap: 8px;
  }
}

/* 小屏幕手机进一步优化 */
@media (max-width: 480px) {
  .stat-card {
    padding: 6px 6px;
  }
  
  .stat-value {
    font-size: 14px;
  }
  
  .stat-label {
    font-size: 11px;
    margin-top: 1px;
  }
  
  .tooltip {
    max-width: 200px;
    font-size: 10px;
  }
  
  .edit-dialog-content {
    padding: 15px;
  }
  
  .edit-dialog-content h3 {
    font-size: 1.1rem;
  }
  
  .edit-input {
    padding: 10px 14px;
    font-size: 13px;
  }
  
  .cancel-btn, .save-btn {
    padding: 8px 14px;
    font-size: 13px;
  }
}

/* 折叠动画和UI优化 */
.fold-header {
  cursor: pointer;
  user-select: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
  border-radius: var(--radius-lg);
  padding: 10px 15px;
  background-color: var(--stats-item-bg);
  border: 1px solid var(--card-border);
  margin-bottom: 15px;
}

.fold-header:hover {
  background-color: var(--color-background-mute);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.fold-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease;
  color: var(--button-primary);
}

.fold-icon.rotated {
  transform: rotate(180deg);
}

.fold-content {
  overflow: hidden;
}

/* 折叠动画 */
.fold-enter-active,
.fold-leave-active {
  transition: all 0.3s ease;
  max-height: 1000px;
  opacity: 1;
  overflow: hidden;
}

.fold-enter-from,
.fold-leave-to {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .fold-header {
    padding: 8px 12px;
  }
}

@media (max-width: 480px) {
  .fold-header {
    padding: 6px 10px;
  }
}
</style>