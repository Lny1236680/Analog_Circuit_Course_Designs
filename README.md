# 模拟电路课程设计作品集

本仓库收录两个模拟电路方向的课程设计：**多功能音频功率放大器**与**点光源跟踪器**。内容包括设计推导、元件选型、Multisim 仿真工程/网表、电路图与控制分析，用于展示模拟电路设计、仿真验证与控制系统分析能力。

| 项目 | 类型 | 主要工具 | 目录 |
|---|---|---|---|
| 多功能音频功率放大器 | 模拟电子技术课程设计 | Multisim、手工计算 | [`audio-amplifier/`](audio-amplifier/) |
| 点光源跟踪器 | 控制原理课程设计（纯模拟，无 MCU） | Multisim、Python(control/matplotlib) | [`light-tracker/`](light-tracker/) |

## 项目一：多功能音频功率放大器

在**禁用专用功放 IC**的约束下，完成 1 W / 8 Ω、20 Hz–20 kHz、高低音 ±12 dB 的音频功放设计。

- 三级架构：NE5532 输入缓冲 → 有源 Baxandall 音调控制 → 运放驱动 TIP41C/TIP42C 互补 AB 类推挽输出；
- 完成从指标到元件值的完整推导：输出峰值 4 V / 0.5 A、±15 V 供电、功放级增益 ≈30.3、输出功率 ≈1.15 W；
- 提供 Multisim 工程、SPICE 网表与完整设计文档。

详见 [`audio-amplifier/README.md`](audio-amplifier/README.md)。

## 项目二：点光源跟踪器（纯模拟）

不使用任何可编程器件，用纯模拟电路实现双轴（左右 + 上下）点光源跟踪。

- 4 路光敏电阻分压 → LM358 差动放大（增益 10）→ TB6612 双 H 桥驱动两轴直流电机；
- 建立位置伺服模型 `T(s)=10/(0.001s³+0.11s²+s+10)`，分析阶跃响应、相位裕度（PM=47.4°）、增益灵敏度；
- 提供 Multisim 网表、电路图、阶跃响应/伯德图/根轨迹与分析脚本。

详见 [`light-tracker/README.md`](light-tracker/README.md)。

## 目录结构

```
.
├── audio-amplifier/
│   ├── README.md
│   ├── docs/
│   │   ├── 设计文档.md          # 指标、架构、逐级计算、BOM
│   │   ├── Multisim仿真步骤.md   # 复现仿真并导出波形/频响的操作说明
│   │   └── 简历项目描述.md       # 可直接用于简历的项目描述
│   ├── multisim/
│   │   └── 多功能音频放大器.ms14  # Multisim 工程
│   └── netlist/
│       ├── audio_amplifier.cir
│       ├── audio_amp_mod.cir
│       └── audio_amp_redesign.cir
└── light-tracker/
    ├── 1-系统方案.md ~ 5-仿真验证.md
    ├── 3-控制分析.py / 3-控制分析报告.md
    ├── light_tracker_x.cir
    ├── schem_*.py / schem_*.png
    └── report/                  # 阶跃响应、伯德图、根轨迹
```

## 复现方式

- **Multisim 工程**：Multisim 14.x 打开 `audio-amplifier/multisim/多功能音频放大器.ms14`；
- **SPICE 网表**：Multisim `文件 → 打开` 直接导入 `.cir`（网表不含坐标，导入后需手动整理布局）；
- **电路图**：`light-tracker/schem_*.py` 依赖 `schemdraw` 与 `matplotlib`，运行即可重新生成 PNG；
- **控制分析**：`light-tracker/3-控制分析.py` 依赖 Python `control`、`matplotlib`。

## 说明

- 仓库内容以**设计计算与 Multisim 仿真**为主，实物测试数据与示波器波形尚未整理归档；
- 另一版分立元件 OCL 音频功放课设报告含个人信息，未收入本仓库。
