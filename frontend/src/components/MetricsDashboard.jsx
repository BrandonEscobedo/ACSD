export default function MetricsDashboard({ contenedores, eventos }) {
  const enPatio = contenedores.filter(c => c.posicion_actual === 'PATIO').length
  const ocupacion = ((enPatio / 40) * 100).toFixed(1)

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px', marginBottom: '20px' }}>
      <Metric label="Procesados" value={contenedores.length} />
      <Metric label="En Patio" value={enPatio} color="var(--color-patio)" />
      <Metric label="Ocupación" value={`${ocupacion}%`} color={+ocupacion > 80 ? 'var(--color-danger)' : 'var(--color-success)'} />
      <Metric label="Eventos" value={eventos.length} color="var(--color-buque)" />
    </div>
  )
}

function Metric({ label, value, color }) {
  return (
    <div className="metric-card">
      <div className="label">{label}</div>
      <div className="value" style={color ? { color } : {}}>{value}</div>
    </div>
  )
}
