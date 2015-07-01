#!/usr/bin/python
import sys
import os
import optparse
import urllib

USAGE = """\
"""

def parse_args(args):
    parser = optparse.OptionParser(usage=USAGE)
    parser.add_option("-z", "--source", type="string", default=None,
                      nargs=1,
                      help="source from the notification")
    parser.add_option("-s", "--summary", type="string", default=None,
                      nargs=1,
                      help="summary (title)")
    parser.add_option("-m", "--message", default=None, type="string",
                      default=None, nargs=1)
    parser.add_option("-i", "--id", type="file",
                      help="location of the Bot's ID file")
    parser.add_option("--init", action="store_true", default=False)
    opts, args = parser.parse_args(args)
    return opts, args

def main(args):
    opts, args = parse_args(args)
    if opts.init:
        init()
    else:
        notify(opts.source, opts.summary, opts.message)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
