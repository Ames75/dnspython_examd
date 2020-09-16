#!/usr/bin/python3
import dns.rcode

class Reply(dict):
  def __init__(self,ips,flag_list, qname, ttl, rtype=dns.rcode.NOERROR,cname=""):
    # flags should be in the order of AA,TC,RA, all boolean  
    dict.__init__(self, ips = ips, flags=flag_list, qname=qname, \
                  ttl=ttl, rtype = rtype,cname=cname)
    self.ips = ips
    self.flags = flag_list
    self.qname = qname
    self.cname = ""
    self.ttl = ttl
    self.rtype = dns.rcode.NOERROR 
  '''stringify function '''  
  def __str__(self):
    for ip in self.ips:
      print(self.qname, self.ttl, ip)
    return ""
    #print ("query name is ", qname)


# class Reply(dict):
#   def __init__(self,ips,flag_list,qname, ttl, rtype=dns.rcode.NOERROR,cname=""):
#     # flags should be in the order of AA,TC,RA, all boolean  
#     dict.__init__(self,flags=flag_list, ips=ips, qname=qname, \
#                   ttl=ttl, cname=cname, rtype = rtype)
#     self.flags = flag_list
#     self.ips = ips
#     self.qname = qname
#     self.cname = ""
#     self.ttl = ttl
#     self.rtype = dns.rcode.NOERROR 
#   '''stringify function '''  


class Request():
  def __init__(self,qname,src_ip=None,ecs_info=None):
    self.qname = qname;
    self.ecs_info = ecs_info;
    self.src_ip = src_ip;