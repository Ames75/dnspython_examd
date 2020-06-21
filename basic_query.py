#!/usr/bin/python3

import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query
import sys

def usage():
    print("usage: basic_query.py <domain name> [name server ip]")

def main(argv):
    if len(argv) > 1:
        print("total arguments is %d" % len(argv));
    else:
        usage()
        exit()
    ns_server = argv[2] if len(argv) > 2 else '8.8.8.8'   
    qname = dns.name.from_text(argv[1])    
    qmsg = dns.message.make_query(qname, dns.rdatatype.A)
    reply = dns.query.udp(qmsg,ns_server) 
    print(reply)

if __name__ == "__main__":
    main(sys.argv)
