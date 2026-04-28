import { useEffect, useState } from 'react'
import {
  startAuto, stopAuto, addContainer,
  resetMonitor, updateConfig,
} from '../api/client'
import EventFeed from './EventFeed'

export default function Sidebar({ state, events, onError }) {
  const [busy, setBusy] = useState(false)

  const cfg = state?.config ?? {
    arrival_interval: 5, buque_time: 8, piso_time: 6,
    max_containers: 40, auto_advance: true,
  }
  const autoRunning = state?.auto_running ?? false

  async function run(fn) {
    setBusy(true)
    try { await fn() } catch (e) { onError?.(e.message) }
    finally { setBusy(false) }
  }

  async function handleCfg(key, value) {
    await run(() => updateConfig({ ...cfg, [key]: value }))
  }

  return (
    <div style={{
      display: 'flex', flexDirection: 'column',
      height: '100%',
      background: 'var(--surface)',
      borderRight: '1px solid var(--border)',
    }}>
      {/* ── Scrollable controls ─────────────────────────── */}
      <div style={{ overflowY: 'auto', padding: '20px 18px', flexShrink: 0, userSelect: 'none' }}>

        {/* ── Auto mode ─────────────────────────────────── */}
        <div className="section-label">Modo de operación</div>
        <button
          onClick={() => run(autoRunning ? stopAuto : startAuto)}
          disabled={busy}
          style={{
            width: '100%', padding: '14px 18px', fontSize: '15px',
            borderRadius: '10px', justifyContent: 'center',
            background: autoRunning
              ? 'linear-gradient(135deg, #052e16, #14532d)'
              : 'linear-gradient(135deg, #0c1e36, #0c4a6e)',
            border: `1.5px solid ${autoRunning ? '#16a34a' : '#0284c7'}`,
            color: autoRunning ? '#4ade80' : '#38bdf8',
            boxShadow: autoRunning ? '0 0 20px #22c55e20' : '0 0 20px #38bdf820',
          }}
        >
          <span style={{ fontSize: '18px' }}>{autoRunning ? '⏹' : '▶'}</span>
          <span>{autoRunning ? 'Detener automático' : 'Iniciar automático'}</span>
        </button>

        {autoRunning && (
          <div style={{
            marginTop: '10px', padding: '8px 12px',
            background: '#052e16', border: '1px solid #14532d',
            borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '8px',
            fontSize: '13px', color: '#4ade80',
          }}>
            <span style={{
              width: 8, height: 8, borderRadius: '50%',
              background: '#4ade80', flexShrink: 0,
              animation: 'pulseDot 1.2s ease-in-out infinite',
              display: 'inline-block',
            }} />
            Generando contenedores automáticamente
          </div>
        )}

        <div className="divider" />

        {/* ── Config ────────────────────────────────────── */}
        <div className="section-label">Parámetros de simulación</div>

        <Slider
          label="Intervalo de llegada"
          value={cfg.arrival_interval} unit="s"
          min={1} max={30} step={0.5}
          onCommit={v => handleCfg('arrival_interval', v)}
          hint="Segundos entre cada contenedor nuevo"
        />
        <Slider
          label="Tiempo en Buque"
          value={cfg.buque_time} unit="s"
          min={1} max={60} step={1}
          onCommit={v => handleCfg('buque_time', v)}
          hint="Cuánto espera antes de pasar a Piso"
        />
        <Slider
          label="Tiempo en Piso"
          value={cfg.piso_time} unit="s"
          min={1} max={60} step={1}
          onCommit={v => handleCfg('piso_time', v)}
          hint="Cuánto dura la verificación"
        />
        <Slider
          label="Máx. contenedores activos"
          value={cfg.max_containers}
          min={0} max={40} step={1}
          onCommit={v => handleCfg('max_containers', v)}
          note={cfg.max_containers === 0 ? 'Sin límite' : String(cfg.max_containers)}
          hint={cfg.max_containers === 0 ? 'Genera hasta que el patio esté lleno' : 'El sistema pausará al llegar al límite'}
        />

        <label style={{
          display: 'flex', alignItems: 'center', gap: '10px',
          fontSize: '13px', color: 'var(--text2)', cursor: 'pointer',
          padding: '10px 12px', borderRadius: '8px',
          background: 'var(--surface2)', border: '1px solid var(--border)',
          marginBottom: '4px',
        }}>
          <input
            type="checkbox"
            checked={cfg.auto_advance}
            onChange={e => handleCfg('auto_advance', e.target.checked)}
          />
          <div>
            <div style={{ fontWeight: 600 }}>Avance automático</div>
            <div style={{ fontSize: '12px', color: 'var(--text3)', marginTop: '2px' }}>
              Los contenedores progresan solos por las zonas
            </div>
          </div>
        </label>

        <div className="divider" />

        {/* ── Manual actions ────────────────────────────── */}
        <div className="section-label">Acciones manuales</div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <button
            className="btn-primary"
            onClick={() => run(addContainer)}
            disabled={busy}
            style={{ width: '100%', padding: '12px', fontSize: '14px', justifyContent: 'center' }}
          >
            <span>＋</span>
            Agregar contenedor al buque
          </button>
          <button
            className="btn-outline"
            onClick={() => run(resetMonitor)}
            disabled={busy}
            style={{
              width: '100%', padding: '12px', fontSize: '13px', justifyContent: 'center',
              border: '1.5px solid var(--danger)', color: 'var(--danger)',
            }}
          >
            <span>↺</span>
            Reiniciar todo el sistema
          </button>
        </div>

        <div className="divider" />
      </div>

      {/* ── Event feed — takes remaining height ─────────── */}
      <div style={{ flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column', minHeight: '200px' }}>
        <EventFeed events={events} />
      </div>
    </div>
  )
}

function Slider({ label, value, unit = '', min, max, step, onCommit, note, hint }) {
  const [draft, setDraft] = useState(value)

  useEffect(() => {
    setDraft(value)
  }, [value])

  function commit(v) {
    if (v !== value) onCommit(v)
  }

  return (
    <div style={{ marginBottom: '16px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '8px' }}>
        <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text2)' }}>{label}</span>
        <span style={{
          fontSize: '14px', fontWeight: 800, color: 'var(--buque)',
          background: 'var(--surface2)', padding: '2px 10px', borderRadius: '6px',
          border: '1px solid var(--border)',
        }}>
          {note ?? `${draft}${unit}`}
        </span>
      </div>
      <input
        type="range" min={min} max={max} step={step} value={draft}
        onChange={e => setDraft(+e.target.value)}
        onMouseUp={() => commit(draft)}
        onTouchEnd={() => commit(draft)}
        onKeyUp={() => commit(draft)}
      />
      {hint && (
        <div style={{ fontSize: '11px', color: 'var(--text4)', marginTop: '4px' }}>{hint}</div>
      )}
    </div>
  )
}
