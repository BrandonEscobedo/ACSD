import { useCallback, useEffect, useRef, useState } from 'react'

const emptyZones = () => ({ BUQUE: [], PISO: [], PATIO: [] })
const emptyPatio = () => Array.from({ length: 10 }, () => Array(4).fill(null))

export function useAnimation(simData, speed) {
  const [index, setIndex] = useState(0)
  const [playing, setPlaying] = useState(false)
  const [zones, setZones] = useState(emptyZones)
  const [patio, setPatio] = useState(emptyPatio)
  const [activeId, setActiveId] = useState(null)

  // Refs para leer estado actual dentro del setInterval sin stale closure
  const indexRef = useRef(0)
  const zonesRef = useRef(emptyZones())
  const patioRef = useRef(emptyPatio())
  const contMapRef = useRef({})

  useEffect(() => {
    if (!simData) return
    contMapRef.current = Object.fromEntries(simData.contenedores.map(c => [c.id, c]))
  }, [simData])

  const applyStep = useCallback(() => {
    if (!simData) return false
    if (indexRef.current >= simData.eventos.length) return false

    const evt = simData.eventos[indexRef.current]
    const cont = contMapRef.current[evt.contenedor_id]

    if (cont) {
      // Actualizar zonas
      const nz = {
        BUQUE: zonesRef.current.BUQUE.filter(c => c.id !== cont.id),
        PISO:  zonesRef.current.PISO.filter(c => c.id !== cont.id),
        PATIO: zonesRef.current.PATIO.filter(c => c.id !== cont.id),
      }
      if (evt.destino in nz) nz[evt.destino] = [...nz[evt.destino], cont]
      zonesRef.current = nz

      // Actualizar patio si el contenedor fue colocado
      if (evt.destino === 'PATIO' && cont.columna != null && cont.piso != null) {
        const np = patioRef.current.map(col => [...col])
        np[cont.columna][cont.piso] = cont.id
        patioRef.current = np
      }

      setZones({ ...zonesRef.current })
      setPatio([...patioRef.current])
      setActiveId(cont.id)
    }

    indexRef.current += 1
    setIndex(indexRef.current)
    return indexRef.current < simData.eventos.length
  }, [simData])

  const timerRef = useRef(null)

  useEffect(() => {
    if (!playing || !simData) return

    const delay = Math.max(50, Math.round(500 / speed))
    timerRef.current = setInterval(() => {
      const hasMore = applyStep()
      if (!hasMore) {
        clearInterval(timerRef.current)
        setPlaying(false)
        setActiveId(null)
      }
    }, delay)

    return () => clearInterval(timerRef.current)
  }, [playing, speed, simData, applyStep])

  const play = useCallback(() => setPlaying(true), [])
  const pause = useCallback(() => {
    clearInterval(timerRef.current)
    setPlaying(false)
  }, [])

  const stop = useCallback(() => {
    clearInterval(timerRef.current)
    setPlaying(false)
    indexRef.current = 0
    zonesRef.current = emptyZones()
    patioRef.current = emptyPatio()
    setIndex(0)
    setZones(emptyZones())
    setPatio(emptyPatio())
    setActiveId(null)
  }, [])

  const total = simData?.eventos.length ?? 0

  return {
    index,
    total,
    playing,
    zones,
    patio,
    activeId,
    play,
    pause,
    stop,
    currentEvent: total > 0 && index > 0 ? simData.eventos[index - 1] : null,
  }
}
