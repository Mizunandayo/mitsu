import { Reveal } from '../hooks/useScrollReveal.jsx'

const DownArrow = () => (
  <svg width="11" height="14" viewBox="0 0 12 16" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M6 2v12M2 10.5 6 14.5 10 10.5" />
  </svg>
)

const RightArrow = () => (
  <svg width="16" height="14" viewBox="0 0 18 14" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M1 7h15M11.5 2 16.5 7l-5 5" />
  </svg>
)

export default function Architecture() {
  return (
    <section id="architecture" className="relative py-32 z-10" style={{ background: '#070707' }}>
      <div className="max-w-[1100px] mx-auto px-8">
        <Reveal>
          <p className="micro-label font-bold uppercase text-zinc-300/90 mb-5">Engineering</p>
        </Reveal>

        <Reveal delay={1}>
          <h2 className="font-black tracking-[-0.04em] leading-none text-white mb-5" style={{ fontSize: 'clamp(2.4rem,5vw,4rem)' }}>
            Local handles reflexes.<br/>
            <span className="text-zinc-300/88">Cloud handles cognition.</span>
          </h2>
        </Reveal>

        <Reveal delay={2}>
          <div className="eng-banner-mitsu mb-10">
            <div>
              <div className="eng-banner-tag-mitsu">Solo build · 8 days · OpenAI Build Week 2026</div>
              <div className="eng-banner-claim-mitsu">One decision everything else follows from.</div>
              <div className="eng-banner-sub-mitsu">
                Perception and action are separable from cognition — so when the network drops,
                the part you touch with your hands does not notice.
              </div>
            </div>
            <div className="eng-lang-strip-mitsu">
              <div className="eng-lang-mitsu"><span className="eng-lang-dot-mitsu" style={{ background: '#38bdf8' }} />Python 3.11 · MediaPipe + OpenCV perception</div>
              <div className="eng-lang-mitsu"><span className="eng-lang-dot-mitsu" style={{ background: '#4ade80' }} />pywin32 + ctypes · Win32 window control</div>
              <div className="eng-lang-mitsu"><span className="eng-lang-dot-mitsu" style={{ background: '#c084fc' }} />OpenAI · transcription + tool reasoning</div>
              <div className="eng-lang-mitsu"><span className="eng-lang-dot-mitsu" style={{ background: '#fbbf24' }} />pytest · 100 tests, no webcam required</div>
            </div>
          </div>
        </Reveal>

        <Reveal delay={3}>
          <div className="arch-wrap-mitsu">
            <div className="arch-label-mitsu">System architecture — data flow</div>

            <div className="arch-journey-mitsu">
              <div className="arch-jstep-mitsu an-cyan-mitsu">
                <div className="arch-jstep-num-mitsu">01</div>
                <div>
                  <div className="arch-jstep-headline-mitsu">Perception runs entirely on the device</div>
                  <div className="arch-jstep-desc-mitsu">
                    The webcam feeds MediaPipe Hand Landmarker, which emits 21 3D points per frame.
                    A One Euro filter smooths them — stable when your hand is still, responsive when it moves fast.
                    Raw frames never leave the machine.
                  </div>
                  <div className="arch-jstep-tech-mitsu">OpenCV capture · MediaPipe Tasks · One Euro filter · SHA-256 pinned model</div>
                </div>
              </div>

              <div className="arch-jconn-mitsu">
                <div className="arch-jconn-track-mitsu">
                  <div className="arch-jconn-vline-mitsu" />
                  <div className="arch-jconn-arr-mitsu"><DownArrow /></div>
                  <div className="arch-jconn-vline-mitsu" />
                </div>
                <span className="arch-conn-badge-mitsu cb-blue-mitsu">Smoothed landmarks &rarr; gesture state machine</span>
              </div>

              <div className="arch-jstep-mitsu an-violet-mitsu">
                <div className="arch-jstep-num-mitsu">02</div>
                <div>
                  <div className="arch-jstep-headline-mitsu">One state machine fuses hand and voice</div>
                  <div className="arch-jstep-desc-mitsu">
                    IDLE &rarr; TRACKING &rarr; GRIPPED &rarr; RELEASING. Voice target-lock injects straight into
                    GRIPPED from any state, so a named window becomes the drag target without your hand
                    ever being over it. Three behaviours emerge from one machine, not three modes.
                  </div>
                  <div className="arch-jstep-tech-mitsu">Deterministic state machine · fixed command grammar · target latch · single-writer queue</div>
                </div>
              </div>

              <div className="arch-jconn-mitsu">
                <div className="arch-jconn-track-mitsu">
                  <div className="arch-jconn-vline-mitsu" />
                  <div className="arch-jconn-arr-mitsu"><DownArrow /></div>
                  <div className="arch-jconn-vline-mitsu" />
                </div>
                <span className="arch-conn-badge-mitsu cb-green-mitsu">Resolved intent &rarr; bounded tool call</span>
              </div>

              <div className="arch-jstep-mitsu an-emerald-mitsu">
                <div className="arch-jstep-num-mitsu">03</div>
                <div>
                  <div className="arch-jstep-headline-mitsu">Action lands on real Win32 windows, safely</div>
                  <div className="arch-jstep-desc-mitsu">
                    Per-monitor DPI awareness is set before any window call, so coordinates are true
                    physical pixels. Movement is clamped against the combined virtual-desktop box, which is
                    why crossing monitors is not a special case — it is just continued motion.
                  </div>
                  <div className="arch-jstep-tech-mitsu">EnumWindows · WindowFromPoint · SetWindowPos · screeninfo bounds · global kill switch</div>
                </div>
              </div>
            </div>

            <div className="arch-zoom-wrap-mitsu">
              <div className="arch-zoom-header-mitsu">
                <div className="arch-zoom-tag-mitsu">Step 02 in detail</div>
                <div className="arch-zoom-name-mitsu">Two-tier intent engine</div>
                <div className="arch-zoom-sub-mitsu">Utterance &rarr; Intent &rarr; ToolCall</div>
              </div>
              <div className="arch-zoom-body-mitsu">
                <div className="arch-pipe-mitsu">
                  <div className="arch-step-mitsu">
                    <div className="arch-step-num-mitsu">CAPTURE</div>
                    <div className="arch-step-name-mitsu">Push-to-talk clip</div>
                    <div className="arch-step-detail-mitsu">Deliberate key press starts and ends recording. A local RMS guard drops silent clips.</div>
                    <span className="arch-step-time-mitsu">on demand</span>
                  </div>

                  <div className="arch-pipe-arr-mitsu"><RightArrow /></div>

                  <div className="arch-step-mitsu arch-step-fast-mitsu">
                    <div className="arch-step-num-mitsu">GRAMMAR</div>
                    <div className="arch-step-name-mitsu">Fixed local parse</div>
                    <div className="arch-step-detail-mitsu">verb + app name + optional destination. Deterministic, offline, and the demo-critical path.</div>
                    <span className="arch-step-time-mitsu">local</span>
                  </div>

                  <div className="arch-pipe-arr-mitsu"><RightArrow /></div>

                  <div className="arch-step-mitsu arch-step-llm-mitsu">
                    <div className="arch-step-num-mitsu">ESCALATE</div>
                    <div className="arch-step-name-mitsu">GPT-5.6 tool reasoning</div>
                    <div className="arch-step-detail-mitsu">Only for phrasing the grammar rejects. Bounded rounds, guarded by a circuit breaker.</div>
                    <span className="arch-step-time-mitsu">~1.5s budget</span>
                  </div>

                  <div className="arch-pipe-arr-mitsu"><RightArrow /></div>

                  <div className="arch-step-mitsu">
                    <div className="arch-step-num-mitsu">EXECUTE</div>
                    <div className="arch-step-name-mitsu">Typed tool registry</div>
                    <div className="arch-step-detail-mitsu">Both tiers converge on the same four tools. Only eligible top-level app windows are touched.</div>
                    <span className="arch-step-time-mitsu">deterministic</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="arch-legend-mitsu">
              <div className="arch-leg-item-mitsu"><span className="arch-leg-dot-mitsu" style={{ background: '#38bdf8' }} />On-device perception</div>
              <div className="arch-leg-item-mitsu"><span className="arch-leg-dot-mitsu" style={{ background: '#4ade80' }} />Deterministic local tier</div>
              <div className="arch-leg-item-mitsu"><span className="arch-leg-dot-mitsu" style={{ background: '#c084fc' }} />GPT-5.6 escalation</div>
              <div className="arch-leg-item-mitsu"><span className="arch-leg-dot-mitsu" style={{ background: '#fbbf24' }} />Safety and fail-safe</div>
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  )
}
