import { useEffect, useRef } from 'react'
import ImagePlaceholder from './shared/ImagePlaceholder'

/* ── Star-field canvas ── */
function StarField() {
  const ref = useRef(null)
  useEffect(() => {
    const canvas = ref.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')

    function resize() {
      canvas.width  = canvas.offsetWidth
      canvas.height = canvas.offsetHeight
      draw()
    }

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      for (let i = 0; i < 240; i++) {
        const x  = Math.random() * canvas.width
        const y  = Math.random() * canvas.height
        const r  = Math.random() * 1.1 + 0.15
        const op = Math.random() * 0.55 + 0.08
        ctx.beginPath()
        ctx.arc(x, y, r, 0, Math.PI * 2)
        ctx.fillStyle = `rgba(255,255,255,${op})`
        ctx.fill()
      }
    }

    resize()
    const ro = new ResizeObserver(resize)
    ro.observe(canvas)
    return () => ro.disconnect()
  }, [])

  return (
    <canvas
      ref={ref}
      aria-hidden="true"
      style={{ position:'absolute', inset:0, width:'100%', height:'100%', pointerEvents:'none', zIndex:0 }}
    />
  )
}

/* ── Subtle perspective grid ── */
function PerspectiveGrid() {
  return (
    <div
      aria-hidden="true"
      style={{
        position: 'absolute', inset: 0, zIndex: 0, pointerEvents: 'none',
        backgroundImage: `
          linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px),
          linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px)
        `,
        backgroundSize: '80px 80px',
        maskImage: 'radial-gradient(ellipse 70% 60% at 50% 50%, black 30%, transparent 100%)',
        WebkitMaskImage: 'radial-gradient(ellipse 70% 60% at 50% 50%, black 30%, transparent 100%)',
      }}
    />
  )
}

/* ── Hand-landmark constellation — the 21-point MediaPipe skeleton ── */
function LandmarkConstellation() {
  /* Normalized MediaPipe hand landmark topology (0 = wrist). */
  const PTS = [
    [50, 96], [30, 84], [18, 68], [11, 54], [5, 43],
    [40, 52], [37, 33], [35, 21], [33, 11],
    [51, 49], [52, 28], [52, 15], [52, 4],
    [62, 52], [65, 32], [66, 20], [67, 9],
    [73, 58], [80, 42], [84, 32], [88, 22],
  ]
  const BONES = [
    [0,1],[1,2],[2,3],[3,4],
    [0,5],[5,6],[6,7],[7,8],
    [0,9],[9,10],[10,11],[11,12],
    [0,13],[13,14],[14,15],[15,16],
    [0,17],[17,18],[18,19],[19,20],
    [5,9],[9,13],[13,17],
  ]

  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 100 110"
      className="landmark-breath"
      style={{
        position:'absolute', zIndex:1, pointerEvents:'none',
        right:'6%', top:'16%',
        width:'clamp(180px, 22vw, 320px)',
        opacity:0.5,
      }}
    >
      {BONES.map(([a, b]) => (
        <line
          key={`${a}-${b}`}
          x1={PTS[a][0]} y1={PTS[a][1]}
          x2={PTS[b][0]} y2={PTS[b][1]}
          stroke="rgba(56,189,248,0.55)"
          strokeWidth="0.9"
          strokeLinecap="round"
        />
      ))}
      {PTS.map(([x, y], i) => (
        <circle
          key={i}
          cx={x} cy={y}
          r={i === 0 ? 2.4 : i === 4 || i === 8 ? 2.1 : 1.5}
          fill={i === 4 || i === 8 ? 'rgba(125,211,252,0.95)' : 'rgba(226,232,240,0.75)'}
        />
      ))}
      {/* Pinch indicator between thumb tip (4) and index tip (8) */}
      <line
        x1={PTS[4][0]} y1={PTS[4][1]}
        x2={PTS[8][0]} y2={PTS[8][1]}
        stroke="rgba(74,222,128,0.75)"
        strokeWidth="0.8"
        strokeDasharray="2 2"
      />
    </svg>
  )
}

