import tkinter
import tkinter.messagebox
import tkinter.ttk
import tkinter.font as tkFont
import decimal
import cx_Oracle
import pickle
import os
import webbrowser
import time
import _thread as thread
import sys
import threading
ThreadIsEnd=True
class loginUser:
	def __init__(self,PassWord=None,IP=None,Port=None,SID=None,Remember=False):
		self.PassWord=PassWord
		self.IP=IP
		self.Port=Port
		self.SID=SID
		self.Remember=Remember
	def getPassWord(self):
		return self.PassWord
	def setPassWord(self,PassWord):
		self.PassWord=PassWord
	def getIP(self):
		return self.IP
	def setIP(self,IP):
		self.IP=IP
	def getPort(self):
		return self.Port
	def setPort(self,Port):
		self.Port=Port
	def getSID(self):
		return self.SID
	def setSID(self,SID):
		self.SID=SID
	def getRemember(self):
		return self.Remember
	def setRemember(self,Remember):
		self.Remember=Remember
class GradientFrame(tkinter.Canvas):
    '''A gradient frame which uses a canvas to draw the background'''
    def __init__(self, parent,colorBegin,colorEnd, borderwidth=1, relief="sunken",*pargs,**kargs):
        tkinter.Canvas.__init__(self, parent,borderwidth=borderwidth, relief=relief,*pargs,**kargs)
        self._colorBegin = colorBegin
        self._colorEnd = colorEnd
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        if height>618:
        	limit = 618
        else:
        	limit = height
        (r1,g1,b1) = self.winfo_rgb(self._colorBegin)
        (r2,g2,b2) = self.winfo_rgb(self._colorEnd)
        r_ratio = float(r2-r1) / limit
        g_ratio = float(g2-g1) / limit
        b_ratio = float(b2-b1) / limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
            self.create_line(0,i,width,i, tags=("gradient",), fill=color)
        if height>618:
        	nexts=height-limit
        	for j in range(nexts):
        		self.create_line(0,limit + j,width,limit + j, tags=("gradient",),fill=self._colorEnd)
        self.lower("gradient")

