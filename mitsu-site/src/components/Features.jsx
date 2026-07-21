import { Reveal } from '../hooks/useScrollReveal.jsx'
import ImagePlaceholder from './shared/ImagePlaceholder'

/* ── Animated cross-monitor glide diagram ── */
function CrossMonitorDiagram() {
  return (
    <div className="rounded-xl border border-zinc-500/40 p-5 mb-5" style={{ background:'#050505' }}>
      <div className="text-[0.72rem] font-bold tracking-[0.1em] uppercase text-zinc-300/70 mb-4">
        Combined virtual desktop — one coordinate space
      </div>
      <svg viewBox="0 0 300 96" className="w-full" role="img" aria-label="A window gliding from the right monitor to the left monitor across one continuous coordinate space">
        {/* Left monitor — laptop, high DPI */}
        <rect x="6" y="14" width="120" height="72" rx="4" fill="rgba(255,255,255,0.03)" stroke="rgba(161,161,170,0.45)" strokeWidth="1.2"/>
        <text x="66" y="94" textAnchor="middle" fill="rgba(161,161,170,0.85)" fontSize="7" fontWeight="600">2560 × 1600 · 150%</text>

        {/* Right monitor — external, primary */}
        <rect x="174" y="20" width="120" height="60" rx="4" fill="rgba(255,255,255,0.03)" stroke="rgba(161,161,170,0.45)" strokeWidth="1.2"/>
        <text x="234" y="94" textAnchor="middle" fill="rgba(161,161,170,0.85)" fontSize="7" fontWeight="600">1920 × 1080 · 100%</text>

        {/* Physical gap */}
        <line x1="126" y1="50" x2="174" y2="50" stroke="rgba(161,161,170,0.28)" strokeWidth="1" strokeDasharray="3 3"/>
        <text x="150" y="46" textAnchor="middle" fill="rgba(161,161,170,0.7)" fontSize="6.5">gap</text>

        {/* The gliding window */}
        <g className="window-glide">
          <rect x="20" y="30" width="52" height="34" rx="3" fill="rgba(74,222,128,0.14)" stroke="rgba(74,222,128,0.75)" strokeWidth="1.3"/>
          <rect x="20" y="30" width="52" height="7" rx="3" fill="rgba(74,222,128,0.3)"/>
          <circle cx="25" cy="33.5" r="1.2" fill="rgba(226,232,240,0.8)"/>
          <circle cx="29" cy="33.5" r="1.2" fill="rgba(226,232,240,0.55)"/>
          <circle cx="33" cy="33.5" r="1.2" fill="rgba(226,232,240,0.55)"/>
        </g>
      </svg>
    </div>
  )
}

const SMALL_CARDS = [
  {
    tag: 'Pointer',
    tone: 'text-cyan-200 border-cyan-300/35 bg-cyan-400/15',
    title: 'Physical-pixel cursor',
    sub: 'Hold index and middle fingertips together to drive the cursor. Dip both to click.',
    stat: '1:1',
    statSub: 'physical pixel mapping',
    icon: (
      <svg width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        <path d="M4 3l5.2 13 2-5.2 5.2-2z"/>
      </svg>
    ),
  },
  {
    tag: 'Navigation',
    tone: 'text-violet-200 border-violet-300/35 bg-violet-400/15',
    title: 'Back and forward',
    sub: 'Pointer pose plus a raised pinky goes back; a raised ring finger goes forward.',
    stat: '2',
    statSub: 'browser gestures',
    icon: (
      <svg width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        <path d="M8 4 3 10l5 6M12 4l5 6-5 6"/>
      </svg>
    ),
  },
  {
    tag: 'Fail-safe',
    tone: 'text-amber-200 border-amber-300/35 bg-amber-400/15',
    title: 'Global kill switch',
    sub: 'Ctrl + Alt + Shift + M halts every automated window action instantly.',
    stat: '1 key',
    statSub: 'to stop everything',
    icon: (
      <svg width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="10" cy="10" r="7"/><path d="M10 6v4.5"/><circle cx="10" cy="13.6" r="0.4" fill="currentColor"/>
      </svg>
    ),
  },
]

