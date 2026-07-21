# MITSU (見つ)

**Point at nothing, say a name, and your windows move.**

MITSU is a Windows-first, hand-and-voice window manager for multi-monitor
desktops. It treats windows as physical objects: grip a window with a hand
gesture and move it across the virtual desktop, or use a short spoken command
to restore and relocate an app.

Built for **OpenAI Build Week 2026**, **Apps for Your Life**.

## What Works

- Local webcam hand tracking with MediaPipe Hand Landmarker.
- Relative hand-drag of eligible Windows app windows, including multi-monitor
  movement and mixed-DPI virtual-desktop bounds.
- One Euro smoothing, grip state machine, hand-loss recovery, and a global
  kill switch.
- Hand pointer control, two-fingertip click, back/forward side gestures,
  minimize, maximize, and a V-sign minimized-window shelf.
- Live physical-pixel cursor coordinates and a mixed-DPI-safe overlay.
- Explicit push-to-talk transcription with OpenAI, fixed local command grammar,
  device microphone selection, and a silence guard.
- Optional GPT-5.6 tool-calling reasoning adapter for unsupported commands;
  disabled by default so local controls remain network-independent.

## Architecture

```text
webcam -> MediaPipe -> One Euro filter -> gesture state machine -> Win32 window APIs
                                         |
microphone -> push-to-talk -> OpenAI transcription -> fixed command grammar
                                         |
                              optional GPT-5.6 tool reasoning
```

The continuous hand-control path is local. Camera frames are never uploaded.
Only an explicit push-to-talk clip is sent to OpenAI for the optional voice
feature. The GPT-5.6 path is guarded by a circuit breaker and is off by default.

## Requirements

- Windows 11
- Python 3.11
- Webcam
- A microphone for optional voice commands
- An OpenAI API key for optional voice transcription and cloud reasoning

## Install And Run

Use Windows PowerShell from the repository root.

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install pytest==9.1.0 ruff==0.15.0 black==26.5.0
Copy-Item .env.example .env
```

For voice, set `OPENAI_API_KEY` in `.env`. Leave it empty for a fully local
gesture-only run. Never commit `.env`.

Download the MediaPipe model once. The model is ignored by Git; the committed
SHA-256 pin is verified before MITSU loads it.

```powershell
.venv\Scripts\python.exe scripts\bootstrap_hand_model.py --trust-on-first-use
.venv\Scripts\python.exe -m mitsu.app
```

The application starts a `MITSU Debug` camera window. `Q` or `Esc` exits safely.

## Controls

| Action | Gesture Or Input |
| --- | --- |
| Move a window | Thumb-index pinch or closed-fist grip, then move your hand |
| Release | Open your hand |
| Maximize a held window | Open a wide palm before release |
| Pointer | Hold index and middle fingertips together |
| Click | Dip both close fingertips slightly toward your wrist |
| Back / Forward | Pointer pose plus raised pinky / raised ring finger |
| Minimize | Index-middle-ring pose followed by a downward stroke |
| Window shelf | Hold a V sign, then point at a minimized-window row and click |
| Voice | Press `V` to start, speak, then press `V` again to send |
| Choose microphone | Press `M`, choose an input device, then select **Use microphone** |
| Emergency stop | `Ctrl` + `Alt` + `Shift` + `M` |

Supported fixed voice commands include:

```text
show Discord
open Paint
grab VS Code
show Discord on the left screen
Can you show Discord on my screen
```

## Configuration

Runtime settings are in [config/default.toml](config/default.toml). MITSU
validates them with Pydantic at startup and fails closed on unknown keys. The
microphone selector changes the active input only in memory for the current run.

## Verification

```powershell
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\ruff.exe check .
.venv\Scripts\black.exe --check .
```

## Safety And Privacy

- Per-monitor DPI awareness is enabled before Win32 window calls.
- Only eligible top-level app windows are acted on; MITSU skips shell, system,
  and self windows and never injects arbitrary code into other processes.
- Movement uses `SWP_NOSIZE | SWP_NOZORDER | SWP_NOACTIVATE` where applicable.
- The model downloader uses HTTPS, a size limit, and SHA-256 verification.
- API keys stay in the git-ignored `.env`; logging redacts secret-looking values.
- Push-to-talk audio stays in memory, uses a temporary WAV only for the explicit
  API request, and is deleted immediately after the request completes.

## Built With Codex And GPT-5.6

Codex was used throughout the Build Week implementation to accelerate test-first
development, Windows API integration, MediaPipe plumbing, gesture-state-machine
coverage, coordinate math, and the final safety/observability pass.

The product decisions remained deliberate: local perception and movement are
kept off the network; whole-window movement is prioritized over fragile
tab-level control; and fixed voice grammar remains the reliable path. MITSU also
contains a GPT-5.6 function-calling reasoning adapter over the same validated
window-tool layer for flexible, out-of-grammar commands. It is disabled by
default for predictable offline local behavior and can be enabled only with an
OpenAI API key and a valid configured model.

## License

[MIT](LICENSE)
