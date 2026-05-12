import { useState } from 'react'

export default function Tabs({ tabs, children }) {
  const [active, setActive] = useState(0)

  return (
    <div style={{
      background: 'var(--surface)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius)',
      overflow: 'hidden',
    }}>
      <div style={{
        display: 'flex',
        borderBottom: '1px solid var(--border)',
        background: 'var(--surface2)',
      }}>
        {tabs.map((tab, i) => (
          <button
            key={i}
            onClick={() => setActive(i)}
            style={{
              flex: 1,
              padding: '12px 20px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              fontSize: '14px',
              fontWeight: 700,
              border: 'none',
              borderBottom: active === i
                ? '2px solid var(--buque)'
                : '2px solid transparent',
              background: active === i
                ? 'var(--surface)'
                : 'transparent',
              color: active === i
                ? 'var(--buque)'
                : 'var(--text3)',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
            }}
          >
            {tab}
          </button>
        ))}
      </div>
      <div>
        {children[active]}
      </div>
    </div>
  )
}
