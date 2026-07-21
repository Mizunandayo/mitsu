import { Reveal } from '../hooks/useScrollReveal.jsx'

const SEGMENTS = [
  {
    key: 'TAM',
    value: '1.6B',
    unit: 'Windows devices',
    title: 'Every monthly active Windows device',
    body: 'Microsoft confirmed 1.6 billion monthly active Windows devices in April 2026. MITSU needs no sensor beyond the webcam most of them already ship with.',
  },
  {
    key: 'SAM',
    value: '640M',
    unit: 'multi-monitor seats',
    title: 'Windows users running more than one display',
    body: 'Dual-monitor adoption sits near 40% among productivity users. These are the people who actually feel the window-shuffling friction MITSU removes.',
  },
  {
    key: 'SOM',
    value: '10.2M',
    unit: 'beachhead users',
    title: 'Developers, streamers, and accessibility-driven adopters',
    body: 'The identifiable early-adopter pool: multi-monitor Windows users in exactly the three roles where hands-free window control pays for itself immediately.',
  },
]

const DERIVATION = [
  { step: 'Professional developers worldwide',     value: '28.7M', note: 'Statista, 2025' },
  { step: 'Filtered to Windows-primary (~60%)',    value: '17.2M', note: 'derived' },
  { step: 'Filtered to multi-monitor (~40%)',      value: '6.9M',  note: 'derived' },
  { step: 'Active Twitch streamers',               value: '7.4M',  note: '2026' },
  { step: 'Filtered to Windows + multi-monitor',   value: '3.3M',  note: 'derived' },
  { step: 'Identifiable beachhead',                value: '10.2M', note: 'SOM', total: true },
]

const FIT = [
  {
    title: 'Developers & Analysts',
    copy: 'Move a terminal, docs tab, or editor around a multi-monitor layout without leaving the keyboard home position. 28.7 million professional developers worldwide, and the layout churn is constant.',
    grad: 'from-cyan-400/24',
  },
  {
    title: 'Streamers & Creators',
    copy: 'Relocate a chat overlay or scene window mid-broadcast without breaking eye contact with the camera. 7.4 million people stream actively on Twitch alone.',
    grad: 'from-violet-400/24',
  },
  {
    title: 'Accessibility & RSI',
    copy: 'Around 9% of US adults report a repetitive strain injury in any three-month window, and musculoskeletal problems drive roughly 30% of all sick days. Less mouse-dragging is a health outcome, not a convenience.',
    grad: 'from-emerald-400/24',
  },
]

const SOURCES = [
  { label: '1.6B monthly active Windows devices — Microsoft, Apr 2026', href: 'https://www.windowslatest.com/2026/04/30/microsofts-satya-nadella-confirms-1-6-billion-monthly-windows-users-bing-crosses-1-billion-for-the-first-time/' },
  { label: '~40% dual-monitor adoption — monitor industry statistics, 2026', href: 'https://wifitalents.com/monitor-display-industry-statistics/' },
  { label: '$30.9B touchless sensing market, 22.5% CAGR — MarketsandMarkets', href: 'https://www.marketsandmarkets.com/Market-Reports/touchless-sensing-gesturing-market-369.html' },
  { label: '28.7M professional developers — Statista via Future Processing', href: 'https://www.future-processing.com/blog/how-many-software-developers-are-there-in-the-world/' },
  { label: '7.4M active Twitch streamers — 2026', href: 'https://resourcera.com/data/social/twitch-statistics/' },
  { label: 'RSI and musculoskeletal sick-day figures — US BLS via Enjuris', href: 'https://www.enjuris.com/workplace-injury/repetitive-strain-injuries-work/' },
]

