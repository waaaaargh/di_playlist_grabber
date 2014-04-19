# Digitally Imported playlist grabber for MPD

## Purpose

Download all DI.fm playlists in one go and store them in m3u format

## Usage

```
di.py [--key=YOURLISTENINGKEY] [--destination=PLAYLISTDIR] <quality>
```
where:

* `YOURLISTENINGKEY` is the "listening key" you get from the DI website if you're a premium subscriber
* `PLAYLISTDIR` is the directory where you store your playlists. If you use mpd, it should be `/var/lib/mpd/playlists` in most cases.
* `<QUALITY>` is the stream quality of your choice, has to be one of:
  * `40kaac`
  * `96kmp3`
  * `64kaac`
  * `128kaac`
  * `256kmp3`
