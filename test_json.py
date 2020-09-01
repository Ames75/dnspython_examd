#!/usr/bin/python3
import sys
import json
import os 
class Reply(dict):
  def __init__(self,ips):
    # flags should be in the order of AA,TC,RD,RA  
    dict.__init__(self, flags=[True, False, True, True],
                  ips=ips,name="",ttl=0, rtype = 0)
    self.flags = [True, False, True, True]
    self.ips = ips
    self.name = ""
    self.ttl = 0  

def write_json_file(data, filename='results.json'): 
  appendMode = os.path.exists(filename)
  if appendMode:
    try:
      with open(filename,'r') as f:
        json_data = json.load(f)
        print("json data type is", type(json_data))
        json_data["replies"].append(data["replies"])
        #print(json_data)
    except:
      print("Couldn't open file ", filename, "to read")
      print(sys.exc_info()[0])
      return False
    finally:
      f.close()
  else:
    json_data = data
  # Now we write data to file  
  try:
     with open(filename,'w') as f: 
       print(json_data)
       json.dump(json_data,f)   
  except:
      print("Couldn't write file", filename)
      #print(sys.exc_info()[0])
      return False
  finally:
      f.close()
  return True


def main(argv):
   replies = []
   for i in range(5):
      replies.append(Reply([i]))
   json_data = {"replies":replies}
   #json_content = json.dump({"replies":[reply.__dict__ for reply in replies]})
   #print(json_content)
   write_json_file(json_data)

if  __name__ == "__main__":
    main(sys.argv)

