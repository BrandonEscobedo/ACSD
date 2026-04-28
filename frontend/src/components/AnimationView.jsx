import ZonaBuquePiso from './ZonaBuquePiso'
import YardGrid from './YardGrid'

export default function AnimationView({
  simData,
  speed,
  zones,
  patio,
  activeId,
  playing,
  index,
  currentEvent,
  onPlay,
  onPause,
  onStop,
  onGoToYard,
}) {
  const total = simData?.eventos.length ?? 0
  const progress = total > 0 ? (index / total) * 100 : 0

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {/* Controles */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
        <button
          className={playing ? 'secondary' : 'primary'}
          onClick={playing ? onPause : onPlay}
          disabled={index >= total && !playing}
        >
          {playing ? '⏸ Pausar' : '▶ Reproducir'}
        </button>
        <button className="secondary" onClick={onStop}>⏹ Detener</button>

        <div style={{ flex: 1, minWidth: '160px' }}>
          <div style={{
            height: '6px', background: 'var(--color-surface2)',
            borderRadius: '3px', overflow: 'hidden',
          }}>
            <div style={{
              height: '100%',
              width: `${progress}%`,
              background: 'var(--color-buque)',
              transition: 'width 0.3s ease',
              borderRadius: '3px',
            }} />
          </div>
          <div style={{ fontSize: '11px', color: 'var(--color-text-muted)', marginTop: '3px' }}>
            Evento {index} / {total}
          </div>
        </div>

        {currentEvent && (
          <div style={{
            fontSize: '11px', color: 'var(--color-text-muted)',
            background: 'var(--color-surface2)',
            padding: '4px 10px', borderRadius: '6px',
          }}>
            ⏱ {currentEvent.tiempo.toFixed(1)}s &nbsp;|&nbsp; {currentEvent.contenedor_id}: {currentEvent.accion}
          </div>
        )}

        {index >= total && total > 0 && (
          <button className="warning" onClick={onGoToYard}>
            Ver Patio →
          </button>
        )}
      </div>

      {/* Zonas */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <ZonaBuquePiso
          zona="BUQUE" label="🚢 Buque"
          color="var(--color-buque)"
          contenedores={zones.BUQUE}
          activeId={activeId}
        />
        <ZonaBuquePiso
          zona="PISO" label="📍 Piso"
          color="var(--color-piso)"
          contenedores={zones.PISO}
          activeId={activeId}
        />
        <YardGrid
          patioState={patio}
          contenedores={simData?.contenedores ?? []}
          activeId={activeId}
          selectedId={null}
          onSelect={() => {}}
        />
      </div>

      {/* Log de eventos */}
      {simData && (
        <details style={{ marginTop: '4px' }}>
          <summary style={{ cursor: 'pointer', fontSize: '12px', color: 'var(--color-text-muted)', userSelect: 'none' }}>
            📊 Ver tabla de eventos
          </summary>
          <div style={{ marginTop: '10px', maxHeight: '260px', overflowY: 'auto' }}>
            <table>
              <thead>
                <tr>
                  <th>Tiempo</th>
                  <th>Contenedor</th>
                  <th>Acción</th>
                  <th>Origen</th>
                  <th>Destino</th>
                </tr>
              </thead>
              <tbody>
                {simData.eventos.map((e, i) => (
                  <tr key={i} style={i === index - 1 ? { background: 'var(--color-buque)22' } : {}}>
                    <td>{e.tiempo.toFixed(2)}</td>
                    <td>{e.contenedor_id}</td>
                    <td>{e.accion}</td>
                    <td>{e.origen}</td>
                    <td>{e.destino}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </details>
      )}
    </div>
  )
}
