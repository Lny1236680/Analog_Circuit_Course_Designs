#!/usr/bin/env python3
"""点光源跟踪器 — 完整电路原理图 (单轴示意, 左右轴)。
链路: 光敏分压(左/右) -> LM358 差动放大(带反馈) -> 输出 Vdiff -> TB6612 驱动 -> 电机
"""
import schemdraw
import schemdraw.elements as elm

U = 2.0
d = schemdraw.Drawing()
d.config(unit=U)

# ============ 1. 左光敏分压 → AO_L ============
# VCC → R1(10K) → 节点AO_L → LDR_L → GND
d += elm.Vdd().at((0, 8*U)).label("VCC 5V")
d += elm.Resistor().down().at((0, 8*U)).to((0, 6*U)).label("R1\n10K", "left")
AO_L = (0, 6*U)
d += elm.Photoresistor().down().at(AO_L).to((0, 4*U)).label("LDR_L", "left")
d += elm.Ground().at((0, 4*U))
d += elm.Dot().at(AO_L).label("AO_L", "left")

# ============ 2. 右光敏分压 → AO_R ============
d += elm.Resistor().down().at((4*U, 8*U)).to((4*U, 6*U)).label("R2\n10K", "left")
AO_R = (4*U, 6*U)
d += elm.Photoresistor().down().at(AO_R).to((4*U, 4*U)).label("LDR_R", "left")
d += elm.Ground().at((4*U, 4*U)).label("", "bottom")
d += elm.Dot().at(AO_R).label("AO_R", "left")
d += elm.Line().right().at((0, 8*U)).to((4*U, 8*U))
# 非反相输入匹配电阻 Rm (改善 CMRR)
d += elm.Resistor().down().at((6.5*U, 6*U+0.625)).to((6.5*U, 4*U)).label("Rm\n10K", "left")
d += elm.Ground().at((6.5*U, 4*U))

# ============ 3. LM358 差动放大 ============
# 同相(+) ← AO_R, 反相(-) ← AO_L, Vout = (Rf/Rin)(AO_R - AO_L)
# Rin = 10K (接输入), Rf = 100K (反馈) => 增益 K_a = 10
op = (8*U, 6*U)
d += elm.Opamp().at(op).anchor("in1").label("LM358", "right")
# 接线: AO_R → (+), AO_L → (-)
d += elm.Line().at(AO_R).right().to((7*U, 6*U + 0.625))
d += elm.Line().at((7*U, 6*U+0.625)).right().to((8*U, 6*U+0.625))
d += elm.Line().at(AO_L).right().to((7*U, 6*U - 0.625))
d += elm.Line().at((7*U, 6*U-0.625)).right().to((8*U, 6*U-0.625))

# 输入电阻 Rin (示意, 简化)
d += elm.Resistor().right().at((6.5*U, 6*U+0.625)).to((7*U, 6*U+0.625)).label("Rin", "top").label("10K", "bottom")
d += elm.Resistor().right().at((6.5*U, 6*U-0.625)).to((7*U, 6*U-0.625)).label("Rin", "top")

# 反馈电阻: 反相输入 → 输出
d += elm.Resistor().at((8*U, 6*U-0.625)).to((8*U, 6*U)).label("Rf 100K", "left")

# ============ 4. 输出 → TB6612 → 电机 ============
out = op  # 输出锚点
d += elm.Dot().at((10.5*U, 6*U)).label("Vout_X\n=K_a(AO_R-AO_L)", "right")
d += elm.Line().at(op).right().to((10.5*U, 6*U))

# TB6612 示意 (标签)
d += elm.Label().at((14*U, 6*U)).label("→ TB6612 通道A\nAIN1/AIN2/PWMA\n驱动左右电机", "center")

d.save(__file__.replace(".py", ".png"), dpi=150)
print("saved", __file__.replace(".py", ".png"))
