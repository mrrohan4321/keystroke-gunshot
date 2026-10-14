\# Keystroke Gunshot



Every key you press, in \*\*any\*\* app, plays a gunshot sound. Works system-wide.



By default the gunshot is synthesized in code, so no audio file is needed.



\## Install



```bash

git clone https://github.com/<your-username>/keystroke-gunshot.git

cd keystroke-gunshot

python -m venv .venv

\# Windows: .venv\\Scripts\\activate    macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt

```



No git? Click the green \*\*Code\*\* button on GitHub, choose \*\*Download ZIP\*\*, unzip it, then follow the same steps.



\## Run



```bash

python gunshot.py

```



Stop with `Ctrl+C` in the terminal.



Options:



```bash

python gunshot.py --volume 0.4            # quieter

python gunshot.py --sound my\_shot.wav     # use your own sound

```



Want a real gunshot? Put a file named `shot.wav` in the same folder and it will be used automatically.



\## Platform notes



\- \*\*Windows:\*\* works out of the box.

\- \*\*macOS:\*\* give your terminal \*Accessibility\* and \*Input Monitoring\* permission

&#x20; (System Settings > Privacy \& Security), then restart the terminal.

\- \*\*Linux:\*\* works on X11. Global key capture does not work on Wayland.



\## Privacy



This app only listens for key presses to trigger a sound. It does not record,

store, or send what you type anywhere. The whole source is in `gunshot.py`.