class OracleAnalyze:

    def __init__(self):
        self.LoginStatus=False
        #self.history={'PassWord':None,'IP':None,'Port':None,'SID':None,'Remember':False}
        self.loginU=loginUser()
        self.window = tkinter.Tk()
        self.window.title('Oracle Analyze')
        scnWidth,scnHeight = self.window.maxsize()
        self.window.resizable(0, 0)
        self.proportionX=1200/scnWidth
        self.proportionY=741/scnHeight
        tmpcnf = '%dx%d+%d+%d'%(1200, 741, (scnWidth-1200)/2, (scnHeight-741)/2)
        self.window.geometry(tmpcnf)
        self.window.iconbitmap('./bitmaps/OracleAnalyze.ico')
        self.window.protocol('WM_DELETE_WINDOW', self.closeWindow)
        self.menubar = tkinter.Menu(self.window,bg='#FFFFFF')#lightgray
        self.Session = tkinter.Menu(self.menubar,tearoff = 0)      
        self.Session.add_command(label = 'login',command = self.setFrameLoginContent)
        self.Session.add_command(label = 'logout',command = self.ButtonLogoutEvent)
        self.menubar.add_cascade(label = 'session',menu = self.Session)
        self.DatabaseInfor = tkinter.Menu(self.menubar,tearoff = 0)      
        self.DatabaseInfor.add_command(label = 'database version',command = self.DatabaseVersion)
        self.DatabaseInfor.add_command(label = 'instance information',command = self.InstanceInformation)
        self.DatabaseInfor.add_command(label = 'instance memory',command = self.InstanceSGA)
        self.DatabaseInfor.add_command(label = 'instance directory',command = self.InstanceDirectory)
        self.DatabaseInfor.add_command(label = 'export all information',command = self.GetDatabaseInfor)
        self.menubar.add_cascade(label = 'database',menu = self.DatabaseInfor)
        
        self.Tools = tkinter.Menu(self.menubar,tearoff = 0)
        #self.Tools.add_command(label = 'DB Info',command = self.ButtonDBInfoEvent)
        self.Tools.add_command(label = 'awr',command = self.ButtonAWREvent)
        self.Tools.add_command(label = 'sqlplan',command = self.ButtonSqlPlanEvent)
        #self.ImpExp=tkinter.Menu(self.Tools,tearoff = 0)
        #self.ImpExp.add_command(label = 'import',command = self.Documents)
        #self.ImpExp.add_command(label = 'export',command = self.Documents)
        #self.Tools.add_cascade(label='exp/imp',menu=self.ImpExp)
        self.menubar.add_cascade(label = 'tools',menu = self.Tools)
        self.Information = tkinter.Menu(self.menubar,tearoff = 0)      
        self.Information.add_command(label = 'author',command = self.Author)
        self.Information.add_command(label = 'version',command = self.Version)
        self.Information.add_command(label = 'date',command = self.Date)
        self.menubar.add_cascade(label = 'information',menu = self.Information)
        self.Help = tkinter.Menu(self.menubar,tearoff = 0)      
        self.Help.add_command(label = 'documents',command = self.Documents)
        self.menubar.add_cascade(label = 'help',menu = self.Help)
        self.window['menu'] = self.menubar
        #self.setFrameToolsBar()
        self.setFrameLoginContent()
        self.LoginContent.place(x=0,y=0) 
        self.window.mainloop()
    def closeWindow(self):
    	  closeWindow=tkinter.messagebox.askyesno(title='Warning',message='Close the window?')
    	  if closeWindow:
    	  	self.RememberInfo()
    	  	if self.LoginStatus:
    	  		self.conn.close()
    	  	self.window.destroy()
    	  else:
    	  	return
    def setFrameContent(self):
    	  self.Content = GradientFrame(self.window,'#99CCFF','#FFFFFF',width = 1200,height = 2000,borderwidth = 1)
    def setFrameLoginContent(self):
    	  xrevise=490
    	  yrevise=200
    	  self.LoginContent =  GradientFrame(self.window,'#99CCFF','#FFFFFF',width = 1200,height = 1000,borderwidth = 1)        
    	  self.LoginContent.create_text(xrevise,yrevise,text="LoginUser:")
    	  self.LoginContent.create_text(60+xrevise,yrevise,text="SYS")
    	  self.LoginContent.create_text(xrevise,yrevise+30,text="PassWord:")
    	  self.LoginContent.create_text(xrevise,yrevise+60,text="IP:")
    	  self.LoginContent.create_text(xrevise,yrevise+90,text="Port:")
    	  self.LoginContent.create_text(xrevise,yrevise+120,text="SID:")
    	  self.LoginContent.create_text(140+xrevise,yrevise+150,text="Remember the Database")
    	  #self.LoginContent.create_text(530,568,text="Author JiaZhanying 2018/05/25")
    	  self.PassWordStr = tkinter.StringVar()
    	  self.Password = tkinter.Entry(self.LoginContent,width = 30,bd=3,textvariable=self.PassWordStr,show='*')
    	  self.Password.place(x = 40+xrevise, y = yrevise+20)
    	  self.IPStr = tkinter.StringVar()
    	  self.IP=tkinter.Entry(self.LoginContent,width = 30,bd=3,textvariable=self.IPStr)
    	  self.IP.place(x = 40+xrevise, y = yrevise+50)
    	  self.PortStr = tkinter.StringVar()
    	  self.Port=tkinter.Entry(self.LoginContent,width = 30,bd=3,textvariable=self.PortStr)
    	  self.Port.place(x = 40+xrevise, y = yrevise+80)
    	  self.SIDStr = tkinter.StringVar()
    	  self.SID=tkinter.Entry(self.LoginContent,width = 30,bd=3,textvariable=self.SIDStr)
    	  self.SID.place(x = 40+xrevise, y = yrevise+110)   	  
    	  self.Remember=tkinter.BooleanVar()#text='Remember the Database'
    	  RememberButton =  tkinter.Frame(self.LoginContent,width = 11,height = 12,bg = 'white',borderwidth = 1)
    	  self.History = tkinter.Checkbutton(RememberButton,variable=self.Remember, onvalue = True,offvalue = False,command=self.RememberInfo)
    	  self.History.place(x=-7,y=-7)
    	  RememberButton.place(x = 50+xrevise, y = yrevise+145)
    	  sty=tkinter.ttk.Style()
    	  #sty.configure('TButton',background='#FFFFFF')
    	  #sty.configure('TButton',foreground='#99CCFF')
    	  #sty.map("TButton",foreground=[('pressed', '#99CCFF'), ('active', 'blue')],background=[('pressed', '!disabled', 'black'), ('active', 'white')])
    	  self.Logins = tkinter.ttk.Button(self.LoginContent, text = 'Login', width = 10,style='TButton', command = self.ButtonLoginEvent)
    	  self.Logins.place(x = 50+xrevise, y = yrevise+170)
    	  if os.path.exists('remember.info'):
    	  	self.RememberFile=open('remember.info','rb')
    	  	self.loginU=pickle.load(self.RememberFile)
    	  	self.RememberFile.close()
    	  self.SetInforVar()
    def ButtonLogoutEvent(self):
    	  self.setFrameLoginContent()
    	  self.Content.place_forget()
    	  self.LoginContent.place(x=0,y=0) 
    	  if self.LoginStatus:
    	  	self.conn.close()
    	  	self.window.title('Oracle Analyze                    '+self.IPStr.get()+':'+self.PortStr.get()+'/'+self.SIDStr.get()+' sys as sysdba logout')
    	  self.LoginStatus=False
    def ButtonLoginEvent(self):
    	  if self.LoginStatus:
    	  	self.ButtonLogoutEvent()
    	  	#tkinter.messagebox.showinfo("Login failed:",self.IPStr.get()+':'+self.PortStr.get()+'/'+self.SIDStr.get()+' sys as sysdba already logged in')
    	  self.LoginStatus=self.LoginDatabase('SYS',self.PassWordStr.get(),self.IPStr.get(),self.PortStr.get(),self.SIDStr.get())
    	  if self.LoginStatus:
    	  	self.RememberInfo()	
    	  	self.setFrameContent()
    	  	self.LoginContent.place_forget()
    	  	welcome=tkFont.Font(root=self.window,family='Liberation Serif', size=60 )
    	  	self.Content.create_text(600,300,text="WELCOME",font=welcome)
    	  	self.Content.place(x=0,y=0)
    	  	self.window.title('Oracle Analyze                    '+self.IPStr.get()+':'+self.PortStr.get()+'/'+self.SIDStr.get()+' sys as sysdba login')
    def RememberInfo(self):
    	  if self.Remember.get():
    	  	self.loginU.setPassWord(self.PassWordStr.get())
    	  	self.loginU.setIP(self.IPStr.get())
    	  	self.loginU.setPort(self.PortStr.get())
    	  	self.loginU.setSID(self.SIDStr.get())
    	  	self.loginU.setRemember( True)
    	  	self.RememberFile=open('remember.info','wb')
    	  	pickle.dump(self.loginU,self.RememberFile)
    	  	self.RememberFile.close()
    	  else:
    	  	self.loginU.setPassWord(None)
    	  	self.loginU.setIP(None)
    	  	self.loginU.setPort(None)
    	  	self.loginU.setSID(None)
    	  	self.loginU.setRemember(False)
    	  	self.RememberFile=open('remember.info','wb')
    	  	pickle.dump(self.loginU,self.RememberFile)
    	  	self.RememberFile.close()
    def SetInforVar(self):
    	  	if self.loginU.getPassWord():
    	  		self.PassWordStr.set(self.loginU.getPassWord())
    	  	if self.loginU.getIP():
    	  		self.IPStr.set(self.loginU.getIP())
    	  	if self.loginU.getPort():
    	  		self.PortStr.set(self.loginU.getPort())
    	  	if self.loginU.getSID():
    	  		self.SIDStr.set(self.loginU.getSID())
    	  	if self.loginU.getRemember():
    	  		self.History.select()
    def LoginDatabase(self,UserName,PassWord,IP,Port,SID):
    	  try:
    	  	if UserName=='' or UserName is None:
    	  		tkinter.messagebox.showinfo("Login error:", "Username can not be empty")
    	  		return False
    	  	if PassWord=='' or PassWord is None:
    	  		tkinter.messagebox.showinfo("Login error:", "PassWord can not be empty")
    	  		return False
    	  	if IP=='' or IP is None:
    	  		tkinter.messagebox.showinfo("Login error:", "IP can not be empty")
    	  		return False
    	  	if Port=='' or Port is None:
    	  		tkinter.messagebox.showinfo("Login error:", "Port can not be empty")
    	  		return False
    	  	if SID=='' or SID is None:
    	  		tkinter.messagebox.showinfo("Login error:", "SID can not be empty")
    	  		return False
    	  	self.conn = cx_Oracle.connect(UserName,PassWord,IP+':'+Port+'/'+SID,cx_Oracle.SYSDBA)
    	  except Exception as e:
    	  	tkinter.messagebox.showinfo("Login failed:", "{}".format(e))
    	  	return False
    	  else:
    	  	return True
    def Author(self):
    	  pass;
    def Version(self):
    	  pass;
    def Date(self):
    	  pass;
    def Documents(self):
    	  pass;
    def ButtonSqlPlanEvent(self):
    	  if not self.LoginStatus:
    	  	return
    	  self.Content.destroy()
    	  self.setFrameContent()
    	  self.SqlFrame=tkinter.Frame(self.Content,width = 1000,height = 450,bg = 'white',borderwidth = 1)   	  
    	  self.ButtonFrame=GradientFrame(self.Content,'#99CCFF','#FFFFFF',width = 5000,height = 1000,borderwidth = 1)	  
    	  self.scrollbar = tkinter.Scrollbar(self.SqlFrame)
    	  self.SqlStrInput = tkinter.Text(self.SqlFrame, height=50, width=60,relief='sunken',bg='#FFFFFF')
    	  self.SqlStrInput.pack(side='left', fill='y')
    	  self.scrollbar.pack(side='right',fill='y')
    	  self.scrollbar.config(command=self.SqlStrInput.yview)
    	  self.SqlStrInput.config(yscrollcommand=self.scrollbar.set)
    	  
    	  buttonx=200
    	  buttony=165
    	  self.SqlPlanUserStr = tkinter.StringVar()
    	  self.ButtonFrame.create_text(buttonx,buttony,text="LoginUser:")
    	  self.SqlPlanUser=tkinter.Entry(self.ButtonFrame,width = 30,bd=3,textvariable=self.SqlPlanUserStr)
    	  self.SqlPlanUser.place(x = buttonx+40, y = buttony-15)
    	  
    	  self.SqlPlanPassWordStr = tkinter.StringVar()
    	  self.ButtonFrame.create_text(buttonx,buttony+30,text="PassWord:")
    	  self.SqlPlanPassword = tkinter.Entry(self.ButtonFrame,width = 30,bd=3,textvariable=self.SqlPlanPassWordStr,show='*')
    	  self.SqlPlanPassword.place(x = buttonx+40, y = buttony+15)  
    	  self.ViewSqlPlan = tkinter.ttk.Button(self.ButtonFrame, text = 'View SqlPlan', width = 12,command=self.ButtonViewSqlPlanEvent)
    	  self.ViewSqlPlan.place(x=buttonx+50,y=buttony+60)
    	  
    	  self.ButtonFrame.place(x=500,y=0)
    	  self.SqlFrame.place(x=0,y=0)
    	  self.Content.place(x = 0, y = 0)
    def ButtonViewSqlPlanEvent(self):
    	  if self.LoginStatus:
    	  	print(self.SqlPlanUserStr.get())
    	  	print(type(self.SqlPlanUserStr.get()))
    	  	if self.SqlPlanUserStr.get() =='':
    	  		tkinter.messagebox.showinfo("error:", "Please input username")
    	  		return
    	  	if self.SqlPlanPassWordStr.get()=='':
    	  		tkinter.messagebox.showinfo("error:", "Please input password")
    	  		return
    	  	self.htmlfile=open('SQLPLAN.html','w')
    	  	self.htmlfile.write(' <head><style type="text/css">table,tr,td{border:1px solid black;}td{padding:15px;}#tableStyle{background-color:#F0F0F0;}#colName{background-color:#FFFF33;}#col{color:White; background:#0066CC}</style></head>')
    	  	self.htmlfile.write(' <ul>')
    	  	self.htmlfile.write(' <h4>Author:Jia Zhanying</h4>')
    	  	self.htmlfile.write(' <h4>Version:1.0</h4>')
    	  	self.GetSqlResult("select '<h4>'||to_char(sysdate,'yyyy-mm-dd hh24:mi:ss')||'</h4>' from dual")
    	  	self.htmlfile.write('<h1>==================================================================</h1>')
    	  	self.htmlfile.write('<h1>&nbsp&nbsp&nbsp&nbspSQL PLAN</h1>')
    	  	self.htmlfile.write('<br>')
    	  	returns= self.GetSqlPlan(self.SqlStrInput.get('1.0','end'))
    	  	self.htmlfile.write(' </ul>')
    	  	self.htmlfile.close()
    	  	if returns:
    	  		webbrowser.open_new("SQLPLAN.html");
    def GetSqlPlan(self,vSql):
    	  try:
    	    SqlPlanConn=cx_Oracle.connect(self.SqlPlanUserStr.get(),self.SqlPlanPassWordStr.get(),self.IPStr.get()+":"+self.PortStr.get()+"/"+self.SIDStr.get())
    	    cur=SqlPlanConn.cursor()
    	    cur.callproc("DBMS_APPLICATION_INFO.SET_ACTION",["OracleAnalyze:SqlPlan"])
    	    vSql=vSql.replace("\n", "")
    	    vSql=vSql.rstrip()
    	    vSql=vSql.lstrip()
    	    if vSql[0:6].upper()=='CREATE' or vSql[0:4].upper()=='DROP' or vSql[0:5].upper()=='ALTER' or vSql[0:8].upper()=='TRUNCATE':
    	    	tkinter.messagebox.showinfo("error:", "Only support execution plan for select/delete/update/merge/insert statement")
    	    	return False
    	    if vSql[-1]==';':
    	    	vSql=vSql[:-1]
    	    cur.execute(vSql)
    	    SqlPlanConn.rollback()
    	    cur.callproc("DBMS_APPLICATION_INFO.SET_ACTION",["OracleAnalyze:GetSqlPlan"])
    	    cur.execute("select sql_id,CHILD_NUMBER from v$sql  where action='OracleAnalyze:SqlPlan' and to_char(sql_fulltext)='"+vSql+"' and rownum=1")
    	    data=cur.fetchall()
    	    sqlid=data[0][0]
    	    childid=data[0][1]
    	    cur.execute("select replace(plan_table_output,' ','&'||'nbsp'||'&'||'nbsp'||'&'||'nbsp') from table(dbms_xplan.display_cursor('"+sqlid+"',"+str(childid)+"))")
    	    data=cur.fetchall()
    	    flag=0
    	    secFlag=0
    	    for i in data:
    	    	if i[0][2:5]=='---':
    	    		secFlag=secFlag+1;
    	    	if i[0][0]=='|' and i[0][-1]=='|':
    	    		if flag==0:
    	    			self.htmlfile.write('<table id="tableStyle">')
    	    			self.htmlfile.write('<tr id="col"><td>')
    	    			self.htmlfile.write(i[0][1:-1].replace('|','</td><td>'))
    	    			self.htmlfile.write("</td></tr>")
    	    		else:
    	    			
    	    			self.htmlfile.write('<tr id="colName"><td>')
    	    			self.htmlfile.write(i[0][1:-1].replace('|','</td><td>'))
    	    			self.htmlfile.write("</td></tr>")
    	    		flag=flag+1
    	    	else:
    	    		if secFlag == 3:
    	    			secFlag=0
    	    		else:
    	    			if flag>0:
    	    				self.htmlfile.write("</table>")
    	    				flag=0
    	    			self.htmlfile.write('<br>')
    	    			self.htmlfile.write(i[0])
    	    cur.close()
    	    return True
    	  except Exception as e:
    	  	tkinter.messagebox.showinfo("error:", "{}".format(e))
    	  	cur.close()
    	  	return False
    	  
    def ButtonAWREvent(self):
    	  if not self.LoginStatus:
    	  	return
    	  xrevise=450
    	  yrevise=200
    	  self.Content.destroy()
    	  self.setFrameContent()
    	  self.Content.place(x = 0, y = 0)
    	  self.Content.create_text(xrevise+30,yrevise,text="AWR Begin Time :")
    	  self.AWRBeginTimeValue=tkinter.StringVar()
    	  self.AWRBeginTimeStr=tkinter.ttk.Combobox(self.Content,textvariable=self.AWRBeginTimeValue)
    	  self.AWRBeginTimeStr["values"]=self.GetAWRSnapList()
    	  if self.LoginStatus:
    	  	self.AWRBeginTimeStr.current(0)
    	  self.AWRBeginTimeStr.place(x = xrevise+95, y = yrevise-15)
    	  
    	  self.Content.create_text(xrevise+25,yrevise+30,text="AWR End Time :")
    	  self.AWREndTimeValue=tkinter.StringVar()
    	  self.AWREndTimeStr=tkinter.ttk.Combobox(self.Content,textvariable=self.AWREndTimeValue)
    	  self.AWREndTimeStr["values"]=self.GetAWRSnapList()
    	  if self.LoginStatus:
    	  	self.AWREndTimeStr.current(0)
    	  self.AWREndTimeStr.place(x = xrevise+95, y = yrevise+15)
    	  
    	  self.EnableADDMValue=tkinter.IntVar()
    	  EnableADDMButton =  tkinter.Frame(self.Content,width = 11,height = 12,bg = 'white',borderwidth = 1)
    	  self.EnableADDM=tkinter.Checkbutton(EnableADDMButton,bg='white',variable =self.EnableADDMValue,onvalue = 8,offvalue =0)
    	  self.EnableADDM.place(x=-7,y=-7)
    	  EnableADDMButton.place(x = xrevise-5, y = yrevise+55)
    	  self.Content.create_text(xrevise+50,yrevise+60,text="Enable ADDM")
    	  self.EnableASHValue=tkinter.IntVar()
    	  EnableASHButton =  tkinter.Frame(self.Content,width = 11,height = 12,bg = 'white',borderwidth = 1)
    	  self.EnableASH=tkinter.Checkbutton(EnableASHButton,bg='white',variable =self.EnableASHValue,onvalue = 4,offvalue =0)
    	  self.EnableASH.place(x = -7, y = -7)
    	  EnableASHButton.place(x = xrevise+125, y = yrevise+55)
    	  self.Content.create_text(xrevise+170,yrevise+60,text="Enable ASH")
    	  self.DisableExadataValue=tkinter.IntVar()
    	  DisableExadataButton =  tkinter.Frame(self.Content,width = 11,height = 12,bg = 'white',borderwidth = 1)
    	  self.DisableExadata=tkinter.Checkbutton(DisableExadataButton,bg='white',variable =self.DisableExadataValue,onvalue = 2,offvalue =0)
    	  self.DisableExadata.place(x = -7, y = -7)
    	  DisableExadataButton.place(x = xrevise-5, y = yrevise+85)
    	  self.Content.create_text(xrevise+55,yrevise+90,text="Disable Exadata")
    	  self.PerformanceHubValue=tkinter.IntVar()
    	  PerformanceHubButton =  tkinter.Frame(self.Content,width = 11,height = 12,bg = 'white',borderwidth = 1)
    	  self.PerformanceHub=tkinter.Checkbutton(PerformanceHubButton,bg='white',variable =self.PerformanceHubValue,onvalue = 1,offvalue =0)
    	  self.PerformanceHub.place(x = -7, y = -7)
    	  PerformanceHubButton.place(x = xrevise+125, y = yrevise+85)
    	  self.Content.create_text(xrevise+190,yrevise+90,text="Performance Hub")
    	  
    	  def CreateSnap():
    	    if self.LoginStatus:
    	  	  cur=self.conn.cursor()
    	  	  try:
    	  		  cur.callproc('dbms_workload_repository.create_snapshot')
    	  	  except Exception as e:
    	  	  	cur.close()
    	  	  	tkinter.messagebox.showinfo("create failed:", "{}".format(e))
    	  	  else:
    	  		  cur.close()
    	  		  self.AWRBeginTimeStr["values"]=self.GetAWRSnapList()
    	  		  self.AWREndTimeStr["values"]=self.GetAWRSnapList()
    	  		  tkinter.messagebox.showinfo("Message:", "Created snap successfully")
    	  self.CreateSnap = tkinter.ttk.Button(self.Content, text = 'Create Snap', width = 12, command = CreateSnap)
    	  self.CreateSnap.place(x = xrevise, y = yrevise+115)
    	  self.GetAWR = tkinter.ttk.Button(self.Content, text = 'export Report', width = 12, command = self.GetAWRHtml)
    	  self.GetAWR.place(x = xrevise+110, y = yrevise+115)  	  		
    def GetAWRSnapList(self):
    	  date=[]
    	  if self.LoginStatus:
    	  	cur=self.conn.cursor()
    	  	cur.execute(" select to_char(sn.END_INTERVAL_TIME, 'yyyy-mm-dd hh24:mi:ss') END_INTERVAL_TIME  "+
"   from dba_hist_snapshot sn                                                   "+
#"  where END_INTERVAL_TIME > sysdate - 1                                        "+
"  order by snap_id desc                                                        ");
    	  	data = cur.fetchall()
    	  	cur.close()
    	  	date=[row[0] for row in data]
    	  return date
    def GetAWRSnapId(self,date):
    	  cur=self.conn.cursor()
    	  cur.execute("select snap_id from dba_hist_snapshot sn where to_char(sn.END_INTERVAL_TIME, 'yyyy-mm-dd hh24:mi:ss')='"+date+"'");
    	  data = cur.fetchone()
    	  cur.close()
    	  return str(data[0])
    def GetDBID(self):
    	  cur=self.conn.cursor()
    	  cur.execute("select dbid,instance_number from dba_hist_snapshot where rownum=1")
    	  data=cur.fetchall()
    	  for i in data:
    	  	 self.dbid=i[0]
    	  	 self.insnum=i[1]
    	  cur.close()
    def GetAWRHtml(self):
    	  if self.LoginStatus:
    	  	if self.CheckBeginEnd():
    	  		self.GetDBID();
    	  		self.awroption=self.EnableADDMValue.get()+self.EnableASHValue.get()+self.DisableExadataValue.get()+self.PerformanceHubValue.get()
    	  		self.htmlfile=open('awr.html','w')
    	  		self.GetSqlResult("""select outputs from (select replace(output, 'border="0"', 'border="1"') outputs from table(dbms_workload_repository.awr_report_html("""+str(self.dbid)+","+str(self.insnum)+", "+self.GetAWRSnapId(self.AWRBeginTimeValue.get())+", "+self.GetAWRSnapId(self.AWREndTimeValue.get())+", "+str(self.awroption)+"))) where outputs is not null")
    	  		self.htmlfile.close()
    	  		webbrowser.open_new("awr.html");
    def CheckBeginEnd(self):
    	  if self.AWRBeginTimeValue.get()>=self.AWREndTimeValue.get():
    	  	tkinter.messagebox.showinfo("error:", "The End Time should be greater than the Begin Time")
    	  	return False
    	  else:
    	  	return True
    def InstanceInformation(self):
    	  if not self.LoginStatus:
    	  	return
    	  self.Content.destroy()
    	  #self.WriteHtml()
    	  self.setFrameContent()
    	  yspace=200
    	  spy=40
    	  InstanceFont=tkFont.Font(root=self.window,family='Liberation Serif', size=20 )
    	  self.Content.create_text(580,160,text='Instance Information',font = InstanceFont)
    	  yspace=self.DrawCanvasBySql(yspace,spy,"select tmp, name, max(length(tmp)) over(), max(length(name)) over() from ("+
"select 'Database Name' tmp, name from v$database  union all  "+
"select 'Create Date' tmp, to_char(created, 'yyyy/mm/dd hh24:mi:ss') from v$database union all "+
"select 'Resetlogs Time' tmp, to_char(resetlogs_time, 'yyyy/mm/dd hh24:mi:ss') from v$database union all "+
"select 'Log Mode' tmp, log_mode from v$database union all "+
"select 'Open Mode' tmp, open_mode from v$database union all "+
"select 'Flashback On' tmp, flashback_on from v$database)")
    	  #yspace=self.DrawCanvasBySql(xplace,yspace,spy,"select name,value,description,MAX(length(name)*8) over(),MAX(length(value)*8) over(),MAX(length(description)*8) over() from v$parameter")
    	  self.Content.place(x = 0, y = 0)
    def InstanceDirectory(self):
    	  if not self.LoginStatus:
    	  	return
    	  self.page=0
    	  self.InstanceDirectoryPage() 
    def LastPage(self):
    	  self.page=self.page-1
    	  self.InstanceDirectoryPage()
    def NextPage(self):
    	  self.page=self.page+1
    	  self.InstanceDirectoryPage()
    def InstanceDirectoryPage(self):
    	  self.Content.destroy()
    	  #self.WriteHtml()
    	  self.setFrameContent()
    	  yspace=200
    	  spy=40
    	  InstanceFont=tkFont.Font(root=self.window,family='Liberation Serif', size=20 )
    	  self.Content.create_text(580,160,text='Instance Directory',font = InstanceFont)
    	  vCount=self.GetSqlCount("select count(1) from dba_directories")
    	  yspace=self.DrawCanvasBySql(yspace,spy,"select directory_name,directory_path,p1,p2 from ( select directory_name,directory_path,MAX(length(directory_name)) over() p1,MAX(length(directory_path)) over() p2,rownum nm from dba_directories) where nm between "+str(self.page*5+1)+" and "+str(self.page*5+5))
    	  if vCount>self.page*5+5 and self.page>0:
    	  	self.nextPage=tkinter.Button(self.Content, text = 'next', width = 10, command = self.NextPage)
    	  	self.lastPage=tkinter.Button(self.Content, text = 'last', width = 10, command = self.LastPage)
    	  	self.lastPage.place(x=490,y=yspace+10)
    	  	self.nextPage.place(x=590,y=yspace+10)
    	  if vCount>self.page*5+5 and self.page==0:
    	  	self.nextPage=tkinter.Button(self.Content, text = 'next', width = 10, command = self.NextPage)
    	  	self.nextPage.place(x=540,y=yspace+10)
    	  if vCount<self.page*5+5 and self.page>0:
    	  	self.lastPage=tkinter.Button(self.Content, text = 'last', width = 10, command = self.LastPage)
    	  	self.lastPage.place(x=540,y=yspace+10)
    	  #yspace=self.DrawCanvasBySql(xplace,yspace,spy,"select name,value,description,MAX(length(name)*8) over(),MAX(length(value)*8) over(),MAX(length(description)*8) over() from v$parameter")
    	  self.Content.place(x = 0, y = 0)
    def DatabaseVersion(self):
    	  if not self.LoginStatus:
    	  	return
    	  self.Content.destroy()
    	  self.setFrameContent()
    	  VersionFont=tkFont.Font(root=self.window,family='Liberation Serif', size=20 )
    	  self.Content.create_text(580,160,text='database version',font = VersionFont)
    	  xplace=150
    	  yspace=200
    	  spy=40
    	  yspace=self.DrawCanvasBySql(yspace,spy,"select banner,MAX(length(banner)) over() from v$version")
    	  self.Content.place(x = 0, y = 0)
    def InstanceSGA(self):
    	  if not self.LoginStatus:
    	  	return
    	  self.Content.destroy()
    	  self.setFrameContent()
    	  VersionFont=tkFont.Font(root=self.window,family='Liberation Serif', size=20 )
    	  self.Content.create_text(580,160,text='SGA',font = VersionFont)
    	  yspace=200
    	  spy=40
    	  yspace=self.DrawCanvasBySql(yspace,spy,"select name,value,MAX(length(name)) over(),MAX(length(value)) over() from ( "+
"select name,DECODE(VALUE,'0','auto',round(value / 1024) || 'KB/' || round(value / 1024 / 1024) ||'MB/' || round(value / 1024 / 1024 / 1024) || 'GB') value from v$parameter v where name= 'memory_max_target' union all "+
"select name,DECODE(VALUE,'0','auto',round(value / 1024) || 'KB/' || round(value / 1024 / 1024) ||'MB/' || round(value / 1024 / 1024 / 1024) || 'GB') value from v$parameter v where name= 'memory_target' union all "+
"select name,DECODE(VALUE,'0','auto',round(value / 1024) || 'KB/' || round(value / 1024 / 1024) ||'MB/' || round(value / 1024 / 1024 / 1024) || 'GB') value from v$parameter v where name= 'sga_max_size' union all "+
"select name,DECODE(VALUE,'0','auto',round(value / 1024) || 'KB/' || round(value / 1024 / 1024) ||'MB/' || round(value / 1024 / 1024 / 1024) || 'GB') value from v$parameter v where name= 'sga_target' union all "+
"select name,DECODE(VALUE,'0','auto',round(value / 1024) || 'KB/' || round(value / 1024 / 1024) ||'MB/' || round(value / 1024 / 1024 / 1024) || 'GB') value from v$parameter v where name= 'pga_aggregate_limit' union all "+
"select name,DECODE(VALUE,'0','auto',round(value / 1024) || 'KB/' || round(value / 1024 / 1024) ||'MB/' || round(value / 1024 / 1024 / 1024) || 'GB') value from v$parameter v where name= 'pga_aggregate_target' union all "+
"select name,DECODE(VALUE,'0','auto',round(value / 1024) || 'KB/' || round(value / 1024 / 1024) ||'MB/' || round(value / 1024 / 1024 / 1024) || 'GB') value from v$parameter v where name= 'log_buffer'  union all "+
"select name, value from v$parameter v where name in ('lock_sga', 'pre_page_sga'))")
    	  self.Content.place(x = 0, y = 0)
    def GetSqlCount(self,sql):
    	  cur=self.conn.cursor()
    	  cur.execute(sql);
    	  datas = cur.fetchall()
    	  return datas[0][0]
    def DrawCanvasBySql(self,y,spy,sql):
    	  cur=self.conn.cursor()
    	  cur.execute(sql);
    	  datas = cur.fetchall()
    	  pfont=tkFont.Font(root=self.window,family='Liberation Serif', size=10 )
    	  startx=0
    	  starty=y
    	  X=0
    	  spacY=spy
    	  for records in datas:
    	  	length=int(len(records)/2)
    	  	if X==0:
    	  		for i in range(length):
    	  			X=X+records[i+length]
    	  		X=600-(X*5)
    	  		startx=X
    	  	for seq in range(length):
    	  		spacX=records[seq+length]*10
    	  		self.Content.create_text(startx+spacX/2,starty+spacY/2,text=records[seq],font = pfont)
    	  	#for data in records:
    	  		#self.Content.create_text(startx+spacX/2,starty+spacY/2,text=data)
    	  		self.Content.create_line(startx,starty,startx+spacX,starty)
    	  		self.Content.create_line(startx,starty,startx,starty+spacY)
    	  		self.Content.create_line(startx+spacX,starty,startx+spacX,starty+spacY)
    	  		self.Content.create_line(startx,starty+spacY,startx+spacX,starty+spacY)
    	  		startx=startx+spacX
    	  	startx=X
    	  	starty=starty+spacY
    	  cur.close()
    	  return starty+spacY
    def timer(self):
    	self.timew=tkinter.Toplevel(self.window)
    	scnWidth,scnHeight = self.timew.maxsize()
    	#self.timew.overrideredirect(True)
    	self.timew.resizable(0, 0)
    	self.timew.title('wait')
    	tmpcnf = '%dx%d+%d+%d'%(200, 122, (scnWidth-200)/2, (scnHeight-122)/2)
    	self.timew.geometry(tmpcnf)
    	self.timew.wm_attributes("-topmost", 1)
    	self.timew.iconbitmap('./bitmaps/OracleAnalyze.ico')
    	self.timewContent = GradientFrame(self.timew,'#99CCFF','#FFFFFF',width = 200,height = 121,borderwidth = 0)
    	self.timewContent.place(x=-1,y=-1)
    	self.timewContent.create_text(95,60,text="exporting 0s",tags='mytime')
    	self.timew.update()
    def GetDatabaseInfor(self):
    	global ThreadIsEnd
    	ThreadIsEnd=True
    	self.timer()
    	time_now = int(time.time())
    	getinforhtml=getInforHtml('SYS',self.PassWordStr.get(),self.IPStr.get(),self.PortStr.get(),self.SIDStr.get())
    	#thread.start_new_thread(getinforhtml.WriteHtml, ())
    	gets=threading.Thread(target=getinforhtml.WriteHtml, args=())
    	gets.start()
    	while ThreadIsEnd:
    		waits=str(int(time.time())-time_now)
    		self.timewContent.delete('mytime')
    		self.timewContent.create_text(95,60,text='exporting '+waits+'s',tags='mytime')
    		self.timew.update()
    		time.sleep(0.5)
    	if not ThreadIsEnd:
    		self.timew.destroy()
    		webbrowser.open_new("analyze.html")

