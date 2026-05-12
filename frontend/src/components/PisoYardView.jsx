import { useEffect, useRef, useCallback, useState } from "react"
import { advanceContainer } from "../api/client"

const CARGO_COLORS = {
  'Carga Seca':   '#60a5fa',
  'Refrigerada':  '#34d399',
  'Peligrosa':    '#f87171',
  'Frágil':       '#fbbf24',
  'Nodriza':      '#a78bfa',
}
const FALLBACK = ["#E63946","#457B9D","#F4A261","#2A9D8F","#E9C46A","#6A4C93","#e76f51","#264653","#60a5fa","#34d399"]
const CW = 38, CH = 24, PAD_Y = 2

const CANVAS_W = 500, CANVAS_H = 440
const Y_COLS = 8
const YARD_FLOOR_Y = CANVAS_H - 55
const YARD_START_X = 14
const YARD_COL_W = 56

function drawBox(ctx, x, y, color, glow, hover) {
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
  if (glow) {
    ctx.save()
    ctx.shadowColor = color; ctx.shadowBlur = 14
    ctx.fillStyle = "transparent"; ctx.strokeStyle = color
    ctx.lineWidth = 1.5; ctx.strokeRect(x-1, y-1, CW+2, CH+2)
    ctx.restore()
  }
  if (hover) {
    ctx.save()
    ctx.shadowColor = "rgba(192,132,252,0.7)"; ctx.shadowBlur = 12
    ctx.strokeStyle = "#c084fc"; ctx.lineWidth = 2
    ctx.strokeRect(x-2, y-2, CW+4, CH+4)
    ctx.restore()
  }
}

function containerColor(cont, index) {
  if (cont.carga_tipo && CARGO_COLORS[cont.carga_tipo]) return CARGO_COLORS[cont.carga_tipo]
  return FALLBACK[index % FALLBACK.length]
}

function arrangeContainers(containers) {
  const cols = Array.from({ length: Y_COLS }, () => [])
  containers.forEach((cont, i) => {
    let bestCol = 0
    for (let c = 1; c < Y_COLS; c++) {
      if (cols[c].length < cols[bestCol].length) bestCol = c
    }
    const row = cols[bestCol].length
    cols[bestCol].push({
      ...cont,
      col: bestCol,
      row,
      x: YARD_START_X + bestCol * YARD_COL_W,
      y: YARD_FLOOR_Y - (row + 1) * (CH + PAD_Y),
      color: containerColor(cont, i),
    })
  })
  return cols.flat()
}

function getTopContainerIds(items) {
  const colMaxRow = {}
  for (const item of items) {
    if (colMaxRow[item.col] === undefined || item.row > colMaxRow[item.col]) {
      colMaxRow[item.col] = item.row
    }
  }
  const top = new Set()
  for (const item of items) {
    if (item.row === colMaxRow[item.col]) top.add(item.id)
  }
  return top
}

