import { Reveal } from '../hooks/useScrollReveal.jsx'

const PHASES = [
  {
    num: '1',
    phase: 'Phase 1',
    when: 'Shipped · Jul 2026',
    color: '#4ade80',
    border: 'rgba(74,222,128,0.32)',
    bg: 'rgba(74,222,128,0.07)',
    glow: 'rgba(74,222,128,0.7)',
    done: true,
    title: 'Hand-and-voice window control on Windows',
    items: [
      'Cross-monitor drag over a mixed-DPI virtual desktop',
      'Pointer, two-fingertip click, back/forward, minimize, maximize',
      'V-sign shelf for restoring minimized windows',
      'Push-to-talk voice with a fixed command grammar',
      'GPT-5.6 tool reasoning behind a circuit breaker',
      '100 automated tests, kill switch, pinned model hash',
    ],
  },
  {
    num: '2',
    phase: 'Phase 2',
    when: 'Q4 2026 — Q1 2027',
    color: '#60a5fa',
    border: 'rgba(96,165,250,0.32)',
    bg: 'rgba(96,165,250,0.07)',
    glow: 'rgba(96,165,250,0.65)',
    done: false,
    title: 'Ship as a product, not a prototype',
    items: [
      'Signed installer and auto-update — the real adoption blocker today',
      'Tray icon, first-run calibration, and a Qt settings panel',
      'Two-hand pinch-spread resize and flick-to-snap',
      'Focus Mode — two named windows stay, the rest minimize',
      'Per-app saved layouts persisted in SQLite',
      'Pro licence at $29, benchmarked to DisplayFusion',
    ],
  },
  {
    num: '3',
    phase: 'Phase 3',
    when: 'H2 2027',
    color: '#c084fc',
    border: 'rgba(192,132,252,0.32)',
    bg: 'rgba(192,132,252,0.07)',
    glow: 'rgba(192,132,252,0.65)',
    done: false,
    title: 'Accessibility credibility and platform reach',
    items: [
      'Accessibility conformance work and procurement documentation',
      'macOS backend behind the same four-tool layer',
      'Cross-device handoff — toss a window at another machine',
      'Managed cloud tier for users without their own API key',
      'Per-seat team licensing against accessibility budgets',
      'Privacy guard — auto-blur when a second face enters frame',
    ],
  },
]

const IMPACT = [
  {
    label: 'Scalability',
    color: '#4ade80',
    title: 'There is no backend to scale',
    body: 'Perception and action run on the user machine, so the free tier has no per-user server cost at any volume. Growth is a distribution problem, not an infrastructure bill — which is exactly why the local tier can stay free permanently.',
  },
  {
    label: 'Impact',
    color: '#60a5fa',
    title: 'A health outcome, not a convenience',
    body: 'Around 9% of US adults report a repetitive strain injury in any three-month period, musculoskeletal problems account for roughly 30% of all sick days, and carpal tunnel alone averages 27 lost workdays. Every window move that skips the mouse is load removed from a wrist.',
  },
  {
    label: 'Moat',
    color: '#c084fc',
    title: 'The fusion is the hard part',
    body: 'Bolting voice onto a gesture tool is a weekend. A single state machine where a spoken app name injects directly into the grip state is an architectural head start. Talon showed a free, capable core is what earns the community that later sustains a paid tier.',
  },
]

const HONEST_RISKS = [
  {
    title: 'Windows-only, by choice',
    body: 'The Win32 layer is deliberate and shallow — four typed tools — but a macOS backend is real work, not a recompile.',
  },
  {
    title: 'Lighting and occlusion are real',
    body: 'Webcam hand tracking degrades in poor light and when fingers overlap. Calibration helps; it does not eliminate the failure mode.',
  },
  {
    title: 'The installer is the blocker',
    body: 'Today MITSU needs Python 3.11 and a terminal. Until that is a signed installer, adoption is capped at developers.',
  },
]