export default function Market() {
  return (
    <section id="market" className="relative py-32 z-10 overflow-hidden" style={{ background: '#050505' }}>
      <div className="max-w-[1100px] mx-auto px-8">
        <Reveal>
          <p className="micro-label font-bold uppercase text-zinc-300/90 mb-5">Target Market</p>
        </Reveal>
        <Reveal delay={1}>
          <h2 className="font-black tracking-[-0.04em] leading-none text-white mb-5" style={{ fontSize: 'clamp(2.4rem,5vw,4rem)' }}>
            TAM · SAM · SOM<br />
            <span className="text-zinc-300/88">The sensor is already on the desk.</span>
          </h2>
        </Reveal>
        <Reveal delay={2}>
          <p className="text-zinc-100/85 text-[1.03rem] leading-relaxed max-w-3xl mb-4">
            Gesture computing has been built almost entirely for XR headsets, kiosks, and dedicated
            sensors — Leap Motion, HoloLens, depth cameras. The category is real and growing at
            <strong className="text-white font-semibold"> 22.5% a year toward $30.9B in 2026</strong>,
            but almost none of it targets the ordinary multi-monitor desk using the webcam already there.
          </p>
        </Reveal>
        <Reveal delay={2}>
          <p className="small-copy text-zinc-300/70 max-w-3xl mb-9">
            Every figure below is sourced and the SOM arithmetic is shown in full. Sources are listed
            at the end of this section.
          </p>
        </Reveal>

        <Reveal delay={3}>
          <div className="mb-10 grid grid-cols-1 lg:grid-cols-[1.05fr_0.95fr] gap-10 items-center">
            <div className="relative min-h-[30rem] flex items-center justify-center">
              <div
                className="absolute bottom-3 w-[28rem] h-[24rem] max-w-full"
                style={{
                  clipPath: 'polygon(50% 0%, 100% 100%, 0% 100%)',
                  background:
                    'linear-gradient(180deg, rgba(34,211,238,0.2) 0%, rgba(139,92,246,0.16) 58%, rgba(16,185,129,0.2) 100%)',
                  border: '1px solid rgba(161,161,170,0.42)',
                  boxShadow: '0 22px 80px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.12)',
                }}
              />

              <div className="absolute bottom-3 w-[22rem] max-w-full h-px bg-zinc-200/45" />
              <div className="absolute bottom-[7.25rem] w-[16rem] max-w-full h-px bg-zinc-200/45" />
              <div className="absolute bottom-[12rem] w-[9.25rem] max-w-full h-px bg-zinc-200/45" />

              <div className="absolute bottom-[12.5rem] left-1/2 -translate-x-1/2 text-center">
                <div className="text-[0.74rem] font-bold tracking-widest uppercase text-zinc-100/92">SOM</div>
                <div className="text-[1.55rem] font-black tracking-tight text-zinc-50">10.2M</div>
              </div>
              <div className="absolute bottom-[7.7rem] left-1/2 -translate-x-1/2 text-center">
                <div className="text-[0.74rem] font-bold tracking-widest uppercase text-zinc-100/92">SAM</div>
                <div className="text-[1.55rem] font-black tracking-tight text-zinc-50">640M</div>
              </div>
              <div className="absolute bottom-[3rem] left-1/2 -translate-x-1/2 text-center">
                <div className="text-[0.74rem] font-bold tracking-widest uppercase text-zinc-100/92">TAM</div>
                <div className="text-[1.55rem] font-black tracking-tight text-zinc-50">1.6B</div>
              </div>

              <span className="absolute top-[4.5rem] left-[48%] w-2.5 h-2.5 rounded-full bg-cyan-300 shadow-[0_0_16px_rgba(103,232,249,0.9)]" />
              <span className="absolute top-[9.5rem] left-[29%] w-3 h-3 rounded-full bg-violet-300 shadow-[0_0_15px_rgba(196,181,253,0.85)]" />
              <span className="absolute top-[14rem] left-[66%] w-2.5 h-2.5 rounded-full bg-emerald-300 shadow-[0_0_15px_rgba(110,231,183,0.9)]" />
            </div>

            <div className="space-y-6">
              {SEGMENTS.map((s) => (
                <div key={s.key} className="relative pl-5">
                  <span
                    className="absolute left-0 top-0 bottom-0 w-[2px]"
                    style={{ background: 'linear-gradient(180deg, rgba(212,212,216,0.75), rgba(212,212,216,0.35), transparent)' }}
                  />
                  <div className="flex items-baseline justify-between gap-4 mb-1.5">
                    <span className="text-[0.82rem] font-bold tracking-widest uppercase text-zinc-200/92">{s.key}</span>
                    <span className="text-right">
                      <span className="text-[1.06rem] font-black tracking-tight text-zinc-50">{s.value}</span>
                      <span className="block text-[0.72rem] font-medium text-zinc-300/65">{s.unit}</span>
                    </span>
                  </div>
                  <div className="text-[1.03rem] font-bold text-zinc-50 mb-1.5">{s.title}</div>
                  <div className="text-[0.88rem] text-zinc-200/84 leading-relaxed">{s.body}</div>
                </div>
              ))}
            </div>
          </div>
        </Reveal>

        {/* SOM derivation — show the arithmetic */}
        <Reveal delay={3}>
          <div className="glass-panel rounded-2xl p-7 mb-10">
            <div className="text-[0.76rem] font-bold tracking-[0.1em] uppercase text-zinc-300/85 mb-2">
              How the 10.2M SOM is derived
            </div>
            <p className="small-copy text-zinc-100/78 mb-5 max-w-2xl">
              Two sourced population figures, filtered by platform and monitor count. The filter
              percentages are stated estimates, not measurements — they are marked as derived so the
              assumption is visible rather than buried.
            </p>
            <div className="flex flex-col">
              {DERIVATION.map((d, i) => (
                <div
                  key={d.step}
                  className="flex items-center justify-between gap-4 py-3"
                  style={{
                    borderTop: i === 0 ? 'none' : '1px solid rgba(161,161,170,0.18)',
                    borderTopWidth: d.total ? 1 : undefined,
                    borderTopColor: d.total ? 'rgba(212,212,216,0.45)' : undefined,
                  }}
                >
                  <span className={`text-[0.88rem] ${d.total ? 'font-bold text-zinc-50' : 'text-zinc-200/82'}`}>
                    {d.step}
                  </span>
                  <span className="flex items-baseline gap-3 flex-shrink-0">
                    <span className={`font-mono text-[0.68rem] uppercase tracking-wider ${d.total ? 'text-zinc-100/80' : 'text-zinc-400/70'}`}>
                      {d.note}
                    </span>
                    <span className={`font-mono tabular-nums ${d.total ? 'text-[1.05rem] font-bold text-zinc-50' : 'text-[0.92rem] font-semibold text-zinc-100/88'}`}>
                      {d.value}
                    </span>
                  </span>
                </div>
              ))}
            </div>
          </div>
        </Reveal>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
          {FIT.map((entry, i) => (
            <Reveal key={entry.title} delay={i + 1}>
              <div className="rounded-2xl p-5 h-full relative overflow-hidden border border-zinc-500/45 bg-zinc-900/30">
                <div className={`absolute inset-0 bg-gradient-to-br ${entry.grad} via-transparent to-transparent pointer-events-none`} />
                <div className="relative z-10">
                  <div className="text-[1.02rem] font-bold text-zinc-50 mb-2">{entry.title}</div>
                  <div className="small-copy text-zinc-100/85">{entry.copy}</div>
                </div>
              </div>
            </Reveal>
          ))}
        </div>

        {/* Sources */}
        <Reveal delay={2}>
          <div className="pt-6" style={{ borderTop: '1px solid rgba(161,161,170,0.25)' }}>
            <div className="text-[0.72rem] font-bold tracking-[0.12em] uppercase text-zinc-300/70 mb-4">
              Sources
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-2.5">
              {SOURCES.map((s, i) => (
                <a
                  key={s.href}
                  href={s.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-start gap-2.5 text-[0.78rem] text-zinc-300/72 hover:text-zinc-100 no-underline transition-colors duration-150 group"
                >
                  <span className="font-mono text-[0.7rem] text-zinc-500/80 pt-[2px] flex-shrink-0 tabular-nums">
                    {String(i + 1).padStart(2, '0')}
                  </span>
                  <span className="leading-relaxed group-hover:underline underline-offset-2">{s.label}</span>
                </a>
              ))}
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  )
}
