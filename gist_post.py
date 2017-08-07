#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" gist_post.py
single file gist client

"""

import base64
import json
import os
import sys

from optparse import OptionParser

try:
    from urllib.request import urlopen, Request
except:
    from urllib2 import urlopen, Request

def main():
    parser = OptionParser()

    parser.add_option("-d", "--description", dest="description", metavar="DESCRIPTION")
    parser.add_option("-p", "--public", dest="public", action="store_true", default=False)
    parser.add_option("-t", "--token", dest="token", metavar="TOKEN")
    parser.add_option("-u", "--user", dest="user", metavar="USER")
    parser.add_option("-E", "--endpoint", dest="endpoint", metavar="GIST_ENDPOINT")

    (ops, args) = parser.parse_args()

    if len(args) == 0:
        # do nothing, exit
        sys.exit(0)

    user = get_var(ops.user, "GIST_USER")
    token = get_var(ops.user, "GIST_TOKEN")
    endpoint = get_var(ops.endpoint, "GIST_ENDPOINT", "https://api.github.com/gists")
    description = ops.description
    if description is None:
        description = os.path.basename(args[0])
    
    upload(user, token, endpoint, description, ops.public, args)

def upload(user, token, endpoint, description, public, files):
    data = {
        "description": description,
        "public": public,
        "files": {}
    }
    for fn in files:
        fp = open(fn)
        data["files"][os.path.basename(fn)] = {
            "content": fp.read()
        }
        fp.close()

    auth = "Basic %s" % base64.b64encode(bytes("%s:%s" % (user, token), "utf-8")).decode("utf-8")
    req = Request(endpoint,
                  bytes(json.dumps(data).encode("utf-8")),
                  headers={
                      "Content-type": "application/json",
                      "Authorization": auth
                  })
    resp = urlopen(req)
    print(json.dumps(json.loads(resp.read().decode("utf-8")),indent=2))
    
        
def get_var(op, env, default=None):
    if op:
        return op
    if env in os.environ:
        return os.environ[env]
    return default
    
if __name__ == "__main__":
    main()
