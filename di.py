import sys
from argparse import ArgumentParser
from urllib2 import urlopen
import json

from os.path import join as opj

if __name__ == '__main__':
    parser = ArgumentParser(description='grab di.fm playlists')
    parser.add_argument('quality', help='one of: 40kaac, 96kmp3, 64kaac, 128kaac, 256kmp3')
    parser.add_argument('--key', required=False, help='Listening key')
    parser.add_argument('--target', required=False, help='Target directory for playlists')

    args = parser.parse_args()

    if args.quality not in ['40kaac', '96kmp3', '64kaac', '128kaac', '256kmp3']:
        print("[!] Unrecognized quality option :(")
        sys.exit(1)
    if args.quality in ['128kaac', '256kmp3'] and args.key is None:
        print("[!] Sorry, you get high quality playlists if you supply a listening key :(")
        sys.exit(1)

    # get all channels and IDs
    channels = json.loads(urlopen('http://listen.di.fm/public5').read())
    print("[i] found %i channels." % len(channels))

    if args.key is not None:
        di_servers = [
            'prem1.di.fm:80',
            'prem2.di.fm:80',
            'prem4.di.fm:80',
        ]
        
        quality_to_suffix = {
            '128kaac': '',
            '256kmp3': '_hi',
        }
        
    else:
        di_servers = [
            'pub1.di.fm:80',
            'pub2.di.fm:80',
            'pub3.di.fm:80',
            'pub4.di.fm:80',
            'pub5.di.fm:80',
            'pub6.di.fm:80',
            'pub7.di.fm:80',
            'pub8.di.fm:80'
        ]
            
        quality_to_suffix = {
            '40kaac': '_aacplus',
            '64kmp3': '',
            '64kaac': '_aac'
        }

    for  channel in channels:
        try:
            with open(opj(args.target or "", "di_"+channel['key']+".m3u"), 'w') as f:
                for server in di_servers:
                    stream_uri="http://"
                    stream_uri+=server+"/"
                    if args.key is None:
                        stream_uri+='di_'
                    stream_uri+=channel['key']+quality_to_suffix[args.quality]
                    if args.key is not None:
                        stream_uri += "?"+args.key
                    f.write(stream_uri)
                    f.write("\n")
        except IOError:
            print("[!] Sorry, couldn't open destination file. Are you sure the base directory exists?")
