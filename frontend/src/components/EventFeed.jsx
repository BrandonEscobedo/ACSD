import { useEffect, useRef } from 'react'

const ZONE_COLORS = {
  BUQUE:  'var(--buque)',
  PISO:   'var(--piso)',
  PATIO:  'var(--patio)',
  MAR:    'var(--text4)',
  SALIDA: 'var(--success)',
  '—':    'var(--text4)',
}

const ZONE_ICONS = {
  BUQUE: '🚢',
  PISO:  '📋',
  PATIO: '🏭',
  MAR:   '🌊',
  SALIDA:'✅',
}

function relTime(iso) {
  const s = Math.round((Date.now() - new Date(iso).getTime()) / 1000)
  if (s < 5)   return 'ahora'
  if (s < 60)  return `${s}s`
  if (s < 3600) return `${Math.floor(s / 60)}m`
  return new Date(iso).toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' })
}

export default function EventFeed({ events = [] }) {
  const listRef = useRef(null)

  useEffect(() => {
    if (listRef.current) listRef.current.scrollTop = 0
  }, [events.length])

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      overflow: 'hidden',
    }}>
      {/* Header */}
      <div style={{
        padding: '12px 18px',
        borderBottom: '1px solid var(--border)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexShrink: 0,
      }}>
        <div style={{ fontWeight: 700, fontSize: '14px', color: 'var(--text2)' }}>
          📡 Eventos en vivo
        </div>
        <div style={{
          background: 'var(--surface2)',
          border: '1px solid var(--border)',
          borderRadius: '6px',
          padding: '2px 8px',
          fontSize: '11px',
          color: 'var(--text3)',
        }}>
          {events.length}
        </div>
      </div>

      {/* Event list — newest on top */}
      <div ref={listRef} style={{ flex: 1, overflowY: 'auto' }}>
        {events.length === 0 ? (
          <div style={{
            textAlign: 'center', padding: '32px 16px',
            color: 'var(--text4)', fontSize: '13px',
          }}>
            Los eventos aparecerán aquí cuando haya actividad
          </div>
        ) : (
          events.map((evt, i) => <EventRow key={i} evt={evt} isNew={i === 0} />)
        )}
      </div>
    </div>
  )
}

function EventRow({ evt, isNew }) {
  const isSystem = evt.container_id === 'SYSTEM'
  const srcColor = ZONE_COLORS[evt.origen]  ?? 'var(--text4)'
  const dstColor = ZONE_COLORS[evt.destino] ?? 'var(--text4)'
  const dstIcon  = ZONE_ICONS[evt.destino]  ?? '→'

  return (
    <div
      className={isNew ? 'slide-in' : ''}
      style={{
        padding: '10px 18px',
        borderBottom: '1px solid var(--border)',
        display: 'grid',
        gridTemplateColumns: '38px 1fr',
        gap: '10px',
        alignItems: 'center',
        background: isNew ? 'var(--surface2)' : 'transparent',
        transition: 'background 1.5s ease',
      }}
    >
      {/* Time */}
      <div style={{ fontSize: '11px', color: 'var(--text4)', textAlign: 'right' }}>
        {relTime(evt.timestamp)}
      </div>

      {isSystem ? (
        /* System event */
        <div style={{ fontSize: '12px', color: 'var(--text3)', fontStyle: 'italic' }}>
          ⚙ {evt.accion}
        </div>
      ) : (
        /* Container event */
        <div style={{ display: 'flex', flexDirection: 'column', gap: '3px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{
              fontWeight: 700, fontSize: '12px', color: 'var(--buque)',
              background: 'var(--surface2)',
              padding: '1px 7px', borderRadius: '5px',
              border: '1px solid var(--border2)',
            }}>
              {evt.container_id}
            </span>
          </div>

          {/* Flow: ORIGEN → DESTINO */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <ZonePill label={evt.origen}  icon={ZONE_ICONS[evt.origen]  ?? ''} color={srcColor} />
            <span style={{ color: 'var(--text4)', fontSize: '12px' }}>→</span>
            <ZonePill label={evt.destino} icon={dstIcon} color={dstColor} />
          </div>

          <div style={{ fontSize: '11px', color: 'var(--text4)' }}>
            {evt.accion}
          </div>
        </div>
      )}
    </div>
  )
}

function ZonePill({ label, icon, color }) {
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: '3px',
      background: `${color}18`,
      color, border: `1px solid ${color}40`,
      padding: '1px 7px', borderRadius: '5px',
      fontSize: '11px', fontWeight: 600,
    }}>
      {icon && <span>{icon}</span>}
      {label}
    </span>
  )
}
