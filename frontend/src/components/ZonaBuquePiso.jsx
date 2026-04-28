export default function ZonaBuquePiso({ zona, label, color, contenedores, activeId }) {
  return (
    <div style={{
      position: 'relative',
      width: '100%',
      height: '140px',
      border: `3px solid ${color}`,
      background: `linear-gradient(90deg, ${color}15, ${color}30)`,
      borderRadius: '16px',
      overflow: 'hidden',
      flexShrink: 0,
    }}>
      <span style={{
        position: 'absolute', left: '16px', top: '50%',
        transform: 'translateY(-50%)',
        fontWeight: 800, fontSize: '24px', color,
        textShadow: `0 0 20px ${color}88`,
      }}>
        {label}
      </span>

      <div style={{
        position: 'absolute', top: '12px', right: '12px',
        background: color, color: '#fff',
        borderRadius: '20px', padding: '4px 12px',
        fontWeight: 700, fontSize: '14px',
      }}>
        {contenedores.length} 📦
      </div>

      <div style={{
        position: 'absolute',
        left: '140px', top: '50%',
        transform: 'translateY(-50%)',
        display: 'flex', gap: '8px', alignItems: 'center',
        overflowX: 'hidden', maxWidth: 'calc(100% - 200px)',
      }}>
        {contenedores.slice(0, 14).map(cnt => (
          <div key={cnt.id} style={{
            transition: 'all 0.4s ease',
            transform: cnt.id === activeId ? 'scale(1.2)' : 'scale(1)',
            filter: cnt.id === activeId
              ? `drop-shadow(0 0 8px ${color})`
              : 'drop-shadow(0 2px 4px rgba(0,0,0,0.4))',
          }}>
            {cnt.imagen_src ? (
              <img src={cnt.imagen_src} style={{ width: '44px', height: '44px' }} alt={cnt.id} />
            ) : (
              <div style={{
                width: '44px', height: '44px',
                background: `${color}44`, borderRadius: '6px',
                border: `1px solid ${color}`,
              }} />
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
