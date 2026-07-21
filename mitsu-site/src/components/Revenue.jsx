import { Reveal } from '../hooks/useScrollReveal.jsx'

const STREAMS = [
  {
    n: '01',
    tag: 'Free — local',
    color: '#22d3ee',
    border: 'rgba(34,211,238,0.3)',
    bg: 'rgba(34,211,238,0.07)',
    headerBg: 'linear-gradient(135deg,rgba(34,211,238,0.2) 0%,rgba(34,211,238,0.06) 100%)',
    title: 'The whole local app, free forever',
    body: 'Every gesture, the pointer, the shelf, and the fixed voice grammar. It runs entirely on the user machine, so it costs nothing to serve and there is no honest reason to gate it. Talon Voice proved a free core builds the community that later monetises.',
    stat: '$0',
    statSub: 'zero marginal cost',
    bullets: [
      'Cross-monitor drag and the full gesture set',
      'Voice commands with your own OpenAI key',
      'No backend, so growth costs nothing to serve',
    ],
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#22d3ee" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2.5" y="4" width="19" height="13" rx="2.5"/><path d="M8 20.5h8M12 17v3.5"/>
      </svg>
    ),
  },
  {
    n: '02',
    tag: 'Pro — one-time',
    color: '#c084fc',
    border: 'rgba(192,132,252,0.3)',
    bg: 'rgba(192,132,252,0.07)',
    headerBg: 'linear-gradient(135deg,rgba(192,132,252,0.2) 0%,rgba(192,132,252,0.06) 100%)',
    title: 'A lifetime licence, priced against the category',
    body: 'DisplayFusion Pro — the closest commercial comparable — sells at $25 direct and $39.99 on Steam as a perpetual licence. A subscription for a window manager is a hard sell, so Pro follows the category convention rather than fighting it.',
    stat: '$29',
    statSub: 'one-time, perpetual',
    bullets: [
      'Two-hand resize, flick-to-snap, toss physics',
      'Focus Mode and saved per-app layouts',
      'Benchmarked to DisplayFusion at $25 lifetime',
    ],
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#c084fc" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 2.5 15 8.7l6.8 1-4.9 4.8 1.2 6.8-6.1-3.2-6.1 3.2 1.2-6.8L2.2 9.7l6.8-1z"/>
      </svg>
    ),
  },
  {
    n: '03',
    tag: 'Managed cloud & teams',
    color: '#fbbf24',
    border: 'rgba(251,191,36,0.3)',
    bg: 'rgba(251,191,36,0.07)',
    headerBg: 'linear-gradient(135deg,rgba(251,191,36,0.2) 0%,rgba(251,191,36,0.06) 100%)',
    title: 'The only tier with a real recurring cost',
    body: 'Cloud reasoning burns tokens on every call, so it is the one part that genuinely warrants a subscription. Teams buying MITSU as an RSI and accessibility measure license it per seat — assistive technology is a $26–30B market in 2026.',
    stat: '$6',
    statSub: '/ month, optional',
    bullets: [
      'Managed GPT-5.6 access with no API key setup',
      'Priced to cover token cost plus margin, not to rent the app',
      'Per-seat licensing for accessibility procurement',
    ],
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fbbf24" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        <path d="M6.5 18.5a4.5 4.5 0 0 1-.6-8.96 6 6 0 0 1 11.5-1.3A4.25 4.25 0 0 1 18 18.5z"/><path d="M12 11.5v5M9.75 13.75 12 11.5l2.25 2.25"/>
      </svg>
    ),
  },
]

const BENCHMARK = [
  { name: 'Windows Voice Access', price: 'Free',        model: 'Built into the OS',      note: 'Voice only, no gesture input' },
  { name: 'Talon Voice',          price: 'Free',        model: '$25/mo Patreon for beta', note: 'Free core built the community' },
  { name: 'DisplayFusion Pro',    price: '$25',         model: 'Perpetual licence',       note: 'Closest commercial comparable' },
  { name: 'MITSU Pro',            price: '$29',         model: 'Perpetual licence',       note: 'Gesture + voice + window relocation', us: true },
]

