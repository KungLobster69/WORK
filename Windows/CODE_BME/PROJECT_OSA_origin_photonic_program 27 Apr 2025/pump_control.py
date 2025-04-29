import serial
from serial.tools import list_ports
import datetime
import time
import pyvisa
#******************** Global Variables ****************************************
class pump_control_function():
    def __init__(self):
        self.Mul = 0.375
        self.RecData = 0
        #config parameters
        self.LoadParaFlag = False
        self.Cal_Delay_Us = 0
        self.P1CalVal = 0.0
        self.P2CalVal = 0.0
        self.CalRot =0.0
        self.Mortor_res = 0.0
        self.Motor_Mode = 0.0
        self.Cal_Duration = 0.0
        self.MicrosecPerSec = 0.0
        self.Decimal_corr = 0.0
        self.Cal_step = 0.0
        self.StepVolRatio = 0.0
        #Pumping Control
        self.PumpSt = 0
        self.PumpDir = 0
        self.PumpPosit=0
        self.PumpAct = 0
        self.PrvPumpAct = 0
        self.PumpVol=0
        self.PumpMode = 0
        self.SendCMDFlg = 0
        self.PHFlag =0
        self.PHFlog = 0
        self.CurrTime = 0
        self.PrvTime = 0
        self.MotorStep = 0.1
        self.port_Ctr = "" #controllor port
        self.port_Pump = "" #pump port
        self.port_Sel = "" #selector port
        self.port_CO2 ="" #CO2 sensor
        self.VID_Ctr = "2341"
        self.PID_Ctr = "0043" #Uno

        self.VID_Stir = "2341"
        self.PID_Stir= "0042"  #Mega

        self.VID_Sel = "1A86"
        self.PID_Sel = "7523"  #SV 07 Selector

        self.VID_CO2 = "0403"
        self.PID_CO2 = "6001" #USB To TTL

        self.CMDlist = []
        self.PHlist = []
        self.PrvPHlist = []

        self.SSt1=0
        self.SSt2=0
        self.SSt3=0
        self.SSt4=0
        self.SSt5=0
        self.SSt6=0

        self.CSt1=0
        self.CSt2=0
        self.CSt3=0
        self.CSt4=0
        self.CSt5=0
        self.CSt6=0
        self.CStCTR=0

        self.OperateCk = False
        self.CMDidx = 0

        self.OprLoop=0
        self.OprLoopcnt=0

        self.CurrentPosit  = [0xCC, 0x00, 0x3E, 0x00, 0x00, 0xDD, 0xE7 ,0x01 ]    
        self.Ch1  = [0xCC ,0x00 ,0x44 ,0x01 ,0x00 ,0xDD ,0xEE ,0x01 ]    
        self.Ch2  = [0xCC ,0x00 ,0x44 ,0x02 ,0x00 ,0xDD ,0xEF ,0x01 ]    
        self.Ch3  = [0xCC ,0x00 ,0x44 ,0x03 ,0x00 ,0xDD ,0xF0 ,0x01 ]    
        self.Ch4  = [0xCC ,0x00 ,0x44 ,0x04 ,0x00 ,0xDD ,0xF1 ,0x01 ]  
        self.Ch5  = [0xCC ,0x00 ,0x44 ,0x05 ,0x00 ,0xDD ,0xF2 ,0x01 ]    
        self.Ch6  = [0xCC ,0x00 ,0x44 ,0x06 ,0x00 ,0xDD ,0xF3 ,0x01 ]    
        self.Ch7  = [0xCC ,0x00 ,0x44 ,0x07 ,0x00 ,0xDD ,0xF4 ,0x01 ]    
        self.Ch8  = [0xCC ,0x00 ,0x44 ,0x08 ,0x00 ,0xDD ,0xF5 ,0x01 ]    
        self.Ch9  = [0xCC ,0x00 ,0x44 ,0x09 ,0x00 ,0xDD ,0xF6 ,0x01 ]    
        self.Ch10  = [0xCC ,0x00 ,0x44 ,0x0A ,0x00 ,0xDD ,0xF7 ,0x01 ] 

        self.QueryCMD= [0xFE, 0x44, 0x00, 0x08, 0x02, 0x9F, 0x25]


        self.graph_offset = 20



        #************** Sensor Data Display ****************
        self.PHValRealTime=0
        self.CO2ValRealTime=0
        self.TempValRealTime=0
        self.HumidValRealTime=0

        #************** Date time CO2 pump and Co2 valve
        self.multiplier = 10 #coefficient vlaue only for CO2 sensor model K-30 10%
        self.CO2ReachTar = 0;
        self.Co2Valve=0;
        self.CO2Pump=0;
        self.CO2SetPoint = 5;

        self.StartTime = datetime.datetime.now()
        self.StartPumpTime = datetime.datetime.now()
        self.StartValveTime = datetime.datetime.now()
        self.StartReadTime= datetime.datetime.now() 
        self.ser_syring = serial.Serial(baudrate=9600, timeout=1)
        self.ser_sel = serial.Serial(baudrate=9600, timeout=1)

    def close_pump(self):
        self.ser_syring.close()
        self.ser_sel.close()
    def connect_pump(self):
        self.device_list = list_ports.comports() #list ports based on descriptions ot Harward ID

        for device in self.device_list:
            if (device.vid != None or device.pid != None):
                # print("current vid" + device.vid)
                # print("current pid" + device.pid)
                print("current vid" + str(device.vid))
                print("current pid" + str(device.pid))
                # NEED to check this vid and pid before

                if(device.device == "COM16"):
                    self.port_syring = device.device #return COM port of syring pump
                    self.ser_syring.port = self.port_syring #set COM port of syringe
                    print('Syringe pump is connected')

                if(device.device == "COM15"):
                    self.port_Sel = device.device
                    self.ser_sel.port = self.port_Sel #set COM port of selector
                    print('Selector is connected')

                # if device.vid == 1659 and device.pid == 8963:
                #     self.port_syring = device.device #return COM port of syring pump
                #     self.ser_syring.port = self.port_syring #set COM port of syringe
                # if (device.vid ==  6790 and device.pid == 29987):
                #     self.port_Sel = device.device
                #     self.ser_sel.port = self.port_Sel #set COM port of selector

        can_ser_ctr = False
        can_ser_sel = False
        # try:
            
        #     rm = pyvisa.ResourceManager()
        #     # print(self.port_syring)
        #     ##TODO substring COMnum to only num
        #     port_num = self.port_syring
        #     port_num = port_num[3:]
        #     print(port_num)
        #     self.inst = rm.open_resource('ASRL'+str(port_num)+'::INSTR') 
        #     print(self.inst)
        #     can_ser_ctr = True
        #     self.inst.timeout = 5000
        #     self.inst.baud_rate = 9600
        #     self.read_termination = '\r'
        #     self.inst.write("/1Z001R")
        # except Exception as e:
        #     print("error open syringe pump port")
        #     can_ser_ctr = False

        try:
            self.ser_syring.open()
            can_ser_ctr = True
        except Exception as e:
            print(e)
            can_ser_ctr = False

        try:
            self.ser_sel.open()
            can_ser_sel = True
        except Exception as e:
            print("error open selector port")
            can_ser_ctr = False
        return [can_ser_ctr,can_ser_sel]
        # return [True,True,True]
    #Syringe pump controllor
    def initlization(self):
        #self.inst.write("/1Z000R")
        # hexcode = self.cmdtohex("/1N0R")
        # self.ser_syring.write(hexcode)
        hexcode = self.cmdtohex("/1N0Z000R")
        self.ser_syring.write(hexcode)

    def cmdtohex(self,cmd):
        hexcode = list(cmd.encode('ascii'))
        hexcode = hexcode + [13]
        return hexcode

    def valveIn(self):
        # self.inst.write("/1IR")
        hexcode = self.cmdtohex("/1IR")
        self.ser_syring.write(hexcode)
    def valveOut(self):
        # self.inst.write("/1OR")
        hexcode = self.cmdtohex("/1OR")
        self.ser_syring.write(hexcode)
    ##TODO added flow rate to system use
    # <S> command -> range(0 - 40) 
    # left only test
    def aspirate(self,volume,syringe_size,flowrate_percent):
        self.flow_speed = 40 -int(flowrate_percent * 40)
        self.increment  = int((3000 * volume/syringe_size)//10)
        print(self.increment)
        print(self.flow_speed)
        # self.inst.write("/1P"+str(self.increment)+"R")
        # self.inst.write("/1"+"S"+str(self.flow_speed)+"P"+str(self.increment)+"R")
        cmd = "/1N0"+"S"+str(self.flow_speed)+"P"+str(self.increment)+"R"
        print(cmd)
        hexcode = self.cmdtohex(cmd)
        self.ser_syring.write(hexcode)                       
    def dispense(self,volume,syringe_size,flowrate_percent):
        self.flow_speed = 40 -int(flowrate_percent * 40)
        self.increment  = int((3000 * volume/syringe_size)//10)
        print(self.increment)
        # self.inst.write("/1D"+str(self.increment)+"R")
        # self.inst.write("/1"+"S"+str(self.flow_speed)+"D"+str(self.increment)+"R")
        cmd = "/1N0"+"S"+str(self.flow_speed)+"D"+str(self.increment)+"R"
        print(f'up:cmd')
        hexcode = self.cmdtohex(cmd)
        self.ser_syring.write(hexcode)   
    def fill(self):
        # self.inst.write("/1A3000R")
        hexcode = self.cmdtohex("/1N0S11A3000R")
        self.ser_syring.write(hexcode)
    def empty(self):
        # self.inst.write("/1A0R")
        hexcode = self.cmdtohex("/1N0S11A0R")
        self.ser_syring.write(hexcode)
    def stop(self):
        # self.inst.write("/1T")
        hexcode = self.cmdtohex("/1TR")
        self.ser_syring.write(hexcode)
    def operate(self,input_command):
        self.inst.write("/1"+input_command)
    def ReadCTR(self): 
        
        try:    
            if self.ser_Ctr.inWaiting(): #Return the number of bytes in the receive buffer.
                strReader = (self.ser_Ctr.readline())
                # print(tmpstr)
                if len(strReader)>=5:
                    try:
                        strReader = strReader.decode()
                        strData = strReader.split(",")
                        # print(strData)
                        if (len(strData)>=5):
                            PumpDir = strData[0].strip() # 1 is F , 0 Is B
                            PumpPosit= strData[1].strip() #Limit Switch state
                            PumpAct = strData[2].strip()  #start syringr pump or stop
                            PumpMode = strData[3].strip() #servo motor mode, default is 1
                            PumpVol = strData[4].strip()  # Step Run
                            # print(tmpstr)
                            # print(str(PumpDir) + "," +str(PumpPosit)+ "," +str(PumpAct)+ "," +str(PumpMode)+ "," +str(PumpVol))
                        else:
                            print("Pump Error" + str(strData) + "Length : "+ str(len(strData)) )
                    except:
                        print("Error Read Pump")     
                        self.ser_Ctr.close()
                        try:
                            self.ser_Ctr.open()
                        except:
                            print("Control Pump not connect")
        except:
            print("Error Read Pump")        


    def startPump(self):
        print("Start")
        self.ser_Ctr.write("s".encode()) 
        self.PumpAct = 1	
    
    def LoadParameter(self):    
        #load floadConfig.txt
        with open('./Config.txt') as f:
            lines = f.readlines()
        
        #get value in text file to set in global variables           
        idx = 0
        for i in lines:
            tmpstr = lines[idx]
            strData = tmpstr.split(",")
            if (idx == 0):
                self.P1CalVal = float(strData[1])
                # print(str(P1CalVal))
            elif(idx == 1):
                self.P2CalVal = float(strData[1])
                #print(str(P2CalVal))
            elif(idx == 2):
                self.CalRot = float(strData[1])
                # print(str(CalRot))
            elif(idx == 3):
                self.Mortor_res = float(strData[1])  
                # print(str(Mortor_res))
            elif(idx == 4):
                self.Motor_Mode = float(strData[1])  
                #print(str(Motor_Mode))            
            elif(idx == 5):
                self.Cal_Duration = float(strData[1])  
                # print(str(Cal_Duration))     
            elif(idx == 6):
                self.MicrosecPerSec = float(strData[1])  
                #print(str(MicrosecPerSec))               
            elif(idx == 7):
                self.Decimal_corr = float(strData[1])  
                #print(str(Decimal_corr))                
            elif(idx == 8):
                self.StepVolRatio = float(strData[1])  

            idx = idx+1
        
        f.close()

        self.V1Val =  self.P1CalVal
        self.V2Val =  self.P2CalVal
    #
    #    V1Box.insert(0,P1CalVal)
    #    V2Box.insert(0,P2CalVal)
        Cal_step = self.CalRot*self.Mortor_res*self.Motor_Mode
        self.Cal_Delay_Us = (self.Cal_Duration*self.MicrosecPerSec)/(Cal_step*2)
        print("Config file loaded")
    
    def CheckSelector(self):
        #Check the current position of selector        
        self.ser_sel.write(serial.to_bytes(self.CurrentPosit))   
        selector_th = (self.ser_sel.readline())
        print(selector_th)
        return selector_th[3]
    
    def ChA(self):

        self.ser_sel.write(serial.to_bytes(self.Ch3)) 
        tmpstr = (self.ser_sel.readline())
        print("Selector A")
        
        ResponseFlag = False
        while ResponseFlag == False:   
            self.ser_sel.write(serial.to_bytes(self.CurrentPosit))   
            tmpstr = (self.ser_sel.readline())
            print(tmpstr[3])     
            if (tmpstr[3] == 3):
                ResponseFlag = True
            else:
                ResponseFlag = False

    def ChB(self):
        self.ser_sel.write(serial.to_bytes(self.Ch4))   
        print("Selector B")
        
        ResponseFlag = False
        while ResponseFlag == False:
            self.ser_sel.write(serial.to_bytes(self.CurrentPosit))   
            tmpstr = (self.ser_sel.readline())
            # print(tmpstr[3])    
            if (tmpstr[3] == 4):
                ResponseFlag = True
            else:
                ResponseFlag = False

    def ChC(self):
        self.ser_sel.write(serial.to_bytes(self.Ch5))   
        print("Selector C")
        
        ResponseFlag = False
        while ResponseFlag == False:
            self.ser_sel.write(serial.to_bytes(self.CurrentPosit))   
            tmpstr = (self.ser_sel.readline())
            # print(tmpstr[3])    
            if (tmpstr[3] == 5):
                ResponseFlag = True
            else:
                ResponseFlag = False
        
    def ChD(self):
        self.ser_sel.write(serial.to_bytes(self.Ch6))   
        print("Selector D")
        
        ResponseFlag = False
        while ResponseFlag == False:
            self.ser_sel.write(serial.to_bytes(self.CurrentPosit))   
            tmpstr = (self.ser_sel.readline())
            # print(tmpstr[3])    
            if (tmpstr[3] == 6):
                ResponseFlag = True
            else:
                ResponseFlag = False

    def ChE(self):
        global Ch7
        global CurrentPosit
        self.ser_sel.write(serial.to_bytes(self.Ch7))   
        print("Selector E")
        
        ResponseFlag = False
        while ResponseFlag == False:
            self.ser_sel.write(serial.to_bytes(self.CurrentPosit))   
            tmpstr = (self.ser_sel.readline())
            # print(tmpstr[3])    
            if (tmpstr[3] == 7):
                ResponseFlag = True
            else:
                ResponseFlag = False

    def ChF(self):
        self.ser_sel.write(serial.to_bytes(self.Ch8))   
        print("Selector F")
        
        ResponseFlag = False
        while ResponseFlag == False:
            self.ser_sel.write(serial.to_bytes(self.CurrentPosit))   
            tmpstr = (self.ser_sel.readline())
            # print(tmpstr[3])    
            if (tmpstr[3] == 8):
                ResponseFlag = True
            else:
                ResponseFlag = False

    def ChInlet(self):

        self.ser_sel.write(serial.to_bytes(self.Ch1))   
        print("Selector Media")
        
        ResponseFlag = False
        while ResponseFlag == False:
            self.ser_sel.write(serial.to_bytes(self.CurrentPosit))   
            tmpstr = (self.ser_sel.readline())
            # print(tmpstr[3])    
            if (tmpstr[3] == 1):
                ResponseFlag = True
            else:
                ResponseFlag = False

    def ChOutlet(self):

        self.ser_sel.write(serial.to_bytes(self.Ch2))   
        print("Selector Sewage")
        
        ResponseFlag = False
        while ResponseFlag == False:
            self.ser_sel.write(serial.to_bytes(self.CurrentPosit))   
            tmpstr = (self.ser_sel.readline())
            # print(tmpstr[3])    
            if (tmpstr[3] == 2):
                ResponseFlag = True
            else:
                ResponseFlag = False


    def ConvertDateTime2Sec(TimePeriod):
        Period =0
        tmpstr =str(TimePeriod.strip())
        strData = tmpstr.split(":")
        hours = int(strData[0])
        minuits = int(strData[1])
        secs = int(strData[2])
        
        h2s = hours*3600
        m2s = minuits *60
        Period = h2s+ m2s+secs
        print("Period :" + str(Period))
        return Period    
    def CheckResp(self,CMDSent):
        
        Ckflag = False    
        CMDStr = CMDSent.split(",")  
    
        
        if(CMDStr[0].strip()  == "Ch"):
            
            
            self.ser_sel.write(serial.to_bytes(self.CurrentPosit))  
            selector_th = (self.ser_sel.readline())
            if (CMDStr[1].strip()  == "IN"):
                if (selector_th[3] == 1):
                    Ckflag = True
                else:
                    Ckflag = False              
            elif(CMDStr[1].strip()  == "OUT"):
                if (selector_th[3] == 2):
                    Ckflag = True
                else:
                    Ckflag = False                                  
            elif(CMDStr[1].strip()  == "A"):    
                if (selector_th[3] == 3):
                    Ckflag = True
                else:
                    Ckflag = False         
            elif(CMDStr[1].strip()  == "B"):    
                if (selector_th[3] == 4):
                    Ckflag = True
                else:
                    Ckflag = False        
            elif(CMDStr[1].strip()  == "C"):  
                if (selector_th[3] == 5):
                    Ckflag = True
                else:
                    Ckflag = False     
            elif(CMDStr[1].strip()  == "D"):
                if (selector_th[3] == 6):
                    Ckflag = True
                else:
                    Ckflag = False       
            elif(CMDStr[1].strip()  == "E"):    
                if (selector_th[3] == 7):
                    Ckflag = True
                else:
                    Ckflag = False   
            elif(CMDStr[1].strip()  == "F"):    
                if (selector_th[3] == 8):
                    Ckflag = True
                else:
                    Ckflag = False    
        
                    
        if(CMDStr[0].strip()  == "Pump"):    # check set step run     
            # print(CMDStr[0].strip() + " : " + str(PumpVol))
            if (float(CMDStr[1].strip())  == float(int(self.PumpVol)/self.StepVolRatio)):
                Ckflag = True
                print("Already set")
                time.sleep(5)
            else:
                Ckflag = False 
                
        if(CMDStr[0].strip()  == "Vol"): #useless now
            if (int(self.PumpMode) == 1):
                Ckflag = True
            else:
                Ckflag = False      
                
        if(CMDStr[0].strip()  == "Dir"):
            if (CMDStr[1].strip()  == "F"):    
                if (int(self.PumpDir) == 1):
                    Ckflag = True
                    # btnPumpFWD.select()
                    # btnPumpBWD.deselect()
                else:
                    Ckflag = False  
            elif(CMDStr[1].strip()  == "B"):  
                if (int(self.PumpDir) == 0):
                    Ckflag = True
                    # btnPumpFWD.deselect()
                    # btnPumpBWD.select()
                else:
                    Ckflag = False 
                    
        if(CMDStr[0].strip()  == "Start"):   
            if (int(self.PrvPumpAct)==0):
                if (int(self.PumpAct)==0):
                    self.PrvPumpAct = 1
                else:
                    Ckflag = False 
            else:
                if (int(self.PumpAct)==1):
                    self.PrvPumpAct = 0
                    Ckflag = True 
                else:
                    Ckflag = False                
                    
            
        if (CMDStr[0].strip()  == "Wait"):     
            self.Remain_time = self.target_time- datetime.datetime.now() 
            if (self.Remain_time.total_seconds() <=0):
                Ckflag = True
            else:
                # CurrCMD.config(text = Remain_time) 
                Ckflag = False
            
        if (CMDStr[0].strip()  == "Loop"):     
            Ckflag = True
        
        if(CMDStr[0].strip()  == "Stir"):
            if (CMDStr[1].strip()  == "A"):  
                # if SSt1 == 0:
                    # check_A.set(0)
                # else:
                    # check_A.set(1)
                Ckflag = True
            elif(CMDStr[1].strip()  == "B"): 
                # if SSt2 == 0:
                    # check_B.set(0)
                # else:
                    # check_B.set(1)
                Ckflag = True
            elif(CMDStr[1].strip()  == "C"):  
            #     if SSt3 == 0:
            #         check_C.set(0)
            #     else:
            #         check_C.set(1)
            #     Ckflag = True
            # elif(CMDStr[1].strip()  == "D"):
            #     if SSt4 == 0:
            #         check_D.set(0)
            #     else:
            #         check_D.set(1)
            #     Ckflag = True
            # elif(CMDStr[1].strip()  == "E"):
            #     if SSt5 == 0:
            #         check_E.set(0)
            #     else:
            #         check_E.set(1)
            #     Ckflag = True
            # elif(CMDStr[1].strip()  == "F"):
            #     if SSt6 == 0:
            #         check_F.set(0)
            #     else:
            #         check_F.set(1)
                Ckflag = True
            elif(CMDStr[1].strip()  == "X"):
                # check_OX.set(0)

                # check_A.set(0)
                # chkbtnStirA.config(state=NORMAL)
                # check_B.set(0)
                # chkbtnStirB.config(state=NORMAL)
                # check_C.set(0)
                # chkbtnStirC.config(state=NORMAL)
                # check_D.set(0)
                # chkbtnStirD.config(state=NORMAL)
                # check_E.set(0)
                # chkbtnStirE.config(state=NORMAL)
                # check_F.set(0)
                # chkbtnStirF.config(state=NORMAL)
                    
                Ckflag = True
            elif(CMDStr[1].strip()  == "O"):  
                
                # check_OX.set(1)
                
                # check_A.set(1)
                # chkbtnStirA.config(state=DISABLED)
                # check_B.set(1)
                # chkbtnStirB.config(state=DISABLED)
                # check_C.set(1)
                # chkbtnStirC.config(state=DISABLED)
                # check_D.set(1)
                # chkbtnStirD.config(state=DISABLED)
                # check_E.set(1)
                # chkbtnStirE.config(state=DISABLED)
                # check_F.set(1)
                # chkbtnStirF.config(state=DISABLED)

                
                Ckflag = True
                
        return Ckflag

    # def Operate(self):
    
    #     # CurrLoop.config(text = str(OprLoopcnt)) 

    #     if (self.OperateCk == True):
            
    #         CMDTxt = self.CMDlist[self.CMDidx][0] + "," + str(self.CMDlist[self.CMDidx][1])
    #         #print(CMDlist[CMDidx][0] + " : " + str(CMDlist[CMDidx][1]))     
    #         #send CMD 
            
    #         # listBox.focus_set()
    #         # children = listBox.get_children()
    #         # if children:
    #         #     listBox.focus(children[CMDidx])
    #         #     listBox.selection_set(children[CMDidx])
            
    #         # currItem = listBox.selection_set(CMDidx)
    #         # print(currItem)
    #         # print("CMD: "+CMDTxt)
    #         if self.SendCMDFlg == 0:
                
    #             # CurrCMD.config(text = CMDTxt) 
    #             # print(CMDidx)
    #             if(self.CMDlist[self.CMDidx][0].strip() =="Wait" ):
    #                 TargertSec = self.ConvertDateTime2Sec(str(self.CMDlist[self.CMDidx][1]))
    #                 self.target_time = datetime.datetime.now() - datetime.timedelta(seconds=-int(TargertSec))
    #                 self.SendCMDFlg = 1
                
    #             elif(self.CMDlist[self.CMDidx][0].strip() =="Goto"): 
    #                 print(str(int(self.OprLoopcnt)))
    #                 print(str(int(self.OprLoop)))   
    #                 if (int(self.OprLoopcnt)< (int(self.OprLoop)-1)): # Loop
    #                     self.OprLoopcnt =self.OprLoopcnt+1
    #                     # CurrLoop.config(text = str(OprLoopcnt)) 
    #                     self.CMDidx = int(str(self.CMDlist[self.CMDidx][1]).encode())  # Goto Line After Looping  Pyhton start with 0
    #                     self.CMDidx = self.CMDidx-1                               # Pyhton start with 0
    #                     self.SendCMDFlg = 0
    #                 else: #Done Opr
    #                     self.CMDlist.clear
    #                     self.CMDidx=0
    #                     self.OperateCk = False   
    #                     self.OprLoop=0
    #                     self.OprLoopcnt=0
    #                     self.PHFlog = 0
    #                     # CurrCMD.config(text = "Done Operation") 
    #                     print("Done Operation") 
                
    #             elif(self.CMDlist[self.CMDidx][0].strip() =="Loop"):   
    #                 self.OprLoop = int(self.CMDlist[self.CMDidx][1])
    #                 print(int(self.OprLoop))
                
    #             elif (self.CMDlist[self.CMDidx][0].strip() =="Pump"):
    #                 self.StepMSent = float(str(self.CMDlist[self.CMDidx][1]).encode())
    #                 self.StepMSent = int(self.StepMSent*self.StepVolRatio) #convert volume(ml) to servo steps
    #                 print(self.StepMSent)
    #                 self.ser_Ctr.write(str(self.StepMSent).encode())
    #                 self.SendCMDFlg = 1
                
    #             elif (self.CMDlist[self.CMDidx][0].strip() =="Dir"):
    #                 if (self.CMDlist[self.CMDidx][1].strip() =="F"):    
    #                     self.ser_Ctr.write("f".encode())  
    #                     self.SendCMDFlg = 1
    #                     time.sleep(2)
    #                 elif(self.CMDlist[self.CMDidx][1].strip() =="B"):
    #                     self.ser_Ctr.write("b".encode())
    #                     self.SendCMDFlg = 1
    #                     time.sleep(2)
                
    #             elif (self.CMDlist[self.CMDidx][0].strip() =="Stir"):
    #                 if (self.CMDlist[self.MDidx][1].strip() =="A"):
    #                     self.ser_Stir.write("q".encode())
    #                     self.SendCMDFlg = 1
    #                     time.sleep(2)
    #                 elif(self.CMDlist[self.CMDidx][1].strip() =="B"):
    #                     self.ser_Stir.write("w".encode())
    #                     self.SendCMDFlg = 1
    #                     time.sleep(2)
    #                 elif(self.CMDlist[self.CMDidx][1].strip() =="C"):
    #                     self.ser_Stir.write("e".encode())
    #                     self.SendCMDFlg = 1
    #                     time.sleep(2)
    #                 elif(self.CMDlist[self.CMDidx][1].strip() =="D"):
    #                     self.ser_Stir.write("r".encode())
    #                     self.SendCMDFlg = 1
    #                     time.sleep(2)    
    #                 elif(self.CMDlist[self.CMDidx][1].strip() =="E"):
    #                     self.ser_Stir.write("t".encode())
    #                     self.SendCMDFlg = 1
    #                     time.sleep(2)                    
    #                 elif(self.CMDlist[self.CMDidx][1].strip() =="F"):
    #                     self.ser_Stir.write("y".encode())
    #                     self.SendCMDFlg = 1
    #                     time.sleep(2)                    
    #                 elif(self.CMDlist[self.CMDidx][1].strip() =="O"):
    #                     self.ser_Stir.write("s".encode())
    #                     self.SendCMDFlg = 1
    #                     time.sleep(2)                    
    #                 elif(self.CMDlist[self.CMDidx][1].strip() =="X"):
    #                     self.ser_Stir.write("x".encode())
    #                     self.SendCMDFlg = 1
    #                     time.sleep(2)                    
                    
    #             elif (self.CMDlist[self.CMDidx][0].strip() =="Ch"):
    #                 if (self.CMDlist[self.CMDidx][1].strip() =="A"):
    #                     self.ser_sel.write(serial.to_bytes(self.Ch3))   
    #                     self.SendCMDFlg = 1
    #                     time.sleep(2)
    #                 elif(self.CMDlist[self.CMDidx][1].strip() =="B"):  
    #                     self.ser_sel.write(serial.to_bytes(self.Ch4)) 
    #                     self.SendCMDFlg = 1
    #                     time.sleep(2)
    #                 elif(self.CMDlist[self.CMDidx][1].strip() =="C"):  
    #                     self.ser_sel.write(serial.to_bytes(self.Ch5)) 
    #                     self.SendCMDFlg = 1
    #                     time.sleep(2)
    #                 elif(self.CMDlist[self.CMDidx][1].strip() =="D"):  
    #                     self.ser_sel.write(serial.to_bytes(self.Ch6)) 
    #                     self.SendCMDFlg = 1
    #                     time.sleep(2)
    #                 elif(self.CMDlist[self.CMDidx][1].strip() =="E"):  
    #                     self.ser_sel.write(serial.to_bytes(self.Ch7)) 
    #                     self.SendCMDFlg = 1
    #                     time.sleep(2)
    #                 elif(self.CMDlist[self.CMDidx][1].strip() =="F"):  
    #                     self.ser_sel.write(serial.to_bytes(self.Ch8))  
    #                     self.SendCMDFlg = 1
    #                     time.sleep(2)    
    #                 elif(self.CMDlist[self.CMDidx][1].strip() =="IN"):  #Media
    #                     self.ser_sel.write(serial.to_bytes(self.Ch1)) 
    #                     self.SendCMDFlg = 1
    #                     time.sleep(2)  
    #                 elif(self.CMDlist[self.CMDidx][1].strip() =="OUT"):  #Sewage
    #                     self.ser_sel.write(serial.to_bytes(self.Ch2)) 
    #                     self.SendCMDFlg = 1
    #                     time.sleep(2)  
                        
    #             elif (self.CMDlist[self.CMDidx][0].strip() =="Start"):
    #                     self.ser_Ctr.write("s".encode()) 
    #                     self.SendCMDFlg = 1
    #                     time.sleep(2)      
    #             else:
    #                 self.ser_Ctr.write(str(self.CMDlist[self.CMDidx][1]).encode())   
    #                 self.SendCMDFlg = 1
                    
    #     #Check Response of Current Command
    #         cmdresp = self.CheckResp(CMDTxt)
    #         # print(cmdresp)
    #         if cmdresp == True:
    #             self.CMDidx = self.CMDidx +1         # Do next CMD
    #             self.SendCMDFlg = 0
                
    #         if (self.CMDidx > len(self.CMDlist)-1):  # Operation Over
    #             self.CMDlist.clear
    #             self.CMDidx=0
    #             self.OperateCk = False   
    #             self.OprLoop=0
    #             self.OprLoopcnt=0
    #             self.PHFlog = 0
    #             # CurrCMD.config(text = "Done Operation") 
    #             print("Done Operation")
    #     else:
    #         self.CMDidx = 0
