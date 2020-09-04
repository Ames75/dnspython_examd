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

def usage():
    print("usage: generat_tests.py <nameserver ip> [query names or input file] [src ip or subnet]")

def parse_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("nsip", help="name server that generates expected test results")
    group.add_argument("-n", "--names", nargs='*', help="query name to use, you can have multiple names")
    group.add_argument("-i", "--input", nargs=1, help="input file of query names, cannot be used with -n")
    parser.add_argument("-s", "--src", nargs='?', help="source ip to use, if it is in subnet, then its ECS")
    return parser.parse_args()

def getQnamesFromFile(input_file):
    return None

def main(argv):
    if len(argv) < 2:
        usage()
        exit()
    args = parse_arguments()
    print(args.nsip)
    print(type(args.names))
    from_file = args.input is not None
    query_names = args.names if not from_file else getQnamesFromFile(args.input) 
    for value in query_names:
        print(value)    

if __name__ == "__main__":
    main(sys.argv)
