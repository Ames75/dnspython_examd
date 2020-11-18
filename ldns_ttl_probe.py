#!/usr/bin/python3
"""This script is used to test whether a given set of LDNS increase TTL of A records  
   given by tDNS authoratative servers.  
 """
import argparse
import re
import sys
import dns
import dns.name
import dns.query
import dns.resolver


def usage():
    print("usage: ldns_ttl_probe.py queryname [-i file that lists all LDNS] ")

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("qname", help="name server that generates expected test results")
    parser.add_argument("-i", "--input_file", help="input file of query names, cannot be used with -n", type=str)
    return parser.parse_args()

def get_iplist(iplist_filename):
    try:
        with open(iplist_filename) as fp:
           content = fp.read() 
           return list(filter(None,re.split("[;,\s]",content)))                
    except:
        print("fail to open file ", iplist_filename)
        print(sys.exc_info()[0])    
        exit()
    finally:
        fp.close() 
    return None

def resolve_name_to_ip(domainname):
    answer = dns.resolver.resolve(domainname)
    return answer.rrset[0]

def get_authdns_ip(domainname):
    qname = dns.name.from_text(domainname)
    local_resolver = dns.resolver.get_default_resolver()
    resolver_ip = local_resolver.nameservers[0]
    # 取出zone name,假设是二级域名
    zonename =(qname.split(3))[1]
    query = dns.message.make_query(zonename, dns.rdatatype.SOA)
    response = dns.query.udp(query, resolver_ip)
    rcode = response.rcode()
    if rcode != dns.rcode.NOERROR:
        if rcode == dns.rcode.NXDOMAIN:
            raise Exception('%s does not exist.' % zonename)
        else:
            raise Exception('Error %s' % dns.rcode.to_text(rcode))
    rrset = None
    # 如果存在SOA记录，那么取SOA记录里指出的权威
    rrset = response.answer[0]
    rr = rrset[0]
    return resolve_name_to_ip(rr.mname).to_text()

def get_ttl_from_ns(domainname, nsip, timeout=5):
    qname = dns.name.from_text(domainname)
    qmsg = dns.message.make_query(qname, dns.rdatatype.A)
    try:
        response = dns.query.udp(qmsg, nsip, timeout)
    except dns.exception.Timeout as e:
        print("LDNS ", nsip, " time out ", e.args)
        return -1    
    rcode = response.rcode()
    if rcode != dns.rcode.NOERROR:
        raise Exception('Error when query auth %s' % dns.rcode.to_text(rcode))
    # 找到第一个A记录
    for rrset in response.answer:
        if rrset.rdtype == dns.rdatatype.A:
            #print(rrset)
            #找到一个就结束了！
            return rrset.ttl
    return -1

def get_ttl_from_auth(domainname):
    authdns_ip = get_authdns_ip(domainname)
    return get_ttl_from_ns(domainname, authdns_ip, 5)

def main(argv):
    if len(argv) < 2:
        usage()
        exit()
    args = parse_arguments()
    print("query name is ", args.qname)
    qname = args.qname
    from_file = args.input_file is not None
    #print(type(args.input_file))
    ldns_ip_list = None if not from_file else get_iplist(args.input_file) 
    auth_ttl = get_ttl_from_auth(args.qname)
    if auth_ttl < 0 :
        print("Error, cannot get ttl from auth server")
        exit(1)
    print("auth_ttl is ", auth_ttl)
    for ldns_ip in ldns_ip_list:
        # time out 设为 5s
        ldns_ttl = get_ttl_from_ns(qname, ldns_ip, 5)
        if ldns_ttl < 0:
           continue   
        print("ldns ", ldns_ip, " ttl diff is ", ldns_ttl - auth_ttl)
        if ldns_ttl > auth_ttl:
            print("LDNS ", ldns_ip, "has greater ttl ", ldns_ttl)

if __name__ == "__main__":
    main(sys.argv)   