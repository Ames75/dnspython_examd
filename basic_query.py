#!/usr/bin/python3

import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query
import sys

def main(argv):
    if len(argv) > 1:
        print("total arguments is %d" % len(argv));
    qname = dns.name.from_text(argv[1])    



if __name__ == "__main__":
    main(sys.argv)
