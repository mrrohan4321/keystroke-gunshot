#!/usr/bin/env python3
"""Keystroke Gunshot - every key you press (in any app) plays a gunshot.

Run:   python gunshot.py
Stop:  Ctrl+C in the terminal where it is running.
"""
import argparse
import os
import sys

import numpy as np
import pygame
from pynput import keyboard

SAMPLE_RATE = 44100


def synth_gunshot(rng: np.random.Generator, length: float = 0.9) -> np.ndarray:
    """Punchier gunshot: sharp crack + heavy thump + distortion + echo."""
    n = int(SAMPLE_RATE * length)
    t = np.arange(n) / SAMPLE_RATE
    noise = rng.uniform(-1, 1, n)

    # Crack: high-passed noise, very short and sharp
    smooth = np.convolve(noise, np.ones(8) / 8, mode="same")
    crack = (noise - smooth) * np.exp(-t / 0.008) * 1.5

    # Body: mid noise
    k = int(rng.integers(10, 16))
    body = np.convolve(noise, np.ones(k) / k, mode="same") * np.exp(-t / 0.05)

    # Thump: deeper, punchier bass sweep
    f0 = rng.uniform(150, 220)
    freq = 40 + (f0 - 40) * np.exp(-t / 0.025)
    phase = 2 * np.pi * np.cumsum(freq) / SAMPLE_RATE
    thump = np.sin(phase) * np.exp(-t / 0.12)

    mix = 1.4 * crack + 0.8 * body + 1.2 * thump
    mix = np.tanh(mix * 2.0)  # distortion = punchy / loud feel

    # Echo (two quiet repeats, like a room)
    for delay, gain in ((0.09, 0.3), (0.18, 0.15)):
        d = int(delay * SAMPLE_RATE)
        echo = np.zeros(n)
        echo[d:] = mix[:-d] * gain
        mix = mix + echo

    return mix / np.max(np.abs(mix)) * 0.9


def to_sound(mono: np.ndarray) -> pygame.mixer.Sound:
    pcm = (mono * 32767).astype(np.int16)
    stereo = np.ascontiguousarray(np.column_stack((pcm, pcm)))
    return pygame.sndarray.make_sound(stereo)


def main() -> None:
    parser = argparse.ArgumentParser(description="Play a gunshot on every keystroke.")
    parser.add_argument("--sound", help="path to your own .wav/.ogg to use instead of the synthesized shot")
    parser.add_argument("--volume", type=float, default=0.7, help="volume from 0.0 to 1.0 (default 0.7)")
    parser.add_argument("--variants", type=int, default=8, help="number of synthesized variants (default 8)")
    args = parser.parse_args()

    pygame.mixer.pre_init(SAMPLE_RATE, -16, 2, 256)
    pygame.mixer.init()
    pygame.mixer.set_num_channels(32)  # lets fast typing overlap shots

    sound_path = args.sound
    if not sound_path:
        default = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shot.wav")

        if os.path.exists(default):
            sound_path = default

    if sound_path:
        sounds = [pygame.mixer.Sound(sound_path)]
    else:
        rng = np.random.default_rng()
        sounds = [to_sound(synth_gunshot(rng)) for _ in range(max(1, args.variants))]

    volume = min(max(args.volume, 0.0), 1.0)
    for s in sounds:
        s.set_volume(volume)

    held = set()  # ignore OS key-repeat while a key is held down
    idx = 0

    def on_press(key):
        nonlocal idx
        if key in held:
            return
        held.add(key)
        sounds[idx % len(sounds)].play()
        idx += 1

    def on_release(key):
        held.discard(key)

    print("Gunshot keyboard is running. Press Ctrl+C here to stop.")
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    try:
        while listener.is_alive():
            listener.join(0.5)  # short wait so Ctrl+C can get through
    except KeyboardInterrupt:
        pass
    finally:
        listener.stop()
        print("\nStopped.")


if __name__ == "__main__":
    main()

