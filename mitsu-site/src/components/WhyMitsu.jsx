import { Reveal } from '../hooks/useScrollReveal.jsx'

const Check = () => (
  <svg width="14" height="14" viewBox="0 0 16 16" fill="none" role="img" aria-label="Supported">
    <circle cx="8" cy="8" r="7" stroke="rgba(74,222,128,0.65)" strokeWidth="1.2"/>
    <path d="m5 8 2 2 4-4" stroke="#4ade80" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
)
const Cross = () => (
  <svg width="14" height="14" viewBox="0 0 16 16" fill="none" role="img" aria-label="Not supported">
    <circle cx="8" cy="8" r="7" stroke="rgba(251,113,133,0.45)" strokeWidth="1.2"/>
    <path d="m5.5 5.5 5 5M10.5 5.5l-5 5" stroke="#fb7185" strokeWidth="1.45" strokeLinecap="round"/>
  </svg>
)
const Part = () => (
  <svg width="14" height="14" viewBox="0 0 16 16" fill="none" role="img" aria-label="Partial">
    <circle cx="8" cy="8" r="7" stroke="rgba(250,204,21,0.5)" strokeWidth="1.2"/>
    <path d="M5 8h6" stroke="#facc15" strokeWidth="1.4" strokeLinecap="round"/>
  </svg>
)

const COLUMNS = [
  { name: 'Voice Access',  sub: 'Free, built in' },
  { name: 'DisplayFusion', sub: '$25 lifetime' },
  { name: 'Talon Voice',   sub: 'Free core' },
  { name: 'MediaPipe apps', sub: 'Open source' },
]

const ROWS = [
  { feat:'Works with no network at all',              m:true,  d:[true,  true,  true,  true ] },
  { feat:'Window management is the core purpose',     m:true,  d:[false, true,  false, false] },
  { feat:'Hand gesture input from a plain webcam',    m:true,  d:[false, false, '~',   true ] },
  { feat:'Continuous cross-monitor window drag',      m:true,  d:['~',   true,  '~',   false] },
  { feat:'Voice command by app name',                 m:true,  d:[true,  false, true,  false] },
  { feat:'Voice locks a window as the drag target',   m:true,  d:[false, false, false, false] },
  { feat:'Hand and voice fused in one state machine', m:true,  d:[false, false, false, false] },
  { feat:'Cloud reasoning for out-of-grammar speech', m:true,  d:[false, false, false, false] },
  { feat:'Open source licence',                       m:'MIT', d:['No',  'No',  'No',  'Varies'] },
]

function Cell({ v }) {
  if (v === true)  return <Check />
  if (v === false) return <Cross />
  if (v === '~')   return <Part />
  return <span className="font-mono text-[0.8rem] font-bold text-zinc-200/90">{v}</span>
}

const HONEST = [
  {
    name: 'Windows Voice Access',
    body: 'Genuinely capable and free. It has a grid overlay that now spans multiple displays, supports drag-and-drop, and switches focus between monitors by phonetic letter. But every interaction is discrete and voice-driven — you call out grid coordinates rather than physically moving a window.',
  },
  {
    name: 'DisplayFusion',
    body: 'The strongest commercial window manager on Windows, and the closest thing to a direct competitor on function. It is entirely mouse and hotkey driven, so it solves the layout problem without ever removing the reach for the mouse.',
  },
  {
    name: 'Talon Voice',
    body: 'The benchmark for serious hands-free computing, especially for people with RSI. Its focus is voice, eye tracking, and noise commands for general control — not treating a window as a physical object you push across a desk.',
  },
  {
    name: 'MediaPipe virtual-mouse projects',
    body: 'A saturated hobby and hackathon pattern: AirTouch, NPointer, Zesture, and dozens of GitHub repos. Nearly all of them map the hand to a cursor. Almost none do window-level control, and none fuse voice into the same state machine.',
  },
]

const DIFFS = [
  { n:'01', title:'Relocation, not cursors',      desc:'Prior gesture tools map your hand to a mouse. MITSU makes moving a whole window the mechanic itself.' },
  { n:'02', title:'Names beat pointing',          desc:'Voice target-lock resolves a buried window by name, so occlusion and z-order stop being obstacles at all.' },
  { n:'03', title:'One fused state machine',      desc:'Hand-only, voice-lock-plus-hand, and voice-only are three behaviours emerging from one machine, not three modes.' },
  { n:'04', title:'Cognition where it earns it',  desc:'GPT-5.6 is scoped to flexible phrasing and screen reasoning, never to the continuous-motion path.' },
]

