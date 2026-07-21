import { Reveal } from '../hooks/useScrollReveal.jsx'

/* ─────────────────────────────────────────────────────────────
   ICONS

   Two sources, no emojis anywhere:
   1. Simple Icons CDN (`cdn.simpleicons.org/<slug>/<hex>`) for brands
      that publish an official mark.
   2. Hand-authored inline SVG for everything Simple Icons does not
      carry — OpenAI, Windows, Pillow, sounddevice, screeninfo,
      pywin32, ctypes, One Euro, Hatchling, VS Code.
   ───────────────────────────────────────────────────────────── */

/* Official OpenAI blossom mark. */
const OPENAI_SVG = `<svg viewBox="0 0 24 24" fill="#e4e4e7" xmlns="http://www.w3.org/2000/svg"><path d="M22.2819 9.8211a5.9847 5.9847 0 0 0-.5157-4.9108 6.0462 6.0462 0 0 0-6.5098-2.9A6.0651 6.0651 0 0 0 4.9807 4.1818a5.9847 5.9847 0 0 0-3.9977 2.9 6.0462 6.0462 0 0 0 .7427 7.0966 5.98 5.98 0 0 0 .511 4.9107 6.051 6.051 0 0 0 6.5146 2.9001A5.9847 5.9847 0 0 0 13.2599 24a6.0557 6.0557 0 0 0 5.7718-4.2058 5.9894 5.9894 0 0 0 3.9977-2.9001 6.0557 6.0557 0 0 0-.7475-7.0729zm-9.022 12.6081a4.4755 4.4755 0 0 1-2.8764-1.0408l.1419-.0804 4.7783-2.7582a.7948.7948 0 0 0 .3927-.6813v-6.7369l2.02 1.1686a.071.071 0 0 1 .038.052v5.5826a4.504 4.504 0 0 1-4.4945 4.4944zm-9.6607-4.1254a4.4708 4.4708 0 0 1-.5346-3.0137l.142.0852 4.783 2.7582a.7712.7712 0 0 0 .7806 0l5.8428-3.3685v2.3324a.0804.0804 0 0 1-.0332.0615L9.74 19.9502a4.4992 4.4992 0 0 1-6.1408-1.6464zM2.3408 7.8956a4.485 4.485 0 0 1 2.3655-1.9728V11.6a.7664.7664 0 0 0 .3879.6765l5.8144 3.3543-2.0201 1.1685a.0757.0757 0 0 1-.071 0l-4.8303-2.7865A4.504 4.504 0 0 1 2.3408 7.872zm16.5963 3.8558L13.1038 8.364 15.1192 7.2a.0757.0757 0 0 1 .071 0l4.8303 2.7913a4.4944 4.4944 0 0 1-.6765 8.1042v-5.6772a.79.79 0 0 0-.407-.667zm2.0107-3.0231l-.142-.0852-4.7735-2.7818a.7759.7759 0 0 0-.7854 0L9.409 9.2297V6.8974a.0662.0662 0 0 1 .0284-.0615l4.8303-2.7866a4.4992 4.4992 0 0 1 6.6802 4.66zM8.3065 12.863l-2.02-1.1638a.0804.0804 0 0 1-.038-.0567V6.0742a4.4992 4.4992 0 0 1 7.3757-3.4537l-.142.0805L8.704 5.459a.7948.7948 0 0 0-.3927.6813zm1.0976-2.3654l2.602-1.4998 2.6069 1.4998v2.9994l-2.5974 1.4997-2.6067-1.4997Z"/></svg>`

/* Windows 11 four-pane mark. */
const WINDOWS_SVG = `<svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg"><rect x="1" y="1" width="6.2" height="6.2" rx="0.5" fill="#0078D4"/><rect x="8.8" y="1" width="6.2" height="6.2" rx="0.5" fill="#0078D4"/><rect x="1" y="8.8" width="6.2" height="6.2" rx="0.5" fill="#0078D4"/><rect x="8.8" y="8.8" width="6.2" height="6.2" rx="0.5" fill="#0078D4"/></svg>`

/* One Euro Filter — a jagged raw signal resolving into a smooth curve. */
const ONE_EURO_SVG = `<svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1 11.5 2.2 7 3.4 12 4.6 6.2 5.8 11 7 5.5" stroke="#71717a" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/><path d="M7 5.5C9 5.5 10 9 11.4 9c1.6 0 2.2-3.6 3.6-3.6" stroke="#60a5fa" stroke-width="1.4" stroke-linecap="round"/><circle cx="7" cy="5.5" r="1.2" fill="#60a5fa"/></svg>`

