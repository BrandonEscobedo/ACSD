// PortScene.jsx
// Two panels side-by-side:
//   Left  → CraneCanvas  (ship + quay crane animation)
//   Right → YardPanel    (container yard – stacks containers as they arrive)
// Usage: <PortScene />

import { useEffect, useRef, useState, useCallback } from "react";

/* ─────────────── shared ─────────────── */
const COLORS = ["#E63946","#457B9D","#F4A261","#2A9D8F","#E9C46A","#6A4C93","#e76f51","#264653"];
const CW = 38, CH = 24, PAD_X = 3, PAD_Y = 2;

function drawBox(ctx, x, y, color) {
  ctx.fillStyle = color;
  ctx.fillRect(x, y, CW, CH);
  ctx.strokeStyle = "rgba(0,0,0,0.22)"; ctx.lineWidth = 0.5;
  ctx.strokeRect(x, y, CW, CH);
  ctx.strokeStyle = "rgba(0,0,0,0.13)";
  for (let i = 1; i < 3; i++) {
    ctx.beginPath(); ctx.moveTo(x + i*(CW/3), y); ctx.lineTo(x + i*(CW/3), y + CH); ctx.stroke();
  }
  ctx.strokeStyle = "rgba(255,255,255,0.32)"; ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(x+2, y+2); ctx.lineTo(x+CW-2, y+2); ctx.stroke();
}

function drawCloud(ctx, x, y, s) {
  ctx.fillStyle = "rgba(255,255,255,0.65)";
  [[0,0,28],[22,5,20],[44,2,22],[66,5,18]].forEach(([dx,dy,r]) => {
    ctx.beginPath(); ctx.arc(x+dx*s, y+dy*s, r*s, 0, Math.PI*2); ctx.fill();
  });
}

/* ─────────────── CraneCanvas constants ─────────────── */
const CW_C = 560, CH_C = 460;
const SHIP_LEFT = 150, SHIP_RIGHT = 515;
const SHIP_DECK_Y = 248, SHIP_HULL_BOTTOM = 310;
const QUAY_Y = 340;
const CRANE_ARM_Y = 52, CRANE_ARM_LEN = 180;
const CRANE_BASE_Y = QUAY_Y;
const S_COLS = 8, S_ROWS = 5;
const STACK_SX = SHIP_LEFT + 14;
const STACK_SY = SHIP_DECK_Y - S_ROWS*(CH+PAD_Y);

function makeShipContainers() {
  const a = [];
  for (let r = 0; r < S_ROWS; r++)
    for (let c = 0; c < S_COLS; c++)
      a.push({
        col: c, row: r,
        x: STACK_SX + c*(CW+PAD_X),
        y: STACK_SY + r*(CH+PAD_Y),
        color: COLORS[(r*S_COLS+c) % COLORS.length],
        visible: true,
      });
  return a;
}

/* ─────────────── YardPanel constants ─────────────── */
const YW = 180, YH = 460;
const Y_COLS = 4;
const YARD_FLOOR_Y = YH - 60;
const YARD_START_X = 10;
const YARD_COL_W = CW + PAD_X;

function getYardSlot(existing) {
  const heights = Array(Y_COLS).fill(0);
  existing.forEach(c => { heights[c.col]++; });
  let col = 0;
  for (let i = 1; i < Y_COLS; i++) if (heights[i] < heights[col]) col = i;
  const row = heights[col];
  return {
    col, row,
    x: YARD_START_X + col*YARD_COL_W,
    y: YARD_FLOOR_Y - (row+1)*(CH+PAD_Y),
  };
}

