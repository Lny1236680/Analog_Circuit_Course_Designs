#!/usr/bin/env python3
"""点光源跟踪器 — 控制原理分析
================================
系统建模 (单轴 X):
  光敏传感 Gs(s)  = Ks / (τs·s + 1)       # 一阶惯性 (光响应 ~ms)
  差动放大 Ga(s)  = Ka = Rf/Rin = 10      # 比例 (P 控制)
  电机+负载 Gm(s) = Km / [s(τm·s + 1)]    # 一阶惯性 + 积分 (位置伺服)
  闭环 = 单位负反馈

  G(s) = Ka · Gs · Gm = K / [s(τs s+1)(τm s+1)],  K = Ka·Ks·Km

分析内容:
  1. 传递函数模型与开环/闭环
  2. 阶跃响应 (跟踪性能: 稳态误差, 超调, 调节时间)
  3. 伯德图 (稳定性裕度)
  4. 根轨迹 (增益 K 变化对稳定性的影响)
  5. 参数灵敏度 (K/τ 对性能影响)

输出 PNG 到 report/ 目录, 供课设报告使用。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import control as ct

# 注册中文字体 (微软雅黑, 从 WSL 的 Windows 字体复制)
_FONT = '/home/yang/.local/lib/python3.12/site-packages/matplotlib/mpl-data/fonts/ttf/msyh.ttc'
try:
    fm.fontManager.addfont(_FONT)
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
except Exception:
    pass  # 无中文字体时回退默认

# ================= 参数 (典型值, 可调) =================
Ka  = 10.0      # 差动放大增益 Rf/Rin = 100k/10k
Ks  = 0.5       # 光敏传感增益 (V/V, 分压灵敏度)
Km  = 2.0       # 电机增益 (rad/s per V)
tau_s = 0.01    # 光敏时间常数 10ms
tau_m = 0.1     # 电机机械时间常数 100ms

# ================= 1. 传递函数建模 =================
# 传感: Ks/(τs s + 1)
Gs = ct.tf([Ks], [tau_s, 1])
# 放大: Ka
Ga = ct.tf([Ka], [1])
# 电机: Km/[s(τm s + 1)]
Gm = ct.tf([Km], [1, 0]) * ct.tf([1], [tau_m, 1])  # = Km/[s(τm s+1)]

# 开环
G_open = Ga * Gs * Gm
# 闭环 (单位负反馈)
G_closed = ct.feedback(G_open, 1)

print("=" * 60)
print("点光源跟踪器 单轴控制模型")
print("=" * 60)
print(f"\n传感 Gs(s)    = {Ks}/({tau_s}s+1) =")
print(Gs)
print(f"\n放大 Ga       = {Ka}")
print(f"\n电机 Gm(s)    = {Km}/[s({tau_m}s+1)]")
print(f"\n开环 G(s)     = Ka·Gs·Gm =")
print(G_open)
print(f"\n闭环 T(s)     = G/(1+G) =")
print(G_closed)

# ================= 2. 阶跃响应 =================
t_end = 2.0
t = np.linspace(0, t_end, 2000)
t_open, y_open = ct.step_response(G_open, T=t)
t_cl, y_cl = ct.step_response(G_closed, T=t)

# 稳态误差 (闭环对单位阶跃的跟踪)
yss = y_cl[-1]
ess = 1.0 - yss
print(f"\n[阶跃响应]")
print(f"  闭环稳态值 yss = {yss:.3f}")
print(f"  稳态误差 ess   = {ess:.3f}  ({ess*100:.1f}%)")
print(f"  → 一型系统, 对阶跃输入有 {ess*100:.0f}% 稳态误差 (P 控制固有)")
# 超调
peak = np.max(y_cl)
Mp = (peak - yss) / yss * 100 if yss != 0 else 0
print(f"  超调量 Mp     = {Mp:.1f}%")
# 调节时间 (2%)
settle_idx = np.where(np.abs(y_cl - yss) > 0.02 * yss)[0]
ts = t_cl[-1] if len(settle_idx) == 0 else t_cl[settle_idx[-1]] if settle_idx[-1] < len(t_cl)-1 else t_cl[-1]
print(f"  调节时间 ts   ≈ {ts:.2f} s (5% 带)")
# 上升时间
rise_idx = np.where(y_cl >= 0.9 * yss)[0]
tr = t_cl[rise_idx[0]] if len(rise_idx) else float('nan')
print(f"  上升时间 tr   ≈ {tr:.2f} s")

# ================= 3. 伯德图 (稳定性) =================
gm, pm, wgm, wpm = ct.margin(G_open)
print(f"\n[稳定性裕度]")
print(f"  增益裕度 GM = {gm:.2f} ({20*np.log10(gm):.1f} dB)")
print(f"  相位裕度 PM = {pm:.1f}°")
print(f"  穿越频率   = {wpm:.2f} rad/s")
print(f"  → PM > 30° 系统稳定; 当前 PM={pm:.1f}° {'稳定✓' if pm > 30 else '需降增益⚠️'}")

# ================= 4. 根轨迹 =================
plt.figure(figsize=(10, 7))
ct.root_locus(G_open, plot=True, grid=True)
plt.title(f"根轨迹 (K = Ka·Ks·Km = {Ka*Ks*Km:.1f})")
plt.grid(True)
plt.savefig("report/根轨迹.png", dpi=130)
plt.close()
print("\n[图] 根轨迹 → report/根轨迹.png")

# ================= 5. 绘图: 阶跃响应 =================
plt.figure(figsize=(10, 6))
plt.plot(t_cl*1000, y_cl, 'b-', linewidth=2, label=f"闭环阶跃 (K={Ka*Ks*Km:.1f})")
plt.plot(t_open*1000, y_open, 'r--', linewidth=1.5, label="开环 (不收敛)")
plt.axhline(1.0, color='gray', ls=':', label="参考输入=1")
plt.axhline(yss, color='green', ls='--', alpha=0.7, label=f"稳态 yss={yss:.2f}")
plt.xlabel("时间 (ms)")
plt.ylabel("跟踪位置 (归一化)")
plt.title("点光源跟踪器 — 阶跃响应 (P 控制)")
plt.legend()
plt.grid(True)
plt.savefig("report/阶跃响应.png", dpi=130)
plt.close()
print("[图] 阶跃响应 → report/阶跃响应.png")

# ================= 6. 伯德图 =================
plt.figure(figsize=(10, 8))
mag, phase, omega = ct.bode_plot(G_open, dB=True, plot=False)
# 用 freqresp 拿数据
omega_r = np.logspace(-2, 3, 500)
mag_r, phase_r, om = ct.freqresp(G_open, omega_r)
mag_db = 20 * np.log10(abs(mag_r))
phase_deg = np.degrees(phase_r)

plt.subplot(2, 1, 1)
plt.semilogx(om, mag_db)
plt.axhline(0, color='k', ls='--', lw=0.8)
plt.axhline(-3, color='r', ls='--', lw=0.8, label="-3 dB")
plt.ylabel("幅值 (dB)")
plt.title("开环伯德图 — 稳定性分析")
plt.legend()
plt.grid(True, which='both')

plt.subplot(2, 1, 2)
plt.semilogx(om, phase_deg)
plt.axhline(-180, color='r', ls='--', lw=0.8)
plt.ylabel("相位 (°)")
plt.xlabel("频率 (rad/s)")
plt.grid(True, which='both')
plt.tight_layout()
plt.savefig("report/伯德图.png", dpi=130)
plt.close()
print("[图] 伯德图 → report/伯德图.png")

# ================= 7. 参数灵敏度分析 =================
# 增益 K 对 PM 的影响 (找到临界稳定增益)
print(f"\n[参数灵敏度] 增益 K 对稳定性影响:")
K_test = np.logspace(0, 2, 5)
for Kc in K_test:
    Gc = G_open * (Kc / (Ka*Ks*Km))   # 缩放增益
    gm_c, pm_c, _, _ = ct.margin(Gc)
    stable = "稳定" if pm_c > 0 else "不稳定"
    print(f"  K={Kc:6.1f} → PM={pm_c:6.1f}°  {stable}")

print("\n" + "=" * 60)
print("结论: P 控制有稳态误差; 若要消除需加积分 (PI 控制器)。")
print("可通过减小 Ka (增益) 提高稳定性, 但会增大稳态误差。")
print("=" * 60)
