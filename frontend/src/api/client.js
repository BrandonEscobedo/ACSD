const BASE = '/api'

async function post(path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

async function put(path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

async function del(path) {
  const res = await fetch(`${BASE}${path}`, { method: 'DELETE' })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

// Monitor controls
export const startAuto    = ()         => post('/monitor/start')
export const stopAuto     = ()         => post('/monitor/stop')
export const addContainer = ()         => post('/monitor/add')
export const resetMonitor = ()         => post('/monitor/reset')
export const advanceContainer = (id)  => post(`/monitor/advance/${id}`)
export const removeContainer  = (id)  => del(`/monitor/container/${id}`)
export const updateConfig     = (cfg) => put('/monitor/config', cfg)

// Assignment + Reports
export async function assignLine(contenedor) {
  return post('/assignment', { contenedor })
}

export async function downloadReport(contenedor, lineaInfo) {
  const res = await fetch(`${BASE}/reports/dispatch`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ contenedor, linea_info: lineaInfo }),
  })
  if (!res.ok) throw new Error('Error al generar reporte')
  const blob = await res.blob()
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `Despacho_${contenedor.id}_${Date.now()}.pdf`
  a.click()
  URL.revokeObjectURL(url)
}
