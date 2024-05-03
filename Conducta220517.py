########################################################
#LABORATORIO DE PLASTICIDAD Y CONDUCTA SEXUAL, INB, UNAM

#Registro y evaluación de conducta sexual en roedores


########################################################
            #DATOS PRUEBA#
#1,2,60:00
#7,10
#14,19,2
#17,0,0
#00:10,1:01,5:10,6:20

#00:13,00:42
#1:15,2:03,3:01,4:18
#5:13

#00:15,00:52
#1:17,2:06,3:22,5:01
#6:00

import os
from csv import writer
from tkinter import *
import numpy as np
import tkinter.font as tkFont

state=False
bt_state=DISABLED

root=Tk()
root.title('Laboratorio de Plasticidad y Conducta Sexual')
#root.iconbitmap('rata.ico')


class Error(Exception):
    pass

class GeneralDataError(Error):#General Data Error
    pass

class EventError(Error):
    pass

class LordosisError(Error):
    pass

class NumberLordosisError(Error):#incongruent number of lordosis and mounts+intros
    pass 

class LatencyError(Error):
    pass

class PacingError(Error):#pacing format error
    pass

class NumberPacingError(Error):#diferent number of exits and returns in pacing
    pass

class TimeFormatError(Error):#no more than 60 seconds
    pass

def create_frame(spc,tx,r,c):#create a general frame
    frame=LabelFrame(spc,text=tx,padx=20,pady=10)
    frame.grid(row=r, column=c)
    return frame

def create_label(spc,tx,r,c):#create a general label
    title=Label(spc,text=tx)
    title.grid(row=r,column=c)
    
def data_int(spc,tx,n,c,w,st):#create a text input with a title above
    subtitle=Label(spc,text=tx)
    subtitle.grid(row=n,column=c)
    e=Entry(spc,width=w,state=st)#
    e.grid(row=n+1,column=c)
    if st==NORMAL:
        entries.append(e)#save the inputs in a vector
    return entries

def entry_time(data):#convert minutes and seconds to minutes
    if data=='0':
        data=0
        return data
    else:
        data=data.split(":")
        data[0]=int(data[0])
        data[1]=int(data[1]) 
        if data[0]<1000 and data[1]<60:#just keeps times with less than 60 sec in the seconds part
            data=data[0]*60+data[1]
            return data
        else:
            raise TimeFormatError
            
def entry_pacing(data):#convert a list of minutes and seconds to a list of
    time1=[]           #second
    if data=='0':
        time1=np.array(0)
        return time1
    else:
        data=data.split(',')
        for t in data:
            time1.append(entry_time(t))
        time1=np.array(time1)
        return time1 

def pacing_command(bt_state):#Pacing section. Input boxes desabled
    n=6
    frame=create_frame(root,"PACING**",n-1,1)
    fontEx = tkFont.Font(size=8,slant="italic")#family="Arial", weight="bold",
    title=Label(frame,text='SI SE USÓ DIVISIÓN EN LA CAJA DE CÓPULA, ACTIVE EL PACING')
    title.grid(row=0,column=0,columnspan=4)
    title.configure(font=fontEx)
    pacing=Button(frame,text="Activar pacing",padx=52,command=pacing_on)
    pacing.grid(row=1,column=0)
    
    frame1=create_frame(frame,"Salida después del contacto copulatorio",2,0)
    
    data_int(frame1,"MONTAS",n,0,20,bt_state)
    data_int(frame1,"INTROMISIONES",n,1,20,bt_state)
    data_int(frame1,"EYACULACIONES",n,2,20,bt_state)
    
    n=n+1
    frame2=create_frame(frame,"Regreso después del contacto copulatorio",3,0)
    data_int(frame2,"MONTAS",n,0,20,bt_state)
    data_int(frame2,"INTROMISIONES",n,1,20,bt_state)
    data_int(frame2,"EYACULACIONES",n,2,20,bt_state)

def pacing_on():#enable the pacing boxes
    global state,bt_state
    state=True
    bt_state=NORMAL
    pacing_command(bt_state)
    
def pacing_off():#disable the pacing boxes
    state=False
    bt_state=DISABLED
    pacing_command(bt_state)
   
