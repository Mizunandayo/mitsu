import { Reveal } from '../hooks/useScrollReveal.jsx'
import YouTubePlaceholder from './shared/YouTubePlaceholder'

/* Set this to the YouTube video ID once the demo is uploaded. */
const DEMO_VIDEO_ID = ''

const CONTROLS = [
  {
    group: 'Move',
    rows: [
      { action: 'Move a window',           input: 'Thumb-index pinch or closed-fist grip, then move your hand' },
      { action: 'Release',                 input: 'Open your hand' },
      { action: 'Maximize a held window',  input: 'Open a wide palm before releasing' },
      { action: 'Minimize',                input: 'Index-middle-ring pose, then a downward stroke' },
    ],
  },
  {
    group: 'Point',
    rows: [
      { action: 'Pointer',        input: 'Hold index and middle fingertips together' },
      { action: 'Click',          input: 'Dip both close fingertips slightly toward your wrist' },
      { action: 'Back',           input: 'Pointer pose plus a raised pinky' },
      { action: 'Forward',        input: 'Pointer pose plus a raised ring finger' },
      { action: 'Window shelf',   input: 'Hold a V sign, then point at a minimized-window row and click' },
    ],
  },
  {
    group: 'Speak',
    keys: true,
    rows: [
      { action: 'Start and send voice', input: ['V'], suffix: 'press once to start, once again to send' },
      { action: 'Choose microphone',    input: ['M'], suffix: 'then select an input device' },
      { action: 'Emergency stop',       input: ['Ctrl', 'Alt', 'Shift', 'M'], suffix: 'halts all automated window movement' },
      { action: 'Exit',                 input: ['Q'], suffix: 'or Esc, from the debug window' },
    ],
  },
]

const COMMANDS = [
  'show Discord',
  'open Paint',
  'grab VS Code',
  'show Discord on the left screen',
  'Can you show Discord on my screen',
]

export default function Demo() {
  return (
    <section id="demo" className="relative py-32 z-10" style={{ background:'#070707' }}>
      <div className="max-w-[1100px] mx-auto px-8">

        <Reveal><p className="micro-label font-bold uppercase text-zinc-300/90 mb-5">Demo</p></Reveal>
        <Reveal delay={1}>
          <h2 className="font-black tracking-[-0.04em] leading-none text-white mb-3"
              style={{ fontSize:'clamp(2.4rem,5vw,4rem)' }}>
            A window crosses two screens<br/>
            <span style={{ color:'rgba(255,255,255,0.22)' }}>because a hand moved.</span>
          </h2>
        </Reveal>
        <Reveal delay={2}>
          <p className="text-white/65 mb-12 max-w-2xl leading-relaxed">
            MITSU is a Windows desktop application, so there is no hosted demo to click.
            Watch the walkthrough below, or clone{' '}
            <a href="https://github.com/Mizunandayo/mitsu"
               target="_blank" rel="noopener noreferrer"
               className="text-white/75 font-semibold underline underline-offset-2 hover:text-white transition-colors">
              github.com/Mizunandayo/mitsu
            </a>{' '}
            and run it against your own webcam.
          </p>
        </Reveal>

        {/* YouTube embed */}
        <Reveal delay={3}>
          <div className="mb-14">
            <YouTubePlaceholder
              videoId={DEMO_VIDEO_ID}
              title="MITSU — Cross-monitor hand drag, voice target-lock, and voice relocate"
            />
          </div>
        </Reveal>

        {/* Controls reference */}
        <Reveal delay={2}>
          <div className="text-[0.78rem] font-bold tracking-[0.1em] uppercase text-zinc-300/85 mb-5">
            Full gesture and key reference
          </div>
        </Reveal>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-12">
          {CONTROLS.map((section, i) => (
            <Reveal key={section.group} delay={i + 1}>
              <div className="glass-panel rounded-2xl p-6 h-full">
                <div className="text-[0.82rem] font-bold tracking-[0.1em] uppercase text-zinc-200/92 mb-4 pb-3 border-b border-zinc-500/35">
                  {section.group}
                </div>
                <div className="flex flex-col gap-4">
                  {section.rows.map(row => (
                    <div key={row.action}>
                      <div className="text-[0.9rem] font-bold text-zinc-50 mb-1.5">{row.action}</div>
                      {section.keys ? (
                        <div className="flex flex-wrap items-center gap-1.5">
                          {row.input.map((k, ki) => (
                            <span key={k} className="flex items-center gap-1.5">
                              <kbd className="kbd-mitsu">{k}</kbd>
                              {ki < row.input.length - 1 ? <span className="text-zinc-400/70 text-[0.72rem]">+</span> : null}
                            </span>
                          ))}
                          <span className="text-[0.78rem] text-zinc-200/72 ml-1">{row.suffix}</span>
                        </div>
                      ) : (
                        <div className="text-[0.82rem] text-zinc-200/78 leading-relaxed">{row.input}</div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </Reveal>
          ))}
        </div>

        {/* Voice command grammar */}
        <Reveal delay={3}>
          <div className="glass-panel rounded-2xl p-7">
            <div className="text-[0.78rem] font-bold tracking-[0.1em] uppercase text-zinc-300/85 mb-2">
              Fixed voice grammar
            </div>
            <div className="small-copy text-zinc-100/82 mb-5 max-w-2xl">
              These resolve locally and deterministically. Anything outside this shape escalates
              to GPT-5.6 rather than failing.
            </div>
            <div className="flex flex-wrap gap-2.5">
              {COMMANDS.map(cmd => (
                <span
                  key={cmd}
                  className="inline-flex items-center gap-2 rounded-lg border border-zinc-500/40 px-3.5 py-2 font-mono text-[0.82rem] text-zinc-100/90"
                  style={{ background:'rgba(255,255,255,0.02)' }}
                >
                  <svg width="11" height="11" viewBox="0 0 16 16" fill="none" stroke="rgba(74,222,128,0.9)" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                    <path d="M3 8.5 6.2 11.7 13 4.9"/>
                  </svg>
                  {cmd}
                </span>
              ))}
            </div>
          </div>
        </Reveal>

      </div>
    </section>
  )
}
