#!/usr/bin/python3

import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query
import sys
import argparse

def usage():
    print("usage: basic_query.py <domain name> [name server ip] [options]")

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("domain_name", help="Domain name to query about",type=str)
    parser.add_argument("--dns_server", help="DNS Server IP to query against")
    return parser.parse_args()

def main(argv):
    if len(argv) > 1:
        print("total arguments is %d" % len(argv));
    else:
        usage()
        exit()
    args = parse_arguments()
    ns_server = args.dns_server or '8.8.8.8'   
    qname = dns.name.from_text(args.domain_name)    
    qmsg = dns.message.make_query(qname, dns.rdatatype.A)
    #qmsg.use_edns(options=[dns.edns.ECSOption('1.2.3.4',26)])
    reply = dns.query.udp(qmsg,ns_server) 
    print(reply)

if __name__ == "__main__":
    main(sys.argv)
