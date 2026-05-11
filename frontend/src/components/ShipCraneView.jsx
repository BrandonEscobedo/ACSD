import { useEffect, useRef, useState, useCallback } from "react"

const CARGO_COLORS = {
  'Carga Seca':   '#60a5fa',
  'Refrigerada':  '#34d399',
  'Peligrosa':    '#f87171',
  'Frágil':       '#fbbf24',
  'Nodriza':      '#a78bfa',
}
const FALLBACK_COLORS = ["#E63946","#457B9D","#F4A261","#2A9D8F","#E9C46A","#6A4C93","#e76f51","#264653","#60a5fa","#34d399"]
const CW = 38, CH = 24, PAD_X = 3, PAD_Y = 2

/* ─── layout ─── */
const CANVAS_W = 620, CANVAS_H = 440
const SHIP_LEFT = 140, SHIP_RIGHT = 505
const SHIP_DECK_Y = 240, SHIP_HULL_BOTTOM = 300
const QUAY_Y = 330
const CRANE_ARM_Y = 50, CRANE_ARM_LEN = 175
const S_COLS = 8, S_ROWS = 5
const STACK_SX = SHIP_LEFT + 12
const STACK_SY = SHIP_DECK_Y - S_ROWS*(CH+PAD_Y)

const DROP_X = CANVAS_W - 72
const DROP_Y = QUAY_Y + 10

function containerColor(cont, index) {
  if (cont.carga_tipo && CARGO_COLORS[cont.carga_tipo]) return CARGO_COLORS[cont.carga_tipo]
  return FALLBACK_COLORS[index % FALLBACK_COLORS.length]
}

function getShipPosition(index) {
  const col = index % S_COLS
  const rowsFromBottom = Math.floor(index / S_COLS)
  const row = S_ROWS - 1 - rowsFromBottom
  return {
    col, row,
    x: STACK_SX + col*(CW+PAD_X),
    y: SHIP_DECK_Y - (rowsFromBottom + 1)*(CH+PAD_Y),
  }
}

/* ─── draw helpers ─── */
function drawBox(ctx, x, y, color) {
  ctx.fillStyle = color
  ctx.fillRect(x, y, CW, CH)
  ctx.strokeStyle = "rgba(0,0,0,0.22)"; ctx.lineWidth = 0.5
  ctx.strokeRect(x, y, CW, CH)
  ctx.strokeStyle = "rgba(0,0,0,0.13)"
  for (let i = 1; i < 3; i++) {
    ctx.beginPath(); ctx.moveTo(x + i*(CW/3), y); ctx.lineTo(x + i*(CW/3), y + CH); ctx.stroke()
  }
  ctx.strokeStyle = "rgba(255,255,255,0.32)"; ctx.lineWidth = 1
  ctx.beginPath(); ctx.moveTo(x+2, y+2); ctx.lineTo(x+CW-2, y+2); ctx.stroke()
}

function drawCloud(ctx, x, y, s) {
  ctx.fillStyle = "rgba(255,255,255,0.65)"
  ;[[0,0,28],[22,5,20],[44,2,22],[66,5,18]].forEach(([dx,dy,r]) => {
    ctx.beginPath(); ctx.arc(x+dx*s, y+dy*s, r*s, 0, Math.PI*2); ctx.fill()
  })
}

function drawDropZone(ctx) {
  ctx.fillStyle = "rgba(192,132,252,0.22)"
  ctx.strokeStyle = "rgba(192,132,252,0.5)"; ctx.lineWidth = 1.5; ctx.setLineDash([6,4])
  ctx.beginPath(); ctx.roundRect(DROP_X - 4, DROP_Y - 2, CW + 8, CH + 14, 6); ctx.fill(); ctx.stroke()
  ctx.setLineDash([])
  ctx.fillStyle = "rgba(192,132,252,0.55)"; ctx.font = "bold 9px sans-serif"
  ctx.fillText("VERIF.", DROP_X + 2, DROP_Y - 5)
}