export default function WhyMitsu() {
  return (
    <section id="differentiation" className="relative py-32 z-10" style={{ background:'#070707' }}>
      <div className="max-w-[1100px] mx-auto px-8">

        <Reveal><p className="micro-label font-bold uppercase text-zinc-300/90 mb-5">Why MITSU</p></Reveal>
        <Reveal delay={1}>
          <h2 className="font-black tracking-[-0.04em] leading-none text-white mb-4"
              style={{ fontSize:'clamp(2.4rem,5vw,4rem)' }}>
            Adjacent tools exist.<br/>
            <span style={{ color:'rgba(228,228,231,0.48)' }}>None combine it this way.</span>
          </h2>
        </Reveal>

        <Reveal delay={2}>
          <p className="text-zinc-100/85 text-[1.03rem] leading-relaxed mb-4 max-w-3xl">
            Touchless PC control is not, by itself, a differentiator. Windows ships voice control for
            free, DisplayFusion has solved multi-monitor layout commercially for years, and MediaPipe
            virtual-mouse projects are a saturated hobby pattern.
          </p>
        </Reveal>
        <Reveal delay={2}>
          <p className="small-copy text-zinc-300/72 mb-6 max-w-3xl">
            Pretending otherwise would not survive a judge who knows the category. What follows is an
            honest scorecard — including the rows where competitors match or beat MITSU — and then the
            three rows where nothing else lands at all.
          </p>
        </Reveal>

        {/* Comparison table */}
        <Reveal delay={3}>
          <div className="glass-panel rounded-2xl overflow-auto mb-6">
            <table className="w-full border-collapse" style={{ minWidth:760 }}>
              <thead>
                <tr className="border-b border-zinc-500/35">
                  <th className="py-4 px-5 text-left text-[0.78rem] font-bold text-zinc-200/95 tracking-wide uppercase">Capability</th>
                  <th className="py-4 px-5 text-left" style={{ background:'rgba(161,161,170,0.22)' }}>
                    <div className="text-[0.78rem] font-bold text-zinc-50 uppercase tracking-wide">MITSU</div>
                    <div className="text-[0.68rem] font-medium text-zinc-300/70 normal-case mt-0.5">Free + $29 Pro</div>
                  </th>
                  {COLUMNS.map(c => (
                    <th key={c.name} className="py-4 px-5 text-left">
                      <div className="text-[0.78rem] font-bold text-zinc-200/95 tracking-wide uppercase whitespace-nowrap">{c.name}</div>
                      <div className="text-[0.68rem] font-medium text-zinc-300/60 normal-case mt-0.5 whitespace-nowrap">{c.sub}</div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {ROWS.map((r, i) => (
                  <tr key={r.feat} className={`${i < ROWS.length-1 ? 'border-b border-zinc-500/30' : ''} hover:bg-zinc-400/10 transition-colors`}>
                    <td className="py-3 px-5 text-[0.88rem] text-zinc-100/88 font-medium">{r.feat}</td>
                    <td className="py-3 px-5" style={{ background:'rgba(113,113,122,0.16)' }}><Cell v={r.m}/></td>
                    {r.d.map((v, j) => (
                      <td key={j} className="py-3 px-5"><Cell v={v}/></td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Reveal>

        {/* Legend */}
        <Reveal delay={3}>
          <div className="flex flex-wrap gap-6 mb-12 text-[0.8rem] text-zinc-200/80">
            <span className="flex items-center gap-2"><Check /> Supported</span>
            <span className="flex items-center gap-2"><Part /> Partial or indirect</span>
            <span className="flex items-center gap-2"><Cross /> Not supported</span>
          </div>
        </Reveal>

        {/* Honest read on each competitor */}
        <Reveal delay={2}>
          <div className="text-[0.78rem] font-bold tracking-[0.1em] uppercase text-zinc-300/85 mb-5">
            What each of them actually does well
          </div>
        </Reveal>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-12">
          {HONEST.map((h, i) => (
            <Reveal key={h.name} delay={(i % 2) + 1}>
              <div className="glass-panel rounded-2xl p-6 h-full">
                <div className="text-[0.94rem] font-bold text-zinc-50 mb-2">{h.name}</div>
                <div className="small-copy text-zinc-100/82">{h.body}</div>
              </div>
            </Reveal>
          ))}
        </div>

        {/* 4 diff cards */}
        <Reveal delay={2}>
          <div className="text-[0.78rem] font-bold tracking-[0.1em] uppercase text-zinc-300/85 mb-5">
            The four rows nothing else fills
          </div>
        </Reveal>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {DIFFS.map((d, i) => (
            <Reveal key={d.n} delay={i + 1}>
              <div className="glass-panel rounded-2xl p-5 group hover:border-zinc-300/45 transition-colors duration-300 h-full">
                <div className="text-3xl font-black tracking-[-0.06em] text-zinc-300/55 mb-3 group-hover:text-zinc-100 transition-colors">{d.n}</div>
                <div className="text-[1rem] font-bold text-zinc-50 mb-2">{d.title}</div>
                <div className="small-copy text-zinc-100/82">{d.desc}</div>
              </div>
            </Reveal>
          ))}
        </div>

      </div>
    </section>
  )
}
