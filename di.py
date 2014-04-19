#!/usr/bin/env python3

from argparse import ArgumentParser
import json
import os.path
import sys
from urllib.request import urlopen

if __name__ == '__main__':
    parser = ArgumentParser(description='Grab di.fm playlists')
    parser.add_argument('--key', help='Listening key')
    parser.add_argument('--destination', help='Target directory for playlist files')
    parser.add_argument('quality', choices=["40kaac", "96kmp3", "64kaac", "128kaac", "256kmp3"], help='Stream bitrate')

    args = parser.parse_args()

    if args.quality in ['128kaac', '256kmp3'] and args.key is None:
        print("[!] Sorry, you get high quality playlists if you supply a listening key :(")
        sys.exit(1)

    # get all channels and IDs
    channels = json.loads(urlopen('http://listen.di.fm/public5').read().decode("utf-8"))
    print("[i] found %d channels." % len(channels))

    quality_to_suffix = {
        '40kaac':  '_aacplus',
        '64kaac':  '_aac',
        '96kmp3':  '',
        '128kaac': '',
        '256kmp3': '_hi',
    }

    # premium-servers
    if args.key is not None:
        di_servers = [
            'prem1.di.fm:80',
            'prem2.di.fm:80',
            'prem4.di.fm:80',
        ]

    # free (as in free beer) servers
    else:
        di_servers = [
            'pub1.di.fm:80',
            'pub2.di.fm:80',
            'pub3.di.fm:80',
            'pub4.di.fm:80',
            'pub5.di.fm:80',
            'pub6.di.fm:80',
            'pub7.di.fm:80',
            'pub8.di.fm:80',
        ]

    try:
        for channel in channels:
            playlist_name = os.path.join(args.destination or "", "di_" + channel['key'] + ".m3u")
            with open(playlist_name, 'w') as f:
                for server in di_servers:
                    stream_path = channel['key'] + quality_to_suffix[args.quality]

                    if args.key is None:
                        stream_path = 'di_' + stream_path
                    else:
                        stream_path += "?%s" % args.key

                    f.write("http://%s/%s\n" % (server, stream_path))
    except IOError:
        print("[!] Sorry, couldn't open destination file. Are you sure the base directory exists?")
