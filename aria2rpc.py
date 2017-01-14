#!/usr/bin/env python

import json, urllib2, sys, os
from argparse import ArgumentParser
from collections import defaultdict
import base64 #paway 2017/01/14 to support basic auth.

parser = ArgumentParser()
parser.add_argument('-c', '--cookie', help='use cookies', type=str, 
					default='', metavar='COOKIES', dest='cookies')
parser.add_argument('-o', '--output', help='output name', type=str, 
					default='', metavar='NAME', dest='output')
parser.add_argument('-d', '--dir', help='dest dir (server side)', type=str, 
					default='', metavar='DIR', dest='dir')
parser.add_argument('-R', '--rpc', 
					help='aria2 rpc (http://localhost:6800/jsonroc)',
					type=str, default='http://127.0.0.1:6800/jsonrpc',
					metavar='URL', dest='rpc')
parser.add_argument('-s', '--secret', dest='secret', default='', metavar='TOKEN', help='token')
parser.add_argument('-u', '--user', dest='user', default='', metavar='USER', help='user name (deprecated)')
parser.add_argument('-p', '--passwd', dest='pw', default='', metavar='PASSWD', help='password (deprecated)')
parser.add_argument('-r', '--referer', help='referer', default='', type=str, 
					metavar='URL', dest='referer')
parser.add_argument('-H', '--host', dest='host', default='')
parser.add_argument('URIs', nargs='+', help='URIs', type=str, 
					default='', metavar='URI')
opts = parser.parse_args()

jsondict = {'jsonrpc':'2.0',
		'id':'meoow/aria2rpc',
		'method':'aria2.addUri'}

jsondict['params'] = []
if opts.secret:
	jsondict['params'].append('token:{0}'.format(opts.secret))
jsondict['params'].append(opts.URIs)

aria2optsDefault={
		'continue'                  :'true',
		'max-connection-per-server' :15,
		'split'                     :15,
		'min-split-size'            :'10M',
		'user-agent':'Mozilla/5.0 (X11; Linux; rv:5.0) Gecko/5.0 Firefox/5.0'}

aria2opts = defaultdict(lambda:[])
aria2opts.update(aria2optsDefault)

if opts.output:
	aria2opts['out'] = opts.output
if opts.dir:
	aria2opts['dir'] = opts.dir
if opts.referer:
	aria2opts['referer'] = opts.referer
if opts.cookies:
	aria2opts['header'].append('Cookie: {0}'.format(opts.cookies))
if opts.host:
	aria2opts['header'].append('Host: {0}'.format(opts.host))
if opts.secret:
	aria2opts['rpc-secret'] = opts.secret

if not opts.secret and opts.user and opts.pw: #paway 2017/01/14 to support basic auth.
	base64string = base64.b64encode('{}:{}'.format(opts.user, opts.pw))
	request = urllib2.Request(opts.rpc, headers = {'Authorization': 'Basic {}'.format(base64string)})
else:
	request = urllib2.Request(opts.rpc)
	

jsondict['params'].append(aria2opts)

jsonreq = json.dumps(jsondict)
#print jsonreq

print urllib2.urlopen(request, jsonreq).read() #paway 2017/01/14 to support basic auth.
