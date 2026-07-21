import { useState, useEffect } from 'react'
import { Reveal } from '../hooks/useScrollReveal.jsx'
import ImagePlaceholder from './shared/ImagePlaceholder'

const STEPS = [
  {
    n:'01', name:'Capture', sub:'Webcam frame grab', tech:'OpenCV', color:'#38bdf8',
    icon:(
      <svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2" y="5" width="16" height="11" rx="2.5"/><circle cx="10" cy="10.5" r="3"/><path d="M7 5l1.2-2h3.6L13 5"/>
      </svg>
    ),
  },
  {
    n:'02', name:'Landmark', sub:'21 3D hand points', tech:'MediaPipe', color:'#38bdf8',
    icon:(
      <svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        <path d="M10 17V9M10 9V4.5M7 17v-6M13 17v-6M4.5 13.5 7 11M15.5 13.5 13 11"/>
        <circle cx="10" cy="3.4" r="1.2"/><circle cx="7" cy="9.8" r="1.2"/><circle cx="13" cy="9.8" r="1.2"/>
      </svg>
    ),
  },
  {
    n:'03', name:'Smooth', sub:'Speed-adaptive filter', tech:'One Euro', color:'#60a5fa',
    icon:(
      <svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        <path d="M2 14c2-6 4 4 6-2s4 4 6-3 2 1 4 1"/>
      </svg>
    ),
  },
  {
    n:'04', name:'Classify', sub:'Grip, pointer, swipe', tech:'State machine', color:'#a78bfa',
    icon:(
      <svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="5" cy="5" r="2.4"/><circle cx="15" cy="5" r="2.4"/><circle cx="15" cy="15" r="2.4"/>
        <path d="M7.4 5H12.6M15 7.4v5.2"/>
      </svg>
    ),
  },
  {
    n:'05', name:'Resolve', sub:'Which window, which screen', tech:'Win32 hit-test', color:'#34d399',
    icon:(
      <svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="9" cy="9" r="5.4"/><path d="M13 13l4 4"/>
      </svg>
    ),
  },
  {
    n:'06', name:'Act', sub:'Move, restore, maximize', tech:'SetWindowPos', color:'#34d399',
    icon:(
      <svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2.5" y="4" width="9" height="7" rx="1.5"/><path d="M12 14.5h5.5M15 12l2.5 2.5L15 17"/>
      </svg>
    ),
  },
]

export default function Workflow() {
  const [active, setActive] = useState(0)

  useEffect(() => {
    const t = setInterval(() => setActive(p => (p + 1) % STEPS.length), 1400)
    return () => clearInterval(t)
  }, [])

  return (
    <section id="solution" className="relative py-32 z-10" style={{ background:'#050505' }}>
      <div className="max-w-[1100px] mx-auto px-8">

        <Reveal>
          <p className="micro-label font-bold uppercase text-zinc-300/90 mb-5">How It Works</p>
        </Reveal>
        <Reveal delay={1}>
          <h2 className="font-black tracking-[-0.04em] leading-none text-white mb-4"
              style={{ fontSize:'clamp(2.4rem,5vw,4rem)' }}>
            One camera frame.<br/>
            <span style={{ color:'rgba(228,228,231,0.48)' }}>One window, moved.</span>
          </h2>
        </Reveal>
        <Reveal delay={2}>
          <p className="text-zinc-100/85 text-[1.03rem] leading-relaxed mb-8 max-w-2xl">
            Capture &rarr; landmark &rarr; smooth &rarr; classify &rarr; resolve &rarr; act.
            Every stage runs on your machine, and the whole loop closes before you perceive lag.
          </p>
        </Reveal>

        <Reveal delay={3}>
          <div className="glass-panel rounded-2xl p-4 mb-8">
            <div className="flow-lane mb-2">
              <span className="flow-pulse" />
              <span className="flow-pulse delay-1" />
              <span className="flow-pulse delay-2" />
            </div>
            <div className="small-copy text-zinc-200/80 text-center">
              Continuous loop from webcam frame to Win32 window position. No network hop on this path.
            </div>
          </div>
        </Reveal>

        {/* Animated pipeline */}
        <Reveal delay={4}>
          <div className="glass-panel rounded-2xl p-2 mb-12 overflow-auto">
            <div className="flex items-stretch min-w-[680px]">
              {STEPS.map((s, i) => (
                <div key={s.n} className="flex-1 flex items-center">
                  <div className="flex-1 flex flex-col items-center text-center px-3 py-7 relative">
                    {/* Connecting line left */}
                    {i > 0 && (
                      <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1/2 h-px bg-zinc-500/30"
                        style={i <= active ? { background:'rgba(228,228,231,0.9)', boxShadow:'0 0 8px rgba(228,228,231,0.38)', transition:'all .45s ease' } : {}} />
                    )}
                    {/* Connecting line right */}
                    {i < STEPS.length - 1 && (
                      <div className="absolute right-0 top-1/2 -translate-y-1/2 w-1/2 h-px bg-zinc-500/30"
                        style={i < active ? { background:'rgba(228,228,231,0.9)', boxShadow:'0 0 8px rgba(228,228,231,0.38)', transition:'all .45s ease' } : {}} />
                    )}
                    {/* Node circle */}
                    <div className={`relative z-10 w-12 h-12 rounded-full border flex items-center justify-center mb-3 transition-all duration-300 ${
                      i === active
                        ? 'pipe-node-active text-white'
                        : i < active
                          ? 'pipe-node-passed text-zinc-200'
                          : 'border-zinc-500/45 text-zinc-400'
                    }`}
                      style={
                        i === active
                          ? { background:'rgba(212,212,216,0.16)', borderColor:'rgba(212,212,216,0.9)', boxShadow:'0 0 22px rgba(212,212,216,0.35), 0 0 60px rgba(212,212,216,0.1)' }
                          : i < active
                            ? { borderColor:'rgba(161,161,170,0.55)', background:'rgba(161,161,170,0.12)' }
                            : {}
                      }>
                      <span style={{ color: s.color }}>{s.icon}</span>
                    </div>
                    <div className={`text-[0.84rem] font-bold tracking-wide mb-1 transition-colors duration-300 ${i === active ? 'text-white' : 'text-zinc-300/80'}`}>{s.n}</div>
                    <div className={`text-[0.96rem] font-bold mb-1.5 transition-colors duration-300 ${i === active ? 'text-white' : 'text-zinc-200/90'}`}>{s.name}</div>
                    <div className={`text-[0.84rem] font-medium transition-colors duration-300 ${i === active ? 'text-zinc-100/90' : 'text-zinc-300/70'}`}>{s.sub}</div>
                    <div className={`text-[0.82rem] font-semibold mt-2 px-2 py-0.5 rounded border transition-all duration-300 ${
                      i === active
                        ? 'border-zinc-300/50 text-zinc-100/90 bg-zinc-400/20'
                        : 'border-zinc-500/45 text-zinc-300/75 bg-transparent'
                    }`}>{s.tech}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </Reveal>

        {/* Workflow screenshot */}
        <Reveal delay={5}>
          <ImagePlaceholder
            src="/screenshots/workflow.png"
            label="Full loop — camera overlay, gesture state readout, and the window mid-glide"
            alt="MITSU running: camera overlay with landmarks, gesture state readout, and a window mid-glide between monitors"
          />
        </Reveal>

      </div>
    </section>
  )
}
