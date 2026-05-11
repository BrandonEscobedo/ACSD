import { useEffect, useState } from 'react'
import {
  addContainer,
  resetMonitor, updateConfig,
} from '../api/client'

export default function Sidebar({ state, onError, isOpen, onClose }) {
  const [busy, setBusy] = useState(false)

  const cfg = state?.config ?? {
    arrival_interval: 5, buque_time: 8, piso_time: 6,
    max_containers: 40, auto_advance: true,
  }

  async function run(fn) {
    setBusy(true)
    try { await fn() } catch (e) { onError?.(e.message) }
    finally { setBusy(false) }
  }

  async function handleCfg(key, value) {
    await run(() => updateConfig({ ...cfg, [key]: value }))
  }

  if (!isOpen) return null

  return (
    <>
      {/* Backdrop */}
      <div
        onClick={onClose}
        style={{
          position: 'fixed', inset: 0,
          background: 'rgba(0,0,0,0.3)',
          zIndex: 800,
        }}
      />

      {/* Panel */}
      <div style={{
        position: 'fixed',
        top: 0, left: 0, bottom: 0,
        width: '320px',
        background: 'var(--surface)',
        borderRight: '1px solid var(--border)',
        zIndex: 801,
        display: 'flex',
        flexDirection: 'column',
        overflowY: 'auto',
        padding: '20px 18px',
        boxShadow: '8px 0 32px #00000060',
        animation: 'slideInX .25s ease',
      }}>
        {/* Close button */}
        <button
          onClick={onClose}
          style={{
            position: 'absolute', top: '14px', right: '14px',
            background: 'var(--surface2)', border: '1px solid var(--border)',
            borderRadius: '8px', width: '32px', height: '32px',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '16px', color: 'var(--text3)', cursor: 'pointer',
            padding: 0,
          }}
        >
          {'\u2715'}
        </button>

        {/* ── Config ────────────────────────────────────── */}
        <div className="section-label" style={{ marginTop: 0 }}>Parámetros de simulación</div>

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
          hint="Cuanto espera antes de pasar a Piso"
        />
        <Slider
          label="Tiempo en Piso"
          value={cfg.piso_time} unit="s"
          min={1} max={60} step={1}
          onCommit={v => handleCfg('piso_time', v)}
          hint="Cuanto dura la verificacion"
        />
        <Slider
          label="Max. contenedores activos"
          value={cfg.max_containers}
          min={0} max={40} step={1}
          onCommit={v => handleCfg('max_containers', v)}
          note={cfg.max_containers === 0 ? 'Sin limite' : String(cfg.max_containers)}
          hint={cfg.max_containers === 0 ? 'Genera hasta que el patio este lleno' : 'El sistema pausara al llegar al limite'}
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
            <div style={{ fontWeight: 600 }}>Avance automatico</div>
            <div style={{ fontSize: '13px', color: 'var(--text2)', marginTop: '2px' }}>
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
            <span>{'\uff0b'}</span>
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
            <span>{'\u21ba'}</span>
            Reiniciar todo el sistema
          </button>
        </div>
      </div>
    </>
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
        <div style={{ fontSize: '12px', color: 'var(--text3)', marginTop: '4px' }}>{hint}</div>
      )}
    </div>
  )
}
