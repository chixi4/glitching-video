#!/usr/bin/env python3
"""用法: python corrupt.py input.mp4 output.mp4 [要删的第几个I帧, 默认5]"""
import subprocess, sys, tempfile

def ffmpeg(*a): subprocess.run(["ffmpeg", "-y", *a], capture_output=True, check=True)

def find_iframes(data):
    frames, pos = [], 0
    while pos < len(data) - 4:
        if   data[pos:pos+4] == b'\x00\x00\x00\x01': hdr = pos + 4
        elif data[pos:pos+3] == b'\x00\x00\x01':     hdr = pos + 3
        else: pos += 1; continue
        if (data[hdr] & 0x1F) != 5: pos = hdr + 1; continue
        end = hdr + 1
        while end < len(data) - 3 and data[end:end+3] != b'\x00\x00\x01': end += 1
        frames.append((pos, end if end < len(data) - 3 else len(data)))
        pos = end
    return frames

inp, out = sys.argv[1], sys.argv[2]
target = int(sys.argv[3]) if len(sys.argv) > 3 else 5

with tempfile.TemporaryDirectory() as tmp:
    raw, bad, mux = f"{tmp}/a.h264", f"{tmp}/b.h264", f"{tmp}/c.mp4"
    ffmpeg("-i", inp, "-c:v", "copy", "-bsf:v", "h264_mp4toannexb", "-an", "-f", "h264", raw)
    with open(raw, "rb") as f: data = bytearray(f.read())
    s, e = find_iframes(bytes(data))[target - 1]
    data[s:e] = b'\x00' * (e - s)
    with open(bad, "wb") as f: f.write(data)
    ffmpeg("-f", "h264", "-i", bad, "-c:v", "copy", "-fflags", "+genpts", mux)
    ffmpeg("-i", mux, "-c:v", "libx264", "-preset", "fast", "-crf", "18", out)
print(f"完成 → {out}")
