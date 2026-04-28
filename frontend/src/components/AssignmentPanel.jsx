import { useState } from 'react'
import { assignLine, downloadReport } from '../api/client'
import RankingTable from './RankingTable'

export default function AssignmentPanel({ container, onError }) {
  const [loading,     setLoading]     = useState(false)
  const [result,      setResult]      = useState(null)
  const [downloading, setDownloading] = useState(false)

  async function handleAssign() {
    setLoading(true)
    setResult(null)
    try {
      const data = await assignLine(container)
      setResult(data)
    } catch (e) {
      onError?.(e.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleDownload() {
    if (!result?.mejor) return
    setDownloading(true)
    try {
      await downloadReport(container, result.mejor)
    } catch (e) {
      onError?.(e.message)
    } finally {
      setDownloading(false)
    }
  }

  const mejor = result?.mejor

  return (
    <div style={{
      background: 'var(--surface)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius)',
      overflow: 'hidden',
      display: 'flex', flexDirection: 'column',
    }}>
      {/* Header */}
      <div style={{
        padding: '14px 18px',
        borderBottom: '1px solid var(--border)',
        background: 'linear-gradient(90deg, var(--patio)12 0%, transparent 100%)',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      }}>
        <div>
          <div style={{ fontWeight: 800, fontSize: '15px', color: 'var(--patio)' }}>
            🚚 Asignación de Línea
          </div>
          <div style={{ fontSize: '12px', color: 'var(--text4)', marginTop: '2px' }}>
            Análisis multicriterio de operadores
          </div>
        </div>
        {result && (
          <span style={{
            background: 'var(--surface2)', border: '1px solid var(--border)',
            borderRadius: '6px', padding: '3px 10px',
            fontSize: '11px', color: 'var(--text3)',
          }}>
            {result.resultados?.length ?? 0} líneas evaluadas
          </span>
        )}
      </div>

      <div style={{ padding: '16px 18px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
        {/* Assign button */}
        <button
          className="btn-primary"
          onClick={handleAssign}
          disabled={loading}
          style={{ width: '100%', padding: '13px', fontSize: '14px', justifyContent: 'center' }}
        >
          {loading ? (
            <>
              <span style={{
                width: 14, height: 14,
                border: '2px solid #00000040',
                borderTopColor: '#000',
                borderRadius: '50%',
                animation: 'spin 0.7s linear infinite',
                display: 'inline-block', flexShrink: 0,
              }} />
              Analizando líneas…
            </>
          ) : (
            <>
              <span>🔍</span>
              Encontrar mejor línea de transporte
            </>
          )}
        </button>

        {/* Best result card */}
        {mejor && (
          <div className="fade-up" style={{
            background: 'var(--surface2)',
            border: '1px solid var(--patio)44',
            borderRadius: '12px',
            overflow: 'hidden',
          }}>
            <div style={{
              padding: '10px 14px',
              borderBottom: '1px solid var(--border)',
              background: 'linear-gradient(90deg, var(--patio)18 0%, transparent 100%)',
              display: 'flex', alignItems: 'center', gap: '10px',
            }}>
              <span style={{ fontSize: '16px' }}>⭐</span>
              <div>
                <div style={{ fontSize: '10px', fontWeight: 700, color: 'var(--text4)', textTransform: 'uppercase', letterSpacing: '.06em' }}>
                  Línea recomendada
                </div>
                <div style={{ fontWeight: 800, fontSize: '15px', color: 'var(--patio)', marginTop: '2px' }}>
                  {mejor.línea}
                </div>
              </div>
            </div>

            <div style={{ padding: '12px 14px', display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px' }}>
              <MiniStat label="Puntaje"      value={mejor.puntaje.toFixed(2)}         color="var(--patio)" />
              <MiniStat label="Cumplimiento" value={`${mejor.cumplimiento}%`}          />
              <MiniStat label="Lead Time"    value={`${mejor.lead_time.toFixed(1)}h`} />
              <MiniStat
                label="EIR"
                value={mejor.tiene_eir ? '✓ Completo' : '✗ Sin EIR'}
                color={mejor.tiene_eir ? 'var(--success)' : 'var(--danger)'}
              />
            </div>

            <div style={{
              padding: '8px 14px',
              borderTop: '1px solid var(--border)',
              fontSize: '12px', color: 'var(--text3)',
              display: 'flex', alignItems: 'center', gap: '6px',
            }}>
              <span>📞</span>
              {mejor.contacto}
            </div>

            {!mejor.tiene_eir && (
              <div style={{
                margin: '0 14px 12px',
                padding: '8px 12px',
                background: 'var(--danger)18',
                border: '1px solid var(--danger)44',
                borderRadius: '8px',
                fontSize: '12px', color: 'var(--danger)',
                display: 'flex', alignItems: 'flex-start', gap: '6px',
              }}>
                <span style={{ flexShrink: 0 }}>⚠</span>
                {mejor.observaciones}
              </div>
            )}
          </div>
        )}

        {/* Ranking table */}
        {result && (
          <>
            <div style={{
              fontSize: '12px', fontWeight: 700, color: 'var(--text3)',
              textTransform: 'uppercase', letterSpacing: '.06em',
            }}>
              Comparativa completa
            </div>
            <RankingTable resultados={result.resultados} />

            <button
              className="btn-primary"
              onClick={handleDownload}
              disabled={downloading || !mejor}
              style={{ width: '100%', padding: '12px', fontSize: '14px', justifyContent: 'center' }}
            >
              {downloading ? (
                <>
                  <span style={{
                    width: 14, height: 14,
                    border: '2px solid #00000040',
                    borderTopColor: '#000',
                    borderRadius: '50%',
                    animation: 'spin 0.7s linear infinite',
                    display: 'inline-block', flexShrink: 0,
                  }} />
                  Generando PDF…
                </>
              ) : (
                <>
                  <span>📄</span>
                  Descargar reporte de despacho
                </>
              )}
            </button>
          </>
        )}
      </div>
    </div>
  )
}

function MiniStat({ label, value, color }) {
  return (
    <div style={{
      background: 'var(--surface)',
      border: '1px solid var(--border)',
      borderRadius: '8px',
      padding: '8px 10px',
    }}>
      <div style={{
        fontSize: '10px', fontWeight: 700, color: 'var(--text4)',
        textTransform: 'uppercase', letterSpacing: '.05em', marginBottom: '4px',
      }}>
        {label}
      </div>
      <div style={{ fontWeight: 700, fontSize: '14px', color: color ?? 'var(--text2)', lineHeight: 1 }}>
        {value}
      </div>
    </div>
  )
}
