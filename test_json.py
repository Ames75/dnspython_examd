#!/usr/bin/python3
import sys
import json
class Reply(object):
  def __init__(self,ips):
    # flags should be in the order of AA,TC,RD,RA  
    self.flags = [True, False, True, True]
    self.ips = ips
    self.name = ""
    self.ttl = 0  

def write_json_file(data, filename='results.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4)

def main(argv):
   replies = []
   for i in range(5):
      replies.append(Reply([i]))
   json_content = json.dumps({"replies":[reply.__dict__ for reply in replies]})
   #print(json_content)
   write_json_file(json_content)

if  __name__ == "__main__":
    main(sys.argv)

