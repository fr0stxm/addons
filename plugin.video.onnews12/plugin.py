'''
These addons are only possible because websites are open and allow us to view them for free.

These addons are also only possible due to the numerous hours the kodi developers and addon developers put in to ensure that
you, the user can have as much content as you need.

However, it is incredibly clear that numerous people exist to take content and pass it off as their own. PLEASE do not do that
if you are going to borrow code, then please ensure you credit those involved.

Author: oneil from Ninjasys - @oneilxm_uk
Git: github.com/fr0stxm
Addon: News 12: Free
Thank you / Acknowledgement: Those that exist in the Kodi telegram groups.
'''

import sys, os, xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib, urllib2, cookielib, re

settings = xbmcaddon.Addon(id='plugin.video.onnews12')
cookiejar = cookielib.LWPCookieJar()
cookie_handler = urllib2.HTTPCookieProcessor(cookiejar)
opener = urllib2.build_opener(cookie_handler)
addon_id = 'plugin.video.onnews12'
selfAddon = xbmcaddon.Addon(id=addon_id)
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
playbackicon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
proxy = 'http://hls.iptv.optimum.net/news12/nipadlive/index_new.m3u8?callsign='

def VIDEOLIST():
    addLink('News 12: Bronx',proxy + 'N12BX',2,icon)
    addLink('News 12: Brooklyn',proxy + 'N12KN',2,icon)
    addLink('News 12: Connecticut',proxy + 'N12CT_WEST',2,icon)
    addLink('News 12: Hudson Valley',proxy + 'N12HV',2,icon)
    addLink('News 12: Long Island',proxy + 'N12LI_WEST',2,icon)
    addLink('News 12: New Jersey',proxy + 'N12NJ_CENTRAL',2,icon)
    addLink('News 12: Westchester',proxy + 'N12WH_WESTCHESTER',2,icon)
    addLink('News 12: Bronx [COLOR yellow]Weather[/COLOR]',proxy + 'N12TW_NYC',2,icon)
    addLink('News 12: Brooklyn [COLOR yellow]Weather[/COLOR]',proxy + 'N12TW_NYC',2,icon)
    addLink('News 12: Connecticut [COLOR yellow]Weather[/COLOR]',proxy + 'N12TW_CT',2,icon)
    addLink('News 12: Hudson Valley [COLOR yellow]Weather[/COLOR]',proxy + 'N12TW_WC',2,icon)
    addLink('News 12: Long Island [COLOR yellow]Weather[/COLOR]',proxy + 'N12TW_LI',2,icon)
    addLink('News 12: New Jersey [COLOR yellow]Weather[/COLOR]',proxy + 'N12TW_NJ',2,icon)
    addLink('News 12: Westchester [COLOR yellow]Weather[/COLOR]',proxy + 'N12TW_WC',2,icon)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PLAYVIDEO(url, name):
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    xbmc.Player().play(url, liz, False)

def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params)-1] == '/'):
            params = params[0:len(params)-2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


def addLink(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode)\
        + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="icon.png",
                           thumbnailImage=iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                     listitem=liz, isFolder=False)
    return ok

def openURL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link


def main():
    params = get_params()
    url = None
    name = None
    mode = None
    page = 1

    try:
        url = urllib.unquote_plus(params["url"])
    except:
        pass
    try:
        name = urllib.unquote_plus(params["name"])
    except:
        pass
    try:
        mode = int(params["mode"])
    except:
        pass
    try:
        page = int(params["page"])
    except:
        pass

    if mode == None or url == None or len(url) < 1:
        VIDEOLIST()

    elif mode == 1:
        VIDEOLIST(url)

    elif mode == 2:
        PLAYVIDEO(url, name)


if __name__ == "__main__":
    main()
