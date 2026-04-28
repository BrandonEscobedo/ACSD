import { useEffect, useState } from 'react'

export default function MonitorHeader({ connected, state }) {
  const [time, setTime] = useState(new Date())
  useEffect(() => {
    const t = setInterval(() => setTime(new Date()), 1000)
    return () => clearInterval(t)
  }, [])

  const buque   = state?.buque.length  ?? 0
  const piso    = state?.piso.length   ?? 0
  const patio   = state ? state.patio.flat().filter(Boolean).length : 0
  const ocupPct = Math.round((patio / 40) * 100)

  return (
    <header style={{
      height: 'var(--header-h)',
      background: 'var(--surface)',
      borderBottom: '1px solid var(--border)',
      display: 'flex',
      alignItems: 'center',
      padding: '0 28px',
      gap: '32px',
      flexShrink: 0,
    }}>
      {/* Brand */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', minWidth: '220px' }}>
        <div style={{
          width: '38px', height: '38px', borderRadius: '10px',
          background: 'linear-gradient(135deg, #0ea5e9, #0369a1)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '20px', flexShrink: 0,
          boxShadow: '0 0 16px #38bdf830',
        }}>
          🚢
        </div>
        <div>
          <div style={{ fontWeight: 800, fontSize: '16px', color: 'var(--text)', letterSpacing: '-.02em' }}>
            ACSD Monitor
          </div>
          <div style={{ fontSize: '12px', color: 'var(--text3)', marginTop: '1px' }}>
            Control de Puerto
          </div>
        </div>
      </div>

      {/* Separator */}
      <div style={{ width: '1px', height: '32px', background: 'var(--border)' }} />

      {/* Connection pill */}
      <div style={{
        display: 'flex', alignItems: 'center', gap: '8px',
        background: connected ? '#0c2e20' : '#2e0c0c',
        border: `1px solid ${connected ? '#14532d' : '#7f1d1d'}`,
        borderRadius: '20px', padding: '5px 14px',
      }}>
        <span style={{
          width: '8px', height: '8px', borderRadius: '50%', flexShrink: 0,
          background: connected ? 'var(--success)' : 'var(--danger)',
          boxShadow: connected ? '0 0 8px var(--success)' : '0 0 8px var(--danger)',
          animation: connected ? 'pulseDot 2s ease-in-out infinite' : 'none',
        }} />
        <span style={{ fontSize: '13px', fontWeight: 600, color: connected ? '#4ade80' : '#fca5a5' }}>
          {connected ? 'En línea' : 'Sin conexión'}
        </span>
      </div>

      <div style={{ flex: 1 }} />

      {/* Live stats */}
      <div style={{ display: 'flex', gap: '8px' }}>
        <StatPill icon="🚢" label="Buque"  value={buque}              color="var(--buque)"   bg="#0c1e2e" />
        <StatPill icon="📋" label="Piso"   value={piso}               color="var(--piso)"    bg="#1a0c2e" />
        <StatPill icon="🏭" label="Patio"  value={`${patio} / 40`}    color="var(--patio)"   bg="#2e1a0c" />
        <StatPill
          icon="📊"
          label="Ocupación"
          value={`${ocupPct}%`}
          color={ocupPct > 80 ? 'var(--danger)' : ocupPct > 50 ? 'var(--warning)' : 'var(--success)'}
          bg={ocupPct > 80 ? '#2e0c0c' : '#0c2e20'}
        />
      </div>

      {/* Separator */}
      <div style={{ width: '1px', height: '32px', background: 'var(--border)' }} />

      {/* Clock */}
      <div style={{
        fontFamily: 'monospace', fontSize: '15px', fontWeight: 600,
        color: 'var(--text2)', letterSpacing: '.04em', minWidth: '76px',
      }}>
        {time.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
      </div>
    </header>
  )
}

function StatPill({ icon, label, value, color, bg }) {
  return (
    <div style={{
      display: 'flex', alignItems: 'center', gap: '8px',
      background: bg, border: '1px solid var(--border)',
      borderRadius: '10px', padding: '6px 14px',
    }}>
      <span style={{ fontSize: '15px' }}>{icon}</span>
      <div>
        <div style={{ fontSize: '10px', color: 'var(--text4)', textTransform: 'uppercase', letterSpacing: '.07em', marginBottom: '1px' }}>
          {label}
        </div>
        <div style={{ fontWeight: 800, fontSize: '15px', color, lineHeight: 1 }}>{value}</div>
      </div>
    </div>
  )
}
