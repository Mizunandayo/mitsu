import { Reveal } from '../hooks/useScrollReveal.jsx'
import ImagePlaceholder from './shared/ImagePlaceholder'

/* Official OpenAI blossom mark — inline so it renders with no network dependency. */
export const OpenAIMark = ({ size = 22, color = 'currentColor', className = '' }) => (
  <svg
    width={size} height={size} viewBox="0 0 24 24" fill={color}
    className={className} aria-hidden="true"
    style={{ display:'inline-block', verticalAlign:'middle', flexShrink:0 }}
  >
    <path d="M22.2819 9.8211a5.9847 5.9847 0 0 0-.5157-4.9108 6.0462 6.0462 0 0 0-6.5098-2.9A6.0651 6.0651 0 0 0 4.9807 4.1818a5.9847 5.9847 0 0 0-3.9977 2.9 6.0462 6.0462 0 0 0 .7427 7.0966 5.98 5.98 0 0 0 .511 4.9107 6.051 6.051 0 0 0 6.5146 2.9001A5.9847 5.9847 0 0 0 13.2599 24a6.0557 6.0557 0 0 0 5.7718-4.2058 5.9894 5.9894 0 0 0 3.9977-2.9001 6.0557 6.0557 0 0 0-.7475-7.0729zm-9.022 12.6081a4.4755 4.4755 0 0 1-2.8764-1.0408l.1419-.0804 4.7783-2.7582a.7948.7948 0 0 0 .3927-.6813v-6.7369l2.02 1.1686a.071.071 0 0 1 .038.052v5.5826a4.504 4.504 0 0 1-4.4945 4.4944zm-9.6607-4.1254a4.4708 4.4708 0 0 1-.5346-3.0137l.142.0852 4.783 2.7582a.7712.7712 0 0 0 .7806 0l5.8428-3.3685v2.3324a.0804.0804 0 0 1-.0332.0615L9.74 19.9502a4.4992 4.4992 0 0 1-6.1408-1.6464zM2.3408 7.8956a4.485 4.485 0 0 1 2.3655-1.9728V11.6a.7664.7664 0 0 0 .3879.6765l5.8144 3.3543-2.0201 1.1685a.0757.0757 0 0 1-.071 0l-4.8303-2.7865A4.504 4.504 0 0 1 2.3408 7.872zm16.5963 3.8558L13.1038 8.364 15.1192 7.2a.0757.0757 0 0 1 .071 0l4.8303 2.7913a4.4944 4.4944 0 0 1-.6765 8.1042v-5.6772a.79.79 0 0 0-.407-.667zm2.0107-3.0231l-.142-.0852-4.7735-2.7818a.7759.7759 0 0 0-.7854 0L9.409 9.2297V6.8974a.0662.0662 0 0 1 .0284-.0615l4.8303-2.7866a4.4992 4.4992 0 0 1 6.6802 4.66zM8.3065 12.863l-2.02-1.1638a.0804.0804 0 0 1-.038-.0567V6.0742a4.4992 4.4992 0 0 1 7.3757-3.4537l-.142.0805L8.704 5.459a.7948.7948 0 0 0-.3927.6813zm1.0976-2.3654l2.602-1.4998 2.6069 1.4998v2.9994l-2.5974 1.4997-2.6067-1.4997Z" />
  </svg>
)

const MODELS = [
  {
    badge: 'Reasoning',
    name: 'gpt-5.6',
    tone: 'from-violet-500/20 via-indigo-500/10 to-transparent',
    use: 'Out-of-grammar phrasing · Responses API function calling',
    points: [
      'Calls the same four tools the local tier calls',
      'Bounded tool rounds — never an open-ended agent loop',
      'Only reached when the fixed grammar cannot resolve a command',
    ],
  },
  {
    badge: 'Transcription',
    name: 'gpt-4o-mini-transcribe',
    tone: 'from-cyan-500/20 via-blue-500/10 to-transparent',
    use: 'Push-to-talk speech → text · explicit, never ambient',
    points: [
      'Recording starts and stops on a deliberate key press',
      'Local RMS silence guard rejects dead-mic clips before upload',
      'Audio lives in memory; the temp WAV is deleted after the request',
    ],
  },
  {
    badge: 'Resilience',
    name: 'Circuit breaker',
    tone: 'from-amber-500/15 via-zinc-400/10 to-transparent',
    use: 'Trips to local-only after repeated cloud failures',
    chain: [
      'Fixed local grammar',
      'GPT-5.6 tool reasoning',
      'Breaker opens on N failures',
      'Cooldown window',
      'Local grammar only',
    ],
  },
]