/* ─────────────── CraneCanvas ─────────────── */
function CraneCanvas({ onContainerDelivered, onReset }) {
  const canvasRef = useRef(null);
  const stateRef  = useRef({ containers: makeShipContainers(), animState: null, craneMastX: 60, rafId: null });
  const [status, setStatus] = useState("Presiona para descargar un contenedor");
  const [busy, setBusy]     = useState(false);

  const draw = useCallback(() => {
    const canvas = canvasRef.current; if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const { containers, animState, craneMastX } = stateRef.current;
    ctx.clearRect(0, 0, CW_C, CH_C);

    // sky
    ctx.fillStyle = "#b8ddf0"; ctx.fillRect(0, 0, CW_C, CH_C);
    drawCloud(ctx, 40, 36, 0.65); drawCloud(ctx, 310, 22, 0.48); drawCloud(ctx, 190, 15, 0.55);

    // water
    ctx.fillStyle = "#4a90b8"; ctx.fillRect(0, SHIP_HULL_BOTTOM, CW_C, QUAY_Y - SHIP_HULL_BOTTOM + 2);
    ctx.fillStyle = "#3d7fa8"; ctx.fillRect(0, SHIP_HULL_BOTTOM, CW_C, 28);
    ctx.strokeStyle = "rgba(255,255,255,0.2)"; ctx.lineWidth = 1.5;
    for (let i = 0; i < 5; i++) {
      const wx = i*95+5, wy = SHIP_HULL_BOTTOM + 10 + (i%2)*6;
      ctx.beginPath(); ctx.moveTo(wx, wy); ctx.bezierCurveTo(wx+18, wy-4, wx+45, wy+4, wx+75, wy); ctx.stroke();
    }

    // quay
    ctx.fillStyle = "#8a8070"; ctx.fillRect(0, QUAY_Y, CW_C, CH_C-QUAY_Y);
    ctx.fillStyle = "#a09585"; ctx.fillRect(0, QUAY_Y, CW_C, 10);
    ctx.fillStyle = "#6e6055"; ctx.fillRect(0, QUAY_Y+10, CW_C, 4);
    ctx.strokeStyle = "rgba(0,0,0,0.07)"; ctx.lineWidth = 1;
    for (let i = 0; i < CW_C; i += 40) { ctx.beginPath(); ctx.moveTo(i, QUAY_Y+14); ctx.lineTo(i, CH_C); ctx.stroke(); }
    for (let j = QUAY_Y+14; j < CH_C; j += 30) { ctx.beginPath(); ctx.moveTo(0, j); ctx.lineTo(CW_C, j); ctx.stroke(); }
    ctx.fillStyle = "#555045";
    for (let bx = 40; bx < CW_C; bx += 70) {
      ctx.beginPath(); ctx.arc(bx, QUAY_Y+8, 5, 0, Math.PI*2); ctx.fill();
      ctx.fillStyle = "#777"; ctx.beginPath(); ctx.arc(bx, QUAY_Y+8, 2.5, 0, Math.PI*2); ctx.fill();
      ctx.fillStyle = "#555045";
    }
    ctx.fillStyle = "rgba(0,0,0,0.18)"; ctx.fillRect(0, QUAY_Y, CW_C, 3);

    // ship
    ctx.fillStyle = "#1a3a5c";
    ctx.beginPath(); ctx.moveTo(SHIP_LEFT, SHIP_DECK_Y); ctx.lineTo(SHIP_LEFT-8, SHIP_HULL_BOTTOM); ctx.lineTo(SHIP_RIGHT+8, SHIP_HULL_BOTTOM); ctx.lineTo(SHIP_RIGHT, SHIP_DECK_Y); ctx.closePath(); ctx.fill();
    ctx.fillStyle = "#2d5a8e"; ctx.fillRect(SHIP_LEFT, SHIP_DECK_Y-8, SHIP_RIGHT-SHIP_LEFT, 10);
    ctx.fillStyle = "#c0392b"; ctx.fillRect(SHIP_LEFT-6, SHIP_HULL_BOTTOM-7, SHIP_RIGHT-SHIP_LEFT+12, 5);
    ctx.fillStyle = "#c9d6e3"; ctx.fillRect(SHIP_RIGHT-50, SHIP_DECK_Y-55, 44, 50);
    ctx.fillStyle = "#a8bdd4"; for (let i = 0; i < 3; i++) ctx.fillRect(SHIP_RIGHT-45+i*13, SHIP_DECK_Y-48, 9, 9);
    ctx.fillStyle = "#888"; ctx.fillRect(SHIP_RIGHT-37, SHIP_DECK_Y-70, 10, 17);

    // containers on ship
    containers.filter(c => c.visible).forEach(con => drawBox(ctx, con.x, con.y, con.color));

    // crane
    const mx = craneMastX;
    const armEnd = mx + CRANE_ARM_LEN;
    const trolleyX = animState ? animState.cableX : armEnd;

    ctx.fillStyle = "#4a4035"; ctx.fillRect(mx-55, CRANE_BASE_Y-6, 110, 10);
    ctx.fillStyle = "#333"; ctx.fillRect(mx-50, CRANE_BASE_Y-8, 100, 3);
    ctx.fillStyle = "#2a2a2a";
    for (let wx = -36; wx <= 36; wx += 24) {
      ctx.beginPath(); ctx.arc(mx+wx, CRANE_BASE_Y+6, 7, 0, Math.PI*2); ctx.fill();
      ctx.fillStyle = "#555"; ctx.beginPath(); ctx.arc(mx+wx, CRANE_BASE_Y+6, 3.5, 0, Math.PI*2); ctx.fill();
      ctx.fillStyle = "#2a2a2a";
    }
    ctx.strokeStyle = "#5a5045"; ctx.lineWidth = 9; ctx.lineCap = "round";
    ctx.beginPath(); ctx.moveTo(mx-16, CRANE_BASE_Y); ctx.lineTo(mx, CRANE_ARM_Y+20); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(mx+16, CRANE_BASE_Y); ctx.lineTo(mx, CRANE_ARM_Y+20); ctx.stroke();
    ctx.strokeStyle = "#666"; ctx.lineWidth = 8;
    ctx.beginPath(); ctx.moveTo(mx, CRANE_BASE_Y); ctx.lineTo(mx, CRANE_ARM_Y); ctx.stroke();
    ctx.lineWidth = 7; ctx.beginPath(); ctx.moveTo(mx-18, CRANE_ARM_Y); ctx.lineTo(armEnd, CRANE_ARM_Y); ctx.stroke();
    ctx.lineWidth = 2; ctx.strokeStyle = "#888";
    for (let i = 0; i < 5; i++) {
      const bx = mx+8+i*((CRANE_ARM_LEN-8)/5);
      ctx.beginPath(); ctx.moveTo(bx, CRANE_ARM_Y); ctx.lineTo(bx+18, CRANE_ARM_Y+20); ctx.stroke();
    }
    ctx.strokeStyle = "#666"; ctx.lineWidth = 7;
    ctx.beginPath(); ctx.moveTo(mx-18, CRANE_ARM_Y); ctx.lineTo(mx-58, CRANE_ARM_Y); ctx.stroke();
    ctx.fillStyle = "#4a4035"; ctx.fillRect(mx-68, CRANE_ARM_Y-13, 18, 20);
    ctx.fillStyle = "#444"; ctx.fillRect(trolleyX-7, CRANE_ARM_Y+4, 14, 8);

    const cableBot = animState ? animState.hookY : CRANE_ARM_Y + 30;
    ctx.strokeStyle = "#bbb"; ctx.lineWidth = 1; ctx.setLineDash([3,3]);
    ctx.beginPath(); ctx.moveTo(trolleyX, CRANE_ARM_Y+12); ctx.lineTo(trolleyX, cableBot); ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = "#777"; ctx.fillRect(trolleyX-4, cableBot, 8, 5);

    if (animState && animState.carrying) drawBox(ctx, animState.containerX, animState.containerY, animState.color);
  }, []);

  const finishAnim = useCallback((color) => {
    const s = stateRef.current;
    s.animState = null; s.craneMastX = 60;
    setBusy(false);
    const vis = s.containers.filter(c => c.visible);
    setStatus(vis.length ? `Quedan ${vis.length} contenedores en el buque.` : "¡Buque vacío!");
    onContainerDelivered(color);
    draw();
  }, [draw, onContainerDelivered]);

  const loop = useCallback(() => {
    const s = stateRef.current; const anim = s.animState; if (!anim) return;
    if (anim.phase === "moveCrane") {
      const dx = anim.targetMastX - s.craneMastX; s.craneMastX += dx*0.08;
      anim.cableX = s.craneMastX + CRANE_ARM_LEN;
      if (Math.abs(dx) < 0.5) {
        s.craneMastX = anim.targetMastX;
        anim.cableX = s.craneMastX + CRANE_ARM_LEN;
        anim.phase = "moveTrolleyToPickup";
      }
    } else if (anim.phase === "moveTrolleyToPickup") {
      const dx = anim.targetCableX - anim.cableX; anim.cableX += dx*0.09;
      if (Math.abs(dx) < 0.8) {
        anim.cableX = anim.targetCableX;
        anim.phase = "lowerHook";
      }
    } else if (anim.phase === "lowerHook") {
      const dy = anim.pickupY - anim.hookY; anim.hookY += dy*0.12;
      if (Math.abs(dy) < 0.8) {
        anim.hookY = anim.pickupY;
        anim.pickRef.visible = false;
        anim.carrying = true;
        anim.containerX = anim.cableX - CW/2;
        anim.containerY = anim.pickupY;
        anim.phase = "liftUp";
      }
    } else if (anim.phase === "liftUp") {
      const dy = anim.liftTargetY - anim.hookY; anim.hookY += dy*0.1;
      anim.containerX = anim.cableX - CW/2;
      anim.containerY = anim.hookY;
      if (Math.abs(dy) < 0.8) {
        anim.hookY = anim.liftTargetY;
        anim.containerY = anim.hookY;
        anim.phase = "moveTrolleyRight";
      }
    } else if (anim.phase === "moveTrolleyRight") {
      const armEnd = s.craneMastX + CRANE_ARM_LEN;
      const dx = armEnd - anim.cableX;
      anim.cableX += dx*0.08;
      anim.containerX = anim.cableX - CW/2;
      anim.containerY = anim.hookY;
      if (Math.abs(dx) < 0.8) {
        anim.cableX = armEnd;
        anim.containerX = anim.cableX - CW/2;
        anim.phase = "moveCraneRight";
      }
    } else if (anim.phase === "moveCraneRight") {
      s.craneMastX += 4;
      anim.cableX = s.craneMastX + CRANE_ARM_LEN;
      anim.containerX = anim.cableX - CW/2;
      anim.containerY = anim.hookY;
      if (anim.containerX > CW_C + 10) { finishAnim(anim.color); return; }
    }
    draw(); s.rafId = requestAnimationFrame(loop);
  }, [draw, finishAnim]);

  const startAnim = useCallback(() => {
    const s = stateRef.current; if (s.animState) return;
    const vis = s.containers.filter(c => c.visible);
    vis.sort((a,b) => a.row - b.row || a.col - b.col);
    const top = vis[0]; if (!top) { setStatus("¡Buque vacío!"); return; }
    const conCenterX = top.x + CW/2;
    const idealMastX = Math.max(20, Math.min(320, conCenterX - CRANE_ARM_LEN));
    setBusy(true);
    s.animState = {
      phase: "moveCrane", targetMastX: idealMastX,
      targetCableX: conCenterX, cableX: s.craneMastX + CRANE_ARM_LEN,
      pickupY: top.y,
      hookY: CRANE_ARM_Y + 30,
      carrying: false,
      pickRef: top,
      containerX: top.x,
      containerY: top.y,
      color: top.color, liftTargetY: CRANE_ARM_Y + 14,
    };
    s.rafId = requestAnimationFrame(loop);
  }, [loop]);

  const reset = useCallback(() => {
    const s = stateRef.current;
    if (s.rafId) cancelAnimationFrame(s.rafId);
    s.animState = null; s.craneMastX = 60; s.containers = makeShipContainers();
    setBusy(false); setStatus("Presiona para descargar un contenedor"); draw();
    if (onReset) onReset();
  }, [draw, onReset]);

  useEffect(() => { draw(); }, [draw]);

  return (
    <div style={{ display:"flex", flexDirection:"column" }}>
      <canvas ref={canvasRef} width={CW_C} height={CH_C}
        style={{ borderRadius:"12px 12px 0 0", display:"block" }} />
      <div style={{
        background:"#1a2a3a", borderRadius:"0 0 12px 12px", width:CW_C,
        padding:"11px 16px", display:"flex", alignItems:"center", justifyContent:"space-between", gap:8,
      }}>
        <span style={{ fontSize:12, color:"#8aabcc", flex:1 }}>{status}</span>
        <div style={{ display:"flex", gap:8 }}>
          <button onClick={startAnim} disabled={busy} style={{
            padding:"8px 18px", borderRadius:7, border:"none",
            background:"#2d7dd2", color:"#fff", fontSize:12, fontWeight:600,
            cursor: busy ? "not-allowed" : "pointer", opacity: busy ? 0.4 : 1,
          }}>⬡ Descargar</button>
          <button onClick={reset} style={{
            padding:"8px 12px", borderRadius:7,
            border:"1px solid #3a5a7a", background:"transparent",
            color:"#8aabcc", fontSize:12, cursor:"pointer",
          }}>↺</button>
        </div>
      </div>
    </div>
  );
}

