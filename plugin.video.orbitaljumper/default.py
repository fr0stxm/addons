'''
These addons are only possible because websites are open and allow us to view them for free.

These addons are also only possible due to the numerous hours the kodi developers and addon developers put in to ensure that
you, the user can have as much content as you need.

However, it is incredibly clear that numerous cunts exist in the community and like nothing than to rip of the code of us,
the hard working developers. You are known, we are watching.
'''

import sys, os, xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib, urllib2, cookielib, re

settings = xbmcaddon.Addon(id='plugin.video.orbitaljumper')
cookiejar = cookielib.LWPCookieJar()
cookie_handler = urllib2.HTTPCookieProcessor(cookiejar)
opener = urllib2.build_opener(cookie_handler)
addon_id = 'plugin.video.orbitaljumper'
selfAddon = xbmcaddon.Addon(id=addon_id)
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
playbackicon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))

def CATEGORIES():
    link = openURL('http://source.orbitalstreams.pw/_jumper/home.txt')
    match = re.compile('^(.*?)\s(.*?)$', re.MULTILINE|re.DOTALL).findall(link)
    for name, rellink in match:
        addDir(name,'http://source.orbitalstreams.pw/_jumper/' + rellink,1, icon, 1)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def VIDEOLIST(url):
    link = openURL(url)
    match = re.compile('^#EXTINF:-0 tvg-logo="(.*?)",(.*?)\n(.*?);name=Orbital$', re.MULTILINE|re.DOTALL).findall(link)
    for icon, name, videourl, in match:
        addLink(name,videourl,2,icon)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def PLAYVIDEO(url, name):
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=playbackicon,thumbnailImage=playbackicon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
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


def addDir(name, url, mode, iconimage, page):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) +\
        "&name=" + urllib.quote_plus(name) + "&page=" + str(page)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="icon.png",
                           thumbnailImage=iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                     listitem=liz, isFolder=True)
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
        CATEGORIES()

    elif mode == 1:
        VIDEOLIST(url)

    elif mode == 2:
        PLAYVIDEO(url, name)


if __name__ == "__main__":
    main()