const USES = [
  {
    tone: 'text-violet-200 border-violet-300/35 bg-violet-400/16',
    title: 'Bounded tool registry',
    desc: 'find_window, restore_window, move_window, read_screen. The model picks; it never writes window coordinates directly.',
    icon: (
      <svg width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2.5" y="3" width="15" height="4" rx="1.4"/><rect x="2.5" y="9.5" width="15" height="4" rx="1.4"/><path d="M5.5 16.5h9"/>
      </svg>
    ),
  },
  {
    tone: 'text-cyan-200 border-cyan-300/35 bg-cyan-400/16',
    title: 'Push-to-talk voice',
    desc: 'Press V, speak, press V again. A short clip goes up, structured intent comes back, the window moves.',
    icon: (
      <svg width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        <rect x="7" y="2" width="6" height="10" rx="3"/><path d="M10 16v-3M5 11a5 5 0 0 0 10 0"/>
      </svg>
    ),
  },
  {
    tone: 'text-emerald-200 border-emerald-300/35 bg-emerald-400/16',
    title: 'Grammar first, model second',
    desc: 'Show Discord on the left screen resolves locally in a fixed grammar. Only unusual phrasing escalates.',
    icon: (
      <svg width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        <path d="M3 6h14M3 10h9M3 14h5"/><path d="M14 13l2 2 3-3.5"/>
      </svg>
    ),
  },
  {
    tone: 'text-amber-200 border-amber-300/35 bg-amber-400/16',
    title: 'Frames never leave the device',
    desc: 'Only geometric landmarks cross any boundary on the hand path. Camera images are never uploaded, ever.',
    icon: (
      <svg width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        <path d="M10 2.5l6 2.4v4.3c0 3.6-2.5 6.6-6 8.3-3.5-1.7-6-4.7-6-8.3V4.9z"/><path d="M7.6 10.1 9.3 11.8l3.4-3.6"/>
      </svg>
    ),
  },
]

