# Glitching Video

制作 h264 视频花屏效果。

## 用法

```bash
python3 glitch.py input.mp4 output.mp4 3     # 删除第 3 个 I 帧
```

## 原理

```
ffmpeg 提取裸码流          ← 把 MP4 的壳剥掉，拿到纯 H.264 字节
data[s:e] = b'\x00' * N   ← 把找到的 I 帧数据全填零
ffmpeg 封装回 MP4          ← 把字节塞回壳里
ffmpeg 重编码              ← 解码（产生拖影）→ 编码（烘焙进像素）
```

## 依赖

Python 3 + ffmpeg
# glitching-video
