#!/usr/bin/env python3
"""差动放大级电路图 — LM358 差分放大 (单轴).
链路: AO_R -> Rin -> (+), AO_L -> Rin -> (-) -> Rf 反馈 -> Vout
"""
import schemdraw
import schemdraw.elements as elm

U = 2.0
d = schemdraw.Drawing()
d.config(unit=U)

# 运放 (中心 ~8U, 3U)
op = (8*U, 3*U)
d += elm.Opamp().at(op).anchor("in1").label("LM358", "right")

# 同相输入 (+) : AO_R -> Rin -> (+)
d += elm.Dot().at((2*U, 4*U)).label("AO_R", "left")
d += elm.Resistor().right().at((2*U, 4*U)).to((6*U, 4*U)).label("Rin 10K", "top")
d += elm.Line().at((6*U, 4*U)).right().to((8*U, 3*U+0.625))
# 匹配电阻 Rm (+ → GND)
d += elm.Resistor().down().at((6*U, 4*U)).to((6*U, 2*U)).label("Rm 10K", "right")
d += elm.Ground().at((6*U, 2*U))

# 反相输入 (-) : AO_L -> Rin -> (-)
d += elm.Dot().at((2*U, 2*U)).label("AO_L", "left")
d += elm.Resistor().right().at((2*U, 2*U)).to((6*U, 2*U)).label("Rin 10K", "bottom")
d += elm.Line().at((6*U, 2*U)).right().to((8*U, 3*U-0.625))

# 反馈电阻 Rf: (-) -> 输出
d += elm.Resistor().at((8*U, 3*U-0.625)).to((8*U, 3*U)).label("Rf 100K", "left")

# 输出
d += elm.Line().right().at((8*U, 3*U)).to((11*U, 3*U))
d += elm.Dot().at((11*U, 3*U)).label("Vout_X", "right").label(f"= Ka·(AO_R−AO_L)\nKa=Rf/Rin=10", "bottom")

d.save(__file__.replace(".py", ".png"), dpi=150)
print("saved", __file__.replace(".py", ".png"))