export default function PisoYardView({ containers, onError }) {
  const canvasRef = useRef(null)
  const itemsRef = useRef([])
  const [itemCount, setItemCount] = useState(0)
  const [hoveredId, setHoveredId] = useState(null)
  const prevIdsRef = useRef(new Set())
  const glowIdsRef = useRef(new Set())

  const conts = containers ?? []

  useEffect(() => {
    const currIds = new Set(conts.map(c => c.id))
    const prevIds = prevIdsRef.current

    for (const id of currIds) {
      if (!prevIds.has(id)) {
        glowIdsRef.current.add(id)
        setTimeout(() => glowIdsRef.current.delete(id), 2500)
      }
    }

    prevIdsRef.current = currIds
    setItemCount(conts.length)
  }, [conts])

  const drawYard = useCallback(() => {
    const canvas = canvasRef.current; if (!canvas) return
    const ctx = canvas.getContext("2d")
    ctx.clearRect(0, 0, CANVAS_W, CANVAS_H)

    // sky gradient
    const skyGrad = ctx.createLinearGradient(0, 0, 0, YARD_FLOOR_Y)
    skyGrad.addColorStop(0, "#c084fc18")
    skyGrad.addColorStop(0.6, "#b8ddf0")
    skyGrad.addColorStop(1, "#b8ddf0")
    ctx.fillStyle = skyGrad; ctx.fillRect(0, 0, CANVAS_W, YARD_FLOOR_Y)

    // tiny clouds
    ctx.fillStyle = "rgba(255,255,255,0.55)"
    ;[[16,24,8],[58,18,7],[100,28,9],[140,20,6],[180,26,8]].forEach(([x,y,r]) => {
      ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI*2); ctx.fill()
      ctx.beginPath(); ctx.arc(x+12, y+2, r-2, 0, Math.PI*2); ctx.fill()
    })

    // asphalt floor
    ctx.fillStyle = "#5a5650"; ctx.fillRect(0, YARD_FLOOR_Y, CANVAS_W, CANVAS_H - YARD_FLOOR_Y)
    ctx.fillStyle = "#6a6560"; ctx.fillRect(0, YARD_FLOOR_Y, CANVAS_W, 8)
    ctx.strokeStyle = "rgba(0,0,0,0.1)"; ctx.lineWidth = 1
    for (let i = 0; i < CANVAS_W; i += 20) { ctx.beginPath(); ctx.moveTo(i, YARD_FLOOR_Y+8); ctx.lineTo(i, CANVAS_H); ctx.stroke() }
    for (let j = YARD_FLOOR_Y+8; j < CANVAS_H; j += 25) { ctx.beginPath(); ctx.moveTo(0, j); ctx.lineTo(CANVAS_W, j); ctx.stroke() }

    // column footprints
    ctx.fillStyle = "rgba(192,132,252,0.15)"
    for (let c = 0; c < Y_COLS; c++) {
      ctx.fillRect(YARD_START_X + c*YARD_COL_W, YARD_FLOOR_Y, CW, 8)
      ctx.strokeStyle = "rgba(192,132,252,0.25)"; ctx.lineWidth = 1; ctx.setLineDash([4,4])
      ctx.beginPath(); ctx.moveTo(YARD_START_X + c*YARD_COL_W + CW/2, YARD_FLOOR_Y + 8); ctx.lineTo(YARD_START_X + c*YARD_COL_W + CW/2, CANVAS_H); ctx.stroke()
      ctx.setLineDash([])
    }

    // title
    ctx.fillStyle = "rgba(192,132,252,0.55)"; ctx.font = "bold 10px sans-serif"
    ctx.fillText("VERIFICACION", 6, YARD_FLOOR_Y - 10)

    // stacked containers
    const items = arrangeContainers(conts)
    itemsRef.current = items
    const topIds = getTopContainerIds(items)

    items.forEach(item => {
      const isNew = glowIdsRef.current.has(item.id)
      const isTop = topIds.has(item.id)
      const isHovered = hoveredId === item.id && isTop
      drawBox(ctx, item.x, item.y, item.color, isNew, isHovered)
    })

    // count badge
    if (conts.length > 0) {
      ctx.fillStyle = "rgba(26,42,58,0.85)"
      ctx.beginPath(); ctx.roundRect(CANVAS_W - 44, 6, 38, 22, 6); ctx.fill()
      ctx.fillStyle = "#c084fc"; ctx.font = "11px sans-serif"
      ctx.fillText(`${conts.length}`, CANVAS_W - 26, 21)
    }
  }, [conts, hoveredId])

  useEffect(() => { drawYard() }, [drawYard])

  const handleCanvasClick = useCallback(async (e) => {
    const canvas = canvasRef.current; if (!canvas) return
    const rect = canvas.getBoundingClientRect()
    const scaleX = CANVAS_W / rect.width
    const scaleY = CANVAS_H / rect.height
    const mx = (e.clientX - rect.left) * scaleX
    const my = (e.clientY - rect.top) * scaleY

    const items = itemsRef.current
    const topIds = getTopContainerIds(items)

    for (let i = items.length - 1; i >= 0; i--) {
      const item = items[i]
      if (mx >= item.x && mx <= item.x + CW &&
          my >= item.y && my <= item.y + CH) {
        if (topIds.has(item.id)) {
          try {
            await advanceContainer(item.id)
          } catch (err) {
            onError?.(err.message)
          }
        }
        return
      }
    }
  }, [onError])

  const handleCanvasMove = useCallback((e) => {
    const canvas = canvasRef.current; if (!canvas) return
    const rect = canvas.getBoundingClientRect()
    const scaleX = CANVAS_W / rect.width
    const scaleY = CANVAS_H / rect.height
    const mx = (e.clientX - rect.left) * scaleX
    const my = (e.clientY - rect.top) * scaleY

    const items = itemsRef.current
    const topIds = getTopContainerIds(items)

    let found = null
    for (let i = items.length - 1; i >= 0; i--) {
      const item = items[i]
      if (mx >= item.x && mx <= item.x + CW &&
          my >= item.y && my <= item.y + CH &&
          topIds.has(item.id)) {
        found = item.id
        break
      }
    }
    setHoveredId(found)
  }, [])

  const handleCanvasLeave = useCallback(() => {
    setHoveredId(null)
  }, [])

  const pct = (CANVAS_H / CANVAS_W) * 100

  return (
    <div style={{
      display: "flex", flexDirection: "column",
      width: "100%",
    }}>
      <div style={{
        width: "100%",
        position: "relative",
        paddingBottom: `${pct}%`,
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
          onClick={handleCanvasClick}
          onMouseMove={handleCanvasMove}
          onMouseLeave={handleCanvasLeave}
          style={{
            position: "absolute",
            inset: 0,
            width: "100%",
            height: "100%",
            cursor: hoveredId ? "pointer" : "default",
          }}
        />
      </div>
      <div style={{
        background: "var(--surface)", borderRadius: "0 0 12px 12px",
        padding: "11px 12px", display: "flex", alignItems: "center",
        justifyContent: "center",
        border: "1px solid var(--border)", borderTop: "none",
      }}>
        <span style={{ fontSize: 13, color: "var(--text3)", textAlign: "center" }}>
          {`${conts.length} en verificacion — Click para mover al patio`}
        </span>
      </div>
    </div>
  )
}
