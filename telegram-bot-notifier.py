#!/usr/bin/python
import sys
import os
import optparse
import urllib
import json
import pprint

USAGE = """\
"""

BASEURL = "https://api.telegram.org/bot%(id)s/%(method)s?%(args)s"

class Error(Exception):
    pass

def call(id, method, **args):
    encoded_args = urllib.urlencode(args)
    info = dict(id=id, method=method, args=encoded_args)
    query_url = BASEURL % (info)
    try:
        data = json.load(urllib.urlopen(query_url))
    except EnvironmentError, e:
        raise Error("failed to send request to %s: %s" % (query_url, e))
    return data

def updates(id):
    return call(id, "getUpdates")

def notify(id, to, source, summary, message):
    return call(id, "sendMessage", chat_id=to,
                text="%s: %s: %s" % (source, summary, message))

def init(id):
    data = call(id, "getMe")
    return data

def parse_args(args):
    parser = optparse.OptionParser(usage=USAGE)
    parser.add_option("-z", "--source", type="string", default=None,
                      nargs=1,
                      help="source from the notification")
    parser.add_option("-s", "--summary", type="string", default=None,
                      nargs=1,
                      help="summary (title)")
    parser.add_option("-m", "--message", default=None, type="string",
                      nargs=1,
                     help="the message itself")
    parser.add_option("-i", "--id",
                      default=os.path.expanduser("~/.tg-bot"),
                      help="location of the Bot's ID file")
    parser.add_option("--init", action="store_true", default=False)
    parser.add_option("--to", type="string", default=None)
    parser.add_option("--updates", action="store_true", default=False)
    opts, args = parser.parse_args(args)
    if opts.to is None and opts.updates is None:
        opts.init = True
    elif opts.message:
        if opts.to is None:
            parser.error("--to is necessary")
    return opts, args

def load_id(path):
    try:
        with open(path) as f:
            raw = f.read()
    except EnvironmentError, e:
        raise Error("failed to load ID file: %s" % (e))
    else:
        return raw.strip()

def main(args):
    opts, args = parse_args(args)
    id = load_id(opts.id)
    if opts.init:
        print init(id)
    elif opts.updates:
        print pprint.pprint(updates(id))
    else:
        notify(id, opts.to, opts.source, opts.summary, opts.message)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
