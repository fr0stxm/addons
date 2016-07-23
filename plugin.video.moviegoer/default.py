'''
These addons are only possible because websites are open and allow us to view them for free.

These addons are also only possible due to the numerous hours the kodi developers and addon developers put in to ensure that
you, the user can have as much content as you need.

However, it is incredibly clear that numerous cunts exist in the community and like nothing than to rip of the code of us,
the hard working developers. You are known, we are watching.
'''

import sys, os, xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib, urllib2, cookielib, re

settings = xbmcaddon.Addon(id='plugin.video.moviegoer')
cookiejar = cookielib.LWPCookieJar()
cookie_handler = urllib2.HTTPCookieProcessor(cookiejar)
opener = urllib2.build_opener(cookie_handler)
addon_id = 'plugin.video.moviegoer'
selfAddon = xbmcaddon.Addon(id=addon_id)
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
playbackicon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'playbackicon.png'))

def CATEGORIES():
    addDir('[COLOR red]Latest[/COLOR]', 'http://www.moviego.cc', 1, icon, 1)
    addDir('[COLOR red]Top 2016[/COLOR]', 'http://www.moviego.cc/top2016', 1, icon, 1)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def VIDEOLIST(url):
    link = openURL(url)
    match = re.compile('<div class="short_content">\n<a href="(.*)">\n<img src="(.*)" alt="(.*)" class=').findall(link)
    for url, thumb, name, in match:
        addLink(name,url,2,thumb)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


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


def addLink(name, url, mode, thumb):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode)\
        + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
    return ok


def addDir(name, url, mode, thumb, page):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) +\
        "&name=" + urllib.quote_plus(name) + "&page=" + str(page)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                     listitem=liz, isFolder=True)
    return ok

def PLAYVIDEO(url, name):
    link = openURL(url)
    match = re.compile('file:\s"(.*)"').findall(link)
    for video in match:
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=playbackicon,thumbnailImage=playbackicon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player().play(video, liz, False)

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
        xbmc.log("VIDEOLIST ")
        xbmc.log("VIDEOLIST ")
        VIDEOLIST(url)

    elif mode == 2:
        xbmc.log("PLAYVIDEO ")
        PLAYVIDEO(url, name)


if __name__ == "__main__":
    main()
