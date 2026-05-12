export default function SummaryView({ container, result }) {
  if (!container) {
    return (
      <div style={{ padding: '40px 20px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '10px', color: 'var(--text4)', minHeight: '200px' }}>
        <span style={{ fontSize: '32px', opacity: 0.5 }}>📊</span>
        <span style={{ fontSize: '14px', fontWeight: 600 }}>
          Selecciona un contenedor del patio y ejecuta la asignacion
        </span>
        <span style={{ fontSize: '12px' }}>
          Ve a la pestana "Asignacion de Linea" y haz clic en "Encontrar mejor linea"
        </span>
      </div>
    )
  }

  if (!result) {
    return (
      <div style={{ padding: '40px 20px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '10px', color: 'var(--text4)', minHeight: '200px' }}>
        <span style={{ fontSize: '32px', opacity: 0.5 }}>🔍</span>
        <span style={{ fontSize: '14px', fontWeight: 600 }}>
          Ejecuta la asignacion para {container.id}
        </span>
        <span style={{ fontSize: '12px' }}>
          Ve a la pestana "Asignacion de Linea" y haz clic en "Encontrar mejor linea"
        </span>
      </div>
    )
  }

  const mejor = result.mejor
  const resultados = [...(result.resultados ?? [])].sort((a, b) => b.puntaje - a.puntaje)
  const totalLineas = resultados.length
  const conEIR = resultados.filter(r => r.tiene_eir).length
  const sinEIR = totalLineas - conEIR
  const avgPuntaje = resultados.length > 0
    ? (resultados.reduce((s, r) => s + r.puntaje, 0) / resultados.length).toFixed(2)
    : '0'
  const avgLeadTime = resultados.length > 0
    ? (resultados.reduce((s, r) => s + r.lead_time, 0) / resultados.length).toFixed(1)
    : '0'
  const maxScore = resultados.length > 0 ? Math.max(...resultados.map(r => r.puntaje)) : 1

  return (
    <div style={{ padding: '20px 18px', display: 'flex', flexDirection: 'column', gap: '18px' }}>
      {/* Container header */}
      <div style={{
        background: 'var(--surface2)',
        border: '1px solid var(--border)',
        borderRadius: '10px',
        padding: '12px 16px',
        display: 'flex', alignItems: 'center', gap: '14px',
        flexWrap: 'wrap',
      }}>
        <span style={{ fontSize: '24px' }}>📦</span>
        <div>
          <div style={{ fontWeight: 800, fontSize: '14px', color: 'var(--text)' }}>
            {container.id}
          </div>
          <div style={{ fontSize: '11px', color: 'var(--text4)', marginTop: '1px' }}>
            {container.carga_tipo} · {container.tamano_pies}ft · {container.comprador}
          </div>
        </div>
        <div style={{ flex: 1 }} />
        <span style={{
          background: 'var(--patio)18',
          border: '1px solid var(--patio)30',
          borderRadius: '6px',
          padding: '3px 10px',
          fontSize: '11px', color: 'var(--patio)', fontWeight: 700,
        }}>
          {totalLineas} lineas evaluadas
        </span>
      </div>

      {/* Best line card */}
      {mejor && (
        <div style={{
          background: 'var(--surface2)',
          border: '1px solid var(--patio)40',
          borderRadius: '12px',
          overflow: 'hidden',
        }}>
          <div style={{
            padding: '12px 16px',
            borderBottom: '1px solid var(--border)',
            background: 'linear-gradient(90deg, var(--patio)14 0%, transparent 100%)',
            display: 'flex', alignItems: 'center', gap: '10px',
          }}>
            <span style={{ fontSize: '20px' }}>⭐</span>
            <div>
              <div style={{ fontSize: '10px', fontWeight: 700, color: 'var(--text4)', textTransform: 'uppercase', letterSpacing: '.06em' }}>
                Linea Recomendada
              </div>
              <div style={{ fontWeight: 800, fontSize: '16px', color: 'var(--patio)', marginTop: '2px' }}>
                {mejor.línea}
              </div>
            </div>
            <div style={{ flex: 1 }} />
            <div style={{
              background: 'var(--patio)',
              color: '#04111f',
              fontWeight: 800,
              fontSize: '16px',
              borderRadius: '8px',
              padding: '4px 14px',
            }}>
              {mejor.puntaje.toFixed(2)}
            </div>
          </div>

          <div style={{ padding: '14px 16px', display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '10px' }}>
            <MiniStat label="Cumplimiento" value={`${mejor.cumplimiento}%`} />
            <MiniStat label="Lead Time"     value={`${mejor.lead_time.toFixed(1)}h`} />
            <MiniStat label="EIR"
              value={mejor.tiene_eir ? 'Completo' : 'Sin EIR'}
              color={mejor.tiene_eir ? 'var(--success)' : 'var(--danger)'}
            />
            <MiniStat label="Contacto" value={mejor.contacto ?? '—'} />
          </div>

          {!mejor.tiene_eir && mejor.observaciones && (
            <div style={{
              margin: '0 16px 14px',
              padding: '8px 12px',
              background: 'var(--danger)14',
              border: '1px solid var(--danger)30',
              borderRadius: '8px',
              fontSize: '12px', color: 'var(--danger)',
              display: 'flex', alignItems: 'flex-start', gap: '6px',
            }}>
              <span style={{ flexShrink: 0 }}>⚠</span>
              {mejor.observaciones}
            </div>
          )}
        </div>
      )}

      {/* Summary metrics */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '10px' }}>
        <MetricCardMini label="Lineas evaluadas" value={totalLineas} color="var(--text)" />
        <MetricCardMini label="Con EIR" value={conEIR} color="var(--success)" />
        <MetricCardMini label="Sin EIR" value={sinEIR} color="var(--danger)" />
        <MetricCardMini label="Puntaje prom." value={avgPuntaje} color="var(--patio)" />
      </div>

      {/* Charts row */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        gap: '16px',
      }}>
        {/* Puntaje comparison */}
        <div style={{
          background: 'var(--surface2)',
          border: '1px solid var(--border)',
          borderRadius: '12px',
          padding: '16px',
        }}>
          <div style={{ fontSize: '12px', fontWeight: 700, color: 'var(--text3)', marginBottom: '14px', textTransform: 'uppercase', letterSpacing: '.06em' }}>
            Comparativa de Puntaje
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {resultados.slice(0, 8).map((r, i) => {
              const pct = Math.round((r.puntaje / maxScore) * 100)
              const isBest = i === 0
              return (
                <div key={r.línea}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '3px' }}>
                    <span style={{
                      fontSize: '11px', fontWeight: isBest ? 700 : 500,
                      color: isBest ? 'var(--patio)' : 'var(--text2)',
                      maxWidth: '140px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                    }}>
                      {isBest ? '⭐ ' : ''}{r.línea}
                    </span>
                    <span style={{ fontSize: '11px', fontWeight: 700, color: isBest ? 'var(--patio)' : 'var(--text3)' }}>
                      {r.puntaje.toFixed(2)}
                    </span>
                  </div>
                  <div style={{
                    height: '6px', background: 'var(--border)',
                    borderRadius: '3px', overflow: 'hidden',
                  }}>
                    <div style={{
                      height: '100%', width: `${pct}%`,
                      background: isBest ? 'var(--patio)' : 'var(--border2)',
                      borderRadius: '3px',
                      transition: 'width 0.5s ease',
                    }} />
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* Lead Time comparison */}
        <div style={{
          background: 'var(--surface2)',
          border: '1px solid var(--border)',
          borderRadius: '12px',
          padding: '16px',
        }}>
          <div style={{ fontSize: '12px', fontWeight: 700, color: 'var(--text3)', marginBottom: '14px', textTransform: 'uppercase', letterSpacing: '.06em' }}>
            Lead Time por Linea (horas)
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {resultados.slice(0, 8).map((r, i) => {
              const maxLT = Math.max(...resultados.map(x => x.lead_time), 1)
              const pct = Math.round((r.lead_time / maxLT) * 100)
              const isBest = i === 0
              const barColor = r.lead_time < 20 ? 'var(--success)' : r.lead_time < 40 ? 'var(--warning)' : 'var(--danger)'
              return (
                <div key={r.línea}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '3px' }}>
                    <span style={{
                      fontSize: '11px', fontWeight: isBest ? 700 : 500,
                      color: isBest ? 'var(--patio)' : 'var(--text2)',
                      maxWidth: '140px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                    }}>
                      {r.línea}
                    </span>
                    <span style={{ fontSize: '11px', fontWeight: 700, color: barColor }}>
                      {r.lead_time.toFixed(1)}h
                    </span>
                  </div>
                  <div style={{
                    height: '6px', background: 'var(--border)',
                    borderRadius: '3px', overflow: 'hidden',
                  }}>
                    <div style={{
                      height: '100%', width: `${pct}%`,
                      background: barColor,
                      borderRadius: '3px',
                      transition: 'width 0.5s ease',
                    }} />
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      {/* EIR distribution */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '16px',
      }}>
        <div style={{
          background: 'var(--surface2)',
          border: '1px solid var(--border)',
          borderRadius: '12px',
          padding: '16px',
        }}>
          <div style={{ fontSize: '12px', fontWeight: 700, color: 'var(--text3)', marginBottom: '10px', textTransform: 'uppercase', letterSpacing: '.06em' }}>
            Cumplimiento EIR
          </div>
          {totalLineas > 0 ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
              <div style={{
                width: '80px', height: '80px', borderRadius: '50%',
                background: `conic-gradient(var(--success) 0% ${Math.round((conEIR/totalLineas)*100)}%, var(--danger) ${Math.round((conEIR/totalLineas)*100)}% 100%)`,
                flexShrink: 0,
                border: '3px solid var(--border)',
              }} />
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', flex: 1 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px' }}>
                  <span style={{ width: '8px', height: '8px', borderRadius: '2px', background: 'var(--success)', flexShrink: 0 }} />
                  <span style={{ color: 'var(--text2)', flex: 1 }}>Con EIR</span>
                  <span style={{ fontWeight: 700, color: 'var(--success)' }}>{conEIR}</span>
                  <span style={{ color: 'var(--text4)', fontSize: '10px' }}>{Math.round((conEIR/totalLineas)*100)}%</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px' }}>
                  <span style={{ width: '8px', height: '8px', borderRadius: '2px', background: 'var(--danger)', flexShrink: 0 }} />
                  <span style={{ color: 'var(--text2)', flex: 1 }}>Sin EIR</span>
                  <span style={{ fontWeight: 700, color: 'var(--danger)' }}>{sinEIR}</span>
                  <span style={{ color: 'var(--text4)', fontSize: '10px' }}>{Math.round((sinEIR/totalLineas)*100)}%</span>
                </div>
              </div>
            </div>
          ) : (
            <div style={{ color: 'var(--text4)', fontSize: '12px', textAlign: 'center', padding: '20px 0' }}>Sin datos</div>
          )}
        </div>

        {/* Risk analysis */}
        <div style={{
          background: 'var(--surface2)',
          border: '1px solid var(--border)',
          borderRadius: '12px',
          padding: '16px',
        }}>
          <div style={{ fontSize: '12px', fontWeight: 700, color: 'var(--text3)', marginBottom: '10px', textTransform: 'uppercase', letterSpacing: '.06em' }}>
            Riesgo (prob. sin EIR)
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {resultados.filter(r => !r.tiene_eir).slice(0, 6).map(r => (
              <div key={r.línea}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '3px', fontSize: '11px' }}>
                  <span style={{ color: 'var(--text2)', maxWidth: '120px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{r.línea}</span>
                  <span style={{ fontWeight: 700, color: r.probabilidad_sin_eir > 30 ? 'var(--danger)' : 'var(--warning)' }}>
                    {r.probabilidad_sin_eir.toFixed(1)}%
                  </span>
                </div>
                <div style={{
                  height: '6px', background: 'var(--border)',
                  borderRadius: '3px', overflow: 'hidden',
                }}>
                  <div style={{
                    height: '100%',
                    width: `${Math.min(r.probabilidad_sin_eir, 100)}%`,
                    background: r.probabilidad_sin_eir > 30 ? 'var(--danger)' : 'var(--warning)',
                    borderRadius: '3px',
                    transition: 'width 0.5s ease',
                  }} />
                </div>
              </div>
            ))}
            {resultados.filter(r => !r.tiene_eir).length === 0 && (
              <div style={{ color: 'var(--success)', fontSize: '12px', padding: '10px 0', fontWeight: 600 }}>
                Todas las lineas tienen EIR completo
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

function MiniStat({ label, value, color }) {
  return (
    <div style={{
      background: 'var(--surface)',
      border: '1px solid var(--border)',
      borderRadius: '8px',
      padding: '10px 12px',
    }}>
      <div style={{
        fontSize: '10px', fontWeight: 700, color: 'var(--text4)',
        textTransform: 'uppercase', letterSpacing: '.05em', marginBottom: '4px',
      }}>
        {label}
      </div>
      <div style={{ fontWeight: 700, fontSize: '14px', color: color ?? 'var(--text2)', lineHeight: 1 }}>
        {value}
      </div>
    </div>
  )
}

function MetricCardMini({ label, value, color }) {
  return (
    <div style={{
      background: 'var(--surface2)',
      border: '1px solid var(--border)',
      borderRadius: '10px',
      padding: '12px 14px',
      textAlign: 'center',
    }}>
      <div style={{ fontSize: '20px', fontWeight: 800, color }}>{value}</div>
      <div style={{ fontSize: '10px', color: 'var(--text4)', textTransform: 'uppercase', letterSpacing: '.06em', marginTop: '4px' }}>
        {label}
      </div>
    </div>
  )
}