/* pywin32 — a window chrome with a control handle. */
const PYWIN32_SVG = `<svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="1.2" y="2.4" width="13.6" height="11.2" rx="1.6" stroke="#4ade80" stroke-width="1.3"/><path d="M1.2 5.6h13.6" stroke="#4ade80" stroke-width="1.3"/><circle cx="3.4" cy="4" r="0.7" fill="#4ade80"/><circle cx="5.4" cy="4" r="0.7" fill="#4ade80" opacity="0.6"/><rect x="4" y="7.6" width="6" height="4" rx="0.8" fill="#4ade80" opacity="0.35"/></svg>`

/* ctypes — a bridge between a Python call and a native symbol. */
const CTYPES_SVG = `<svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="1" y="5" width="4.6" height="6" rx="1" stroke="#a1a1aa" stroke-width="1.2"/><rect x="10.4" y="5" width="4.6" height="6" rx="1" stroke="#a1a1aa" stroke-width="1.2"/><path d="M5.6 8h4.8" stroke="#fbbf24" stroke-width="1.4" stroke-linecap="round"/><path d="M8.8 6.6 10.4 8 8.8 9.4" stroke="#fbbf24" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>`

/* screeninfo — two displays of different sizes, i.e. mixed DPI. */
const SCREENINFO_SVG = `<svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="0.8" y="3" width="7.4" height="6" rx="1" stroke="#34d399" stroke-width="1.2"/><rect x="9.2" y="4.6" width="6" height="4.4" rx="1" stroke="#34d399" stroke-width="1.2" opacity="0.75"/><path d="M4.5 9v2M2.8 11h3.4" stroke="#34d399" stroke-width="1.1" stroke-linecap="round"/><path d="M12.2 9v1.6M10.9 10.6h2.6" stroke="#34d399" stroke-width="1.1" stroke-linecap="round" opacity="0.75"/></svg>`

/* sounddevice / PortAudio — an input waveform. */
const SOUNDDEVICE_SVG = `<svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1.4 8h1.4M4.2 5.2v5.6M6.6 2.8v10.4M9 4.4v7.2M11.4 6.2v3.6M13.8 7.2v1.6" stroke="#22d3ee" stroke-width="1.4" stroke-linecap="round"/></svg>`

/* Pillow — the PIL image-composition mark, simplified. */
const PILLOW_SVG = `<svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="1.2" y="2.4" width="13.6" height="11.2" rx="1.8" stroke="#e4e4e7" stroke-width="1.2"/><circle cx="5.2" cy="6.2" r="1.5" fill="#fbbf24"/><path d="M1.6 12.4 5.6 8.4l2.4 2.4 3-3.4 3.4 4" stroke="#e4e4e7" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>`

/* Hatchling — the PyPA build-backend egg/hatch mark, simplified. */
const HATCHLING_SVG = `<svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8 1.4c2.6 0 4.6 3 4.6 6.2A4.6 4.6 0 0 1 8 12.2 4.6 4.6 0 0 1 3.4 7.6C3.4 4.4 5.4 1.4 8 1.4Z" stroke="#c084fc" stroke-width="1.3" stroke-linejoin="round"/><path d="M4 8.4l2-1.6 2 1.6 2-1.6 2 1.6" stroke="#c084fc" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M5.6 14.2h4.8" stroke="#c084fc" stroke-width="1.3" stroke-linecap="round"/></svg>`

/* SHA-256 integrity — a shield with a verified check. */
const INTEGRITY_SVG = `<svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8 1.4 13.4 3.5v4.1c0 3.2-2.2 5.9-5.4 7.1-3.2-1.2-5.4-3.9-5.4-7.1V3.5z" stroke="#fbbf24" stroke-width="1.3" stroke-linejoin="round"/><path d="M5.8 7.9 7.4 9.5l3-3.2" stroke="#fbbf24" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>`

/* Visual Studio Code ribbon mark. */
const VSCODE_SVG = `<svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11.6 1.2 5.4 7.1 2.6 5 1.2 5.7v4.6L2.6 11l2.8-2.1 6.2 5.9 3.2-1.5V2.7z" fill="#0098FF" opacity="0.9"/><path d="M11.6 4.4v7.2L7.4 8z" fill="#050505" opacity="0.45"/></svg>`

/* Gesture state machine — three linked nodes. */
const STATEMACHINE_SVG = `<svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="3.4" cy="4" r="2.2" stroke="#a78bfa" stroke-width="1.2"/><circle cx="12.6" cy="4" r="2.2" stroke="#a78bfa" stroke-width="1.2"/><circle cx="12.6" cy="12.2" r="2.2" stroke="#a78bfa" stroke-width="1.2"/><path d="M5.6 4h4.8M12.6 6.2V10" stroke="#a78bfa" stroke-width="1.2" stroke-linecap="round"/><path d="M9.4 2.9 10.6 4 9.4 5.1M11.5 8.8 12.6 10l1.1-1.2" stroke="#a78bfa" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/></svg>`

