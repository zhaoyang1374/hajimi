<script setup>
import { useDashboardStore } from '../../../stores/dashboard'

const dashboardStore = useDashboardStore()

// 传递编辑函数
const props = defineProps({
  openEditDialog: {
    type: Function,
    required: true
  }
})
</script>

<template>
  <div>
    <h3 class="section-title">基本配置</h3>
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-value">{{ dashboardStore.config.maxRequestsPerMinute }}</div>
        <div class="stat-label">每分钟请求限制</div>
        <button class="edit-btn" @click="props.openEditDialog('maxRequestsPerMinute', dashboardStore.config.maxRequestsPerMinute)">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
        </button>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ dashboardStore.config.maxRequestsPerDayPerIp }}</div>
        <div class="stat-label">每IP每日请求限制</div>
        <button class="edit-btn" @click="props.openEditDialog('maxRequestsPerDayPerIp', dashboardStore.config.maxRequestsPerDayPerIp)">
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
  </div>
</template>

<style scoped>
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
}
</style> 