def save_csv(data,file_name):#open the csv. If not, creates a new one
    with open(file_name+'.csv','a',newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(data)
        f_object.close( )

def check_new_file():#Check if there's a csv with required name. If not, creates
    name_file=gral_data[0]+'.csv' #a new one with all the titles
    list_files=os.listdir()
    if (name_file in list_files)==False:
        title=['Subject','Test','Duration','N° Mount S1','N° Intro S1','N° Mount','N° Intro',
               'N° Ejac','Mount Lat','Intro Lat','Ejac Lat','Inter Post Eyac'
               ,'III','Lord Intensity S1','Lord quot S1','Lord Intensity','Lord quot']
        title_raw=['Subject','Test','Duration','N° Mount S1','N° Intro S1','N° Mount','N° Intro',
                   'N° Ejac','Mount Lat','Intro Lat','Ejac time','Ejac Return',
                   'Lord II S1','Lord I S1','Lord 0 S1','Lord II','Lord I','Lord 0']
        if state==True:
              title=title+['Lat Mount Return','Lat Intro Return','Lat Ejac Return',
                           'Mount Exit %','Intro Exit %','Ejac Exit %' ]
              title_raw=title_raw+['Mount Exit','Intro Exit','Ejac Exit','Mount Return',
                                   'Intro Return','Ejac Return'  ]
        save_csv(title,gral_data[0])#file for outut data
        save_csv(title_raw,gral_data[0]+'-RAW')#file for input data

def error_msg(msg):#general format for errors
    errors=Label(root,text=msg,fg="red")
    errors.grid(row=3,column=3)
    errors.after(5000, errors.destroy)    

def save_data(): #check errors
    try:
        show_data()
    except Exception as e:
        error_msg(e)   
    return   

def save_file():#save data in the file
    check_new_file() 
    save_csv(List,gral_data[0])
    save_csv(List_raw,gral_data[0]+'-RAW')
    msg="\n\n\n Rata: "+str(gral_data[1])+"--Prueba: "+str(gral_data[2])+"--GUARDADA    "
    errors=Label(root,text=msg,fg="green")
    errors.grid(row=3,column=3)   
def new_file():#creates a new file. Erase all the data in the interface
    entries[0].delete(0,END)
    entries[3].delete(0,END)
    new_subject()
    pacing_off() 
    label1=create_label(root,   "\n\n\n                                                                         ",4,3)
 
def new_subject():#Erase all the data in the interface, except the file name
    entries[1].delete(0,END) #and the duration test
    entries[2].delete(0,END)
    for i in range(4,19):
        entries[i].delete(0,END)
    if state==True:
        for i in range(19,25):
            entries[i].delete(0,END)

###############################################################################
global entries#entries=data object inputs
entries=[]

subtitle=Label(root,text="       ")
subtitle.grid(row=0,column=0)
subtitle=Label(root,text="       ")
subtitle.grid(row=0,column=4)
subtitle=Label(root,text="    ")
subtitle.grid(row=0,column=2)

#GENERAL DATA SECTION
n=1
frame=create_frame(root,'DATOS GENERALES',n-1,1)
subtitle=Label(frame,text="     NOMBRE DEL ARCHIVO:")
subtitle.grid(row=0,column=0)
entries.append(Entry(frame,width=20))#NAME
entries[0].grid(row=0,column=1)
label1=create_label(frame,".csv",0,2)
#labe=create_label(frame,'    ',1,0)
data_int(frame,"NÚMERO DE SUJETO",1,0,20,NORMAL)
data_int(frame,"NÚMERO DE PRUEBA",1,1,20,NORMAL)
data_int(frame,"DURACIÓN",1,3,19,NORMAL)

#COPULATORY EVENTS SECTION
#FIRST SERIES
n=n+1
frame=create_frame(root,'EVENTOS COPULATORIOS',n-1,1)
frame1=create_frame(frame,'1° SERIE EYACULATORIA',0,0)
data_int(frame1,"MONTAS",n,0,10,NORMAL)
data_int(frame1,"INTROS",n,1,11,NORMAL)
#TOTAL TEST
frame2=create_frame(frame,'TOTALES',0,1)
data_int(frame2,"MONTAS",n,0,10,NORMAL)
data_int(frame2,"INTROS",n,1,11,NORMAL)
data_int(frame2,"EYAC",n,2,10,NORMAL)

#LORDOSIS SECTION
#FIRST SERIES
n=n+1
l=9
frame=create_frame(root,'LORDOSIS',n-1,1)
frame1=create_frame(frame,'1° SERIE EYACULATORIA',0,0)
data_int(frame1,"II",n,0,l,NORMAL)
data_int(frame1,"I",n,1,l,NORMAL)
data_int(frame1,"0",n,2,l,NORMAL)
#TOTAL TEST
frame2=create_frame(frame,'TOTALES',0,1)
data_int(frame2,"II",n,0,l-1,NORMAL)
data_int(frame2,"I",n,1,l-1,NORMAL)
data_int(frame2,"0",n,2,l-1,NORMAL)
#LATENCY TEST
n=n+2
frame=create_frame(root,"LATENCIA*",n-2,1)
data_int(frame,"MONTA",n,0,16,NORMAL)
data_int(frame,"INTROMISION",n,1,17,NORMAL)
data_int(frame,"EYACULACION",n,2,17,NORMAL)
data_int(frame,"REGRESO",n,3,17,NORMAL)
pacing_command(bt_state)

def show_data():#calculate all the data
    global gral_data,cop_data,lord_data,lat_data_seg
    global lat_data,iii,lord_inten,lord_quo,inter_pos_ejac
    global List,List_raw
    global flag
    
    gral_data=[]#general data
    #gral_data=[name,subject,test,duration]
    cop_data=[]#S1 and total copulatory event 
    #cop_data=[mountS1,introS1,mount,intro,ejac]
    lord_data=[]#S1 and total lordosis
    #lord_data=[L2S1,L1S1,L0S1,L2,L1,L0]
    lat_data=[]#latency and return time
    #lat_data=[mount,intro,ejac,return]
    lat_data_seg=[]#latency and return time in seconds
    #lat_data_seg=[mount,intro,ejac,return,lat_ejac]
    try:#converts the object to strings
        for e in range(0,4):
            gral_data.append(entries[e].get())
        gral_data[1]=int(gral_data[1])
        gral_data[2]=int(gral_data[2])
        gral_data.append(entry_time(gral_data[3]))
    except:
        raise GeneralDataError('Error en DATOS GENERALES')
        
    try: 
        for e in range(4,9):
            cop_data.append(int(entries[e].get()))
    except:
        raise EventError('Error en EVENTOS COPULATORIOS')
        
    try:
        for e in range(9,15):
            lord_data.append(int(entries[e].get()))
    except:
        raise LordosisError('Error en LORDOSIS')
        
    try:
        for e in range(15,19):
            lat_data.append(entries[e].get())
        for e in range(15,19):
            lat_data_seg.append(entry_time(entries[e].get()))
        if lat_data_seg[2]==0:#no ejac
            lat_data_seg.append(0)#lat ejac
        else:#intro+ejac
            lat_data_seg.append(lat_data_seg[2]-lat_data_seg[1])#lat ejac  
    except:
        raise LatencyError('Error en LATENCIA')

    if cop_data[3]==0 and cop_data[4]==0:#no intro & no ejac
        inter_pos_ejac=0#inter_pos_ejac=0
        iii=0
     
    if cop_data[4]==0 and cop_data[3]!=0:#no ejac, + intros 
        inter_pos_ejac=0
        iii=np.round((gral_data[4]-lat_data_seg[1])/cop_data[1],2) 
    
    if cop_data[4]!=0 and lat_data_seg[3]==0:# + ejac, no intros 
        inter_pos_ejac=0
        iii=np.round((gral_data[4]-lat_data_seg[1])/cop_data[1],2) 

    if cop_data[4]!=0 and lat_data_seg[2]!=0 and lat_data_seg[3]!=0:#normal
        #print('Caso NORMAL') 
        inter_pos_ejac=(lat_data_seg[3]-lat_data_seg[2])#inter_pos_ejac=reg_ejac-lat_ejac
        iii=np.round((lat_data_seg[4])/cop_data[1],2)#(lat_ejac-lat_intro)/n_intro1

       
    n_acc_s1=np.sum(lord_data[0:3])#num S1 cop events
    n_acc=np.sum(lord_data[3:6])#number of total copulatory events
    
    if n_acc_s1!=np.sum(cop_data[0:2]):
        raise NumberLordosisError('N° incongruente de LORDOSIS S1')
    lord_calc=[]
    lord_calc.append(np.round((lord_data[0]*2+lord_data[1])/(n_acc_s1),2))#lord intensity S1
    lord_calc.append(np.round(((lord_data[0]+lord_data[1])/(n_acc_s1))*100,2))#lordosis quotient S1
    
    if n_acc!=0:
        if n_acc!=np.sum(cop_data[2:4]):
            raise NumberLordosisError('N° incongruente de LORDOSIS TOTALES')
        else:
            lord_calc.append(np.round((lord_data[3]*2+lord_data[4])/(n_acc),2))#lord inten Total
            lord_calc.append(np.round(((lord_data[3]+lord_data[4])/(n_acc))*100,2))#lord quot Total
    else:
        lord_calc.append(0)#lord intentsity
        lord_calc.append(0)#lord quotient
        
    List=gral_data[1:4]+cop_data+lat_data_seg[0:2]+[lat_data_seg[4]]+[inter_pos_ejac]+[iii]+lord_calc#output file
    List_raw=gral_data[1:4]+cop_data+lat_data+lord_data#input file
    
    ##########################   PACING ##################################
    if state==True:
        global p_times,p_times_seg,lat_pacing, exit_por
        p_times=[]
        p_times_seg=[]
        
        try:
            for i in range(19,25):
                p_times.append(entries[i].get())
      
            for e in p_times:
                p_times_seg.append(entry_pacing(e))
        except:
            raise PacingError('Error en PACING')
        # except:
             #raise PacingError('Error en PACING')
        # except Exception as e:
        #     error_msg(e) 
            
        for n in [0,1,2]:
            if np.sum(p_times_seg[n])==0:
                if np.sum(p_times_seg[n+3])!=0:
                    raise NumberPacingError('Núm. incongruente en PACING')
            else:
                if len(p_times_seg[n])!=len(p_times_seg[n+3]):
                    raise NumberPacingError('Núm. incongruente en PACING')
                
        lat_pacing=[]
        for i in range(0,3):
            if np.sum(p_times_seg[i])==0:#if no pacing
                lat_pacing.append(0)
            
            else:
                lat_pacing.append(np.round(np.sum(p_times_seg[3+i]-p_times_seg[i])/len(p_times_seg[i]),2))

        exit_por=[]
        for i in range(0,3):
            if np.sum(p_times_seg[i])==0:
                exit_por.append(0)                
            else:
                if i==2:
                    exit_por.append(np.round((len(p_times_seg[2])/1)*100))
                else:
                    exit_por.append(np.round((len(p_times_seg[i])/cop_data[i])*100))

        List=List+lat_pacing+exit_por
        List_raw=List_raw+p_times
    save_file()


##############################################################################
c=3   
new_rat=Button(root,text="Nuevo Sujeto",padx=34,pady=10,command=new_subject)
new_rat.grid(row=0,column=c)

new_file=Button(root,text="Nuevo Archivo",padx=30,pady=10,command=new_file)
new_file.grid(row=1,column=c)

save_f=Button(root,text="Guardar",padx=49,pady=10,command=save_data)#to check data, change save_data to show_data
save_f.grid(row=2,column=c)

fontEx = tkFont.Font(size=8,slant="italic")#family="Arial", weight="bold",
title=Label(root,text='SI NO HAY DATOS, INGRESE 0\n\n'
            '*Ingrese los tiempos en el formato mm:ss.\n' 
            'P. ej: Diez min con cuarenta seg= 10:40\n'
            'No ingresar tiempos como: ":10,00-10,00.10"\n\n'
            '**Ingrese los tiempos en el formato\n mm:ss, mm:ss '
'\n P. ej: Dos min con un seg y seis \n min con quince seg= 2:01,6:15\n\n'
            'Los datos de LATENCIAS y PACING se \n toman de la PRIMERA SERIE eyaculatoria')
title.grid(row=5,column=c)
title.configure(font=fontEx)

root.mainloop()
#28:07,29:12,29:43,31:23,32:23
#29:10,29:41,31:20,32:20,33:44
