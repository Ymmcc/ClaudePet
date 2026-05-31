# 番茄钟功能实现计划

## 概述

基于设计文档 `docs/superpowers/specs/2026-05-31-pomodoro-timer-design.md`，实现轻量级番茄钟功能。

---

## 任务清单

### 任务 1：修改 behaviors.py

**文件**：`core/behaviors.py`

**修改内容**：
- 添加 `pause()` 和 `resume()` 方法
- 添加 `_paused` 状态标志
- `_tick()` 中检查暂停状态，暂停时不触发行为

**验收标准**：
- 调用 `pause()` 后，定时器继续运行但不触发行为
- 调用 `resume()` 后，恢复正常随机行为

---

### 任务 2：修改 pet_window.py - 添加 FocusTimer

**文件**：`core/pet_window.py`

**新增类**：`FocusTimer(QObject)`

**属性**：
- `_timer`: QTimer (1000ms)
- `_remaining`: int (剩余秒数)
- `_state`: "idle" | "focus" | "break"
- `_paused`: bool

**信号**：
- `tick(int, str)`: 每秒发射，传递(剩余秒数, 状态)
- `finished(str)`: 状态完成时发射

**方法**：
- `start_focus()`: 开始25分钟专注
- `start_break()`: 开始5分钟休息
- `pause()`: 暂停计时
- `resume()`: 恢复计时
- `stop()`: 停止计时
- `_on_tick()`: 每秒更新逻辑
- `_format_time(int)`: 格式化时间显示

---

### 任务 3：修改 pet_window.py - 集成到 PetWindow

**文件**：`core/pet_window.py`

**修改内容**：

1. **__init__ 中添加**：
   - 创建 `FocusTimer` 实例
   - 连接 `tick` 信号到 `_on_focus_tick`
   - 连接 `finished` 信号到 `_on_focus_finished`

2. **新增方法**：
   - `_on_focus_tick(remaining, state)`: 更新气泡显示
   - `_on_focus_finished(state)`: 处理状态完成
   - `start_focus()`: 开始专注（触发动画+计时器）
   - `stop_focus()`: 停止专注
   - `toggle_focus_pause()`: 切换暂停/恢复

3. **修改右键菜单**：
   - 在 `contextMenuEvent` 中根据番茄钟状态添加菜单项

---

## 实现顺序

1. 先实现 `behaviors.py` 的暂停功能
2. 再实现 `FocusTimer` 类
3. 最后集成到 `PetWindow`

---

## 测试场景

1. **基本流程**：开始专注 → 25分钟倒计时 → 休息5分钟 → 回到空闲
2. **暂停/恢复**：专注中暂停 → 恢复继续倒计时
3. **放弃**：专注中放弃 → 回到空闲
4. **跳过休息**：休息中跳过 → 回到空闲
5. **气泡显示**：倒计时正确显示，格式正确