export default function Roadmap() {
  return (
    <section id="roadmap" className="relative py-32 z-10 overflow-hidden" style={{ background: '#050505' }}>
      <div className="absolute inset-0 pointer-events-none"
           style={{ background: 'radial-gradient(ellipse 60% 40% at 50% 0%, rgba(255,255,255,0.025) 0%, transparent 70%)' }} />

      <div className="max-w-[1100px] mx-auto px-8 relative z-10">

        <Reveal>
          <p className="micro-label font-bold uppercase text-zinc-300/90 mb-5">Future Prospects</p>
        </Reveal>
        <Reveal delay={1}>
          <h2 className="font-black tracking-[-0.04em] leading-none text-white mb-5"
              style={{ fontSize: 'clamp(2.4rem,5vw,4rem)' }}>
            Scalability &amp; impact roadmap.<br/>
            <span className="text-zinc-300/55">From one desk to every desk.</span>
          </h2>
        </Reveal>
        <Reveal delay={2}>
          <p className="text-zinc-100/85 text-[1.03rem] leading-relaxed max-w-3xl mb-4">
            MITSU works today. The tool layer it acts through is deliberately small and typed, which is
            what makes new gestures and new platforms additive rather than structural rewrites.
          </p>
        </Reveal>
        <Reveal delay={2}>
          <p className="small-copy text-zinc-300/72 max-w-3xl mb-14">
            Phase 2 leads with packaging rather than features on purpose. The single biggest thing
            standing between MITSU and its 10.2M beachhead is that installing it currently requires
            Python and a terminal.
          </p>
        </Reveal>

        {/* Horizontal timeline + phase cards */}
        <Reveal delay={3}>
          <div className="relative mb-6">
            {/* Timeline track */}
            <div className="relative flex items-start justify-between mb-8">
              <div
                className="absolute hidden md:block"
                style={{
                  top: 20, left: 'calc(16.5% + 4px)', right: 'calc(16.5% + 4px)',
                  height: 2,
                  background: 'linear-gradient(90deg, #4ade80 0%, #60a5fa 50%, #c084fc 100%)',
                  zIndex: 1,
                }}
              />

              {PHASES.map((p) => (
                <div key={p.phase} className="flex flex-col items-center gap-3" style={{ flex: 1 }}>
                  <div
                    className="relative z-10 flex items-center justify-center rounded-full font-black"
                    style={{
                      width: 40, height: 40,
                      background: p.done ? p.color : '#111',
                      border: `2px solid ${p.color}`,
                      boxShadow: `0 0 22px ${p.glow}`,
                      color: p.done ? '#050505' : p.color,
                      fontSize: '1rem',
                    }}
                  >
                    {p.done ? (
                      <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="#050505" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                        <path d="M3.5 9l4 4 7-7"/>
                      </svg>
                    ) : p.num}
                  </div>
                  <div className="text-center">
                    <div className="text-[0.64rem] font-bold tracking-[0.14em] uppercase" style={{ color: p.color }}>{p.phase}</div>
                    <div className="text-[0.68rem] font-medium text-zinc-300/60 whitespace-nowrap">{p.when}</div>
                  </div>
                </div>
              ))}
            </div>

            {/* Phase cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {PHASES.map((p) => (
                <div
                  key={p.phase}
                  className="rounded-2xl p-6 flex flex-col gap-4"
                  style={{ border: `1px solid ${p.border}`, background: p.bg }}
                >
                  <div className="text-[1rem] font-bold text-zinc-50">{p.title}</div>
                  <ul className="flex flex-col gap-2.5">
                    {p.items.map((item, j) => (
                      <li key={j} className="flex items-start gap-2.5">
                        <svg className="flex-shrink-0 mt-[3px]" width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true">
                          <circle cx="6.5" cy="6.5" r="6" stroke={p.color} strokeWidth="1" strokeOpacity="0.5"/>
                          <path d="M4 6.5 5.5 8 9 4.5" stroke={p.color} strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                        <span className="text-[0.78rem] text-zinc-200/78 leading-relaxed">{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        </Reveal>

        {/* Impact summary */}
        <Reveal delay={4}>
          <div className="rounded-2xl border border-zinc-500/35 bg-zinc-900/30 overflow-hidden mb-6">
            <div className="grid grid-cols-1 md:grid-cols-3 divide-y md:divide-y-0 md:divide-x divide-zinc-500/30">
              {IMPACT.map((item) => (
                <div key={item.label} className="p-7">
                  <div
                    className="text-[0.65rem] font-bold tracking-[0.14em] uppercase mb-3"
                    style={{ color: item.color }}
                  >
                    {item.label}
                  </div>
                  <div className="text-[0.96rem] font-bold text-zinc-50 mb-2">{item.title}</div>
                  <div className="small-copy text-zinc-200/75 leading-relaxed">{item.body}</div>
                </div>
              ))}
            </div>
          </div>
        </Reveal>

        {/* Known limits */}
        <Reveal delay={2}>
          <div className="glass-panel rounded-2xl p-7">
            <div className="text-[0.76rem] font-bold tracking-[0.1em] uppercase text-zinc-300/85 mb-2">
              What stands in the way
            </div>
            <p className="small-copy text-zinc-100/78 mb-6 max-w-2xl">
              A roadmap that lists only wins is a wishlist. These are the three constraints that
              actually govern how fast the phases above can land.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {HONEST_RISKS.map((r, i) => (
                <div key={r.title} className="relative pl-5">
                  <span className="absolute left-0 top-1 font-mono text-[0.72rem] text-zinc-500/80 tabular-nums">
                    {String(i + 1).padStart(2, '0')}
                  </span>
                  <div className="text-[0.9rem] font-bold text-zinc-50 mb-1.5">{r.title}</div>
                  <div className="text-[0.8rem] text-zinc-200/75 leading-relaxed">{r.body}</div>
                </div>
              ))}
            </div>
          </div>
        </Reveal>

      </div>
    </section>
  )
}