/* ─────────────── YardPanel ─────────────── */
function YardPanel({ yardItems }) {
  const canvasRef = useRef(null);

  const drawYard = useCallback(() => {
    const canvas = canvasRef.current; if (!canvas) return;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, YW, YH);

    // sky
    ctx.fillStyle = "#b8ddf0"; ctx.fillRect(0, 0, YW, YH);
    // tiny clouds
    ctx.fillStyle = "rgba(255,255,255,0.6)";
    [[20,30,10],[60,20,8],[110,35,9],[150,24,7]].forEach(([x,y,r]) => {
      ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI*2); ctx.fill();
      ctx.beginPath(); ctx.arc(x+14, y+2, r-2, 0, Math.PI*2); ctx.fill();
    });

    // asphalt
    ctx.fillStyle = "#5a5650"; ctx.fillRect(0, YARD_FLOOR_Y, YW, YH-YARD_FLOOR_Y);
    ctx.fillStyle = "#6a6560"; ctx.fillRect(0, YARD_FLOOR_Y, YW, 8);
    ctx.strokeStyle = "rgba(0,0,0,0.1)"; ctx.lineWidth = 1;
    for (let i = 0; i < YW; i += 20) { ctx.beginPath(); ctx.moveTo(i, YARD_FLOOR_Y+8); ctx.lineTo(i, YH); ctx.stroke(); }
    for (let j = YARD_FLOOR_Y+8; j < YH; j += 25) { ctx.beginPath(); ctx.moveTo(0, j); ctx.lineTo(YW, j); ctx.stroke(); }
    // yellow lane line
    ctx.strokeStyle = "rgba(255,220,0,0.35)"; ctx.lineWidth = 1.5; ctx.setLineDash([8,6]);
    const laneX = YARD_START_X + Y_COLS*YARD_COL_W + 4;
    ctx.beginPath(); ctx.moveTo(laneX, YARD_FLOOR_Y+8); ctx.lineTo(laneX, YH); ctx.stroke();
    ctx.setLineDash([]);
    // col footprints
    ctx.fillStyle = "rgba(255,255,255,0.1)";
    for (let c = 0; c < Y_COLS; c++) ctx.fillRect(YARD_START_X+c*YARD_COL_W, YARD_FLOOR_Y, CW, 8);

    // label
    ctx.fillStyle = "rgba(255,255,255,0.5)"; ctx.font = "bold 9px sans-serif";
    ctx.fillText("PATIO DE CONTENEDORES", 5, YARD_FLOOR_Y - 8);

    // stacked containers
    yardItems.forEach(item => drawBox(ctx, item.x, item.y, item.color));

    // count badge
    if (yardItems.length > 0) {
      ctx.fillStyle = "rgba(26,42,58,0.85)";
      ctx.beginPath(); ctx.roundRect(YW-44, 6, 38, 22, 6); ctx.fill();
      ctx.fillStyle = "#8aabcc"; ctx.font = "11px sans-serif";
      ctx.fillText(`${yardItems.length}/40`, YW-30, 21);
    }
  }, [yardItems]);

  useEffect(() => { drawYard(); }, [drawYard]);

  return (
    <div style={{ display:"flex", flexDirection:"column" }}>
      <canvas ref={canvasRef} width={YW} height={YH}
        style={{ borderRadius:"12px 12px 0 0", display:"block" }} />
      <div style={{
        background:"#1a2a3a", borderRadius:"0 0 12px 12px", width:YW,
        padding:"11px 12px", display:"flex", alignItems:"center", justifyContent:"center",
      }}>
        <span style={{ fontSize:12, color:"#8aabcc", textAlign:"center" }}>
          {yardItems.length === 0
            ? "Patio vacío"
            : yardItems.length === 40
            ? "Patio lleno ✓"
            : `${yardItems.length} contenedor${yardItems.length !== 1 ? "es" : ""} en patio`}
        </span>
      </div>
    </div>
  );
}

/* ─────────────── PortScene (root) ─────────────── */
export default function PortScene() {
  const [yardItems, setYardItems] = useState([]);

  const handleDelivered = useCallback((color) => {
    setYardItems(prev => {
      const next = [...prev];
      const slot = getYardSlot(next);
      next.push({ ...slot, color });
      return next;
    });
  }, []);

  const handleReset = useCallback(() => {
    setYardItems([]);
  }, []);

  return (
    <div style={{
      display: "flex",
      flexDirection: "row",
      gap: 20,
      alignItems: "flex-start",
      padding: "12px 0",
      fontFamily: "sans-serif",
    }}>
      <CraneCanvas onContainerDelivered={handleDelivered} onReset={handleReset} />
      <YardPanel yardItems={yardItems} />
    </div>
  );
}