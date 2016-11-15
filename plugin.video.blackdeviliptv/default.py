# -*- coding: utf-8 -*-

import json
import requests
import sys
import urllib, urllib2
import urlparse
import xbmc
import base64
import xbmcaddon
import xbmcgui
import xbmcplugin
import xmltodict
import addon_vars
from und3ad.kodi_specific import *
from und3ad.kodi_specific.api import my_account as ma
from und3ad.kodi_specific.api import panel_auth
from und3ad.kodi_specific.api import *
import und3ad.kodi_specific.pvr as pvr

def server_address():
    return panel_auth.getServer(addon_vars.panel)
server = server_address()

addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('id')

fanart = path_names.art('fanart', addon_name)
icon = path_names.art('icon', addon_name)

addon_handle = int(sys.argv[1])
base_url = sys.argv[0]
params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '')))

setting = xbmcaddon.Addon().getSetting
subuser = setting('devilsiptv_user')
subpass = setting('devilsiptv_pass')
mainuser = setting('devilssub_user')
mainpass = setting('devilssub_pass')

################UND3AD CODE########################

# identify credentials to use here
USERNAME = mainuser
PASSWORD = mainpass


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)


def decodeText(text):
    return base64.b64decode(text)


def start_up():
    # Check for Username and password
    if USERNAME == '' or PASSWORD == '':
        xbmcgui.Dialog().ok('[COLOR red]Credentials not set[/COLOR]', 'On the next screen, please enter your subscription information.')
        addon.openSettings()
        return
    if panel_auth.getAuth(USERNAME, PASSWORD, addon_vars.panel):
        return True
    return

###SHOW DETAILS###
def my_account():
    ma.show_account(USERNAME, PASSWORD, addon_vars.panel, icon, fanart)


##############END OF UND3AD CODE################################

def live_tv():
    xbmc.log(str(route.params))
    xtream_codes.show_live_television_categories(server, USERNAME, PASSWORD, fanart, icon)

def show_tv_playlist(cat_id):
    xbmc.log(str(route.params))
    xtream_codes.show_television_channels_for_category(server, USERNAME, PASSWORD, fanart, icon)

def playevl():
    player.play(fanart, icon)

def configure_pvr():
    pvr.enable_pvr_iptvsimple()
    iptvUrl = '%s/get.php?username=%s&password=%s&type=m3u&output=hls'% (server,USERNAME,PASSWORD)
    addons.checkSetAddonSettings(addon_vars.pvrID, addon_vars.m3uUrlId, iptvUrl)
    addons.checkSetAddonSettings(addon_vars.pvrID, addon_vars.epgUrlId, addon_vars.epgUrl)
    xbmc.executebuiltin('PVR.StartManager')

xbmc.log(str(params))
try:
    mode = params['mode']
except:
    mode = None
try:
    action = params['action']
except:
    action = None
try:
    content = params['content']
except:
    content = None
try:
    name = params['name']
except:
    name = None
try:
    url = params['url']
except:
    url = None
try:
    image = params['image']
except:
    image = None
try:
    fanart = params['fanart']
except:
    fanart = None
    #und3ad
try:
    cat_id = params['cat_id']
except:
    cat_id = None
try:
    channel_name = params['channel_name']
except:
    channel_name = None
try:
    channel_image = params['channel_image']
except:
    channel_image = None
try:
    channel_stream_url = params['channel_stream_url']
except:
    channel_stream_url = None
    #und3ad
if url != None:
    pass

if action == None and mode == None:
    start = start_up()
    if start == True:
        from resources.lib.indexers import devilsoriginstreams

        devilsoriginstreams.indexer().root()


elif action == 'directory':
    start = start_up()
    if start == True:
        from resources.lib.indexers import devilsoriginstreams

        devilsoriginstreams.indexer().get(url)

elif action == 'ivuesport':
    runstring = 'RunScript(script.ivuesport)'
    xbmc.executebuiltin(runstring)

elif action == 'developer':
    from resources.lib.indexers import devilsoriginstreams

    devilsoriginstreams.indexer().developer()

elif action == 'play':
    start = start_up()
    if start == True:
        from resources.lib.indexers import devilsoriginstreams

        devilsoriginstreams.resolver().play(url)

elif action == 'browser':
    from resources.lib.indexers import devilsoriginstreams

    devilsoriginstreams.resolver().browser(url)

elif action == 'search':
    from resources.lib.indexers import devilsoriginstreams

    devilsoriginstreams.indexer().search()

elif action == 'addSearch':
    from resources.lib.indexers import devilsoriginstreams

    devilsoriginstreams.indexer().addSearch(url)

elif action == 'delSearch':
    from resources.lib.indexers import devilsoriginstreams

    devilsoriginstreams.indexer().delSearch()

elif action == 'openSettings':
    from resources.lib.modules import control

    control.openSettings()

elif action == 'addView':
    from resources.lib.modules import views

    views.addView(content)

elif action == 'downloader':
    from resources.lib.modules import downloader

    downloader.downloader()

elif action == 'addDownload':
    from resources.lib.modules import downloader

    downloader.addDownload(name, url, image)

elif action == 'removeDownload':
    from resources.lib.modules import downloader

    downloader.removeDownload(url)

elif action == 'startDownload':
    from resources.lib.modules import downloader

    downloader.startDownload()

elif action == 'startDownloadThread':
    from resources.lib.modules import downloader

    downloader.startDownloadThread()

elif action == 'stopDownload':
    from resources.lib.modules import downloader

    downloader.stopDownload()

elif action == 'statusDownload':
    from resources.lib.modules import downloader

    downloader.statusDownload()

elif action == 'trailer':
    from resources.lib.modules import trailer

    trailer.trailer().play(name)

elif action == 'clearCache':
    from resources.lib.modules import cache

    cache.clear()

elif action == 'todaysSchedule':
	from resources.lib.modules import scheduleBuilder
	scheduleBuilder.getTodaysSchedule()

elif action == 'tomorrowsSchedule':
	from resources.lib.modules import scheduleBuilder
	scheduleBuilder.getTomorrowsSchedule()

#####UND3AD CODE####
elif action == 'startup':
    start_up()
elif action == 'myaccount':
    my_account()
elif action == 'livetv':
    live_tv()
elif action == 'configure_pvr':
    configure_pvr()
elif mode == 'show_tv_playlist':
    show_tv_playlist(cat_id)
elif mode == 'play':
    playevl()