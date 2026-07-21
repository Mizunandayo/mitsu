# Screenshots

Drop PNGs here using these exact filenames. Each one is already wired into a
component — no code change is needed once the file exists. Until then a labelled
dashed placeholder renders in its place, so the layout never collapses.

| Filename | Used in | What to capture |
| --- | --- | --- |
| `heroimage.png` | `Hero.jsx` | The `MITSU Debug` window with live hand landmarks drawn, gesture state, and physical-pixel pointer coordinates visible. |
| `workflow.png` | `Workflow.jsx` | The full loop in one frame — camera overlay on one side, a window mid-glide on the other. |
| `voicecommand.png` | `OpenAI.jsx` | Push-to-talk capture with the transcript and the parsed action / target / destination. |
| `crossdrag.png` | `Features.jsx` | A window caught mid-glide between the laptop display and the external monitor. |
| `shelf.png` | `Features.jsx` | The V-sign shelf listing minimized windows. |
| `overlay.png` | `Features.jsx` | Debug overlay showing gesture state and the resolved window handle. |
| `micpicker.png` | `Features.jsx` | The Qt microphone selector listing input devices. |

## Capture notes

- Shoot at 16:9 where possible. The components accept any aspect, but a
  consistent ratio keeps the grid even.
- 1920×1080 or larger. These are displayed up to 1100px wide on a high-DPI
  screen, so anything smaller will look soft.
- Keep the desktop tidy. The screenshots are the proof, and a cluttered
  background reads as noise rather than evidence.
- For `crossdrag.png`, framing both monitors in one shot is worth the awkward
  angle. That single image is the strongest thing on the page.

## Adding a new slot

`ImagePlaceholder` takes `src`, `label`, and `alt`. It renders the real image
when `src` resolves and falls back to the labelled slot when it does not:

```jsx
<ImagePlaceholder
  src="/screenshots/yourfile.png"
  label="Short description shown in the empty state"
  alt="Accessible description of the screenshot"
/>
```
