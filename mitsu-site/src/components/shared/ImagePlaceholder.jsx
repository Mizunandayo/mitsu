/**
 * Dark-themed ImagePlaceholder.
 *
 * Renders a real screenshot when `src` is provided and the file exists.
 * Falls back to a labelled dashed slot so the layout never collapses while
 * screenshots are still being captured.
 *
 * Drop PNGs into `public/screenshots/` using the filenames documented in
 * `public/screenshots/README.md` and they appear with no code change.
 */
import { useState } from 'react'

export default function ImagePlaceholder({
  src,
  label = 'Screenshot',
  alt,
  aspect = '16/9',
  className = '',
}) {
  const [failed, setFailed] = useState(false)

  if (src && !failed) {
    return (
      <img
        src={src}
        alt={alt || label}
        loading="lazy"
        onError={() => setFailed(true)}
        style={{
          maxWidth: '100%',
          height: 'auto',
          display: 'block',
          margin: '0 auto',
          borderRadius: '0.75rem',
          border: '1px solid rgba(163,163,163,0.15)',
        }}
        className={className}
      />
    )
  }

  return (
    <div
      className={`w-full rounded-xl border border-dashed border-zinc-400/35 bg-zinc-700/15 flex flex-col items-center justify-center gap-2.5 ${className}`}
      style={{ aspectRatio: aspect }}
    >
      <svg width="32" height="32" viewBox="0 0 32 32" fill="none" opacity="0.3" aria-hidden="true">
        <rect x="2" y="6" width="28" height="20" rx="3" stroke="white" strokeWidth="1.4" />
        <circle cx="12" cy="16" r="4.5" stroke="white" strokeWidth="1.4" />
        <path d="M2 22l7-7 5 5 5-7 7 9" stroke="white" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      <div className="text-center px-4">
        <p className="text-[0.84rem] font-semibold text-zinc-200/90">{label}</p>
        <p className="text-[0.78rem] text-zinc-300/70 mt-0.5">
          Drop into <code className="font-mono">public/screenshots/</code>
          {src ? <> as <code className="font-mono">{src.split('/').pop()}</code></> : null}
        </p>
      </div>
    </div>
  )
}