const STATS = [
  { num:'21-pt',     lbl:'Hand landmark model' },
  { num:'Mixed DPI', lbl:'Any monitor layout' },
  { num:'100',       lbl:'Automated tests' },
  { num:'0',         lbl:'Camera frames uploaded' },
]

const REPO_URL = 'https://github.com/Mizunandayo/mitsu'

export default function Hero() {
  const scrollToDemo = e => {
    e.preventDefault()
    document.querySelector('#demo')?.scrollIntoView({ behavior:'smooth', block:'start' })
  }

  return (
    <section id="hero" className="relative overflow-hidden" style={{ minHeight:'100dvh', background:'#050505' }}>

      <StarField />
      <PerspectiveGrid />
      <LandmarkConstellation />

      {/* Radial spotlight — behind the headline */}
      <div aria-hidden="true" style={{
        position:'absolute', inset:0, zIndex:1, pointerEvents:'none',
        background:'radial-gradient(ellipse 65% 55% at 50% 42%, rgba(255,255,255,0.055) 0%, transparent 70%)',
      }} />

      {/* ── Main content ── */}
      <div
        style={{
          position:'relative', zIndex:2,
          display:'flex', flexDirection:'column', alignItems:'center',
          justifyContent:'center', minHeight:'100dvh',
          padding:'100px 32px 80px',
          textAlign:'center',
        }}
      >
        {/* Submission data strip — Swiss-industrial, no container */}
        <div className="hero-enter hero-strip" style={{ animationDelay: '0.05s' }}>
       
          <div className="hero-strip-row">
            <span className="hero-strip-primary">OpenAI Build Week</span>
            <span className="hero-strip-slash" aria-hidden="true">///</span>
            <span className="hero-strip-primary">Jul 14 — 21 &nbsp;2026</span>
          </div>
         
        </div>

        {/* Hero wordmark */}
        <h1
          className="hero-enter"
          style={{
            animationDelay:'0.20s',
            fontWeight:900,
            fontFamily:'Outfit, Poppins, system-ui, sans-serif',
            letterSpacing:'-0.035em',
            lineHeight:0.9,
            color:'#ffffff',
            marginBottom:18,
            fontSize:'clamp(4rem,11vw,8.4rem)',
            display:'flex',
            alignItems:'baseline',
            justifyContent:'center',
            gap:'clamp(0.5rem,1.8vw,1.4rem)',
            flexWrap:'wrap',
          }}
        >
          <span style={{ color:'#f5f5f5', letterSpacing:'0.08em' }}>MITSU</span>
          <span style={{ color:'rgba(113,113,122,0.95)', fontWeight:800, letterSpacing:'-0.02em' }}>
            見つ
          </span>
        </h1>

        {/* Subtitle */}
        <p
          className="hero-enter"
          style={{
            animationDelay:'0.30s',
            fontSize:'clamp(1rem,2.2vw,1.4rem)',
            fontWeight:500,
            color:'rgba(255,255,255,0.55)',
            letterSpacing:'-0.01em',
            marginBottom:14,
            lineHeight:1.4,
          }}
        >
          Hand-and-Voice Window Control for Windows
        </p>

        {/* One-liner */}
        <p
          className="hero-enter"
          style={{
            animationDelay:'0.38s',
            fontSize:'clamp(0.98rem,1.55vw,1.14rem)',
            fontWeight:400,
            color:'rgba(212,212,216,0.8)',
            maxWidth:540,
            lineHeight:1.75,
            marginBottom:44,
          }}
        >
          Point at nothing, say a name, and your windows move. Pinch a window on one
          monitor, slide your hand, and watch it glide to the other. No mouse. No clicking.
        </p>

        {/* CTA buttons */}
        <div
          className="hero-enter"
          style={{
            animationDelay:'0.46s',
            display:'flex', gap:12, flexWrap:'wrap',
            justifyContent:'center', marginBottom:56,
          }}
        >
          <a
            href="#demo"
            onClick={scrollToDemo}
            style={{
              display:'inline-flex', alignItems:'center', gap:10,
              background:'#ffffff', color:'#050505',
              fontSize:'0.88rem', fontWeight:700,
              padding:'14px 28px', borderRadius:999,
              textDecoration:'none',
              transition:'opacity 150ms cubic-bezier(0.16,1,0.3,1)',
            }}
            onMouseEnter={e => e.currentTarget.style.opacity='0.86'}
            onMouseLeave={e => e.currentTarget.style.opacity='1'}
          >
            Watch the Demo
            <span style={{
              width:24, height:24, borderRadius:'50%',
              background:'rgba(0,0,0,0.10)',
              display:'flex', alignItems:'center', justifyContent:'center',
              flexShrink:0,
            }}>
              <svg width="9" height="9" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
                <polygon points="4,2 13,8 4,14" />
              </svg>
            </span>
          </a>
          <a
            href={REPO_URL}
            target="_blank" rel="noopener noreferrer"
            style={{
              display:'inline-flex', alignItems:'center', gap:8,
              border:'1px solid rgba(255,255,255,0.18)',
              color:'rgba(255,255,255,0.72)',
              fontSize:'0.88rem', fontWeight:500,
              padding:'14px 28px', borderRadius:999,
              textDecoration:'none',
              background:'rgba(255,255,255,0.04)',
              backdropFilter:'blur(8px)',
              transition:'all 200ms cubic-bezier(0.16,1,0.3,1)',
            }}
            onMouseEnter={e => { e.currentTarget.style.color='#fff'; e.currentTarget.style.borderColor='rgba(255,255,255,0.32)' }}
            onMouseLeave={e => { e.currentTarget.style.color='rgba(255,255,255,0.72)'; e.currentTarget.style.borderColor='rgba(255,255,255,0.18)' }}
          >
            <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
              <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
            </svg>
            View on GitHub
          </a>
        </div>

        {/* Stats bar */}
        <div
          className="hero-enter"
          style={{
            animationDelay:'0.54s',
            display:'grid',
            gridTemplateColumns:`repeat(${STATS.length}, 1fr)`,
            border:'1px solid rgba(163,163,163,0.25)',
            borderRadius:16,
            overflow:'hidden',
            background:'rgba(39,39,42,0.45)',
            backdropFilter:'blur(12px)',
            width:'100%', maxWidth:600,
          }}
        >
          {STATS.map((s, i) => (
            <div
              key={s.num}
              style={{
                display:'flex', flexDirection:'column', alignItems:'center',
                padding:'18px 14px',
                borderLeft: i !== 0 ? '1px solid rgba(255,255,255,0.08)' : 'none',
              }}
            >
              <span style={{
                fontSize:'clamp(1.2rem,2.4vw,1.55rem)',
                fontWeight:900, letterSpacing:'-0.05em', lineHeight:1,
                color:'#ffffff', marginBottom:4,
              }}>{s.num}</span>
              <span style={{
                fontSize:'0.72rem', fontWeight:500,
                color:'rgba(212,212,216,0.78)',
                textAlign:'center',
              }}>{s.lbl}</span>
            </div>
          ))}
        </div>

        {/* Metadata row */}
        <div
          className="hero-enter"
          style={{
            animationDelay:'0.62s',
            marginTop:32,
            display:'flex', flexWrap:'wrap', gap:20,
            justifyContent:'center', alignItems:'center',
          }}
        >
          {[
            { label:'Team', value:'Francis Daniel, Marc Parubrub, Veeny Bautista' },
            { label:'Track', value:'Apps for Your Life' },
            { label:'Built with', value:'Codex · GPT-5.6' },
          ].map(m => (
            <div key={m.label} style={{ display:'flex', flexDirection:'column', alignItems:'center', gap:2 }}>
              <span style={{ fontSize:'0.76rem', fontWeight:700, letterSpacing:'0.10em', textTransform:'uppercase', color:'rgba(212,212,216,0.62)' }}>{m.label}</span>
              <span style={{ fontSize:'0.9rem', fontWeight:600, color:'rgba(228,228,231,0.88)' }}>{m.value}</span>
            </div>
          ))}
        </div>

      </div>

      {/* App screenshot strip below fold */}
      <div style={{
        position:'relative', zIndex:2,
        width:'100%', maxWidth:1100,
        margin:'0 auto',
        padding:'0 32px 80px',
      }}>
        {/* Floating chips */}
        <div className="chip-f1" style={{
          position:'absolute', top:32, right:16, zIndex:10,
          display:'flex', alignItems:'center', gap:6,
          border:'1px solid rgba(163,163,163,0.24)', borderRadius:12,
          padding:'8px 14px', fontSize:'0.82rem', fontWeight:700,
          color:'rgba(244,244,245,0.95)',
          background:'rgba(39,39,42,0.72)', backdropFilter:'blur(12px)',
        }}>
          <span style={{ width:6, height:6, borderRadius:'50%', background:'#22c55e' }} />
          On-device tracking
        </div>
        <div className="chip-f2" style={{
          position:'absolute', top:100, left:0, zIndex:10,
          display:'flex', alignItems:'center', gap:6,
          border:'1px solid rgba(163,163,163,0.24)', borderRadius:12,
          padding:'8px 14px', fontSize:'0.82rem', fontWeight:700,
          color:'rgba(244,244,245,0.95)',
          background:'rgba(39,39,42,0.72)', backdropFilter:'blur(12px)',
        }}>
          <svg width="11" height="11" viewBox="0 0 24 24" fill="#c084fc" aria-hidden="true">
            <path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 3.2a2.3 2.3 0 1 1 0 4.6 2.3 2.3 0 0 1 0-4.6zm0 13.6c-1.9 0-3.6-.97-4.6-2.44.02-1.53 3.07-2.37 4.6-2.37s4.58.84 4.6 2.37A5.49 5.49 0 0 1 12 18.8z"/>
          </svg>
          GPT-5.6 tool calling
        </div>
        <div className="chip-f3" style={{
          position:'absolute', bottom:120, right:0, zIndex:10,
          display:'flex', alignItems:'center', gap:6,
          border:'1px solid rgba(163,163,163,0.24)', borderRadius:12,
          padding:'8px 14px', fontSize:'0.82rem', fontWeight:700,
          color:'rgba(244,244,245,0.95)',
          background:'rgba(39,39,42,0.72)', backdropFilter:'blur(12px)',
        }}>
          <span style={{ width:6, height:6, borderRadius:'50%', background:'#fbbf24' }} />
          Kill switch armed
        </div>

        <div style={{
          position:'relative',
          borderRadius:20,
          overflow:'hidden',
          border:'1px solid rgba(255,255,255,0.09)',
          boxShadow:'0 0 80px rgba(255,255,255,0.04), 0 40px 100px rgba(0,0,0,0.6)',
        }}>
          <ImagePlaceholder
            src="/screenshots/heroimage.png"
            label="MITSU debug overlay — live hand landmarks, gesture state, pointer coordinates"
            alt="MITSU debug overlay showing live hand landmarks, gesture state, and physical-pixel pointer coordinates"
            aspect="16/9"
          />
        </div>
      </div>

      {/* Scroll cue */}
      <div style={{
        position:'relative', zIndex:2,
        display:'flex', flexDirection:'column', alignItems:'center',
        gap:6, paddingBottom:24, opacity:0.28,
      }}>
        <div style={{ width:1, height:32, background:'rgba(255,255,255,0.5)' }} />
        <span style={{ fontSize:'0.78rem', fontWeight:600, letterSpacing:'0.16em', textTransform:'uppercase', color:'rgba(228,228,231,0.75)' }}>Scroll</span>
      </div>
    </section>
  )
}