/* ── Icon renderer ── */
const Icon = ({ slug, color, alt, svg, size = 17 }) =>
  svg ? (
    <span
      role="img"
      aria-label={alt}
      style={{ display: 'inline-block', width: size, height: size, verticalAlign: 'middle', lineHeight: 0 }}
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  ) : (
    <img
      src={`https://cdn.simpleicons.org/${slug}/${color}`}
      width={size}
      height={size}
      alt={alt}
      loading="lazy"
      style={{ objectFit: 'contain' }}
    />
  )

/* ── Full technology inventory ── */
const LAYERS = [
  {
    cat: 'Perception',
    note: 'Runs on-device, every frame, with no network dependency.',
    items: [
      { role: 'Hand tracking', name: 'MediaPipe',   ver: '0.10.35',   icon: <Icon slug="mediapipe" color="0097A7" alt="MediaPipe" /> },
      { role: 'Inference',     name: 'TFLite XNNPACK',                icon: <Icon slug="tensorflow" color="FF6F00" alt="TensorFlow Lite" /> },
      { role: 'Camera',        name: 'OpenCV',      ver: '5.0.0',     icon: <Icon slug="opencv" color="5C3EE8" alt="OpenCV" /> },
      { role: 'Array math',    name: 'NumPy',                         icon: <Icon slug="numpy" color="4DABCF" alt="NumPy" /> },
      { role: 'Smoothing',     name: 'One Euro Filter',               icon: <Icon svg={ONE_EURO_SVG} alt="One Euro Filter" /> },
    ],
  },
  {
    cat: 'Voice & Cognition',
    note: 'Explicit, user-initiated network actions only.',
    items: [
      { role: 'Reasoning',     name: 'GPT-5.6',                       icon: <Icon svg={OPENAI_SVG} alt="OpenAI GPT-5.6" /> },
      { role: 'Transcription', name: 'gpt-4o-mini-transcribe',        icon: <Icon svg={OPENAI_SVG} alt="OpenAI transcription" /> },
      { role: 'SDK',           name: 'OpenAI Python', ver: '2.45.0',  icon: <Icon svg={OPENAI_SVG} alt="OpenAI Python SDK" /> },
      { role: 'Mic capture',   name: 'sounddevice',   ver: '0.5.3',   icon: <Icon svg={SOUNDDEVICE_SVG} alt="sounddevice" /> },
    ],
  },
  {
    cat: 'Window Control',
    note: 'Direct Win32 access — no abstraction layer in between.',
    items: [
      { role: 'Win32 API',     name: 'pywin32',       ver: '312',     icon: <Icon svg={PYWIN32_SVG} alt="pywin32" /> },
      { role: 'Native calls',  name: 'ctypes · user32',               icon: <Icon svg={CTYPES_SVG} alt="ctypes and user32" /> },
      { role: 'Monitors',      name: 'screeninfo',    ver: '0.8.1',   icon: <Icon svg={SCREENINFO_SVG} alt="screeninfo" /> },
      { role: 'Gestures',      name: 'State machine',                 icon: <Icon svg={STATEMACHINE_SVG} alt="Gesture state machine" /> },
      { role: 'Platform',      name: 'Windows 11',                    icon: <Icon svg={WINDOWS_SVG} alt="Windows 11" /> },
    ],
  },
  {
    cat: 'Interface',
    note: 'One toolkit for every designed surface.',
    items: [
      { role: 'GUI toolkit',   name: 'PySide6 · Qt',  ver: '6.11.1',  icon: <Icon slug="qt" color="41CD52" alt="Qt for Python" /> },
      { role: 'Text render',   name: 'Pillow',        ver: '12.3.0',  icon: <Icon svg={PILLOW_SVG} alt="Pillow" /> },
      { role: 'Typeface',      name: 'Poppins',                       icon: <Icon slug="googlefonts" color="4285F4" alt="Google Fonts" /> },
    ],
  },
  {
    cat: 'Application',
    note: 'Typed configuration and secrets that fail closed at startup.',
    items: [
      { role: 'Language',      name: 'Python',        ver: '3.11',    icon: <Icon slug="python" color="3776AB" alt="Python" /> },
      { role: 'Validation',    name: 'Pydantic',      ver: '2.13.0',  icon: <Icon slug="pydantic" color="E92063" alt="Pydantic" /> },
      { role: 'Config',        name: 'tomllib',                       icon: <Icon slug="toml" color="9C4121" alt="TOML" /> },
      { role: 'Secrets',       name: 'python-dotenv', ver: '1.2.0',   icon: <Icon slug="dotenv" color="ECD53F" alt="python-dotenv" /> },
      { role: 'Integrity',     name: 'SHA-256 pin',                   icon: <Icon svg={INTEGRITY_SVG} alt="SHA-256 model integrity" /> },
    ],
  },
  {
    cat: 'Tooling & Delivery',
    note: '100 tests, two linters, and a clean gate before every commit.',
    items: [
      { role: 'Build partner', name: 'Codex',                         icon: <Icon svg={OPENAI_SVG} alt="Codex" /> },
      { role: 'Editor',        name: 'VS Code',                       icon: <Icon svg={VSCODE_SVG} alt="Visual Studio Code" /> },
      { role: 'Tests',         name: 'pytest',        ver: '9.1.0',   icon: <Icon slug="pytest" color="0A9EDC" alt="pytest" /> },
      { role: 'Lint',          name: 'Ruff',          ver: '0.15.0',  icon: <Icon slug="ruff" color="D7FF64" alt="Ruff" /> },
      { role: 'Format',        name: 'Black',         ver: '26.5.0',  icon: <Icon slug="black" color="E4E4E7" alt="Black" /> },
      { role: 'Packaging',     name: 'uv',                            icon: <Icon slug="uv" color="DE5FE9" alt="uv" /> },
      { role: 'Build backend', name: 'Hatchling',                     icon: <Icon svg={HATCHLING_SVG} alt="Hatchling" /> },
      { role: 'Version control', name: 'Git',                         icon: <Icon slug="git" color="F05032" alt="Git" /> },
      { role: 'Source host',   name: 'GitHub',                        icon: <Icon slug="github" color="E4E4E7" alt="GitHub" /> },
    ],
  },
]

