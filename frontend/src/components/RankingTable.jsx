const MEDALS = [
  { label: 'Recomendada', icon: '⭐', color: 'var(--patio)' },
  { label: 'Segunda',     icon: '🥈', color: 'var(--text2)' },
  { label: 'Tercera',     icon: '🥉', color: 'var(--text3)' },
]

export default function RankingTable({ resultados }) {
  const sorted = [...resultados].sort((a, b) => b.puntaje - a.puntaje)

  return (
    <div style={{
      background: 'var(--surface2)',
      border: '1px solid var(--border)',
      borderRadius: '12px',
      overflow: 'hidden',
    }}>
      {/* Column headers */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '28px 1fr 72px 80px 70px 72px 60px',
        gap: '0',
        padding: '8px 14px',
        borderBottom: '1px solid var(--border)',
        background: 'var(--surface)',
      }}>
        {['#', 'Línea', 'Puntaje', 'Cumpl.', 'Lead T.', 'EIR', 'Riesgo'].map(h => (
          <div key={h} style={{
            fontSize: '10px', fontWeight: 700, color: 'var(--text4)',
            textTransform: 'uppercase', letterSpacing: '.06em',
          }}>
            {h}
          </div>
        ))}
      </div>

      {/* Rows */}
      {sorted.map((r, idx) => {
        const medal   = MEDALS[idx]
        const isFirst = idx === 0
        return (
          <div
            key={r.línea}
            style={{
              display: 'grid',
              gridTemplateColumns: '28px 1fr 72px 80px 70px 72px 60px',
              gap: '0',
              padding: '10px 14px',
              borderBottom: idx < sorted.length - 1 ? '1px solid var(--border)' : 'none',
              background: isFirst ? 'var(--patio)0d' : 'transparent',
              alignItems: 'center',
            }}
          >
            {/* Rank */}
            <div style={{ fontSize: '14px' }}>
              {medal ? medal.icon : `${idx + 1}`}
            </div>

            {/* Line name */}
            <div style={{
              fontSize: '13px', fontWeight: isFirst ? 700 : 500,
              color: medal?.color ?? 'var(--text2)',
              overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
              paddingRight: '8px',
            }}>
              {r.línea}
            </div>

            {/* Score */}
            <div style={{
              fontWeight: 800, fontSize: '14px',
              color: isFirst ? 'var(--patio)' : 'var(--text2)',
            }}>
              {r.puntaje.toFixed(2)}
            </div>

            {/* Compliance */}
            <div style={{ fontSize: '13px', color: 'var(--text2)', fontWeight: 600 }}>
              {r.cumplimiento}%
            </div>

            {/* Lead time */}
            <div style={{ fontSize: '13px', color: 'var(--text2)' }}>
              {r.lead_time.toFixed(1)}h
            </div>

            {/* EIR */}
            <div>
              <span style={{
                display: 'inline-block',
                padding: '2px 8px',
                borderRadius: '5px',
                fontSize: '11px',
                fontWeight: 700,
                background: r.tiene_eir ? 'var(--success)18' : 'var(--danger)18',
                color:      r.tiene_eir ? 'var(--success)'   : 'var(--danger)',
                border:     r.tiene_eir ? '1px solid var(--success)40' : '1px solid var(--danger)40',
              }}>
                {r.tiene_eir ? '✓' : '✗'}
              </span>
            </div>

            {/* Risk */}
            <div style={{
              fontSize: '12px', fontWeight: 600,
              color: r.probabilidad_sin_eir > 30 ? 'var(--danger)' : 'var(--text4)',
            }}>
              {r.probabilidad_sin_eir.toFixed(1)}%
            </div>
          </div>
        )
      })}
    </div>
  )
}
