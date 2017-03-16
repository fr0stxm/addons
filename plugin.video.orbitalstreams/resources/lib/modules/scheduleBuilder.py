import re, os, urllib, urllib2, cookielib, xbmc, xbmcgui

#scheduleDump = 'C:\Users\chris\Desktop\scheduleDump.txt'

ADDON_ID = 'plugin.video.blackdeviliptv'
scheduleDump = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + ADDON_ID , 'scheduleDump.txt'))

def open_Url(url, cookieJar=None,post=None, timeout=20, headers=None):

    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if headers:
        for h,hv in headers:
            req.add_header(h,hv)

    response = opener.open(req,post,timeout=timeout)
    link=response.read()
    response.close()
    return link;

# Create On Screen Text Viewer
def Text_Boxes(heading,anounce):
	class TextBox():
		WINDOW=10147
		CONTROL_LABEL=1
		CONTROL_TEXTBOX=5
		def __init__(self,*args,**kwargs):
			xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
			self.win=xbmcgui.Window(self.WINDOW) # get window
			xbmc.sleep(500) # give window time to initialize
			self.setControls()
		def setControls(self):
			self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
			try: f=open(anounce); text=f.read()
			except: text=anounce
			self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
			return
	TextBox() 

# This is used to open the schedule document then append it once done closes the document to prevent corruption
def appendSchedule(document,data):
	# Open The Text Document To Save Dump File
	appendSchedule = open(document,'a')
	# Append The Channel Data To The Text Document To Save Dump File
	appendSchedule.write(data+'\n'+'\n')
	appendSchedule.close()
	
# Used To Display The Schedule
def displaySchedule():
	schedule = open(scheduleDump, 'r')
	readSchedule = schedule.read()
	Text_Boxes('Selected Schedule',readSchedule)
	schedule.close()

def getTodaysSchedule():
	url = 'http://blackdevilslounge.co.uk/schedule/schedules/today.xml'
	channelData = open_Url(url)
	days = re.compile("<day data='Today'>(.*?)</day>",re.DOTALL).findall(channelData)
	# Create New Text Document To Save Dump File
	dump = open(scheduleDump,'w')
	# Find All Available Days And Loop Through Each Day
	for day in days:
		channels = re.compile('<channel>(.*?)</channel>',re.DOTALL).findall(day)
		
		for channel in channels:
			# Send Data To Be Appended To The Text Document To Save Dump File
			appendSchedule(scheduleDump,channel)
	
	# Open Schedule Document And Show On Screen
	displaySchedule()
	
def getTomorrowsSchedule():
	url = 'http://blackdevilslounge.co.uk/schedule/schedules/tomorrow.xml'
	channelData = open_Url(url)
	days = re.compile("<day data='Tomorrow'>(.*?)</day>",re.DOTALL).findall(channelData)
	# Create New Text Document To Save Dump File
	dump = open(scheduleDump,'w')
	# Find All Available Days And Loop Through Each Day
	for day in days:
		channels = re.compile('<channel>(.*?)</channel>',re.DOTALL).findall(day)
		
		for channel in channels:
			# Send Data To Be Appended To The Text Document To Save Dump File
			appendSchedule(scheduleDump,channel)
	
	# Open Schedule Document And Show On Screen
	displaySchedule()
