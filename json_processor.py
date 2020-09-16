#!/usr/bin/python3
import sys
import json
import os 
from dns_class_defs import Reply

class JSONProcessor():
  def __init__(self,filename):
    self.filename = filename

  def read_json_data(self):
    is_file_exist = os.path.exists(self.filename)
    if is_file_exist is None:
      print("json file ", self.filename, " does not exist" )
      return None
    try:
      with open(self.filename, 'r') as f:
        json_data = json.load(f)
        #print("json data type is", type(json_data))
        return json_data
    except:
      print("In read_json_data, cannot read file ", self.filename)
    finally:
      f.close()      

  def write_json_data(self,data):
    filename = self.filename 
    appendMode = os.path.exists(filename)
    if appendMode:
      try:
        with open(filename,'r') as f:
          json_data = json.load(f)
          print("json data type is", type(json_data))
          json_data["replies"].extend(data["replies"])
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
          #print(json_data)
          json.dump(json_data,f) 
    except:
        print("Couldn't write file", filename)
        print(sys.exc_info()[0])
        return False
    finally:
        f.close()
    return True


def main(argv):
   replies = []
   flag_list = [True, False, False] # its AA, TC, RA
   qname = 'test.com'
   for i in range(5):
      replies.append(Reply([i], flag_list, qname,12+i))
   json_data = {"replies":replies}
   #json_content = json.dump({"replies":[reply.__dict__ for reply in replies]})
   #print(json_content)
   json_processor = JSONProcessor(qname+".result.json")
   json_processor.write_json_data(json_data)
   json_read_data = json_processor.read_json_data()
   #print(type(json_read_data))
   reply_list = json_read_data["replies"]
   #print(type(reply_list))
   for answer in reply_list:
     #print(type(answer))
     print(answer)


if  __name__ == "__main__":
    main(sys.argv)