/* ─── component ─── */
export default function ShipCraneView({ containers, autoPlay }) {
  const canvasRef = useRef(null)
  const rafRef = useRef(null)
  const animRef = useRef(null)
  const shipRef = useRef([])
  const autoPlayRef = useRef(autoPlay)
  const pauseTimerRef = useRef(null)
  const [status, setStatus] = useState("Esperando inicio de monitoreo")
  const [busy, setBusy] = useState(false)
  const containerCount = (containers ?? []).length

  autoPlayRef.current = autoPlay

  /* ─── draw ─── */
  const draw = useCallback(() => {
    const canvas = canvasRef.current; if (!canvas) return
    const ctx = canvas.getContext("2d")
    const anim = animRef.current
    ctx.clearRect(0, 0, CANVAS_W, CANVAS_H)

    // sky
    ctx.fillStyle = "#b8ddf0"; ctx.fillRect(0, 0, CANVAS_W, CANVAS_H)
    drawCloud(ctx, 40, 34, 0.62); drawCloud(ctx, 330, 20, 0.46); drawCloud(ctx, 200, 14, 0.52); drawCloud(ctx, 500, 30, 0.4)

    // water
    ctx.fillStyle = "#4a90b8"; ctx.fillRect(0, SHIP_HULL_BOTTOM, CANVAS_W, QUAY_Y - SHIP_HULL_BOTTOM + 2)
    ctx.fillStyle = "#3d7fa8"; ctx.fillRect(0, SHIP_HULL_BOTTOM, CANVAS_W, 26)
    ctx.strokeStyle = "rgba(255,255,255,0.2)"; ctx.lineWidth = 1.5
    for (let i = 0; i < 6; i++) {
      const wx = i*95+5, wy = SHIP_HULL_BOTTOM + 10 + (i%2)*6
      ctx.beginPath(); ctx.moveTo(wx, wy); ctx.bezierCurveTo(wx+18, wy-4, wx+45, wy+4, wx+75, wy); ctx.stroke()
    }

    // quay
    ctx.fillStyle = "#8a8070"; ctx.fillRect(0, QUAY_Y, CANVAS_W, CANVAS_H-QUAY_Y)
    ctx.fillStyle = "#a09585"; ctx.fillRect(0, QUAY_Y, CANVAS_W, 10)
    ctx.fillStyle = "#6e6055"; ctx.fillRect(0, QUAY_Y+10, CANVAS_W, 4)
    ctx.strokeStyle = "rgba(0,0,0,0.07)"; ctx.lineWidth = 1
    for (let i = 0; i < CANVAS_W; i += 40) { ctx.beginPath(); ctx.moveTo(i, QUAY_Y+14); ctx.lineTo(i, CANVAS_H); ctx.stroke() }
    for (let j = QUAY_Y+14; j < CANVAS_H; j += 30) { ctx.beginPath(); ctx.moveTo(0, j); ctx.lineTo(CANVAS_W, j); ctx.stroke() }
    ctx.fillStyle = "#555045"
    for (let bx = 40; bx < CANVAS_W; bx += 70) {
      ctx.beginPath(); ctx.arc(bx, QUAY_Y+8, 5, 0, Math.PI*2); ctx.fill()
      ctx.fillStyle = "#777"; ctx.beginPath(); ctx.arc(bx, QUAY_Y+8, 2.5, 0, Math.PI*2); ctx.fill()
      ctx.fillStyle = "#555045"
    }
    ctx.fillStyle = "rgba(0,0,0,0.18)"; ctx.fillRect(0, QUAY_Y, CANVAS_W, 3)

    // ship
    ctx.fillStyle = "#1a3a5c"
    ctx.beginPath(); ctx.moveTo(SHIP_LEFT, SHIP_DECK_Y); ctx.lineTo(SHIP_LEFT-8, SHIP_HULL_BOTTOM); ctx.lineTo(SHIP_RIGHT+8, SHIP_HULL_BOTTOM); ctx.lineTo(SHIP_RIGHT, SHIP_DECK_Y); ctx.closePath(); ctx.fill()
    ctx.fillStyle = "#2d5a8e"; ctx.fillRect(SHIP_LEFT, SHIP_DECK_Y-8, SHIP_RIGHT-SHIP_LEFT, 10)
    ctx.fillStyle = "#c0392b"; ctx.fillRect(SHIP_LEFT-6, SHIP_HULL_BOTTOM-7, SHIP_RIGHT-SHIP_LEFT+12, 5)
    ctx.fillStyle = "#c9d6e3"; ctx.fillRect(SHIP_RIGHT-48, SHIP_DECK_Y-52, 42, 48)
    ctx.fillStyle = "#a8bdd4"; for (let i = 0; i < 3; i++) ctx.fillRect(SHIP_RIGHT-43+i*12, SHIP_DECK_Y-46, 9, 9)
    ctx.fillStyle = "#888"; ctx.fillRect(SHIP_RIGHT-36, SHIP_DECK_Y-66, 10, 16)

    // containers on ship
    shipRef.current.forEach(con => {
      if (con.visible) drawBox(ctx, con.x, con.y, con.color)
    })

    // drop zone
    drawDropZone(ctx)

    // crane
    const mx = anim ? anim.craneMastX : 70
    const armEnd = mx + CRANE_ARM_LEN
    const trolleyX = anim ? anim.cableX : armEnd

    ctx.fillStyle = "#4a4035"; ctx.fillRect(mx-55, QUAY_Y-6, 110, 10)
    ctx.fillStyle = "#333"; ctx.fillRect(mx-50, QUAY_Y-8, 100, 3)
    ctx.fillStyle = "#2a2a2a"
    for (let wx = -36; wx <= 36; wx += 24) {
      ctx.beginPath(); ctx.arc(mx+wx, QUAY_Y+6, 7, 0, Math.PI*2); ctx.fill()
      ctx.fillStyle = "#555"; ctx.beginPath(); ctx.arc(mx+wx, QUAY_Y+6, 3.5, 0, Math.PI*2); ctx.fill()
      ctx.fillStyle = "#2a2a2a"
    }
    ctx.strokeStyle = "#5a5045"; ctx.lineWidth = 9; ctx.lineCap = "round"
    ctx.beginPath(); ctx.moveTo(mx-16, QUAY_Y); ctx.lineTo(mx, CRANE_ARM_Y+20); ctx.stroke()
    ctx.beginPath(); ctx.moveTo(mx+16, QUAY_Y); ctx.lineTo(mx, CRANE_ARM_Y+20); ctx.stroke()
    ctx.strokeStyle = "#666"; ctx.lineWidth = 8
    ctx.beginPath(); ctx.moveTo(mx, QUAY_Y); ctx.lineTo(mx, CRANE_ARM_Y); ctx.stroke()
    ctx.lineWidth = 7; ctx.beginPath(); ctx.moveTo(mx-18, CRANE_ARM_Y); ctx.lineTo(armEnd, CRANE_ARM_Y); ctx.stroke()
    ctx.lineWidth = 2; ctx.strokeStyle = "#888"
    for (let i = 0; i < 5; i++) {
      const bx = mx+8+i*((CRANE_ARM_LEN-8)/5)
      ctx.beginPath(); ctx.moveTo(bx, CRANE_ARM_Y); ctx.lineTo(bx+18, CRANE_ARM_Y+20); ctx.stroke()
    }
    ctx.strokeStyle = "#666"; ctx.lineWidth = 7
    ctx.beginPath(); ctx.moveTo(mx-18, CRANE_ARM_Y); ctx.lineTo(mx-58, CRANE_ARM_Y); ctx.stroke()
    ctx.fillStyle = "#4a4035"; ctx.fillRect(mx-68, CRANE_ARM_Y-13, 18, 20)
    ctx.fillStyle = "#444"; ctx.fillRect(trolleyX-7, CRANE_ARM_Y+4, 14, 8)

    const cableBot = anim ? anim.hookY : CRANE_ARM_Y + 28
    ctx.strokeStyle = "#bbb"; ctx.lineWidth = 1; ctx.setLineDash([3,3])
    ctx.beginPath(); ctx.moveTo(trolleyX, CRANE_ARM_Y+12); ctx.lineTo(trolleyX, cableBot); ctx.stroke()
    ctx.setLineDash([])
    ctx.fillStyle = "#777"; ctx.fillRect(trolleyX-4, cableBot, 8, 5)

    if (anim && anim.carrying) drawBox(ctx, anim.containerX, anim.containerY, anim.color)
  }, [])

  /* ─── animation loop ─── */
  const loop = useCallback(() => {
    const anim = animRef.current; if (!anim) return

    if (anim.phase === "moveCrane") {
      const dx = anim.targetMastX - anim.craneMastX; anim.craneMastX += dx*0.08
      anim.cableX = anim.craneMastX + CRANE_ARM_LEN
      if (Math.abs(dx) < 0.5) { anim.craneMastX = anim.targetMastX; anim.cableX = anim.craneMastX + CRANE_ARM_LEN; anim.phase = "moveTrolleyToPickup" }
    } else if (anim.phase === "moveTrolleyToPickup") {
      const dx = anim.targetCableX - anim.cableX; anim.cableX += dx*0.09
      if (Math.abs(dx) < 0.8) { anim.cableX = anim.targetCableX; anim.phase = "lowerHook" }
    } else if (anim.phase === "lowerHook") {
      const dy = anim.pickupY - anim.hookY; anim.hookY += dy*0.12
      if (Math.abs(dy) < 0.8) {
        anim.hookY = anim.pickupY
        const idx = shipRef.current.findIndex(c => c.id === anim.containerId)
        if (idx >= 0) shipRef.current[idx].visible = false
        anim.carrying = true
        anim.containerX = anim.cableX - CW/2
        anim.containerY = anim.pickupY
        anim.phase = "liftUp"
      }
    } else if (anim.phase === "liftUp") {
      const dy = anim.liftTargetY - anim.hookY; anim.hookY += dy*0.1
      anim.containerX = anim.cableX - CW/2
      anim.containerY = anim.hookY
      if (Math.abs(dy) < 0.8) { anim.hookY = anim.liftTargetY; anim.containerY = anim.hookY; anim.phase = "moveTrolleyRight" }
    } else if (anim.phase === "moveTrolleyRight") {
      const armEnd = anim.craneMastX + CRANE_ARM_LEN
      const dx = armEnd - anim.cableX; anim.cableX += dx*0.08
      anim.containerX = anim.cableX - CW/2; anim.containerY = anim.hookY
      if (Math.abs(dx) < 0.8) { anim.cableX = armEnd; anim.containerX = anim.cableX - CW/2; anim.phase = "moveCraneRight" }
    } else if (anim.phase === "moveCraneRight") {
      anim.craneMastX += 4
      anim.cableX = anim.craneMastX + CRANE_ARM_LEN
      anim.containerX = anim.cableX - CW/2; anim.containerY = anim.hookY
      if (anim.containerX > DROP_X) { anim.phase = "lowerToDrop"; anim.dropTargetY = DROP_Y }
    } else if (anim.phase === "lowerToDrop") {
      const dy = anim.dropTargetY - anim.hookY; anim.hookY += dy*0.12
      anim.containerX = anim.cableX - CW/2
      anim.containerY = anim.hookY
      if (Math.abs(dy) < 0.6) { anim.hookY = anim.dropTargetY; anim.containerY = anim.hookY; anim.phase = "release"; anim.releaseTimer = 0 }
    } else if (anim.phase === "release") {
      anim.containerY = anim.dropTargetY
      anim.releaseTimer++
      if (anim.releaseTimer > 35) {
        anim.carrying = false
        anim.hookY = CRANE_ARM_Y + 28
        animRef.current = null
        setBusy(false)
        draw()
        scheduleNext()
        return
      }
    }
    draw()
    rafRef.current = requestAnimationFrame(loop)
  }, [draw])

  /* ─── schedule next pickup ─── */
  const scheduleNext = useCallback(() => {
    if (pauseTimerRef.current) clearTimeout(pauseTimerRef.current)
    if (!autoPlayRef.current) {
      setStatus("Monitoreo detenido")
      return
    }
    const vis = shipRef.current.filter(c => c.visible)
    if (vis.length === 0) {
      setStatus("Buque vacio - esperando contenedores")
      return
    }
    setStatus(`${vis.length} en buque`)
    pauseTimerRef.current = setTimeout(() => {
      pauseTimerRef.current = null
      if (!autoPlayRef.current) return
      startPickup()
    }, 800)
  }, [])

  /* ─── start pickup animation ─── */
  const startPickup = useCallback(() => {
    if (animRef.current) return
    const vis = shipRef.current.filter(c => c.visible)
    if (vis.length === 0) { setStatus("Buque vacio"); return }

    // pick top-most, left-most container
    vis.sort((a, b) => a.row - b.row || a.col - b.col)
    const top = vis[0]
    const conCenterX = top.x + CW/2
    const idealMastX = Math.max(20, Math.min(340, conCenterX - CRANE_ARM_LEN))

    setBusy(true)
    setStatus(`Descargando: ${top.id}`)

    animRef.current = {
      phase: "moveCrane",
      craneMastX: 70,
      targetMastX: idealMastX,
      targetCableX: conCenterX,
      cableX: 70 + CRANE_ARM_LEN,
      pickupY: top.y,
      hookY: CRANE_ARM_Y + 28,
      carrying: false,
      containerId: top.id,
      containerX: top.x,
      containerY: top.y,
      color: top.color,
      liftTargetY: CRANE_ARM_Y + 14,
    }
    rafRef.current = requestAnimationFrame(loop)
  }, [loop])

  /* ─── sync ship containers from prop ─── */
  const prevIdsRef = useRef(new Set())

  useEffect(() => {
    const list = containers ?? []
    const ids = new Set(list.map(c => c.id))
    const prevIds = prevIdsRef.current

    // build positioned ship containers
    const positioned = list.map((cont, i) => {
      const pos = getShipPosition(i)
      const c = containerColor(cont, i)
      return { ...cont, ...pos, color: c, visible: true }
    })

    // preserve visibility for containers that were already hidden
    if (prevIds.size > 0) {
      const hiddenIds = new Set(shipRef.current.filter(c => !c.visible).map(c => c.id))
      positioned.forEach(p => { if (hiddenIds.has(p.id)) p.visible = false })
    }

    shipRef.current = positioned
    prevIdsRef.current = ids

    // if new containers arrived while idle, try to start
    if (!animRef.current && autoPlayRef.current) {
      const vis = shipRef.current.filter(c => c.visible)
      if (vis.length > 0 && !pauseTimerRef.current) scheduleNext()
    }

    draw()
  }, [containers, draw, scheduleNext])

  /* ─── autoPlay lifecycle ─── */
  useEffect(() => {
    if (autoPlay) {
      if (!animRef.current) {
        const vis = shipRef.current.filter(c => c.visible)
        if (vis.length > 0 && !pauseTimerRef.current) {
          scheduleNext()
        } else if (vis.length === 0) {
          setStatus("Monitoreo activo - esperando contenedores")
        }
      }
    } else {
      if (rafRef.current) { cancelAnimationFrame(rafRef.current); rafRef.current = null }
      if (pauseTimerRef.current) { clearTimeout(pauseTimerRef.current); pauseTimerRef.current = null }
      animRef.current = null
      setBusy(false)
      setStatus("Monitoreo detenido")
    }
    return () => {
      if (pauseTimerRef.current) clearTimeout(pauseTimerRef.current)
    }
  }, [autoPlay, scheduleNext])

  // initial draw
  useEffect(() => { draw() }, [draw])

  // unmount cleanup
  useEffect(() => {
    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current)
      if (pauseTimerRef.current) clearTimeout(pauseTimerRef.current)
    }
  }, [])

  return (
    <div style={{
      display: "flex", flexDirection: "column",
      width: "100%", maxWidth: CANVAS_W,
      margin: "0 auto",
    }}>
      <div style={{
        width: "100%",
        borderRadius: "12px 12px 0 0",
        overflow: "hidden",
        border: "1px solid var(--border)",
        borderBottom: "none",
        background: "#0d1527",
      }}>
        <canvas
          ref={canvasRef}
          width={CANVAS_W}
          height={CANVAS_H}
          style={{
            width: "100%", height: "auto",
            display: "block",
          }}
        />
      </div>
      <div style={{
        background: "var(--surface)", borderRadius: "0 0 12px 12px",
        padding: "10px 16px", display: "flex", alignItems: "center",
        justifyContent: "space-between", gap: 8,
        border: "1px solid var(--border)", borderTop: "none",
      }}>
        <span style={{ fontSize: 13, color: "var(--text3)", flex: 1 }}>{status}</span>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <span style={{ fontSize: 12, color: "var(--text4)" }}>
            {containerCount} total
          </span>
          <span style={{
            width: 9, height: 9, borderRadius: "50%",
            background: autoPlay ? "var(--success)" : "var(--text4)",
            boxShadow: autoPlay ? "0 0 8px var(--success)" : "none",
            transition: "all 0.3s ease",
            flexShrink: 0,
          }} />
        </div>
      </div>
    </div>
  )
}
