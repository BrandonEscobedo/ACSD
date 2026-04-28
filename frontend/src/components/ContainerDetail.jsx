const CARGA_ICON = {
  'Carga Seca':  '',
  'Refrigerada': '',
  'Peligrosa':   '',
  'Frágil':      '',
  'Nodriza':     '',
}

const ZONE_META = {
  BUQUE: { color: 'var(--buque)', label: 'Buque',       icon: '🚢' },
  PISO:  { color: 'var(--piso)',  label: 'Verificación', icon: '📋' },
  PATIO: { color: 'var(--patio)', label: 'Patio',        icon: '🏭' },
}

export default function ContainerDetail({ container }) {
  if (!container) {
    return (
      <div style={{
        display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center',
        padding: '40px 24px', gap: '12px',
        background: 'var(--surface)',
        border: '1px solid var(--border)',
        borderRadius: 'var(--radius)',
        color: 'var(--text4)', textAlign: 'center',
      }}>
        <span style={{ fontSize: '44px', opacity: 0.35 }}></span>
        <div>
          <div style={{ fontSize: '14px', fontWeight: 600, color: 'var(--text3)', marginBottom: '4px' }}>
            Sin contenedor seleccionado
          </div>
          <div style={{ fontSize: '12px', lineHeight: 1.5 }}>
            Haz clic en un contenedor<br />del patio para ver sus detalles
          </div>
        </div>
      </div>
    )
  }

  const zone  = ZONE_META[container.posicion_actual] ?? { color: 'var(--text4)', label: container.posicion_actual, icon: '📍' }
  const cargo = CARGA_ICON[container.carga_tipo] ?? ''

  return (
    <div className="fade-up" style={{
      background: 'var(--surface)',
      border: `1px solid ${zone.color}44`,
      borderRadius: 'var(--radius)',
      overflow: 'hidden',
      boxShadow: `0 0 24px ${zone.color}14`,
    }}>
      {/* Header */}
      <div style={{
        padding: '16px 18px',
        borderBottom: '1px solid var(--border)',
        background: `linear-gradient(90deg, ${zone.color}12 0%, transparent 100%)`,
        display: 'flex', alignItems: 'center', gap: '14px',
      }}>
        {container.imagen_src
          ? <img src={container.imagen_src} style={{ width: '52px', height: '52px', borderRadius: '10px', flexShrink: 0 }} alt="" />
          : <div style={{ width: '52px', height: '52px', borderRadius: '10px', background: `${zone.color}22`, flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '24px' }}>{cargo}</div>
        }
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ fontWeight: 800, fontSize: '17px', color: 'var(--text)', letterSpacing: '-.01em' }}>
            {container.id}
          </div>
          <div style={{ fontSize: '13px', color: zone.color, marginTop: '3px', fontWeight: 600 }}>
            {cargo} {container.carga_tipo}
          </div>
        </div>
        <span style={{
          background: `${zone.color}22`, color: zone.color,
          border: `1px solid ${zone.color}44`,
          padding: '4px 12px', borderRadius: '20px',
          fontSize: '12px', fontWeight: 700, flexShrink: 0,
        }}>
          {zone.icon} {zone.label}
        </span>
      </div>

      {/* Fields */}
      <div style={{ padding: '16px 18px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
        <Field label="Posición en patio"
          value={container.columna != null ? `Col ${container.columna} · Piso ${container.piso}` : '—'}
          wide
        />
        <Field label="Tamaño"    value={`${container.tamano_pies} ft`} />
        <Field label="Comprador" value={container.comprador ?? '—'} />
        <Field label="Estado"    value={container.estado} color={container.estado === 'activo' ? 'var(--success)' : 'var(--text3)'} />
      </div>
    </div>
  )
}

function Field({ label, value, color, wide }) {
  return (
    <div style={{
      background: 'var(--surface2)',
      border: '1px solid var(--border)',
      borderRadius: '10px',
      padding: '10px 12px',
      gridColumn: wide ? 'span 2' : undefined,
    }}>
      <div style={{
        fontSize: '10px', fontWeight: 700,
        color: 'var(--text4)', marginBottom: '4px',
        textTransform: 'uppercase', letterSpacing: '.06em',
      }}>
        {label}
      </div>
      <div style={{ fontWeight: 700, fontSize: '14px', color: color ?? 'var(--text2)', lineHeight: 1.3 }}>
        {value}
      </div>
    </div>
  )
}
