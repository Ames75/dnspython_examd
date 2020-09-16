#!/usr/bin/python3
"""This script is used to generate expected query results that will be used to test 
   correctness of DNS server.  
 """
import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query
import sys
import argparse
import ipaddress
import re
import dns_class_defs

""" TestGenerator class """
class TestGenerator():
    def __init__(self, nsip):
        self.nsip = nsip
    """ query_name returns single Reply oject out of qname """    
    def query_name(self, name):
        qname = dns.name.from_text(name)    
        qmsg = dns.message.make_query(qname, dns.rdatatype.A)
        # we do not want recursion as we are only testing authority
        qmsg.flags = 0
        reply = dns.query.udp(qmsg,self.nsip)
        if not (reply.flags & dns.flags.QR):
            print("query ", qname, " is not getting reply as QR bit is set") 
            return None
        flag_list = [bool(reply.flags & dns.flags.AA),  
                     bool(reply.flags & dns.flags.TC),
                     bool(reply.flags & dns.flags.RA)]
        a_record_set = reply.get_rrset(dns.message.ANSWER, 
                                       qname, dns.rdataclass.IN, 
                                       dns.rdatatype.A)
        if a_record_set is None:
            print("could not find A answer for ",name)
            return None 
        ips = set()
        ttl = a_record_set.ttl
        for record in a_record_set:
            ips.add(record.address)
        #print(type(a_records_set))
        reply_obj = dns_class_defs.Reply(ips,flag_list,name,ttl)
        #print(flag_list)
        #print(reply.to_text())
        print(reply_obj)
        return reply_obj
    def query_all_names(self, qname_list):
        print("number of names are ", len(qname_list))
        for name in qname_list:
            self.query_name(name)

def usage():
    print("usage: generat_tests.py <nameserver ip> [-n query names or -i input file] [-s src ip or subnet]")

def parse_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("nsip", help="name server that generates expected test results")
    group.add_argument("-n", "--names", nargs='*', help="query name to use, you can have multiple names")
    group.add_argument("-i", "--input_file", help="input file of query names, cannot be used with -n", type=str)
    parser.add_argument("-s", "--src", nargs='?', help="source ip to use, if it is in subnet, then its ECS")
    return parser.parse_args()

def getQnamesFromFile(input_file):
    try:
        with open(input_file) as fp:
           content = fp.read() 
           return list(filter(None,re.split("[;,\s]",content)))                
    except:
        print("fail to open file ", input_file)
        print(sys.exc_info()[0])    
        exit()
    finally:
        fp.close() 
    return None

def main(argv):
    if len(argv) < 2:
        usage()
        exit()
    args = parse_arguments()
    print("send querie to ", args.nsip)
    from_file = args.input_file is not None
    #print(type(args.input_file))
    query_names = args.names if not from_file else getQnamesFromFile(args.input_file) 
    test1 = TestGenerator(args.nsip)
    test1.query_all_names(query_names) 

if __name__ == "__main__":
    main(sys.argv)
