import { removeContainer } from '../api/client'

const CARGA_COLOR = {
  'Carga Seca':   '#60a5fa',
  'Refrigerada':  '#34d399',
  'Peligrosa':    '#f87171',
  'Frágil':       '#fbbf24',
  'Nodriza':      '#a78bfa',
}

export default function YardGrid({ patio, containers, selectedId, onSelect, onError }) {
  const contMap = Object.fromEntries((containers ?? []).map(c => [c.id, c]))
  const occupied = patio?.flat().filter(Boolean).length ?? 0
  const ocupPct  = Math.round((occupied / 40) * 100)
  const barColor = ocupPct > 80 ? 'var(--danger)' : ocupPct > 50 ? 'var(--warning)' : 'var(--patio)'

  async function handleRemove(id, e) {
    e.stopPropagation()
    try { await removeContainer(id) }
    catch (err) { onError?.(err.message) }
  }

  return (
    <div style={{
      background: 'var(--surface)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius)',
      overflow: 'hidden',
    }}>
      {/* Header */}
      <div style={{
        padding: '14px 20px',
        borderBottom: '1px solid var(--border)',
        background: 'linear-gradient(90deg, #fbbf2414 0%, transparent 100%)',
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
          <div>
            <div style={{ fontWeight: 800, fontSize: '16px', color: 'var(--patio)' }}>
              🏭 Patio de Almacenamiento
            </div>
            <div style={{ fontSize: '12px', color: 'var(--text4)', marginTop: '2px' }}>
              Haz clic en un contenedor para seleccionarlo · Haz clic en ✕ para retirarlo
            </div>
          </div>
          <div style={{
            background: 'var(--patio)', color: '#04111f',
            fontWeight: 800, fontSize: '15px',
            borderRadius: '8px', padding: '5px 16px',
          }}>
            {occupied} / 40
          </div>
        </div>

        {/* Occupancy bar */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            flex: 1, height: '6px', background: 'var(--border)',
            borderRadius: '3px', overflow: 'hidden',
          }}>
            <div style={{
              height: '100%', width: `${ocupPct}%`,
              background: barColor,
              borderRadius: '3px',
              transition: 'width 0.6s ease',
              boxShadow: `0 0 8px ${barColor}80`,
            }} />
          </div>
          <span style={{
            fontSize: '13px', fontWeight: 700,
            color: barColor, minWidth: '38px', textAlign: 'right',
          }}>
            {ocupPct}%
          </span>
        </div>
      </div>

      {/* Grid */}
      <div style={{ padding: '16px 20px', overflowX: 'auto' }}>
        {/* Column headers */}
        <div style={{ display: 'flex', gap: '8px', marginBottom: '8px', paddingLeft: '0' }}>
          {Array.from({ length: 10 }, (_, i) => (
            <div key={i} style={{
              width: '72px', flexShrink: 0,
              textAlign: 'center',
              fontSize: '11px', fontWeight: 700,
              color: 'var(--text4)',
              letterSpacing: '.04em',
            }}>
              COL {i}
            </div>
          ))}
        </div>

        {/* Floor labels + cells */}
        {[3, 2, 1, 0].map(pisoIdx => (
          <div key={pisoIdx} style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
            {/* Floor label */}
            <div style={{
              width: '44px', flexShrink: 0,
              fontSize: '11px', fontWeight: 700, color: 'var(--text4)',
              textAlign: 'right', paddingRight: '4px',
              letterSpacing: '.04em',
            }}>
              P {pisoIdx}
            </div>

            {/* Cells for this floor, across all columns */}
            {(patio ?? []).map((col, colIdx) => {
              const contId = col[pisoIdx]

              if (!contId) {
                return (
                  <div key={colIdx} style={{
                    width: '72px', height: '72px', flexShrink: 0,
                    border: '1px dashed var(--border)',
                    borderRadius: '8px',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: '11px', color: 'var(--border2)',
                  }}>
                    vacío
                  </div>
                )
              }

              const cont = contMap[contId]
              if (!cont) return null

              const isSelected  = contId === selectedId
              const cargoColor  = CARGA_COLOR[cont.carga_tipo] ?? 'var(--text3)'

              return (
                <div
                  key={colIdx}
                  className="pop-in"
                  onClick={() => onSelect(contId)}
                  title={`${cont.id} · ${cont.carga_tipo} · ${cont.comprador} · ${cont.tamano_pies}ft`}
                  style={{
                    width: '72px', height: '72px', flexShrink: 0,
                    position: 'relative',
                    borderRadius: '8px',
                    border: isSelected
                      ? '2px solid var(--patio)'
                      : `1px solid ${cargoColor}50`,
                    background: isSelected ? '#fbbf2414' : 'var(--surface2)',
                    display: 'flex', flexDirection: 'column',
                    alignItems: 'center', justifyContent: 'center',
                    gap: '3px',
                    cursor: 'pointer',
                    transform: isSelected ? 'scale(1.08)' : 'scale(1)',
                    boxShadow: isSelected
                      ? '0 0 18px var(--patio)'
                      : `0 2px 8px #00000050`,
                    transition: 'all 0.2s ease',
                    zIndex: isSelected ? 3 : 1,
                  }}
                >
                  {/* Container image */}
                  {cont.imagen_src
                    ? <img src={cont.imagen_src} style={{ width: '44px', height: '44px', pointerEvents: 'none' }} alt="" />
                    : <div style={{ width: '44px', height: '44px', background: `${cargoColor}30`, borderRadius: '5px' }} />
                  }

                  {/* ID label */}
                  <span style={{ fontSize: '10px', fontWeight: 700, color: 'var(--text3)', pointerEvents: 'none' }}>
                    {cont.id.split('-')[1]}
                  </span>

                  {/* Cargo color stripe at bottom */}
                  <div style={{
                    position: 'absolute', bottom: 0, left: 0, right: 0, height: '3px',
                    borderRadius: '0 0 8px 8px',
                    background: cargoColor, opacity: 0.7,
                  }} />

                  {/* Remove button (only when selected) */}
                  {isSelected && (
                    <button
                      onClick={e => handleRemove(contId, e)}
                      title="Retirar del patio"
                      style={{
                        position: 'absolute', top: '-9px', right: '-9px',
                        width: '20px', height: '20px',
                        borderRadius: '50%', padding: 0,
                        background: 'var(--danger)', color: '#fff',
                        fontSize: '11px', fontWeight: 700,
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        boxShadow: '0 0 8px var(--danger)',
                        border: '2px solid var(--surface)',
                        zIndex: 4,
                      }}
                    >
                      ×
                    </button>
                  )}
                </div>
              )
            })}
          </div>
        ))}

        {/* Legend */}
        <div style={{
          marginTop: '16px', paddingTop: '14px',
          borderTop: '1px solid var(--border)',
          display: 'flex', flexWrap: 'wrap', gap: '10px', alignItems: 'center',
        }}>
          <span style={{ fontSize: '12px', color: 'var(--text4)', fontWeight: 600 }}>Tipo de carga:</span>
          {Object.entries(CARGA_COLOR).map(([tipo, color]) => (
            <span key={tipo} style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
              <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: color, display: 'inline-block' }} />
              <span style={{ fontSize: '12px', color: 'var(--text3)' }}>{tipo}</span>
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}
