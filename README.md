# Prereqs

To run it you must install `youtube-dl`, `ffmpeg`, and the corresponding Python bindings, `youtube-dl` and `ffmpy`

# What does this do?

When getting live video from youtube. The site follows [Apple's HTTP streaming standards](https://developer.apple.com/library/content/documentation/NetworkingInternet/Conceptual/StreamingMediaGuide/HTTPStreamingArchitecture/HTTPStreamingArchitecture.html) AKA HLS.
So when a request is sent to the youtube direct URL, we get an M3U8 file, which contains a playlist of the available media chunks. The file looks something like this:

```
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:5
#EXT-X-MEDIA-SEQUENCE:14139
#EXT-X-DISCONTINUITY-SEQUENCE:5
#EXT-X-PROGRAM-DATE-TIME:2018-03-30T13:47:50.039+00:00
#EXTINF:5.0,
https://url-to-media.ts
#EXTINF:5.0,
https://url-to-media.ts
#EXTINF:5.0,
https://url-to-media.ts
#EXTINF:5.0,
https://url-to-media.ts
#EXTINF:5.0,
https://url-to-media.ts
#EXTINF:5.0,
https://url-to-media.ts
```

Here, we parse the file, we get the video chunks in order, download them, and transcode them from the original transport stream MPEG-2 to H.264.
The naming convention starts at 0.mp4 for the first video we download.

# Run

`python main.py https://www.youtube.com/watch?v=VIDEO-ID 93` 93 being the video format corresponding to 640x360 in youtube

## Formats:
```
91 - 256x144
92 - 426x240
93 - 640x360
94 - 854x480
95 - 1280x720
96 - 1920x1080
```