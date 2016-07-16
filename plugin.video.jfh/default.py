import sys
import os
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import urllib2
import cookielib
import re

settings = xbmcaddon.Addon(id='plugin.video.jfh')
cookiejar = cookielib.LWPCookieJar()
cookie_handler = urllib2.HTTPCookieProcessor(cookiejar)
opener = urllib2.build_opener(cookie_handler)


def CATEGORIES():
    link = openURL('http://www.perfectgirls.net/')
    match = re.compile('<a href="/category/([0-9][0-9])/(.*)">(.*)</a>').findall(link)
    addDir('Latest', 'http://www.perfectgirls.net/', 1, '', 1)
    for page_id, channame, name in match:
        addDir(name,
               ('http://www.perfectgirls.net/category/' + page_id + '/' + channame),
               2, '', 1)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def VIDEOLIST(url):
    link = openURL(url)
    match = re.compile('-->\n<a href="/([0-9]+)/(.*)" title="(.*)">').findall(link)
    for v_id, videourl, name, in match:
        addLink(name,'http://www.perfectgirls.net' + v_id + '/' + videourl,3,'icon.png')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def PLAYVIDEO(url):
    link = openURL(url)
    match = re.compile('get\("(.*)", function').findall(link)
    for configurl in match:
        link = openURL('http://www.perfectgirls.net' + configurl)
        match2 = re.compile('(.*)').findall(link)
        if match2:
            xbmc.Player().play(match2[-1])


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
        xbmc.log("VIDEOLIST " + url)
        xbmc.log("VIDEOLIST " + str(page))
        VIDEOLIST(url)

    elif mode == 2:
        xbmc.log("PLAYVIDEO " + url)
        PLAYVIDEO(url)


if __name__ == "__main__":
    main()