class getInforHtml:
	  def __init__(self,UserName,PassWord,IP,Port,SID):
    	  	self.conn = cx_Oracle.connect(UserName,PassWord,IP+':'+Port+'/'+SID,cx_Oracle.SYSDBA)
    	  	self.LoginStatus=True
    	  	
	  def WriteHtml(self):
	  	if self.LoginStatus:
	  		global ThreadIsEnd
	  		#progress = Progress()
	  		#progress.start()
	  		v_tablel ='<table id="tableStyle">';
	  		v_tabler ='</table>';
	  		v_enter ='<h3></h3>';
	  		self.htmlfile=open('analyze.html','w')
	  		self.htmlfile.write(' <head><style type="text/css">table,tr,td{border:1px solid black;}td{padding:15px;}#tableStyle{background-color:#F0F0F0;}#colName{background-color:#FFFF33;}#col{color:White; background:#0066CC}</style></head>')
	  		self.htmlfile.write(' <ul>')
	  		self.htmlfile.write(' <h4>Author:Jia Zhanying</h4>')
	  		self.htmlfile.write(' <h4>Version:1.0</h4>')
	  		self.GetSqlResult("select '<h4>'||to_char(sysdate,'yyyy-mm-dd hh24:mi:ss')||'</h4>' from dual")
	  		self.htmlfile.write('<h1>==================================================================</h1>')
	  		self.htmlfile.write('<h1>&nbsp&nbsp&nbsp&nbspDatabase Environment Information</h1>')
	  		self.htmlfile.write('<h1>==================================================================</h1>')
	  		self.htmlfile.write('<li><h3>DATABASE VERSION</h3></li>')
	  		self.htmlfile.write(v_tablel)
	  		self.htmlfile.write('<tr id="col"><td>Banner</td></tr>')
	  		self.GetSqlResult("""select '<tr id="colName"><td>'||banner||'</td></tr>' from v$version""")
	  		self.htmlfile.write(v_tabler)
	  		self.htmlfile.write(v_enter)
    	  
	  		self.htmlfile.write('<li><h3>Database Mode</h3></li>')
	  		self.htmlfile.write(v_tablel)
	  		self.htmlfile.write('<tr id="col"><td>Database Name</td><td>Create Date</td><td>Open_Mode</td><td>Log_Mode</td><td>Flashback_On</td></tr>')
	  		self.GetSqlResult("""select '<tr id="colName"><td>'||name||'</td><td>'||created||'</td><td>'||open_mode||'</td><td>'||log_mode||'</td><td>'||flashback_on||'</td></tr>' from v$database""")
	  		self.htmlfile.write(v_tabler)
	  		self.htmlfile.write(v_enter)
    	  
	  		self.htmlfile.write('<li><h3>Database Instance</h3></li>')
	  		self.htmlfile.write(v_tablel)
	  		self.htmlfile.write('<tr id="col"><td>Instance_Number</td><td>Instance_Name</td><td>hostname</td><td>start time</td><td>Status</td></tr>')
	  		self.GetSqlResult("""select '<tr id="colName"><td>'||instance_number||'</td><td>'||instance_name||'</td><td>'||host_name ||'</td><td>'||startup_time ||'</td><td>'||status||'</td></tr>' from gv$instance""")
	  		self.htmlfile.write(v_tabler)
	  		self.htmlfile.write(v_enter)
    	  
	  		self.htmlfile.write('<li><h3>SGA</h3></li>')
	  		self.htmlfile.write(v_tablel)
	  		self.htmlfile.write('<tr id="col"><td>Parameter Name </td><td>Parameter Value</td></tr>')
	  		self.GetSqlResult("""select '<tr id="colName"><td>' || name || '</td><td>' || value || '</td></tr>'              """+
"  from (select name, value                                                     "+
"          from v$parameter                                                     "+
"         where name in ('cpu_count',                                           "+
"                        'db_writer_processes',                                 "+
"                        'lock_sga',                                            "+
"                        'pre_page_sga',                                        "+
"                        'spfile',                                              "+
"                        'service_names',                                       "+
"                        'processes',                                           "+
"                        'db_create_file_dest',                                 "+
"                        'session_cached_cursors',                              "+
"                        'cursor_sharing',                                      "+
"                        'db_recovery_file_dest')                               "+
"        union all                                                              "+
"        select name,                                                           "+
"               DECODE(VALUE,                                                   "+
"                      '0',                                                     "+
"                      '0',                                                     "+
"                      round(value / 1024) || 'KB/' ||                          "+
"                      round(value / 1024 / 1024) || 'MB/' ||                   "+
"                      round(value / 1024 / 1024 / 1024) || 'GB') value         "+
"          from v$parameter                                                     "+
"         where name in ('db_block_size',                                       "+
"                        'log_buffer',                                          "+
"                        'sga_max_size',                                        "+
"                        'unified_audit_sga_queue_size',                        "+
"                        'sga_target',                                          "+
"                        'db_recovery_file_dest_size',                          "+
"                        'shared_pool_reserved_size',                           "+
"                        'memory_target',                                       "+
"                        'memory_max_target'))                          ")
	  		self.htmlfile.write(v_tabler)
	  		self.htmlfile.write(v_enter)
    	  
	  		self.htmlfile.write('<li><h3>SGA Dynamic</h3></li>')
	  		self.htmlfile.write(v_tablel)
	  		self.htmlfile.write('<tr id="col"><td>Memory Type</td><td>Allocate Size</td><td>Granule_size </td></tr>')
	  		self.GetSqlResult("""select '<tr id="colName"><td>' || v.COMPONENT || '</td><td>' ||  """+
"       decode(v.CURRENT_SIZE,                                                 "+
"              0,                                                              "+
"              '0',                                                            "+
"             round(v.CURRENT_SIZE / 1024 / 1024) || 'MB') || '</td><td>' ||   "+
"             granule_size / 1024 / 1024 || 'M</td></tr>'                      "+
"  from v$sga_dynamic_components v")
	  		self.htmlfile.write(v_tabler)
	  		self.htmlfile.write(v_enter)
    	  
	  		self.htmlfile.write('<li><h3>Logfile Information</h3></li>')
	  		self.htmlfile.write(v_tablel)
	  		self.htmlfile.write('<tr id="col"><td>Log Group</td><td>Log Thread</td><td>Log Member</td><td>Log Size(M)</td></tr>')
	  		self.GetSqlResult("""select '<tr id="colName"><td>'||group#||'</td><td>'||thread#||'</td><td>'||members||'</td><td>'||bytes/1024/1024||'</td></tr>' from gv$log""")
	  		self.htmlfile.write(v_tabler)
	  		self.htmlfile.write(v_enter)
    	  
	  		self.htmlfile.write('<li><h3>File Number</h3></li>')
	  		self.htmlfile.write(v_tablel)
	  		self.htmlfile.write('<tr id="col"><td>File Type</td><td>File Number</td><td>File Path</td></tr>')
	  		self.GetSqlResult("""select '<tr id="colName"><td>Control Files</td><td>'||count(1)over()||'</td><td>'||name||'</td></tr>' from  v$controlfile""")
	  		self.GetSqlResult("""select '<tr id="colName"><td>Log Files</td><td>group '||group#||':'||count(1)over(partition by group#)||'</td><td>'||member||'</td></tr>' from  v$logfile""")
	  		self.GetSqlResult("""select '<tr id="colName"><td>Temp Files</td><td>'||count(1)over()||'</td><td>'||name||'</td></tr>' from  v$tempfile""")
	  		self.GetSqlResult("""select '<tr id="colName"><td>Data Files</td><td>'||count(1)over()||'</td><td>'||name||'</td></tr>' from   v$datafile""")
	  		self.htmlfile.write(v_tabler)
	  		self.htmlfile.write(v_enter)
    	  
	  		self.htmlfile.write('<li><h3>Datafile Information Of Tablespace</h3></li>')
	  		self.htmlfile.write(v_tablel)
	  		self.htmlfile.write('<tr id="col"><td>Tablespaces Name</td><td>Datafile Number</td><td>Tablespace Size(M)</td></tr>')
	  		self.GetSqlResult("""select '<tr id="colName"><td>'||tablespace_name ||'</td><td>'||count(1)||'</td><td>'|| sum(bytes)/1024/1024||'</td></tr>' from dba_temp_files group by tablespace_name union all """+
""" select '<tr id="colName"><td>'||tablespace_name ||'</td><td>'||count(1)||'</td><td>'|| sum(bytes)/1024/1024||'</td></tr>' from dba_data_files group by tablespace_name""")
	  		self.htmlfile.write(v_tabler)
	  		self.htmlfile.write(v_enter)
    	  
	  		self.htmlfile.write('<li><h3>Data File Status</h3></li>')
	  		self.htmlfile.write(v_tablel)
	  		self.htmlfile.write('<tr id="col"><td>Data File Status</td><td>Number</td></tr>')
	  		self.GetSqlResult("""select '<tr id="colName"><td>' ||status|| '</td><td>' ||count(*)|| '</td></tr>' from v$datafile group by status""")
	  		self.htmlfile.write(v_tabler)
	  		self.htmlfile.write(v_enter)
    	  
	  		self.htmlfile.write('<li><h3>Tablespace Size Used</h3></li>')
	  		self.htmlfile.write(v_tablel)
	  		self.htmlfile.write('<tr id="col"><td>Tablespaces Name</td><td>Total Size(M/G)</td><td>Free Size(M/G)</td><td>Used Size(M/G)</td><td>Free %</td></tr>')
	  		self.GetSqlResult("select str                                                                          "+
"""  from (select '<tr id="colName"><td>' || a.tablespace_name || '</td><td>' ||                    """+
"               round(a.total) || 'M/' || round(a.total / 1024) ||                   "+
"               'G</td><td>' || round(decode(f.free, null, 0, f.free)) || 'M/' ||    "+
"               round(decode(f.free, null, 0, f.free)) / 1024 || 'G</td><td>' ||     "+
"               round((a.total - decode(f.free, null, 0, f.free))) || 'M/' ||        "+
"               round((a.total - decode(f.free, null, 0, f.free))) / 1024 ||         "+
"               'G</td><td>' ||                                                      "+
"               round((decode(f.free, null, 0, f.free) / a.total) * 100) ||          "+
"               '</td></tr>' str,                                                    "+
"               round((decode(f.free, null, 0, f.free) / a.total) * 100) rate        "+
"          from (select tablespace_name, sum(bytes / (1024 * 1024)) total            "+
"                  from dba_data_files                                               "+
"                 group by tablespace_name) a,                                       "+
"               (select tablespace_name,                                             "+
"                       round(sum(bytes / (1024 * 1024))) free                       "+
"                  from dba_free_space                                               "+
"                 group by tablespace_name) f                                        "+
"         WHERE a.tablespace_name = f.tablespace_name(+)                             "+
"        union all                                                                   "+
"""        select '<tr id="colName"><td>' || c.tablespace_name || '</td><td>' ||                    """+
"               round(c.bytes / 1024 / 1024) || 'M/' ||                              "+
"               round(c.bytes / 1024 / 1024 / 1024) || 'G</td><td>' ||               "+
"               round((c.bytes - d.bytes_used) / 1024 / 1024) || 'M/' ||             "+
"               round((c.bytes - d.bytes_used) / 1024 / 1024 / 1024) ||              "+
"               'G</td><td>' || round(d.bytes_used / 1024 / 1024) || 'M/' ||         "+
"               round(d.bytes_used / 1024 / 1024 / 1024) || 'G</td><td>' ||          "+
"               round((c.bytes - d.bytes_used) * 100 / c.bytes) ||                   "+
"               '</td></tr>' str,                                                    "+
"               round((c.bytes - d.bytes_used) * 100 / c.bytes) rate                 "+
"          from (select tablespace_name, sum(bytes) bytes                            "+
"                  from dba_temp_files                                               "+
"                 group by tablespace_name) c,                                       "+
"               (select tablespace_name, sum(bytes_cached) bytes_used                "+
"                  from v$temp_extent_pool                                           "+
"                 group by tablespace_name) d                                        "+
"         where c.tablespace_name = d.tablespace_name)                               "+
" order by rate                                                                     ")
	  		self.htmlfile.write(v_tabler)
	  		self.htmlfile.write(v_enter)
    	  
	  		self.htmlfile.write('<h1>==================================================================</h1>')
	  		self.htmlfile.write('<h1>&nbsp&nbsp&nbsp&nbspDatabase Performance Criteria</h1>')
	  		self.htmlfile.write('<h1>==================================================================</h1>')
    	  
	  		self.htmlfile.write('<li><h3>Parse Information</h3></li>')
	  		self.htmlfile.write(v_tablel)
	  		self.htmlfile.write('<tr id="col"><td>Type</td><td>Value</td></tr>')
	  		self.GetSqlResult("""select '<tr id="colName"><td>'||NAME||'</td><td>'||VALUE||'</td></tr>' from v$sysstat where name like 'parse%'""")
	  		self.GetSqlResult("""select '<tr id="colName"><td>Hard Parse Rate %</td><td>'||round(         """+
" (select VALUE from  v$sysstat where name='parse count (hard)')/                      "+
" (select VALUE from  v$sysstat where name='parse count (total)')*100,2)||'%</td></tr>' FROM dual")
	  		self.htmlfile.write(v_tabler)
	  		self.htmlfile.write(v_enter)
    	  
	  		self.htmlfile.write('<li><h3>Shared Pool/Buffer Cache Hit Rate</h3></li>')
	  		self.htmlfile.write(v_tablel)
	  		self.htmlfile.write('<tr id="col"><td>Cache Type</td><td>Total</td><td>Hit</td><td>Hit Rate</td></tr>')
	  		self.GetSqlResult(""" select '<tr id="colName"><td>Library Cache Hit Rate</td><td>Total Pins:'||sum(v.PINS)||'</td><td>Hit Pins:'||sum(v.PINHITS)||'</td><td>'||round(sum(v.PINHITS)/sum(v.PINS)*100,2)||'%</td></tr>' from v$librarycache v union all    """+
""" select '<tr id="colName"><td>Row Cache Hit Rate</td><td>Total Gets:'||sum(gets)||'</td><td>Hit Gets:'||(sum(gets)-sum(getmisses))||'</td><td>'||round(100*sum(gets-getmisses)/sum(gets),2)||'%</td></tr>' from v$rowcache union all """+
""" select '<tr id="colName"><td>Buffer Cache Hit Rate </td><td>Total Logic Reads: ' ||               """+
"        (select value from v$sysstat where name = 'session logical reads') ||         "+
"        '</td><td>Physical Reads:' ||                                                 "+
"        ((select value from v$sysstat where name = 'physical reads') -                "+
"        (select value from v$sysstat where name = 'physical reads direct')) ||        "+
"        '</td><td>' ||                                                                "+
"        round((((select value                                                         "+
"                   from v$sysstat                                                     "+
"                  where name = 'session logical reads') -                             "+
"              ((select value from v$sysstat where name = 'physical reads') -          "+
"              (select value                                                           "+
"                    from v$sysstat                                                    "+
"                   where name = 'physical reads direct'))) /                          "+
"              (select value                                                           "+
"                  from v$sysstat                                                      "+
"                 where name = 'session logical reads')) * 100,                        "+
"              2)||'%</td></tr>'                                                       "+
"   from dual                                                                          ")
	  		self.htmlfile.write(v_tabler)
	  		self.htmlfile.write(v_enter)
    	  
	  		self.htmlfile.write('<li><h3>Shared_pool_reserved Request Fail Number</h3></li>')
	  		self.htmlfile.write(v_tablel)
	  		self.htmlfile.write('<tr id="col"><td>File_Number</td><td>Change Shared_pool_reserved Size Sql</td></tr>')
	  		self.GetSqlResult("""select '<tr id="colName"><td>' || REQUEST_MISSES ||                                                 """+
"""       '</td><td>"alter system set shared_pool_reserved_size= M scope=spfile;" and restart database; </td></tr>' """+
"  from v$shared_pool_reserved")
	  		self.htmlfile.write(v_tabler)
	  		self.htmlfile.write(v_enter)
    	  
	  		self.htmlfile.write('<li><h3>Elapsed Time Top 10</h3></li>')
	  		self.htmlfile.write(v_tablel)
	  		self.htmlfile.write('<tr id="col"><td>SQL_ID</td><td>EXECUTIONS</td><td>USERS_EXECUTING</td><td>ELAPSED_TIME</td><td>CPU_TIME</td><td>CHILD_NUMBER</td><td>DISK_READS</td></tr>')
	  		self.GetSqlResult("""select '<tr id="colName"><td>' || SQL_ID || '</td><td>' || EXECUTIONS || '</td><td>' ||         """+
"       USERS_EXECUTING || '</td><td>' || ELAPSED_TIME || '</td><td>' ||            "+
"       CPU_TIME || '</td><td>' || CHILD_NUMBER || '</td><td>' || DISK_READS ||     "+
"       '</td></tr>'                                                                "+
"  from (select v.SQL_ID,                                                           "+
"               v.EXECUTIONS,                                                       "+
"               v.USERS_EXECUTING,                                                  "+
"               v.ELAPSED_TIME,                                                     "+
"               v.CPU_TIME,                                                         "+
"               v.CHILD_NUMBER,                                                     "+
"               v.DISK_READS,                                                       "+
"               rank() over(order by elapsed_time desc) elapsed_rank                "+
"          from v$sql v)                                                            "+
" where elapsed_rank <= 10                                                          ")
	  		self.htmlfile.write(v_tabler)
	  		self.htmlfile.write(v_enter)
    	  
	  		self.htmlfile.write('<li><h3>Logical Read Top 10</h3></li>')
	  		self.htmlfile.write(v_tablel)
	  		self.htmlfile.write('<tr id="col"><td>SQL_ID</td><td>BUFFER_GETS</td><td>BUFFER_RATE</td><td>EXECUTIONS</td><td>USERS_EXECUTING</td><td>ELAPSED_TIME</td><td>CPU_TIME</td><td>CHILD_NUMBER</td><td>DISK_READS</td></tr>')
	  		self.GetSqlResult("""select '<tr id="colName"><td>' || SQL_ID || '</td><td>' || BUFFER_GETS || '</td><td>' ||                  """+
"       BUFFER_RATE || '%</td><td>' || EXECUTIONS || '</td><td>' ||                           "+
"       USERS_EXECUTING || '</td><td>' || ELAPSED_TIME || '</td><td>' ||                      "+
"       CPU_TIME || '</td><td>' || CHILD_NUMBER || '</td><td>' || DISK_READS ||               "+
"       '</td></tr>'                                                                          "+
"  from (select v.SQL_ID,                                                                     "+
"               v.BUFFER_GETS,                                                                "+
"               to_char(100 * ratio_to_report(v.buffer_gets) over(), '999.99') BUFFER_RATE,   "+
"               v.EXECUTIONS,                                                                 "+
"               v.USERS_EXECUTING,                                                            "+
"               v.ELAPSED_TIME,                                                               "+
"               v.CPU_TIME,                                                                   "+
"               v.CHILD_NUMBER,                                                               "+
"               v.DISK_READS,                                                                 "+
"               rank() over(order by v.BUFFER_GETS desc) buffer_rank                          "+
"          from v$sql v)                                                                      "+
" where buffer_rank <= 10                                                                     ")
	  		self.htmlfile.write(v_tabler)
	  		self.htmlfile.write(v_enter)
    	  
	  		self.htmlfile.write('<li><h3>Disk Read Top 10</h3></li>')
	  		self.htmlfile.write(v_tablel)
	  		self.htmlfile.write('<tr id="col"><td>SQL_ID</td><td>DISK_READS</td><td>EXECUTIONS</td><td>USERS_EXECUTING</td><td>ELAPSED_TIME</td><td>CPU_TIME</td><td>CHILD_NUMBER</td><td>BUFFER_GETS</td></tr>')
	  		self.GetSqlResult("""select '<tr id="colName"><td>' || SQL_ID || '</td><td>' || DISK_READS || '</td><td>' || """+
"       EXECUTIONS || '</td><td>' || USERS_EXECUTING || '</td><td>' ||      "+
"       ELAPSED_TIME || '</td><td>' || CPU_TIME || '</td><td>' ||           "+
"       CHILD_NUMBER || '</td><td>' || BUFFER_GETS || '</td></tr>'          "+
"  from (select v.SQL_ID,                                                   "+
"               v.BUFFER_GETS,                                              "+
"               v.EXECUTIONS,                                               "+
"               v.USERS_EXECUTING,                                          "+
"               v.ELAPSED_TIME,                                             "+
"               v.CPU_TIME,                                                 "+
"               v.CHILD_NUMBER,                                             "+
"               v.DISK_READS,                                               "+
"               row_number() over(order by v.DISK_READS desc) disk_rank     "+
"          from v$sql v)                                                    "+
" where disk_rank <= 10                                                     ")
	  		self.htmlfile.write(v_tabler)
	  		self.htmlfile.write(v_enter)
    	  
	  		self.htmlfile.write('<li><h3>Resource Status</h3></li>')
	  		self.htmlfile.write(v_tablel)
	  		self.htmlfile.write('<tr id="col"><td>Resource Name</td><td>Resource Max</td><td>Resource Value</td></tr>')
	  		self.GetSqlResult("""select '<tr id="colName"><td>' || v.RESOURCE_NAME || '</td><td>' || """+
"       v.CURRENT_UTILIZATION || '</td><td>' || v.INITIAL_ALLOCATION ||           "+
"       '</td></tr>'                                                              "+
"  from v$resource_limit v")
	  		self.htmlfile.write(v_tabler)
	  		self.htmlfile.write(v_enter)
    	  
	  		self.htmlfile.write('<li><h3>Index Analyze</h3></li>')
	  		self.htmlfile.write(v_tablel)
	  		self.htmlfile.write('<tr id="col"><td>owner</td><td>tablename</td><td>index_name</td><td>idx_blocks</td><td>table_blocks</td><td>pct</td></tr>')
	  		self.GetSqlResult("""select '<tr id="colName"><td>' || idx.owner || '</td><td>' || idx.table_name ||                   """+
"       '</td><td>' || idx.index_name || '</td><td>' || idx.blocks ||                 "+
"       '</td><td>' || tbl.blocks || '</td><td>' ||                                   "+
"       trunc(idx.blocks / tbl.blocks * 100) / 100 || '</td></tr>'                    "+
"  from (select i.owner owner,                                                        "+
"               i.index_name index_name,                                              "+
"               SUM(S1.blocks) blocks,                                                "+
"               i.table_owner table_owner,                                            "+
"               i.table_name table_name                                               "+
"          from dba_segments s1, dba_indexes i                                        "+
"         where s1.owner = i.owner                                                    "+
"           and s1.segment_name = i.index_name                                        "+
"           and i.owner not in ('SYS',                                                "+
"                               'OUTLN',                                              "+
"                               'SYSTEM',                                             "+
"                               'MGMT_VIEW',                                          "+
"                               'SYSMAN',                                             "+
"                               'DBSNMP',                                             "+
"                               'WMSYS',                                              "+
"                               'XDB',                                                "+
"                               'DIP',                                                "+
"                               'GOLDENGATE',                                         "+
"                               'CTXSYS')                                             "+
"         GROUP BY i.owner, i.index_name, i.table_owner, i.table_name) idx,           "+
"       (select t.owner owner, t.table_name table_name, SUM(s2.blocks) blocks         "+
"          from dba_segments s2, dba_tables t                                         "+
"         where s2.owner = t.owner                                                    "+
"           and s2.segment_name = t.table_name                                        "+
"           and t.owner not in ('SYS',                                                "+
"                               'OUTLN',                                              "+
"                               'SYSTEM',                                             "+
"                               'MGMT_VIEW',                                          "+
"                               'SYSMAN',                                             "+
"                               'DBSNMP',                                             "+
"                               'WMSYS',                                              "+
"                               'XDB',                                                "+
"                               'DIP',                                                "+
"                               'GOLDENGATE',                                         "+
"                               'CTXSYS')                                             "+
"         GROUP BY T.OWNER, T.TABLE_NAME) tbl                                         "+
" where idx.table_owner = tbl.owner                                                   "+
"   and idx.table_name = tbl.table_name                                               "+
"   and (idx.blocks / tbl.blocks) > 0.5                                               "+
"   and idx.blocks > 200  order by idx.owner,idx.table_name,idx.index_name            ")
	  		self.htmlfile.write(v_tabler)
	  		self.htmlfile.write(v_enter)
    	  
	  		self.htmlfile.write('</ul>')
	  		self.htmlfile.close()
	  		#progress.stop()
	  		self.conn.close()
	  		ThreadIsEnd=False
	  def GetSqlResult(self,sql):
	  		cur=self.conn.cursor()
	  		cur.execute(sql);
	  		data = cur.fetchall()
	  		for i in data:
	  			self.htmlfile.write(i[0])
	  			self.htmlfile.write('\n')
	  		cur.close()
i = OracleAnalyze()