import { useState } from 'react'
import { useWebSocket } from './hooks/useWebSocket'
import MonitorHeader from './components/MonitorHeader'
import Sidebar from './components/Sidebar'
import ShipCraneView from './components/ShipCraneView'
import PisoYardView from './components/PisoYardView'
import YardGrid from './components/YardGrid'
import ContainerDetail from './components/ContainerDetail'
import AssignmentPanel from './components/AssignmentPanel'
import EventFeed from './components/EventFeed'
import Tabs from './components/Tabs'
import SummaryView from './components/SummaryView'

export default function App() {
  const { state, connected } = useWebSocket()
  const [selectedId, setSelectedId] = useState(null)
  const [error, setError] = useState(null)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [assignmentResult, setAssignmentResult] = useState(null)

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
      {/*  Header  */}
      <MonitorHeader connected={connected} state={state} onError={handleError} />

      <div className="shell__body" style={{ position: 'relative' }}>
        {/*  Main  takes full width now */}
        <main style={{
          flex: 1,
          overflowY: 'auto',
          padding: '24px 28px',
          minWidth: 0,
        }}>

          {/* Zones row — Buque + Piso + Patio juntos */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))',
            gap: '16px',
            marginBottom: '16px',
          }}>
            <ShipCraneView
              containers={buque.filter(Boolean)}
              autoPlay={state?.auto_running ?? false}
            />
            <PisoYardView
              containers={piso.filter(Boolean)}
              onError={handleError}
            />
            <YardGrid
              patio={patio}
              containers={allContainersList}
              selectedId={selectedId}
              onSelect={id => setSelectedId(prev => {
                if (prev !== id) setAssignmentResult(null)
                return prev === id ? null : id
              })}
              onError={handleError}
              compact
            />
          </div>

          {/* Tabs: Asignacion + Resumen */}
          <div style={{ marginTop: '20px' }}>
            <Tabs tabs={['🚚 Asignacion de Linea', '📊 Resumen']}>
              {/* Tab 1: Assignment */}
              <div style={{ padding: selectedContainer ? 0 : '40px 20px', minHeight: '200px' }}>
                {selectedContainer ? (
                  <div style={{
                    display: 'grid',
                    gridTemplateColumns: '360px 1fr',
                    gap: '16px',
                    alignItems: 'start',
                    padding: '16px',
                  }}>
                    <ContainerDetail container={selectedContainer} />
                    <AssignmentPanel
                      container={selectedContainer}
                      key={selectedContainer.id}
                      onError={handleError}
                      onResult={setAssignmentResult}
                    />
                  </div>
                ) : (
                  <div style={{
                    display: 'flex', flexDirection: 'column',
                    alignItems: 'center', justifyContent: 'center',
                    gap: '10px', color: 'var(--text4)',
                  }}>
                    <span style={{ fontSize: '32px', opacity: 0.5 }}>📭</span>
                    <span style={{ fontSize: '14px', fontWeight: 600 }}>
                      Selecciona un contenedor del patio para asignar linea de transporte
                    </span>
                    <span style={{ fontSize: '12px' }}>
                      Haz clic en cualquier contenedor del Patio de Almacenamiento
                    </span>
                  </div>
                )}
              </div>

              {/* Tab 2: Summary */}
              <SummaryView container={selectedContainer} result={assignmentResult} />
            </Tabs>
          </div>
        </main>

        {/*  Sidebar toggle button */}
        <button
          onClick={() => setSidebarOpen(v => !v)}
          title="Configuracion"
          style={{
            position: 'absolute',
            top: '16px',
            left: '16px',
            width: '36px',
            height: '36px',
            borderRadius: '10px',
            background: sidebarOpen ? 'var(--buque)' : 'var(--surface2)',
            border: `1px solid ${sidebarOpen ? 'var(--buque)' : 'var(--border)'}`,
            color: sidebarOpen ? '#04111f' : 'var(--text3)',
            fontSize: '18px',
            fontWeight: 700,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            zIndex: 100,
            padding: 0,
            transition: 'all 0.2s ease',
          }}
        >
          ⚙
        </button>
      </div>

      {/*  Sidebar overlay */}
      <Sidebar
        onError={handleError}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      {/*  Event feed  fixed floating panel */}
      <EventFeed events={events} />

      {/*  Error toast */}
      {error && (
        <div style={{
          position: 'fixed', bottom: '28px', left: '50%',
          transform: 'translateX(-50%)',
          background: '#7f1d1d', border: '1px solid var(--danger)',
          color: '#fecaca', padding: '12px 20px', borderRadius: '10px',
          fontWeight: 600, fontSize: '14px',
          boxShadow: '0 8px 32px #ef444440',
          zIndex: 1100, animation: 'fadeUp .25s ease',
          display: 'flex', alignItems: 'center', gap: '10px',
        }}>
          <span style={{ fontSize: '18px' }}>⚠</span>
          {error}
        </div>
      )}

      {/*  Disconnected overlay */}
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
              Asegurate de que el backend este corriendo en :8000
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
