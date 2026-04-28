import YardGrid from './YardGrid'
import ContainerDetail from './ContainerDetail'
import AssignmentPanel from './AssignmentPanel'

export default function YardView({ simData, selectedId, onSelect }) {
  const finalPatio = simData.patio
  const contenedores = simData.contenedores

  const contMap = Object.fromEntries(contenedores.map(c => [c.id, c]))
  const selectedContainer = selectedId ? contMap[selectedId] : null

  const contsEnPatio = contenedores.filter(c => c.posicion_actual === 'PATIO')

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      {/* Patio + selector rápido */}
      <div style={{ flex: 3, minWidth: 0 }}>
        {contsEnPatio.length > 0 && (
          <div style={{ marginBottom: '12px' }}>
            <div style={{ fontSize: '11px', color: 'var(--color-text-muted)', marginBottom: '6px' }}>
              Selección rápida
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
              {contsEnPatio.map(c => (
                <button
                  key={c.id}
                  className={selectedId === c.id ? 'primary' : 'secondary'}
                  onClick={() => onSelect(c.id)}
                  style={{ padding: '4px 10px', fontSize: '11px' }}
                  title={`C${c.columna}, P${c.piso} | ${c.carga_tipo}`}
                >
                  {c.id.split('-')[1]}
                </button>
              ))}
            </div>
          </div>
        )}

        <YardGrid
          patioState={finalPatio}
          contenedores={contenedores}
          activeId={null}
          selectedId={selectedId}
          onSelect={onSelect}
        />

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px', marginTop: '14px' }}>
          <div className="metric-card">
            <div className="label">Total en Patio</div>
            <div className="value">{contsEnPatio.length}</div>
          </div>
          <div className="metric-card">
            <div className="label">Ocupación</div>
            <div className="value" style={{ color: 'var(--color-patio)' }}>
              {((contsEnPatio.length / 40) * 100).toFixed(1)}%
            </div>
          </div>
          <div className="metric-card">
            <div className="label">Disponibles</div>
            <div className="value" style={{ color: 'var(--color-success)' }}>
              {40 - contsEnPatio.length}
            </div>
          </div>
        </div>
      </div>

      {/* Panel derecho */}
      <div style={{ width: '280px', flexShrink: 0, display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <h3>Información del Contenedor</h3>
        <ContainerDetail container={selectedContainer} />

        {selectedContainer && (
          <>
            <div className="divider" />
            <h3>Asignación de Transporte</h3>
            <AssignmentPanel container={selectedContainer} key={selectedContainer.id} />
          </>
        )}
      </div>
    </div>
  )
}
