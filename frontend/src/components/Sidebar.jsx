import { useState } from 'react'
import { addContainer } from '../api/client'

export default function Sidebar({ onError, isOpen, onClose }) {
  const [busy, setBusy] = useState(false)

  async function run(fn) {
    setBusy(true)
    try { await fn() } catch (e) { onError?.(e.message) }
    finally { setBusy(false) }
  }

  if (!isOpen) return null

  return (
    <>
      <div
        onClick={onClose}
        style={{
          position: 'fixed', inset: 0,
          background: 'rgba(0,0,0,0.3)',
          zIndex: 800,
        }}
      />

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

        <div className="section-label" style={{ marginTop: 0 }}>Acciones manuales</div>
        <button
          className="btn-primary"
          onClick={() => run(addContainer)}
          disabled={busy}
          style={{ width: '100%', padding: '12px', fontSize: '14px', justifyContent: 'center' }}
        >
          <span>{'\uff0b'}</span>
          Agregar contenedor al buque
        </button>
      </div>
    </>
  )
}