const JOURNEY = [
  { label: 'Free local user',  color: '#22d3ee', sub: 'Gesture + grammar' },
  { label: 'Pro licence',      color: '#c084fc', sub: '$29 one-time' },
  { label: 'Managed cloud',    color: '#4ade80', sub: '$6 / month' },
  { label: 'Team seats',       color: '#fbbf24', sub: 'Accessibility budget' },
]

export default function Revenue() {
  return (
    <section id="revenue" className="relative py-32 z-10 overflow-hidden" style={{ background: '#070707' }}>
      {/* subtle top glow */}
      <div className="absolute inset-0 pointer-events-none"
           style={{ background: 'radial-gradient(ellipse 55% 35% at 50% 0%, rgba(251,191,36,0.06) 0%, transparent 70%)' }} />

      <div className="max-w-[1100px] mx-auto px-8 relative z-10">

        <Reveal>
          <p className="micro-label font-bold uppercase text-zinc-300/90 mb-5">Business Model</p>
        </Reveal>
        <Reveal delay={1}>
          <h2 className="font-black tracking-[-0.04em] leading-none text-white mb-5"
              style={{ fontSize: 'clamp(2.4rem,5vw,4rem)' }}>
            The paid line is<br/>
            <span className="text-zinc-300/55">the architecture line.</span>
          </h2>
        </Reveal>
        <Reveal delay={2}>
          <p className="text-zinc-100/85 text-[1.03rem] leading-relaxed max-w-3xl mb-4">
            MITSU already separates local reflexes from cloud cognition for engineering reasons. That
            same boundary is the honest free-versus-paid split: the local tier costs nothing to serve
            because it never leaves the device, and the cloud tier is the only part with a real
            recurring cost.
          </p>
        </Reveal>
        <Reveal delay={2}>
          <p className="small-copy text-zinc-300/70 max-w-3xl mb-14">
            Prices are anchored to what this category actually charges today, not picked to look good
            in a deck. The comparison is below.
          </p>
        </Reveal>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-8">
          {STREAMS.map((s, i) => (
            <Reveal key={s.n} delay={i + 1}>
              <div
                className="rounded-2xl h-full overflow-hidden flex flex-col"
                style={{ border: `1px solid ${s.border}`, background: '#0a0a0e' }}
              >
                {/* Colored header area */}
                <div style={{ background: s.headerBg, borderBottom: `1px solid ${s.border}`, padding: '24px 24px 20px' }}>
                  <div className="flex items-start justify-between mb-4">
                    <div
                      className="rounded-xl flex items-center justify-center"
                      style={{
                        width: 52, height: 52,
                        background: `${s.color}22`,
                        border: `1px solid ${s.border}`,
                      }}
                    >
                      {s.icon}
                    </div>
                    <div className="text-right">
                      <div className="font-black leading-none" style={{ fontSize: 'clamp(1.6rem,3vw,2.2rem)', letterSpacing: '-0.05em', color: s.color }}>{s.stat}</div>
                      <div className="text-[0.68rem] font-semibold mt-1" style={{ color: `${s.color}99` }}>{s.statSub}</div>
                    </div>
                  </div>
                  <div className="text-[0.62rem] font-bold tracking-[0.14em] uppercase mb-2" style={{ color: s.color }}>{s.n} — {s.tag}</div>
                  <div className="text-[1.06rem] font-bold text-zinc-50 leading-snug">{s.title}</div>
                </div>

                {/* Body */}
                <div className="p-6 flex flex-col gap-5 flex-1">
                  <p className="text-[0.82rem] text-zinc-200/78 leading-relaxed">{s.body}</p>

                  <div className="flex flex-col gap-2.5 mt-auto">
                    {s.bullets.map((b, j) => (
                      <div key={j} className="flex items-start gap-2.5">
                        <svg className="flex-shrink-0 mt-[3px]" width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
                          <circle cx="6" cy="6" r="5.5" stroke={s.color} strokeWidth="1" strokeOpacity="0.5"/>
                          <path d="M3.5 6 5 7.5 8.5 4" stroke={s.color} strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                        <span className="text-[0.76rem] text-zinc-200/75 leading-relaxed">{b}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </Reveal>
          ))}
        </div>

        {/* Pricing benchmark */}
        <Reveal delay={3}>
          <div className="glass-panel rounded-2xl overflow-auto mb-8">
            <div className="px-7 pt-6 pb-4">
              <div className="text-[0.76rem] font-bold tracking-[0.1em] uppercase text-zinc-300/85 mb-1.5">
                What this category charges today
              </div>
              <p className="small-copy text-zinc-100/78 max-w-2xl">
                The free tier is not generosity — it is what the two closest competitors already do.
                Pro is priced one step above the only paid comparable.
              </p>
            </div>
            <table className="w-full border-collapse" style={{ minWidth: 620 }}>
              <thead>
                <tr style={{ borderTop: '1px solid rgba(161,161,170,0.28)', borderBottom: '1px solid rgba(161,161,170,0.28)' }}>
                  <th className="py-3 px-7 text-left text-[0.72rem] font-bold tracking-[0.1em] uppercase text-zinc-300/80">Product</th>
                  <th className="py-3 px-5 text-left text-[0.72rem] font-bold tracking-[0.1em] uppercase text-zinc-300/80">Price</th>
                  <th className="py-3 px-5 text-left text-[0.72rem] font-bold tracking-[0.1em] uppercase text-zinc-300/80">Model</th>
                  <th className="py-3 px-5 text-left text-[0.72rem] font-bold tracking-[0.1em] uppercase text-zinc-300/80">Note</th>
                </tr>
              </thead>
              <tbody>
                {BENCHMARK.map((b, i) => (
                  <tr
                    key={b.name}
                    style={{
                      borderBottom: i < BENCHMARK.length - 1 ? '1px solid rgba(161,161,170,0.16)' : 'none',
                      background: b.us ? 'rgba(113,113,122,0.18)' : 'transparent',
                    }}
                  >
                    <td className={`py-3.5 px-7 text-[0.88rem] ${b.us ? 'font-bold text-zinc-50' : 'font-medium text-zinc-100/85'}`}>{b.name}</td>
                    <td className={`py-3.5 px-5 font-mono text-[0.88rem] ${b.us ? 'font-bold text-zinc-50' : 'font-semibold text-zinc-100/85'}`}>{b.price}</td>
                    <td className="py-3.5 px-5 text-[0.82rem] text-zinc-200/78">{b.model}</td>
                    <td className="py-3.5 px-5 text-[0.82rem] text-zinc-300/70">{b.note}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Reveal>

        {/* Conversion flow */}
        <Reveal delay={4}>
          <div className="rounded-2xl p-6 border border-zinc-500/35 bg-zinc-900/30">
            <div className="text-[0.68rem] font-bold tracking-[0.12em] uppercase text-zinc-300/70 mb-4">Adoption path — each tier is a natural step from the last</div>
            <div className="flex items-center gap-0 overflow-auto">
              {JOURNEY.map((step, i) => (
                <div key={step.label} className="flex items-center gap-0 min-w-0">
                  <div className="flex flex-col items-center gap-1.5 px-5 py-3 rounded-xl border" style={{ borderColor: `${step.color}40`, background: `${step.color}10`, minWidth: 150 }}>
                    <div className="text-[0.82rem] font-bold text-zinc-50 whitespace-nowrap">{step.label}</div>
                    <div className="text-[0.68rem] font-medium whitespace-nowrap" style={{ color: step.color }}>{step.sub}</div>
                  </div>
                  {i < JOURNEY.length - 1 && (
                    <div className="flex items-center px-2 flex-shrink-0">
                      <svg width="20" height="12" viewBox="0 0 20 12" fill="none" aria-hidden="true">
                        <path d="M0 6h17M13 1l6 5-6 5" stroke="rgba(255,255,255,0.2)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </Reveal>

      </div>
    </section>
  )
}
