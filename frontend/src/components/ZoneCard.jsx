import { advanceContainer } from '../api/client'

const ZONE_META = {
  BUQUE: {
    hint: 'Haz clic en un contenedor para moverlo al Piso',
    emptyMsg: 'Sin contenedores en el buque',
  },
  PISO: {
    hint: 'Haz clic en un contenedor para moverlo al Patio',
    emptyMsg: 'Sin contenedores en verificación',
  },
}

export default function ZoneCard({ zone, label, icon, color, containers, onError }) {
  const meta = ZONE_META[zone]

  async function handleAdvance(id) {
    try { await advanceContainer(id) }
    catch (e) { onError?.(e.message) }
  }

  return (
    <div style={{
      background: 'var(--surface)',
      border: `1px solid var(--border)`,
      borderRadius: 'var(--radius)',
      overflow: 'hidden',
      display: 'flex',
      flexDirection: 'column',
      transition: 'box-shadow 0.3s ease',
      boxShadow: containers.length > 0 ? `0 0 28px ${color}18` : 'none',
    }}>
      {/* Header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '14px 18px',
        borderBottom: `1px solid var(--border)`,
        background: `linear-gradient(90deg, ${color}14 0%, transparent 100%)`,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span style={{ fontSize: '20px' }}>{icon}</span>
          <div>
            <div style={{ fontWeight: 800, fontSize: '16px', color }}>{label}</div>
            <div style={{ fontSize: '11px', color: 'var(--text4)', marginTop: '1px' }}>
              {meta.hint}
            </div>
          </div>
        </div>
        <div style={{
          background: color,
          color: '#04111f',
          fontWeight: 800,
          fontSize: '14px',
          borderRadius: '8px',
          padding: '4px 14px',
          minWidth: '36px',
          textAlign: 'center',
        }}>
          {containers.length}
        </div>
      </div>

      {/* Container list */}
      <div style={{
        padding: '14px 16px',
        minHeight: '130px',
        display: 'flex',
        flexWrap: 'wrap',
        gap: '10px',
        alignContent: 'flex-start',
      }}>
        {containers.length === 0 ? (
          <div style={{
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '24px 0',
            gap: '8px',
            color: 'var(--text4)',
          }}>
            <span style={{ fontSize: '28px', opacity: 0.4 }}>📭</span>
            <span style={{ fontSize: '13px' }}>{meta.emptyMsg}</span>
          </div>
        ) : (
          containers.map(cnt => (
            <ContainerTile
              key={cnt.id}
              container={cnt}
              color={color}
              onAdvance={() => handleAdvance(cnt.id)}
            />
          ))
        )}
      </div>
    </div>
  )
}

function ContainerTile({ container, color, onAdvance }) {
  return (
    <button
      className="pop-in"
      onClick={onAdvance}
      title={`Mover ${container.id} → siguiente zona`}
      style={{
        position: 'relative',
        width: '76px',
        background: 'var(--surface2)',
        border: `1px solid ${color}40`,
        borderRadius: '10px',
        padding: '8px 6px 6px',
        cursor: 'pointer',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '5px',
        transition: 'border-color 0.2s, box-shadow 0.2s, transform 0.15s',
      }}
      onMouseEnter={e => {
        e.currentTarget.style.borderColor = color
        e.currentTarget.style.boxShadow = `0 0 14px ${color}50`
        e.currentTarget.style.transform = 'translateY(-2px)'
      }}
      onMouseLeave={e => {
        e.currentTarget.style.borderColor = `${color}40`
        e.currentTarget.style.boxShadow = 'none'
        e.currentTarget.style.transform = 'none'
      }}
    >
      {container.imagen_src
        ? <img src={container.imagen_src} style={{ width: '46px', height: '46px' }} alt="" />
        : <div style={{ width: '46px', height: '46px', borderRadius: '6px', background: `${color}30` }} />
      }

      {/* ID */}
      <span style={{ fontSize: '11px', fontWeight: 700, color: 'var(--text2)' }}>
        {container.id.split('-')[1]}
      </span>

      {/* Size badge */}
      <span style={{
        position: 'absolute', top: '-7px', right: '-7px',
        background: 'var(--surface)',
        border: `1px solid ${color}`,
        color, fontSize: '9px', fontWeight: 800,
        padding: '1px 5px', borderRadius: '5px',
      }}>
        {container.tamano_pies}ft
      </span>

      {/* Cargo type dot */}
      <div style={{
        position: 'absolute',
        bottom: '-1px', left: 0, right: 0, height: '3px',
        borderRadius: '0 0 10px 10px',
        background: color,
        opacity: 0.5,
      }} />
    </button>
  )
}
