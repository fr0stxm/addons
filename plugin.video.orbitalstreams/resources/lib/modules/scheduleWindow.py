# Import PyXBMCt module.
import pyxbmct
import re, urllib, urllib2, cookielib


class newScheduleWindow(pyxbmct.AddonDialogWindow):
 
	def __init__(self, title=''):
		super(newScheduleWindow, self).__init__(title)
		self.setGeometry(400, 250, 2, 4)
		self.set_active_controls()
		self.setNav()
		self.connect(pyxbmct.ACTION_NAV_BACK, self.close)	  

	def set_active_controls(self):
		self.processToday = pyxbmct.Button('Todays Schedule')
		self.placeControl(self.processToday, 0, 0, columnspan=4)
		self.connect(self.processToday,self.todaySchedule)
		self.processTomorrow = pyxbmct.Button('Tomorrows Schedule')
		self.placeControl(self.processTomorrow, 1, 0, columnspan=4)
		self.connect(self.processTomorrow,self.tomorrowSchedule)

	def setNav(self):
		self.processToday.controlDown(self.processTomorrow)
		self.processTomorrow.controlUp(self.processToday)
		self.setFocus(self.processToday)
		
	def todaySchedule(self):
		todayWindow = viewScheduleWindow(title='Todays Schedule',type='Today')
		todayWindow.doModal()
		del todayWindow
		
	def tomorrowSchedule(self):
		tomorrowWindow = viewScheduleWindow(title='Tomorrows Schedule',type='Tomorrow')
		tomorrowWindow.doModal()
		del tomorrowWindow
		
	def setAnimation(self, control):
		control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=500',),('WindowClose', 'effect=fade start=100 end=0 time=500',)])
		
class viewScheduleWindow(pyxbmct.AddonDialogWindow):
 
	def __init__(self, title='',type=''):
		super(viewScheduleWindow, self).__init__(title)
		self.setGeometry(1280, 720, 12, 12)
		self.items = []
		self.type = type
		self.set_active_controls()
		self.setNav()
		self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		

	def set_active_controls(self):
		self.processliveEvent = pyxbmct.Button('Live Events')
		self.placeControl(self.processliveEvent, 11, 10, columnspan=2)
		#self.connect(self.liveEvent,self.todaySchedule)

		self.Schedule = pyxbmct.List()
		self.placeControl(self.Schedule, 1, 1, 10, 10)
		#self.liveTVList.setVisbile(True)
		# Add items to the list
		self.collectSchedule(self.type)
		self.Schedule.addItems(self.items)

		self.connectEventList(
			[pyxbmct.ACTION_MOVE_DOWN,
			pyxbmct.ACTION_MOVE_UP,
			pyxbmct.ACTION_MOUSE_WHEEL_DOWN,
			pyxbmct.ACTION_MOUSE_WHEEL_UP,
			pyxbmct.ACTION_MOUSE_MOVE],
			self.Schedule)

	def setNav(self):
		self.Schedule.controlRight(self.processliveEvent)
		self.processliveEvent.controlLeft(self.Schedule)
		self.setFocus(self.Schedule)
		
	def collectSchedule(self,type):
		if (type == 'Today'):
			url = 'http://blackdevilslounge.co.uk/schedule/schedules/today.xml'
			channelData = self.open_Url(url)
			days = re.compile("<day data='Today'>(.*?)</day>",re.DOTALL).findall(channelData)
		else:
			url = 'http://blackdevilslounge.co.uk/schedule/schedules/tomorrow.xml'
			channelData = self.open_Url(url)
			days = re.compile("<day data='Tomorrow'>(.*?)</day>",re.DOTALL).findall(channelData)


		
		
		# Find All Available Days And Loop Through Each Day
		for day in days:
			channels = re.compile('<channel>(.*?)</channel>',re.DOTALL).findall(day)
			count = 0
			for channel in channels:
				self.items.append(channel)
				count = count+1

	def open_Url(self,url, cookieJar=None,post=None, timeout=20, headers=None):

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

	def setAnimation(self, control):
		control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=500',),('WindowClose', 'effect=fade start=100 end=0 time=500',)])