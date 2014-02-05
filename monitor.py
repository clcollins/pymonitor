#!/usr/bin/env python

import os
import socket
import smtplib
from email.MIMEText import MIMEText
import datetime
import psutil

### Assumptions ###
# Developed on Ubuntu 13.10
# Python 2.7
# Uses external library "psutil" (python-psutil in Ubuntu repos)
# Tested with T-mobile TXT SMTP Gateway
#
# Email is fine, but using the info below, email to txt message is possible
# and preferred
#
# Change the "recipients" to include phonenumber@provider.txt.smtp.gateway
#
# TXT SMTP Gateways -
# Sprint: <NUMBER>@messaging.sprintpcs.com
# AT&T: <NUMBER>@mobile.att.net
# T-Mobile: <NUMBER>@tmomail.net
# Verizon: <NUMBER>@vtext.com
#
# Or use other email to txt gateways - lists here:
# http://www.emailtextmessages.com/

### If Assumptions changed ###
#
# Python v3 doesn't support os.statvfs()
# Need to use an alternative
#
# Non-Linux or non-Posix machines may need some tweaking to the script
# in order to handle differences in their returned values.  Ex. Solaris has
# some different options in psutils
#
# If sendmail runs on each server being monitored, you could skip the external
# smpt gateways and send to localhost.  This would assume that root@localhost
# is being picked up and sent on to some mailing list.

### Things to Improve ###
# Possibly add "session" info - write out to DB or file and track performance
# over number of runs.  Maybe don't alert immediately - only if issue persists
#
# Data written to a DB could be used for trending/graphing
#
# Actually, psutil does a lot of system statistics, so you could possibly
# monitor network traffic, switch the disk usage checks to use it, monitor
# specific processes, etc
#
# The CPU Utilization check leaves a lot to be desired.  That would definitley
# benifit from tracking usage over time

### Edit the values below for your environment ###

# Mail server configuration
# I suggest using a service account, mailing list
mailserver = ''
sender = ''
recipient = ''

USERNAME = ''
PASSWORD = ''

# Hard disks to check
disks = ['/', '/home']
# Hard disk alert threshold (in %)
disk_thresh = 80

# Memory alert threshold (in %)
mem_thresh = 80
# Swap alert threshold (in %)
swap_thresh = 25

# CPU usage alert threshold (in %)
cpu_thresh = 50
# The interval to record CPU usage (in seconds)
cpu_int = 15

### That's it - stop editing

date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
hostname = socket.gethostname()


def system_check():
    cpucheck()
    diskcheck()
    memcheck()


def diskcheck():
    # Check disk
    threshold = 10 - disk_thresh / 100
    for disk in disks:
        dstat = os.statvfs(disk)
        free = (dstat.f_bavail * dstat.f_bsize) / 1024 ** 3
        total = (dstat.f_blocks * dstat.f_bsize) / 1024 ** 3

        if free < total * threshold:
            subject = "%s: Disk %s - greater than %s percent used" % (hostname, disk, disk_thresh)
            message = "%s: \n Disk %s - %sG left of %sG total" % (hostname, disk, free, total)
            notify(subject, message)


def memcheck():
    threshold = mem_thresh
    mem = psutil.virtual_memory()
    percent = mem.percent
    free = mem.available / 1024 ** 2
    total = mem.total / 1024 ** 2
    if percent > threshold:
        subject = "%s: Memory - greater than %s percent used" % (hostname, threshold)
        message = "%s: Memory -  %sM left of %sM total" % (hostname, free, total)
        notify(subject, message)

    s_threshold = swap_thresh
    s_mem = psutil.swap_memory()
    s_percent = s_mem.percent
    s_used = s_mem.used / 1024 ** 2
    s_total = s_mem.total / 1024 ** 2
    if s_percent > s_threshold:
        subject = "%s: SWAP - greater than %s percent used" % (hostname, s_threshold)
        message = "%s: SWAP -  %sM used of %sM total" % (hostname, s_used, s_total)
        notify(subject, message)


def cpucheck():
    threshold = cpu_thresh
    cpu = psutil.cpu_percent(interval=cpu_int)
    if cpu > threshold:
        subject = "%s: CPU - greater than %s percent" % (hostname, threshold)
        message = "%s: CPU - Last 15 sec. interval checked had %s percent utilization " % (hostname, cpu)
        notify(subject, message)


def notify(subject, message):
    msg = MIMEText(message)
    msg['from'] = sender
    msg['to'] = recipient
    msg['subject'] = subject

    connection = smtplib.SMTP(mailserver, 587)
    connection.ehlo()
    connection.starttls()
    connection.ehlo()
    connection.login(USERNAME, PASSWORD)
    connection.sendmail(sender, recipient, msg.as_string())
    connection.quit()


system_check()
