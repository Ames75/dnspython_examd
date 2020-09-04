#!/usr/bin/python3
import dns.rcode
import ipaddress

class Reply(dict):
  def __init__(self,ips):
    # flags should be in the order of AA,TC,RD,RA  
    dict.__init__(self, flags=[True, False, True, True],
                  ips=ips,qname="",cname="",
                  ttl=0, rtype = dns.rcode.NOERROR)
    self.flags = [True, False, True, True]
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