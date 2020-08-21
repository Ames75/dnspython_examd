#!/usr/bin/python3

import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query
import sys
import argparse
import ipaddress

def usage():
    print("usage: basic_query.py <domain name> [name server ip] [options]")

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("domain_name", help="Domain name to query about",type=str)
    parser.add_argument("--dns_server", help="DNS Server IP to query against")
    parser.add_argument("--subnet", help="EDNS-Client-Subnet")
    return parser.parse_args()

# return true if ECS info is right and added to query
def add_ECS_options(subnet_info, qmsg):
    addr,scope = subnet_info.split('/')
    try:
        ip = ipaddress.ip_address(addr)
        if isinstance(ip,ipaddress.IPv4Address):
            if not (1<= int(scope) <= 32 ):
               print("net scope %d not right" % int(scope))
            else:
               qmsg.use_edns(options=[dns.edns.ECSOption(addr,int(scope))])
               return True
        else:
            print("no support for V6 addr yet")     
        return False
    except ValueError:
        print("invalid ip %s" % addr)
        return False
        

def main(argv):
    if len(argv) > 1:
        print("total arguments is %d" % len(argv));
    else:
        usage()
        exit()
    args = parse_arguments()
    ns_server = args.dns_server or '119.29.29.29'  
    qname = dns.name.from_text(args.domain_name)    
    qmsg = dns.message.make_query(qname, dns.rdatatype.A)
    if args.subnet and add_ECS_options(args.subnet,qmsg):
        print("doing ECS query")
    reply = dns.query.udp(qmsg,ns_server) 
    print(reply)

if __name__ == "__main__":
    main(sys.argv)
