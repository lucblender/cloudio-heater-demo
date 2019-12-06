try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 2
import pygubu
import requests
try:
    import _thread as thread  # for python 3
except:
    import thread as tk  # for python 2    
from time import sleep, time
import json
import os

baseURL = "http://localhost:8081/api/v1/"
endpointUUID = "bc0f1bf8-bdae-11e9-9cb5-2a2ae2dbcce4"

credential = ('root', '')

root = tk.Tk() 

class Application:
    def __init__(self, master):

        #1: Create a builder
        self.builder = builder = pygubu.Builder()
        
        #3: Set images path before creating any widget
        img_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'img')
        img_path = os.path.abspath(os.path.dirname(__file__))
        builder.add_resource_path(img_path)

        #2: Load an ui file
        builder.add_from_file('heaterDemo.ui')

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('mainwindow', master)
        self.lblAmbient = builder.get_object('lblAmbient', master)
        self.lblSetPoint = builder.get_object('lblSetPoint', master)
        self.lblMongo = builder.get_object('lblMongo', master)
        self.btnSetPoint = builder.get_object('btnSetPoint', master)
        self.btnRefresh = builder.get_object('btnRefresh', master)
        self.spinTemp = builder.get_object('spinTemp', master)
        self.canevasInflux = builder.get_object('canevasInflux', master)        
        self.scrollBar = builder.get_object('scrollBar', master)
        
        self.lblMongo.configure(yscrollcommand = self.scrollBar.set)             
        self.scrollBar.configure(command=self.lblMongo.yview)
        

        self.btnSetPoint["command"] = self.btnSetPointCallBack
        self.btnRefresh["command"] = self.btnRefreshBack
        
        self.btnRefreshBack()
        
    def btnSetPointCallBack(self):
        timestamp = time()
        r = requests.request(method='post',url=baseURL+'setAttribute', auth=credential, json= {"attributeTopic": endpointUUID+"/myHeater/temperatures/setPointTemperature","attribute": {"constraint": "SetPoint","type": "Number","timestamp": timestamp,"value": float(self.spinTemp.get())}})
    
    def btnRefreshBack(self):
        r = requests.request(method='get',url=baseURL+'getEndpoint', auth=credential, json={	"endpointUuid": endpointUUID})
        parsedEndpoint = json.loads(r.text)
        txt = json.dumps(parsedEndpoint, indent=4, sort_keys=True)
        
        self.lblMongo['state']= 'normal'
        self.lblMongo.delete(1.0, tk.END)
        self.lblMongo.insert(tk.END, txt)       
        self.lblMongo['state']= 'disabled'     
        
    def create_circle(self, x, y, r, **kwargs):
        return self.canevasInflux.create_oval(x-r, y-r, x+r, y+r, **kwargs)
        
    def drawCanevas(self, tab):
        self.canevasInflux.delete("all")
        w = self.canevasInflux["width"]
        h = self.canevasInflux["height"]
        nPoint = len(tab)
        offsetX = float(w)/(nPoint-1)
        #defined canevas goes from 23 to 27°  
        delta = 27-23
        incr = float(h)/delta     
        for i in range(delta):   
            self.canevasInflux.create_line(0, incr*i, w,  incr*i, dash=(4,4), fill="#d4d4d4")
        tab=tab[::-1]
        for i in range(nPoint-1):   
            self.canevasInflux.create_line(i*offsetX, incr*(delta-(tab[i]-23)), (i+1)*offsetX, incr*(delta-(tab[i+1]-23)))
        for i in range(nPoint-1):   
            self.create_circle((i+1)*offsetX, incr*(delta-(tab[i+1]-23)), 3, fill="black");
            self.create_circle((i+1)*offsetX, incr*(delta-(tab[i+1]-23)), 2, fill="white");
        
 



app = Application(root)      
  

def requestLoop():
    while(True):
        r = requests.request(method='get',url=baseURL+'getAttribute', auth=credential, json={"attributeTopic": endpointUUID+"/myHeater/temperatures/temperature"})
        parsedAttribute = json.loads(r.text)
        app.lblAmbient["text"] = "%.2f" % parsedAttribute["value"]
        
        r = requests.request(method='get',url=baseURL+'getAttribute', auth=credential, json={"attributeTopic": endpointUUID+"/myHeater/temperatures/setPointTemperature"})
        parsedAttribute = json.loads(r.text)
        app.lblSetPoint["text"] = "%.2f" % parsedAttribute["value"]
                
        r = requests.request(method='get',url=baseURL+'getAttributeHistoryRequest', auth=credential, json={"attributeTopic": endpointUUID+"/myHeater/temperatures/temperature", "maxDataPoints": 20})
        parsedPoints = json.loads(r.text)
        points = parsedPoints["results"][0]["series"][0]["values"]
        
        formatedPoints = []
        for point in points:
            formatedPoints.append(float(point[1]))
        
        app.drawCanevas(formatedPoints)
  
             
        sleep(1)
        

if __name__ == '__main__':
    

    thread.start_new_thread(requestLoop,())
    
    
    root.mainloop()
