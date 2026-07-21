import { Reveal } from '../hooks/useScrollReveal.jsx'

const KPIS = [
  {
    n: '100s',
    u: '/ day',
    t: 'Window shuffles break flow every time',
    d: 'Every context switch on a dual-monitor desk costs a reach for the mouse, a drag, and a resize.',
  },
  {
    n: '3',
    u: 'windows deep',
    t: 'Occlusion makes pointing useless',
    d: 'When the window you want is buried behind others, there is nothing on screen left to point at.',
  },
  {
    n: '0',
    u: '',
    t: 'Tools that treat a window as the unit',
    d: 'Every touchless tool maps your hand to a cursor. None make relocating a whole window the point.',
  },
]

export default function Problem() {
  return (
    <section id="problem" className="relative py-32 z-10" style={{ background: '#070707' }}>
      <div className="max-w-[1100px] mx-auto px-8">
        <Reveal>
          <p className="micro-label font-bold uppercase text-zinc-300/90 mb-6 text-center">Problem Statement</p>
        </Reveal>

        <Reveal delay={1}>
          <div className="problem-quote-mitsu text-center mb-10">
            <span className="problem-quote-mark-mitsu">&ldquo;</span>
            <h2
              className="font-black tracking-[-0.035em] leading-[1.08] text-zinc-50 mx-auto"
              style={{
                fontSize: 'clamp(1.35rem,3.2vw,2.25rem)',
                maxWidth: '40rem',
                letterSpacing: '-0.01em',
                marginBottom: '0.7em',
              }}
            >
              Multi-monitor setups solve one problem and quietly create another.
              <br />
              <span className="text-zinc-300/88">More screen space means constant physical window shuffling.</span>
            </h2>
            <p className="small-copy text-zinc-100/82 mx-auto mt-4" style={{ maxWidth: '32rem', fontSize: 'clamp(0.92rem,1.1vw,1.08rem)' }}>
              It is small friction, repeated hundreds of times a day, and it breaks concentration
              every single time. This is not hypothetical — it is the builder&rsquo;s own desk.
            </p>
          </div>
        </Reveal>

        <Reveal delay={2}>
          <div className="mb-5">
            <div className="text-[0.78rem] font-bold tracking-widest uppercase text-zinc-300/85 mb-2">Core Friction</div>
            <div className="text-[1.06rem] font-bold text-zinc-50 mb-2">The mouse is the bottleneck, not the monitor.</div>
            <p className="small-copy text-zinc-100/82 max-w-4xl">
              Gaming laptop on the left, external display on the right, and Discord, a browser,
              and an editor constantly needing to move between them mid-work.
            </p>
          </div>
        </Reveal>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 pt-5 border-t border-zinc-600/45">
          {KPIS.map((k, i) => (
            <Reveal key={k.t} delay={i + 3}>
              <div className="relative py-1">
                <div className="absolute top-0 left-0 h-[2px] w-16 bg-zinc-300/70" />
                <div className="pt-4">
                  <div className="flex items-end gap-1.5 mb-2">
                    <span className="text-[clamp(2rem,4.2vw,3rem)] font-black tracking-tight text-zinc-50">{k.n}</span>
                    {k.u ? <span className="text-zinc-300/85 text-[0.95rem] font-bold mb-1.5">{k.u}</span> : null}
                  </div>
                  <div className="text-[0.98rem] font-bold text-zinc-50 mb-2">{k.t}</div>
                  <div className="small-copy text-zinc-200/80">{k.d}</div>
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  )
}
