#!/usr/bin/python3
import dns.rcode
import ipaddress

class Reply(dict):
  def __init__(self,ips,flag_list,rtype=dns.rcode.NOERROR):
    # flags should be in the order of AA,TC,RA, all boolean  
    dict.__init__(self, 
                  flag_list,
                  ips,qname="",cname="",
                  ttl=0, rtype=dns.rcode.NOERROR)
    self.flags = flag_list
    self.ips = ips
    self.qname = ""
    self.cname = ""
    self.ttl = 0
    self.rtype = dns.rcode.NOERROR 

class Request():
  def __init__(self,qname,src_ip=None,ecs_info=None):
    self.qname = qname;
    self.ecs_info = ecs_info;
    self.src_ip = src_ip;