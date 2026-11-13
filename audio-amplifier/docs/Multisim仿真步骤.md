# Multisim 仿真步骤

本文说明如何在本仓库的 Multisim 工程上复现音频放大器的三类分析：**瞬态（增益/功率/失真）**、**AC 扫频（频响/带宽）**、**音调控制曲线**，并导出可放进报告或简历附件的截图。

> 建议使用 Multisim 14.x。工程文件为 `multisim/多功能音频放大器.ms14`。

## 0. 准备工作

1. 打开 Multisim，`File → Open` 选择 `多功能音频放大器.ms14`；
2. 确认元件模型齐全：NE5532（或等效运放）、TIP41C、TIP42C、1N4148、电位器；
   - 若某元件显示为问号或提示替换，右键 → `Replace Component`，从 `Master Database` 选同型号；
3. 保存一份副本再改参数，保留原始工程。

## 1. 瞬态分析：增益与最大不失真功率

### 1.1 信号源设置

在输入端放置 `AC_VOLTAGE` 或 `AC_POWER` 源（工程中已有则直接改参数）：

| 参数 | 值 |
|---|---|
| 频率 | 1 kHz |
| 幅值 | 100 mV（rms）/ 141 mV（peak） |
| 直流偏置 | 0 V |

输入端串联 47 kΩ 对地电阻（若工程中已有则不用加）。

### 1.2 运行瞬态分析

`Simulate → Analyses and Simulation → Transient Analysis`：

- Start time：`0 s`
- End time：`20 ms`（覆盖 20 个 1 kHz 周期）
- Maximum time step：`1e-5 s`（10 µs）

输出节点选扬声器两端（差分电压），输入节点选信号源输出。

### 1.3 读数与计算

用游标（Cursor）测输出峰值 `V_peak`：

- 输出有效值：`V_rms = V_peak / √2`
- 输出功率：`P = V_rms² / 8 Ω`
- 电压增益：`Av = V_out,rms / V_in,rms`（设计值 ≈30.3）

**设计预期**：输入 100 mV rms 时输出约 3.03 V rms，P ≈ 1.15 W。

### 1.4 测最大不失真功率

把输入幅值从 100 mV 逐步加大（150 → 200 → 300 mV），每次看输出波形：

- 波形顶部/底部刚开始削平（削顶）时，记录此时的 `V_peak`；
- `P_max = (V_peak/√2)² / 8`；
- 截图保存“临界削顶”波形，注明输入幅值。

## 2. AC 扫频：频响与 -3 dB 带宽

`Simulate → Analyses and Simulation → AC Sweep`：

| 参数 | 值 |
|---|---|
| Start frequency | 10 Hz |
| Stop frequency | 100 kHz |
| Sweep type | Decade |
| Points per decade | 100 |
| Vertical scale | Decibel |

输出表达式选 `V(输出节点)`，得到幅频曲线：

- 中频增益应 ≈29.6 dB；
- 找到增益下降 3 dB 的两个频率，即 `f_L` 与 `f_H`；
- 设计预期：`f_L ≈ 1.5 Hz`（由输入耦合电容决定），`f_H` 远高于 20 kHz。

**截图**：幅频曲线全图 + 20 Hz~20 kHz 区间的平坦度。

## 3. 音调控制曲线

Baxandall 音调级需要在两个极端位置各扫一次：

1. 低音电位器 `P_BASS` 旋到最大 → AC 扫频 → 记录 100 Hz 处增益；
2. `P_BASS` 旋到最小 → 再扫一次 → 记录 100 Hz 处增益；
3. 两者之差应 ≈24 dB（±12 dB）；
4. 高音电位器 `P_TREBLE` 同理，在 10 kHz 处测差值。

把两条曲线放在同一张图里导出，就是音调控制特性的标准图。

> 提示：Multisim 的电位器可在仿真前用属性里的 `Key` 或直接改 `Resistance` 百分比来设置位置；也可以做参数扫描（Parameter Sweep）。

## 4. 失真分析（可选）

两种做法：

- **傅里叶分析**：`Simulate → Analyses → Fourier Analysis`，基频 1 kHz，看 2/3 次谐波幅值，估算 THD；
- **失真分析仪**：虚拟仪器栏里的 `Distortion Analyzer`，接输出端直接读 THD。

记录：输入 1 kHz、输出接近最大不失真时的 THD 值。

## 5. 导出截图

- 波形窗口：`Tools → Capture Screen Area`，或直接 `Alt+PrintScreen` 后裁剪；
- 图形（Bode/瞬态曲线）：右键图 → `Export as image`；
- 建议命名：
  - `transient_1kHz_100mV.png`
  - `max_undistorted_output.png`
  - `ac_sweep_bode.png`
  - `tone_bass_max_min.png`

## 6. 常见问题

| 现象 | 原因/处理 |
|---|---|
| 输出一直是 0 | 电源未接/未使能；检查 ±15 V 是否接到运放与输出管 |
| 波形严重削顶 | 输入过大或静态工作点不对；先降输入再看偏置 |
| 运放提示模型替换 | 工程使用了简化宏模型，替换为库内 NE5532 后重新接线 |
| 仿真不收敛 | 减小最大步长（1e-6）、给输出节点加 1 kΩ 到地、检查悬空节点 |
| 输出有高频毛刺 | 正常现象（开关/数值噪声），可加 100 pF 积分电容观察变化 |

## 7. 结果记录模板

| 指标 | 设计值 | 仿真值 | 备注 |
|---|---|---|---|
| 中频增益 | 30.3（29.6 dB） | | 1 kHz，100 mV rms 输入 |
| 最大不失真功率 | >1 W | | 8 Ω 负载 |
| 下限频率 f_L | ≈1.5 Hz | | -3 dB |
| 上限频率 f_H | ≫20 kHz | | -3 dB |
| 低音调节范围 @100 Hz | ±12 dB | | 电位器两端 |
| 高音调节范围 @10 kHz | ±12 dB | | 电位器两端 |
| THD | — | | 接近最大输出时 |
