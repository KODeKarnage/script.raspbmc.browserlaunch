#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright (C) 2013 KodeKarnage
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html

import os
import urllib2
import xbmcgui
import hashlib
import xbmc


live_ver_url         = 'http://svn.stmlabs.com/svn/raspbmc/release/update-system/browserver'
local_ver_loc        = '/scripts/upd_hist/browserver'
browser_download_url = 'http://download.raspbmc.com/downloads/bin/browser/browser.tar.gz'
browser_md5_url      = 'http://download.raspbmc.com/downloads/bin/browser/browser.md5'
prog_bar             = xbmcgui.DialogProgress()
dialog               = xbmcgui.Dialog()


def Launch():

	#check version against source
	live_ver = urllib2.urlopen(live_ver_url).read()
	with open(local_ver_loc,'r') as f:
		my_ver = f.read()

	if my_ver == '' or live_ver > my_ver:
		app_verb = 'Installing...'
		download_file('Downloading...', my_ver)
	else:
		launch_browser()


def download_file(app_verb, my_ver):

	prog_bar.create("Arora Browser","Initializing...")
	prog_bar.update(0,app_verb)

	while not prog_bar.iscanceled():

		file_name    = os.path.join('/tmp/',browser_download_url.split('/')[-1])
		u            = urllib2.urlopen(browser_download_url)
		f            = open(file_name, 'wb')
		meta         = u.info()
		file_size    = int(meta.getheaders("Content-Length")[0])
		file_size_dl = 0
		block_sz     = 8192

		while True:
		    buffer = u.read(block_sz)
		    if not buffer:
		        break

		    file_size_dl += len(buffer)
		    f.write(buffer)
		    status = int(file_size_dl * 100. / file_size)
		    prog_bar.update(status,app_verb)

		f.close()

		#check md5 of downloaded file
		prog_bar.update(100,'Verifying file...')
		with open(file_name, 'rb') as ff:
			my_md5     = hashlib.md5(ff.read()).hexdigest()
		source_md5 = urllib2.urlopen(browser_md5_url).read().split(' ')

		if my_md5 != source_md5[0]:
			#continue without update
			#insert notification, if the browser exists then launch it, otherwise die
			if my_ver != '':
				launch_browser()
			prog_bar.close()

		else:
			#update or install browser from download
			prog_bar.update(100,'Extracting...')
			os.system('sudo gzip -dc /tmp/browser.tar.gz | tar -xf - -C /')
			os.system('sudo cp -rf /scripts/upd_sys/browserver /scripts/upd_hist')
			prog_bar.close()
			launch_browser()

		break

def launch_browser():
	#code to launch the browser
	os.system('sudo bash /scripts/launch_browser.sh')


if __name__ == "__main__":
	Launch()
