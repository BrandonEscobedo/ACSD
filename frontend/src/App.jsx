import { useState } from 'react'
import { useWebSocket } from './hooks/useWebSocket'
import MonitorHeader from './components/MonitorHeader'
import Sidebar from './components/Sidebar'
import ZoneCard from './components/ZoneCard'
import YardGrid from './components/YardGrid'
import ContainerDetail from './components/ContainerDetail'
import AssignmentPanel from './components/AssignmentPanel'

export default function App() {
  const { state, connected } = useWebSocket()
  const [selectedId, setSelectedId] = useState(null)
  const [error, setError] = useState(null)

  const buque      = state?.buque      ?? []
  const piso       = state?.piso       ?? []
  const patio      = state?.patio      ?? Array.from({ length: 10 }, () => Array(4).fill(null))
  const containers = state?.containers ?? {}
  const events     = state?.events     ?? []

  const allContainersList = Object.values(containers)
  const selectedContainer = selectedId ? containers[selectedId] : null

  if (selectedId && !containers[selectedId]) setSelectedId(null)

  function handleError(msg) {
    setError(msg)
    setTimeout(() => setError(null), 4500)
  }

  return (
    <div className="shell">
      {/* ── Header ───────────────────────────────────────── */}
      <MonitorHeader connected={connected} state={state} />

      <div className="shell__body">
        {/* ── Sidebar ──────────────────────────────────────── */}
        <aside className="shell__sidebar">
          <Sidebar state={state} events={events} onError={handleError} />
        </aside>

        {/* ── Main ─────────────────────────────────────────── */}
        <main className="shell__main">

          {/* Zones row */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
            <ZoneCard
              zone="BUQUE"
              label="Buque"
              icon="🚢"
              color="var(--buque)"
              containers={buque.filter(Boolean)}
              onError={handleError}
            />
            <ZoneCard
              zone="PISO"
              label="Piso (Verificación)"
              icon="📋"
              color="var(--piso)"
              containers={piso.filter(Boolean)}
              onError={handleError}
            />
          </div>

          {}
          <YardGrid
            patio={patio}
            containers={allContainersList}
            selectedId={selectedId}
            onSelect={id => setSelectedId(prev => prev === id ? null : id)}
            onError={handleError}
          />

          {}
          {selectedContainer && (
            <div
              className="fade-up"
              style={{
                marginTop: '20px',
                display: 'grid',
                gridTemplateColumns: '360px 1fr',
                gap: '16px',
                alignItems: 'start',
              }}
            >
              <ContainerDetail container={selectedContainer} />
              <AssignmentPanel
                container={selectedContainer}
                key={selectedContainer.id}
                onError={handleError}
              />
            </div>
          )}
        </main>
      </div>

      {/* ── Error toast ──────────────────────────────────── */}
      {error && (
        <div style={{
          position: 'fixed', bottom: '28px', right: '28px',
          background: '#7f1d1d', border: '1px solid var(--danger)',
          color: '#fecaca', padding: '12px 20px', borderRadius: '10px',
          fontWeight: 600, fontSize: '14px',
          boxShadow: '0 8px 32px #ef444440',
          zIndex: 1000, animation: 'fadeUp .25s ease',
          display: 'flex', alignItems: 'center', gap: '10px',
        }}>
          <span style={{ fontSize: '18px' }}>⚠</span>
          {error}
        </div>
      )}

      {/* ── Disconnected overlay ──────────────────────────── */}
      {!connected && (
        <div style={{
          position: 'fixed', inset: 0,
          background: 'rgba(13,21,39,0.92)',
          backdropFilter: 'blur(8px)',
          display: 'flex', flexDirection: 'column',
          alignItems: 'center', justifyContent: 'center',
          zIndex: 900, gap: '20px',
        }}>
          <div style={{
            width: '52px', height: '52px',
            border: '3px solid var(--border2)',
            borderTopColor: 'var(--buque)',
            borderRadius: '50%',
            animation: 'spin .9s linear infinite',
          }} />
          <div>
            <div style={{ fontWeight: 700, fontSize: '18px', textAlign: 'center', color: 'var(--text)' }}>
              Conectando al servidor
            </div>
            <div style={{ color: 'var(--text3)', fontSize: '14px', textAlign: 'center', marginTop: '6px' }}>
              Asegúrate de que el backend esté corriendo en :8000
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