export default function Features() {
  return (
    <section id="features" className="relative py-32 z-10 overflow-hidden" style={{ background:'#050505' }}>
      <div className="max-w-[1100px] mx-auto px-8">

        <Reveal><p className="micro-label font-bold uppercase text-zinc-300/90 mb-5">Features</p></Reveal>
        <Reveal delay={1}>
          <h2 className="font-black tracking-[-0.04em] leading-none text-white mb-14"
              style={{ fontSize:'clamp(2.4rem,5vw,4rem)' }}>
            Windows as physical objects.
          </h2>
        </Reveal>

        {/* Row 1: Cross-monitor drag (large) + Voice target lock */}
        <div className="grid grid-cols-1 lg:grid-cols-[7fr_5fr] gap-3 mb-3">
          <Reveal delay={1}>
            <div className="glass-panel rounded-2xl p-7 hover:border-zinc-300/45 transition-all duration-300 h-full">
              <div className="w-10 h-10 rounded-xl border border-emerald-300/35 flex items-center justify-center mb-5 text-emerald-200"
                   style={{ background:'rgba(16,185,129,0.16)' }}>
                <svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="2" y="4" width="8" height="7" rx="1.5"/><rect x="11" y="8" width="7" height="6" rx="1.5"/><path d="M8 14.5h4"/>
                </svg>
              </div>
              <span className="text-[0.82rem] font-bold tracking-[0.10em] uppercase text-emerald-200/95 mb-2 block">Cross-monitor drag</span>
              <div className="text-[0.96rem] font-bold text-white mb-2">Pinch a window, slide your hand, and it crosses the physical gap between screens.</div>
              <div className="small-copy text-zinc-100/85 mb-5">
                Not snap-to-position. Continuous motion across the whole virtual desktop, with velocity
                gain so a 3000-pixel journey does not require reaching off-camera.
              </div>

              <CrossMonitorDiagram />

              <div className="rounded-xl p-4 font-mono text-[0.82rem] leading-7 mb-5 border border-zinc-500/45"
                   style={{ background:'#050505' }}>
                <span className="code-cm">{'# Movement is clamped against the COMBINED box'}</span><br/>
                <span className="code-kw">bounds</span><span className="code-tx"> = </span><span className="code-tx">virtual_desktop_bounds(monitors)</span><br/>
                <span className="code-kw">target</span><span className="code-tx"> = </span><span className="code-tx">clamp(origin + delta * </span><span className="code-nu">gain</span><span className="code-tx">, bounds)</span><br/>
                <span className="code-cm">{'# crossing monitors is not a special case'}</span>
              </div>

              <ImagePlaceholder
                src="/screenshots/crossdrag.png"
                label="Window mid-glide between the laptop and external display"
                alt="A window mid-glide between the laptop display and the external monitor"
              />
            </div>
          </Reveal>

          <Reveal delay={2}>
            <div className="glass-panel rounded-2xl p-7 hover:border-zinc-300/45 transition-all duration-300 h-full">
              <div className="w-10 h-10 rounded-xl border border-cyan-300/35 flex items-center justify-center mb-5 text-cyan-200"
                   style={{ background:'rgba(34,211,238,0.16)' }}>
                <svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="7" y="2" width="6" height="10" rx="3"/><path d="M10 16v-3"/><path d="M5 11a5 5 0 0 0 10 0"/>
                </svg>
              </div>
              <span className="text-[0.82rem] font-bold tracking-[0.10em] uppercase text-cyan-200/95 mb-2 block">Voice target-lock</span>
              <div className="text-[0.96rem] font-bold text-white mb-2">Name a buried window and it becomes the drag target.</div>
              <div className="small-copy text-zinc-100/85 mb-5">
                Occlusion stops mattering. Say the app name and MITSU locks on regardless of z-order,
                then your hand moves it — or your voice finishes the command with a destination.
              </div>
              <div className="font-black tracking-[-0.07em] leading-none text-white mb-1" style={{ fontSize:'3.4rem' }}>3</div>
              <div className="text-[0.84rem] font-medium text-zinc-200/80 mb-5">
                behaviours from one state machine: hand-only, voice-lock-plus-hand, voice-only
              </div>

              <div className="flex flex-col gap-2 mb-5">
                {[
                  'show Discord on the left screen',
                  'grab VS Code',
                  'open Paint',
                ].map(cmd => (
                  <div key={cmd} className="flex items-center gap-2.5 rounded-lg border border-zinc-500/40 px-3 py-2"
                       style={{ background:'rgba(255,255,255,0.02)' }}>
                    <svg width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="rgba(103,232,249,0.9)" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                      <path d="M2 8h9M8 4.5 11.5 8 8 11.5"/>
                    </svg>
                    <span className="font-mono text-[0.8rem] text-zinc-100/88">{cmd}</span>
                  </div>
                ))}
              </div>

              <ImagePlaceholder
                src="/screenshots/shelf.png"
                label="V-sign shelf — minimized windows brought back into reach"
                alt="The V-sign shelf listing minimized windows ready to be selected"
              />
            </div>
          </Reveal>
        </div>

        {/* Row 2: 3 small cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3">
          {SMALL_CARDS.map((c, i) => (
            <Reveal key={c.tag} delay={i + 1}>
              <div className="glass-panel rounded-2xl p-6 hover:border-zinc-300/45 transition-all duration-300 h-full">
                <div className={`w-9 h-9 rounded-xl border flex items-center justify-center mb-4 ${c.tone}`}>{c.icon}</div>
                <span className="text-[0.82rem] font-bold tracking-[0.10em] uppercase text-zinc-200/92 mb-1.5 block">{c.tag}</span>
                <div className="text-[0.90rem] font-bold text-white mb-1.5">{c.title}</div>
                <div className="small-copy text-zinc-100/85 mb-4">{c.sub}</div>
                <div className="font-black tracking-[-0.06em] leading-none text-white mb-1" style={{ fontSize:'2.4rem' }}>{c.stat}</div>
                <div className="text-[0.84rem] font-medium text-zinc-200/85">{c.statSub}</div>
              </div>
            </Reveal>
          ))}
        </div>

        {/* Row 3: Window state + Mic picker */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {[
            {
              tag: 'Window state',
              title: 'Minimized is not a special case',
              sub: 'A minimized window still has a handle. MITSU restores before moving, so show and move behave identically no matter where the window started.',
              src: '/screenshots/overlay.png',
              alt: 'Debug overlay showing gesture state and window handle resolution',
            },
            {
              tag: 'Input devices',
              title: 'Pick your microphone, mid-run',
              sub: 'A native Qt selector lists every input device. Choosing one swaps the active mic in memory for the current session, without restarting the loop.',
              src: '/screenshots/micpicker.png',
              alt: 'Native microphone selector listing available input devices',
            },
          ].map((c, i) => (
            <Reveal key={c.tag} delay={i + 1}>
              <div className="glass-panel rounded-2xl p-7 hover:border-zinc-300/45 transition-all duration-300 h-full">
                <span className="text-[0.82rem] font-bold tracking-[0.10em] uppercase text-zinc-300/85 mb-2 block">{c.tag}</span>
                <div className="text-[0.96rem] font-bold text-white mb-2">{c.title}</div>
                <div className="small-copy text-zinc-100/85 mb-5">{c.sub}</div>
                <ImagePlaceholder src={c.src} label={c.title} alt={c.alt} />
              </div>
            </Reveal>
          ))}
        </div>

      </div>
    </section>
  )
}
