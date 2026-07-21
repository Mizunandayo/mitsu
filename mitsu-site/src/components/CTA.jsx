import { Reveal } from '../hooks/useScrollReveal.jsx'

const REPO_URL = 'https://github.com/Mizunandayo/mitsu'

const QUICKSTART = [
  'py -3.11 -m venv .venv',
  '.venv\\Scripts\\Activate.ps1',
  'python -m pip install -e .',
  '.venv\\Scripts\\python.exe scripts\\bootstrap_hand_model.py --trust-on-first-use',
  '.venv\\Scripts\\python.exe -m mitsu.app',
]

export default function CTA() {
  const scrollToDemo = e => {
    e.preventDefault()
    document.querySelector('#demo')?.scrollIntoView({ behavior:'smooth', block:'start' })
  }

  return (
    <section className="relative py-32 z-10 overflow-hidden" style={{ background:'#050505' }}>
      {/* Background glow */}
      <div className="absolute inset-0 pointer-events-none"
           style={{ background:'radial-gradient(ellipse 60% 50% at 50% 100%, rgba(255,255,255,0.04) 0%, transparent 70%)' }} />

      <div className="max-w-[1100px] mx-auto px-8 relative z-10">

        {/* Quickstart */}
        <Reveal>
          <div className="glass-panel rounded-2xl p-7 mb-6">
            <div className="flex items-center gap-3 mb-2">
              <svg width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="rgba(74,222,128,0.9)" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M3 5.5 7 9.5 3 13.5M9.5 14.5h7.5"/>
              </svg>
              <div className="text-[0.78rem] font-bold tracking-[0.1em] uppercase text-zinc-200/92">
                Run it yourself — Windows PowerShell
              </div>
            </div>
            <div className="small-copy text-zinc-100/82 mb-5 max-w-2xl">
              Python 3.11, a webcam, and Windows 11. The MediaPipe model is fetched once and
              verified against a committed SHA-256 pin before MITSU will load it.
            </div>
            <div className="rounded-xl p-4 font-mono text-[0.82rem] leading-7 border border-zinc-500/45 overflow-x-auto"
                 style={{ background:'#050505' }}>
              {QUICKSTART.map(line => (
                <div key={line} className="whitespace-nowrap">
                  <span className="code-cm select-none">{'PS> '}</span>
                  <span className="code-tx">{line}</span>
                </div>
              ))}
            </div>
          </div>
        </Reveal>

        {/* Main CTA block */}
        <Reveal delay={1}>
          <div className="glass-panel rounded-3xl px-12 py-20 text-center relative overflow-hidden mb-12">
            {/* Inner glow */}
            <div className="absolute inset-0 pointer-events-none rounded-3xl"
                 style={{ background:'radial-gradient(ellipse 55% 40% at 50% 0%, rgba(212,212,216,0.12) 0%, transparent 70%)' }} />
            <div className="relative z-10">
              <p className="text-[0.82rem] font-bold tracking-[0.14em] uppercase text-zinc-200/90 mb-6">
                OpenAI Build Week · Apps for Your Life · July 14–21, 2026
              </p>
              <h2 className="font-black tracking-[-0.05em] text-white leading-[0.95] mb-6"
                  style={{ fontSize:'clamp(3rem,7vw,6rem)' }}>
                Point at nothing.<br/>Your windows move.
              </h2>
              <p className="text-zinc-100/88 text-[1rem] mb-10 max-w-lg mx-auto leading-relaxed">
                Perception and action stay on your machine. Cloud reasoning is invited in only
                where it earns its place — so the core never depends on it.
              </p>
              <div className="flex gap-3 justify-center flex-wrap">
                <a href="#demo"
                   onClick={scrollToDemo}
                   className="inline-flex items-center gap-2 text-sm font-bold text-black bg-white px-8 py-4 rounded-xl no-underline hover:opacity-90 hover:-translate-y-0.5 transition-all duration-150">
                  <svg width="13" height="13" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><polygon points="3,2 13,8 3,14"/></svg>
                  Watch the Demo
                </a>
                <a href={REPO_URL}
                   target="_blank" rel="noopener noreferrer"
                   className="inline-flex items-center gap-2 text-sm font-medium text-white/65 border border-white/16 px-8 py-4 rounded-xl no-underline hover:text-white hover:border-white/32 hover:-translate-y-0.5 transition-all duration-150"
                   style={{ background:'rgba(255,255,255,0.04)' }}>
                  <svg width="13" height="13" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
                  View Source
                </a>
              </div>
            </div>
          </div>
        </Reveal>

        {/* Footer */}
        <Reveal delay={2}>
          <footer className="flex items-center justify-between flex-wrap gap-3 pt-4" style={{ borderTop:'1px solid rgba(161,161,170,0.35)' }}>
            <span className="text-sm font-bold tracking-[0.16em] uppercase text-white/70">見つ MITSU</span>

            <div className="flex gap-5">
              {[
                { label:'GitHub',  href: REPO_URL },
                { label:'License', href: `${REPO_URL}/blob/main/LICENSE` },
                { label:'README',  href: `${REPO_URL}#readme` },
              ].map(l => (
                <a key={l.label} href={l.href} target="_blank" rel="noopener noreferrer"
                   className="text-xs font-medium text-white/55 hover:text-white/70 no-underline transition-colors duration-150">
                  {l.label}
                </a>
              ))}
            </div>
          </footer>
        </Reveal>

      </div>
    </section>
  )
}