export default function TechStack() {
  return (
    <section id="techstack" className="relative py-32 z-10" style={{ background: '#070707' }}>
      <div className="max-w-[1100px] mx-auto px-8">
        <Reveal>
          <p className="micro-label font-bold uppercase text-zinc-300/90 mb-5">Stack</p>
        </Reveal>

        <Reveal delay={1}>
          <h2
            className="font-black tracking-[-0.04em] leading-none text-white mb-12"
            style={{ fontSize: 'clamp(2.35rem,5vw,4rem)' }}
          >
            Mature parts, assembled{' '}
            <span className="text-zinc-300/88">with intent</span>
          </h2>
        </Reveal>

        <Reveal delay={1}>
          <div className="si-feat-mitsu mb-3">
            <div className="si-feat-ico-mitsu" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 21V12M12 12V7.5M8 21v-6.5M16 21v-6.5M5 17.5 8 14.5M19 17.5 16 14.5" />
                <circle cx="12" cy="4.6" r="2.1" />
              </svg>
            </div>
            <div>
              <div className="si-feat-eyebrow-mitsu">Primary runtime profile</div>
              <div className="si-feat-name-mitsu">MediaPipe + Win32 + OpenAI</div>
              <div className="si-feat-desc-mitsu">
                On-device hand tracking driving real Windows window handles, with an explicit,
                user-initiated voice path layered on top. Nothing on the continuous-motion path
                touches the network.
              </div>
            </div>
            <div className="si-feat-pills-mitsu">
              <span className="si-feat-pill-mitsu">21-point tracking</span>
              <span className="si-feat-pill-mitsu">Mixed-DPI safe</span>
              <span className="si-feat-pill-mitsu">100 tests</span>
              <span className="si-feat-pill-mitsu">Kill switch</span>
              <span className="si-feat-pill-mitsu">SHA-256 pinned model</span>
            </div>
          </div>
        </Reveal>

        <div className="stack-layers-mitsu">
          {LAYERS.map((layer, layerIdx) => (
            <Reveal key={layer.cat} delay={Math.min(layerIdx + 1, 6)}>
              <div className="stack-layer-mitsu">
                <div className="sl-cat-mitsu">
                  {layer.cat}
                  <span className="sl-cat-note-mitsu">{layer.note}</span>
                </div>
                <div className="sl-cards-mitsu">
                  {layer.items.map((item) => (
                    <div key={`${layer.cat}-${item.name}`} className="si-mitsu">
                      <div className="si-icon-mitsu">{item.icon}</div>
                      <div className="si-text-mitsu">
                        <div className="si-role-mitsu">{item.role}</div>
                        <div className="si-name-mitsu">
                          {item.name}
                          {item.ver ? <span className="si-ver-mitsu">{item.ver}</span> : null}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  )
}
