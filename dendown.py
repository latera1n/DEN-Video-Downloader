import os
import urllib.request
import sys

import time

if __name__ == '__main__':
    '''Initialize arguments.'''
    init_url = sys.argv[1]
    init_url_prefix = init_url.split('/playlist')[0]
    file_name_parts = init_url.split('/')[8].split('_')
    file_name = file_name_parts[0] + '_' + file_name_parts[1][-8:]

    '''Resolve M3U8 playlist attributes.'''
    print()
    sys.stdout.write('INFO: Resolving M3U8 playlist URL ... ')
    with urllib.request.urlopen(init_url) as f:
        m3u8_postfix = f.read().split()[-1].decode('utf-8')
    print("Done!")
    m3u8_url = init_url_prefix + '/' + m3u8_postfix

    '''Resolve video segment attributes.'''
    sys.stdout.write('INFO: Resolving video segment URLs ... ')
    with urllib.request.urlopen(m3u8_url) as f:
        m3u8_contents = f.read().decode('utf-8').split('\n')
    print("Done!")
    num_total_segments = int((len(m3u8_contents) - 6) / 2)
    video_segment_prefix = m3u8_contents[5].split('_ps0_')[0] + '_ps0_'

    '''Download video segments and concatenate together into a whole video.'''
    timestamp = int(time.time() * 100)
    os.system('mkdir ./temp_%s/' % timestamp)
    os.system('curl -o ./temp_%s/part_#1.ts %s/%s\[000-%d\].ts'
              % (timestamp, init_url_prefix, video_segment_prefix, num_total_segments - 1))
    os.system('cat ./temp_%s/part* > %s.ts' % (timestamp, file_name))
    os.system('rm -rf ./temp_%s/' % timestamp)

    print()
    print("INFO: %s download completed." % file_name)
    print()
