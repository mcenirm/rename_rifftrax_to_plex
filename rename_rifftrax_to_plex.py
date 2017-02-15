#!/usr/bin/env python3

from __future__ import print_function
import os
import sys

import configparser

from fuzzywuzzy import process
import tvdb_api

if len(sys.argv) < 2:
    print("Usage: {0} downloaded_file ...".format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)

SERIES_NAME = 'Rifftrax'

tvdb_api_config = configparser.ConfigParser()
tvdb_config_search_path = [
    '.',
    os.path.expanduser('~'),
    os.path.dirname(os.path.realpath(__file__)),
]
read_configs = tvdb_api_config.read([os.path.join(d, '.tvdb_api.cfg') for d in tvdb_config_search_path])
print(read_configs)
tvdb_api_config.write(sys.stdout)
apikey = tvdb_api_config.get('init', 'apikey')

t = tvdb_api.Tvdb(apikey=apikey)
series = t[SERIES_NAME]
episodes_by_title = {series[season][episode]['episodename']: (season, episode, series[season][episode].items()) for season in series for episode in series[season] if season > 0}

for downloaded_filename in sys.argv[1:]:
    title_and_resolution, extension = downloaded_filename.rsplit('.', 1)
    raw_title, resolution_marker = title_and_resolution.rsplit('_', 1)
    good_title = process.extractOne(raw_title, episodes_by_title.keys())[0]
    season, episode, details = episodes_by_title[good_title]
    plex_friendly_filename = '{0} - s{1:02}e{2:03} - {3}.{4}'.format(SERIES_NAME, season, episode, good_title, extension)
    print('mv '+repr(downloaded_filename)+' '+repr(plex_friendly_filename))