export default function OpenAISection() {
  return (
    <section id="openai" className="relative py-32 z-10 overflow-hidden" style={{ background:'#050505' }}>
      {/* Background glow */}
      <div className="absolute inset-0 pointer-events-none"
           style={{ background:'radial-gradient(ellipse 60% 50% at 50% 0%, rgba(192,132,252,0.06) 0%, transparent 70%)' }} />

      <div className="max-w-[1100px] mx-auto px-8 relative z-10">

        {/* Header */}
        <div className="flex flex-col items-center gap-8 mb-16">
          <Reveal>
            <OpenAIMark size={110} color="rgba(244,244,245,0.95)" />
          </Reveal>
          <Reveal><p className="micro-label font-bold uppercase text-zinc-300/90 mb-3 text-center">Cloud Cognition</p></Reveal>
          <Reveal delay={1}>
            <h2 className="font-black tracking-[-0.04em] leading-none text-white mb-3 text-center"
                style={{ fontSize:'clamp(2.4rem,5vw,4rem)' }}>
              GPT-5.6 handles<br/>
              <span style={{ color:'rgba(228,228,231,0.5)' }}>what a grammar can&rsquo;t.</span>
            </h2>
          </Reveal>
        </div>

        <Reveal delay={2}>
          <p className="text-zinc-100/85 text-[1.03rem] leading-relaxed max-w-2xl mx-auto text-center mb-10">
            Local handles reflexes. Cloud handles cognition. GPT-5.6 sits precisely where a
            deterministic parser runs out of road — and it reaches the desktop through the
            same four typed tools the local tier already uses.
          </p>
        </Reveal>

        {/* Model cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-8">
          {MODELS.map((m, i) => (
            <Reveal key={m.name} delay={i + 1}>
              <div className="glass-panel rounded-2xl p-0 h-full hover:border-zinc-300/45 transition-colors duration-300 overflow-hidden">
                <div className={`bg-gradient-to-br ${m.tone} p-4 border-b border-zinc-500/35`}>
                  <div className="text-[0.78rem] font-bold tracking-[0.1em] uppercase text-zinc-200/90 mb-2">{m.badge}</div>
                  <div className="flex items-center gap-2.5">
                    <OpenAIMark size={20} color="rgba(244,244,245,0.95)" />
                    <div className="text-[1.02rem] font-bold text-white tracking-tight font-mono">{m.name}</div>
                  </div>
                </div>
                <div className="p-4">
                  <div className="text-[0.86rem] font-medium text-zinc-100/85 mb-4 leading-relaxed">{m.use}</div>

                  {m.points && (
                    <div className="flex flex-col gap-2">
                      {m.points.map(p => (
                        <div key={p} className="flex items-start gap-2 text-[0.84rem] text-zinc-100/82 leading-relaxed">
                          <div className="w-1.5 h-1.5 rounded-full bg-zinc-200/70 shrink-0 mt-2" />
                          {p}
                        </div>
                      ))}
                    </div>
                  )}

                  {m.chain && (
                    <div className="border border-zinc-400/35 rounded-xl p-3.5" style={{ background:'rgba(39,39,42,0.45)' }}>
                      <div className="text-[0.76rem] font-bold tracking-[0.09em] uppercase text-zinc-300/75 mb-3">Degradation order</div>
                      {m.chain.map((n, idx) => (
                        <div key={n}>
                          <div className="flex items-center gap-2 mb-1.5">
                            <div className={`w-1.5 h-1.5 rounded-full shrink-0 ${idx === 0 ? 'bg-green-400' : 'bg-white/22'}`} />
                            <span className={`text-[0.82rem] font-semibold ${idx === 0 ? 'text-zinc-100/95' : 'text-zinc-300/80'}`}>{n}</span>
                          </div>
                          {idx < m.chain.length - 1 && (
                            <div className="flex items-center gap-1.5 pl-4 mb-1.5">
                              <svg width="9" height="9" viewBox="0 0 12 12" fill="none" stroke="rgba(212,212,216,0.6)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                                <path d="M6 2v8M3 7.5 6 10.5 9 7.5"/>
                              </svg>
                              <span className="text-[0.74rem] text-zinc-300/65">on failure</span>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </Reveal>
          ))}
        </div>

        {/* 4 use cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-10">
          {USES.map((u, i) => (
            <Reveal key={u.title} delay={(i % 2) + 1}>
              <div className="glass-panel rounded-2xl p-5 flex items-start gap-4 hover:border-zinc-300/45 transition-colors duration-300 h-full">
                <div className={`w-8 h-8 rounded-lg border flex items-center justify-center shrink-0 ${u.tone}`}>
                  {u.icon}
                </div>
                <div>
                  <div className="text-[0.96rem] font-bold text-zinc-50 mb-1">{u.title}</div>
                  <div className="small-copy text-zinc-100/85">{u.desc}</div>
                </div>
              </div>
            </Reveal>
          ))}
        </div>

        {/* Tool schema code block */}
        <Reveal delay={3}>
          <div className="glass-panel rounded-2xl p-6 mb-8">
            <div className="text-[0.76rem] font-bold tracking-[0.1em] uppercase text-zinc-300/75 mb-4">
              The whole action surface — two callers, one tool layer
            </div>
            <div className="rounded-xl p-4 font-mono text-[0.82rem] leading-7 border border-zinc-500/45 overflow-x-auto"
                 style={{ background:'#050505' }}>
              <span className="code-cm">{'// Shared by the local grammar tier and the GPT-5.6 tier'}</span><br/>
              <span className="code-kw">tools</span><span className="code-tx">: [</span><br/>
              &nbsp;&nbsp;<span className="code-tx">{'{ name: '}</span><span className="code-st">&quot;find_window&quot;</span><span className="code-tx">{',    args: { '}</span><span className="code-st">name</span><span className="code-tx">{': str } },'}</span><br/>
              &nbsp;&nbsp;<span className="code-tx">{'{ name: '}</span><span className="code-st">&quot;restore_window&quot;</span><span className="code-tx">{', args: { '}</span><span className="code-st">handle</span><span className="code-tx">{': int } },'}</span><br/>
              &nbsp;&nbsp;<span className="code-tx">{'{ name: '}</span><span className="code-st">&quot;move_window&quot;</span><span className="code-tx">{',    args: { '}</span><span className="code-st">handle</span><span className="code-tx">{': int, '}</span><span className="code-st">destination</span><span className="code-tx">{': str } },'}</span><br/>
              &nbsp;&nbsp;<span className="code-tx">{'{ name: '}</span><span className="code-st">&quot;read_screen&quot;</span><span className="code-tx">{',    args: { } }'}</span><br/>
              <span className="code-tx">]</span>
            </div>
          </div>
        </Reveal>



      </div>
    </section>
  )
}
