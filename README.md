pymonitor
=========

Python Exercise for Monitoring a Server

### Assumptions ###
* Developed on Ubuntu 13.10
* Python 2.7
* Uses external library "psutil" (python-psutil in Ubuntu repos)
* Tested with T-mobile TXT SMTP Gateway

Email is fine, but using the info below, email to txt message is possible and preferred

Change the "recipients" to include phonenumber@provider.txt.smtp.gateway

TXT SMTP Gateways 
* Sprint: NUMBER@messaging.sprintpcs.com
* AT&T: NUMBER@mobile.att.net
* T-Mobile: NUMBER@tmomail.net
* Verizon: NUMBER@vtext.com

Or use other email to txt gateways - lists here:

http://www.emailtextmessages.com/

### If Assumptions changed ###

Python v3 doesn't support os.statvfs(); Need to use an alternative

Non-Linux or non-Posix machines may need some tweaking to the script  in order to handle differences in their returned values.  Ex. Solaris has some different options in psutils

If sendmail runs on each server being monitored, you could skip the external  smpt gateways and send to localhost.  This would assume that root@localhost is being picked up and sent on to some mailing list.

### Things to Improve ###
Possibly add "session" info - write out to DB or file and track performance over number of runs.  Maybe don't alert immediately - only if issue persists

Data written to a DB could be used for trending/graphing

Actually, psutil does a lot of system statistics, so you could possibly monitor network traffic, switch the disk usage checks to use it, monitor specific processes, etc

The CPU Utilization check leaves a lot to be desired.  That would definitley benifit from tracking usage over time

### Copyright Information ###

Copyright (C) 2013-2014 Chris Collins

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
