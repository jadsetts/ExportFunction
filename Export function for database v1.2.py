# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 15:03:30 2023

@author: Danny Chhin
"""

import os
import re
from datetime import date
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from calendar import month_name
from tkinter import filedialog as fd

"""
List of options for metadata that are chosen from list instead of an user input
To modify options just change the content of the list
To add a variable with options you need to make a new list and link it to the variable using the meta class 
example new_variable(export, label="new variable label text", button="type of button: combobox, entry...", options= "name of the option list variable")
   
"""
#---------------------------------------------------------------------------------------
#General info 
op_list= ["Lindsay Grandy", "Sarah Yassine", "Hu Zhou", "Jon special's"]
tech_list= ["SECCM", "SECM", "SKP"]

#Mapping info
pattern_list= ["Parallel", "Snake"]

#Sample
field_list= ["Battery", "Corrosion", "Sensor"]
project_list= ["Academic", "FATCO", "NRC", "Medtronic"]
inst_list= ["Dr. Scanny Chhin", "ELP3", "HEKA in GB(UQAM)"]
sample_list= ["Al", "AA", "SS"]
alloy_list= ["Pure", "7075", "1000"]
prep_list= ["As is", "Rinsed", "Etching", "Polish: rough", "Polish: mirror"]
polishmat_list= ["Silica", "Diamond", "Alumina"]
etchmat_list= ["HF", "HCl"]

#Experimental list for SECCM
electrolyte_list= ["0.1M KCl", "3.5% NaCl"]
ref_list=["SCE ref", "Ag/AgCl ref", "Ag/AgCl wire", "Ag/AgNO$_3$"]
appmethod_list=["Potentiostatic", "Galvanostatic", "AC potential"]

#Experimental list for SECM
#electrolyte_list= ["0.1M KCl", "3.5% NaCl"]
mediator_list= ["None", "FcMeOH", "RubPy"]
mode_list= ['Feedback', "Tip collection"]

#Experimental list for SKP

#Creating the export main window and frame 
export= tk.Tk()

#Getting current date
date= date.today().strftime("%d/%m/%Y")

# Path to preset file
preset_file= r"C:\Users\Admin\OneDrive - McGill University\Post doc_Mauzeroll\Project\Metadata app\preset.txt" 
# Path to database file
database_file=r"C:\Users\Admin\OneDrive - McGill University\Post doc_Mauzeroll\Project\Metadata app\Meta_database.txt"

"""
Meta class pertaining to any metadata variable
Creating the class meta to generate the metadata variable and any other associated elements such as label and GUI elements.
It will do the following:
    1- Generate 6 attributes (var, text, options, label, button, metabind)
    2- Set the default value of the metavariable to "Not selected yet" 
    3- Create a label from the text self.attribute and is the self.label attribute
    4- Create a button based on the type of button and is the self.button attribute
        
The arguments for the class are:
    1- self: the class instance name aka metavariable name
    2- tkwindow: The window in tkinter in which the metavariable will be attached too for example here in the export function it will be the export window 
    3- text: String variable that serves as a description of the metavariable and also used for the Label text
    4- button_type: Variable to indicate which type of of GUI elements to generate for the metadata variable, for the export window it is either an entry or combobox, more can be added if needed
    5- options: List of options for GUI elements that requires users to select from a list of options.
    6- bind: Nature of event to trigger a binding event with a GUI element. For example, '<FocusIn>' to indicate an GUI is selected by mouse or '<Motion>' for mouse motion over GUI element  
    
The class methods are:
    1- create_button(self, button) create a GUI element based on the attribute self.button, if self.button=None then no button is created
    2- value(self) gets the current metavariable value as it can change based on user input
    3- clear_entry(self, event) clear an antry field on '<FocusIn>'
    4- bind_meta(self) binding the clear_entry method to the metavariable
"""

class meta:       
    
    def __init__(self, tkwindow, text, button_type=None, options=None, bind=None):
        self.var= tk.StringVar(tkwindow) #Initiating tkinter variable that can change during program run
        self.var.set("Not selected yet") #Setting initial value as "not selected yet"
        self.text= text #Text for label of metadata variable
        self.options= options #For method with options chosen from menu, list of all options in the menu
        self.label= tk.Label(tkwindow, text=self.text) #Initializing a label
        self.button_type= button_type
        self.button= self.create_button(button_type) #Initializing a button based on keyword "entry or "combobox"
        self.metabind= bind #Initialize a bind based on the binding trigger '<FocusIn>' or other
    
    def create_button(self, button):
            
        if button=="combobox":
            return ttk.Combobox(export, textvariable=self.var, values=self.options, state='readonly')
            
        if button=="entry":
           return tk.Entry(export, textvariable= self.var)
        
        else:
            pass
       
    def value(self):
        return self.var.get()   
    
    def clear_entry(self, *event):
        self.var.set("")
        
    def integer_only(self, *event):
        if re.fullmatch("^[0-9]+", self.value()):
            pass
        else:
            self.var.set("")
    
    def bind_clear(self):
        return self.button.bind(self.metabind, self.clear_entry, add="+")
    
    def bind_integer_only(self):
        return self.var.trace('w', self.integer_only)
             
           
#Initializing list of variables for all metadata needed to describe experiments from meta class
filename= meta(export, "Name of file")
Xpts= meta(export, "Number of points in X mapped", button_type="entry", bind='<FocusIn>')
Ypts= meta(export, "Number of points in Y mapped", button_type="entry", bind='<FocusIn>')
dmap= meta(export, "Distance between points (um)", button_type="entry", bind='<FocusIn>')
op= meta(export, "Experiment author", options=op_list, button_type="combobox")
tech= meta(export, "Mapping technique", options=tech_list, button_type="combobox")
project= meta(export, "Project", options=project_list, button_type="combobox")
inst= meta(export, "Instrument used", options=inst_list, button_type="combobox")
sample= meta(export, "Nature of sample", options=sample_list, button_type="combobox")
alloy= meta(export, "Specific alloy", options=alloy_list, button_type="combobox")
prep= meta(export, "Sample preparation", options=prep_list, button_type="combobox")
electrolyte= meta(export, "Electrolyte composition", options=electrolyte_list, button_type="combobox")
mediator= meta(export, "Redox mediator", options=mediator_list, button_type="combobox")
mediator_conc= meta(export, "Redox mediator concentration (mM)", button_type="entry", bind='<FocusIn>')
ref= meta(export, "Reference electrode", options=ref_list, button_type="combobox")
appmethod= meta(export, "Approach method", options=appmethod_list, button_type="combobox")
rcap= meta(export, "Capillary tip radius (um)", button_type="entry", bind='<FocusIn>')
pattern= meta(export, "Mapping pattern", options= pattern_list, button_type="combobox")
Vapp= meta(export, "Approach potential (V)", button_type="entry", bind='<FocusIn>')
AC_amp= meta(export, "AC amplitude (mV)", button_type="entry", bind='<FocusIn>')
AC_freq= meta(export, "AC frequency (Hz)", button_type="entry", bind='<FocusIn>')
Field= meta(export, "Field of research", button_type="combobox")


#Function to expedite button construction in the export window
            
"""
@@@@@@@@@@@@  Main section  @@@@@@@@@@@@@@@@
This section contains the metadata required to proceed further
1- the file to export -> Eveything starts here 
2- the technique -> Depending on the technique, the list of metadata to choose can vary significantly
3- the operator -> linked to their own preset settings that they can save and load -> Necessary to choose operator to know which preset setting to load and save to

Positionning of GUI elements: rows: 0-2, column:0-3
"""

def select_file():
    path= fd.askopenfilename(title= "Select file to export", initialdir='/', filetypes=[('MatLab files', '*.mat')])
    filename.var.set(path)
  
main_label= tk.Label(export, text=" Choose your data file, operator and mapping technique ", font=('URW Gothic L','10', 'bold')).grid(row=0, column=0, padx=10, pady=10, columnspan=3, sticky=tk.W)
file_browser= tk.Button(export, text="Browse file", width=15, relief=tk.RAISED, command= lambda: select_file()).grid(column=0, row=1, padx=5, pady=2, sticky=tk.W)
file_lbl= tk.Label(export, textvariable= filename.var, width=80, bg="white", relief=tk.SUNKEN).grid(column=1, row=1, padx=5, pady=2, columnspan=3, sticky=tk.W)
tech.label.grid(column=0, row=2, padx=10, pady=5, sticky=tk.W)
tech.button.grid(column=1, row=2, padx=5, pady=2, sticky=tk.W)
op.label.grid(column=0, row=3, padx=10, pady=5, sticky=tk.W)
op.button.grid(column=1, row=3, padx=5, pady=2, sticky=tk.W)


"""
@@@@@@@@@@@@  Preset section  @@@@@@@@@@@@@@@@
Presettings allows to save and load selections of metadata for convenience.
The buttons are inactive until the operator is selected as the preset are linked to each operator
"""
preset_label= tk.Label(export, text=" Preset", font=('URW Gothic L','10', 'bold')).grid(row=0, column=4, padx=5, columnspan=2, sticky=tk.W) #Preset label for the section
preset_list=[op, tech, project, inst, sample, alloy, prep, Xpts, Ypts, dmap, rcap, pattern, ref, electrolyte, mediator, mediator_conc, appmethod, Vapp, AC_amp, AC_freq]


def preset_buttons(function, button_no, preset_list, preset_file):
    
    preset_values=[]
    for i in preset_list:
        preset_values.append(i.var.get())
    op_preset_list=[] #Initializing the list of all operator in the preset file there can be possibly 3 operator per file corresponding to 3 different saved preset per author. Where the different preset are distinguished by #1,2,3 for example Danny Chhin1 is preset 1 and Danny Chhin2 is preset 2
    chosen_preset= preset_values[0]+f"{button_no}" #Setting up the specific operator preset among preset #1,2,3
    op_found= False #State variable to indicate if the preset is in the preset database
       
    with open(preset_file, 'r') as f: #(preparing to read the preset file)
        data= f.readlines() # File read where each line of the line is an element in the list for example data[0] is first line and data[-1] is last line
        for i,j in enumerate(data):
            op_preset_list.append([j.split("\t")[0],i]) #Making a list of all operators contained in preset file by taking the first element of the line separated by tab and the associated line number
    
        if function=="load":
            for i in op_preset_list: # Cycling through all the preset by operator
                if i[0]== chosen_preset: # Selecting the operator of choice
                    preset_data= data[i[1]].split("\t") #Putting data of interest in list
                    preset_data.remove("\n")
                    preset_data[0]=chosen_preset[0:-1]
                    op_found= True
                    for i,j in enumerate(preset_list):
                       j.var.set(preset_data[i])
                       
            if not op_found:
                messagebox.showinfo("INFORMATION", f"No preset found, cannot load preset {button_no} for {preset_values[0]}!")
                
        if function=="save":
            preset_values.append("\n")
            preset_values[0]= chosen_preset
            new_data= "\t".join(preset_values)
            for i in op_preset_list: # Cycling through all the preset by operator
                if i[0]== chosen_preset: # Selecting the operator of choice
                    data[i[1]]= new_data
                    op_found= True
                    with open(preset_file, 'w') as f:
                        f.writelines(data)
                
            if not op_found:
               with open(preset_file, 'a') as f:
                   f.writelines(new_data)
                   
            messagebox.showinfo("INFORMATION", f"Preset {button_no} saved!")
                          
# Creating loading and saving buttons, by default they start disabled and can only be enabled once the operator has been chosen

load_button1=ttk.Button(export, text="Load Preset 1", command= lambda: preset_buttons("load", "1", preset_list, preset_file), width=30, state='disabled')
load_button2=ttk.Button(export, text="Load Preset 2", command= lambda: preset_buttons("load", "2", preset_list, preset_file), width=30, state='disabled')
load_button3=ttk.Button(export, text="Load Preset 3", command= lambda: preset_buttons("load", "3", preset_list, preset_file), width=30, state='disabled')

load_button1.grid(row=1, column=4, padx=5, sticky=tk.E)
load_button2.grid(row=2, column=4, padx=5, sticky=tk.E)
load_button3.grid(row=3, column=4, padx=5, sticky=tk.E)

save_button1= ttk.Button(export, width=30, text="Save Preset 1", command= lambda: preset_buttons("save", "1", preset_list, preset_file), state='disabled')
save_button2= ttk.Button(export, width=30, text="Save Preset 2", command= lambda: preset_buttons("save", "2", preset_list, preset_file), state='disabled')
save_button3= ttk.Button(export, width=30, text="Save Preset 3", command= lambda: preset_buttons("save", "3", preset_list, preset_file), state='disabled')

save_button1.grid(row=1, column=5, padx=5, sticky=tk.W)
save_button2.grid(row=2, column=5, padx=5, sticky=tk.W)
save_button3.grid(row=3, column=5, padx=5, sticky=tk.W)

# Function to enable presets button to be active once the operator has been chosen
def preset_active(*arg):
    if op.var.get()!="Not selected yet":
        load_button1.config(state='normal')
        load_button2.config(state='normal')
        load_button3.config(state='normal')
        save_button1.config(state='normal')
        save_button2.config(state='normal')
        save_button3.config(state='normal')
        
        
#Linking choice of operator from combobox to trigger the activation of preset buttons        
op.var.trace("w", preset_active)
                     
"""
@@@@@@@@@@@@  Metadata section  @@@@@@@@@@@@@@@@
Where to select or input the metadata for your map
Some of the input are context selective becuase they lead to different choices
This section is split into metadata categories where each one are grouped together in the same column
"""
meta_label= tk.Label(export, text="Fill out the map metadata", font=('URW Gothic L','10', 'bold')).grid(row=5, column=0, padx=10, pady=10, columnspan=6, sticky=tk.W)
blank_label= tk.Label(export, text="").grid(row=4, column=0, padx=10, columnspan=6, sticky=tk.W)


# Sample section. Positionning: column 0-1 row: 6-len(sample_section)
sample_section= [project, inst, sample, alloy, prep]

for i,j in enumerate(sample_section):
    j.label.grid(row=i+6, column=0, padx=5, pady=3)
    j.button.grid(row=i+6, column=1, padx=5, pady=3)
    
# Mapping section: Xpts, Ypts, dmap, rcap, pattern
mapping_section= [Xpts, Ypts, dmap, rcap, pattern]

for i,j in enumerate(mapping_section):
    j.label.grid(row=i+6, column=2, padx=5, pady=3)
    j.button.grid(row=i+6, column=3, padx=5, pady=3)   
    if j.metabind== '<FocusIn>':
        j.bind_clear()     
    if j.button_type== 'entry':
        j.bind_integer_only()
        
# Experimental section
exp_section= [ref, electrolyte, mediator, mediator_conc, appmethod, Vapp, AC_amp, AC_freq]

for i,j in enumerate(exp_section):
    j.label.grid(row=i+6, column=4, padx=5, pady=3)
    j.button.grid(row=i+6, column=5, padx=5, pady=3)  
    if j.metabind== '<FocusIn>':
        j.bind_clear()
    

# Function to trigger context sensitive menu. The approach method input will change depending on the method of approach so only the relevant options are active
# For example if the approach is potentiostatic the only input is the approach potential and the AC entry box (freq, amp and E) will be greyed out
# The opposite is true if AC is chosen then the approach potential will be greyed out
 
def mediator_method(*arg):
    if mediator.var.get()=="None":
        mediator_conc.var.set("0")
        
def approach_method(*arg):

    if appmethod.var.get()== "Potentiostatic":
        Vapp.var.set("Not selected yet")
        Vapp.button.config(state='normal')
        
        AC_amp.var.set(None)   
        AC_freq.var.set(None)
        
        AC_amp.button.config(state='disabled')
        AC_freq.button.config(state='disabled')
                    
    if appmethod.var.get()== "Galvanostatic":
        Vapp.var.set(None)
        AC_amp.var.set(None)   
        AC_freq.var.set(None)
      
        Vapp.button.config(state='disabled')
        AC_amp.button.config(state='disabled')
        AC_freq.button.config(state='disabled')
       
    if  appmethod.var.get()== "AC potential":
        AC_amp.var.set("Not selected yet")   
        AC_freq.var.set("Not selected yet")
        
        AC_amp.button.config(state='normal')
        AC_freq.button.config(state='normal')
        
        Vapp.var.set(None)
        Vapp.button.config(state='disabled')
      
         
# trace method to link change of the variable appmethod to trigger the function approach_method
# the 'w' correspond to a writing event to trigger the event so basically each time the appmethod variable is changed by choosing an option from combobox
appmethod.var.trace("w", approach_method)
mediator.var.trace("w", mediator_method)

"""
@@@@@@@@@@@@@@@@@@@@@@@@ Exporting data @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
This section is the code to export data.
To ensure metadata is properly filled there is a few failsafe
1- All metadata fields mut be filled
2- Entry data must be integers
3- The metadata entry does not already exist in the database

""" 

meta_var=[filename, tech, op, project, inst, sample, alloy, prep, Xpts, Ypts, dmap, rcap, pattern, ref, electrolyte, mediator, mediator_conc, appmethod, Vapp, AC_amp, AC_freq]

def export_meta(meta_var, database_file):
    meta_values=[] # A list of the metadata values from the metadata variables that will be exported
    complete_meta= True
    answer=True
    for var_value in (meta_var): #Going trough all the metadata variables
        if var_value.var.get()=="Not selected yet": #Check if the medatadata variable has been filled or not
            messagebox.showinfo("WARNING!", "Not all metadata has been selected! \n Data not exported!")
            complete_meta= False
            break
        meta_values.append(var_value.var.get()) #Append the metadata values
    meta_values.append('\n') #Add a line change to separate new entries
                      
    if complete_meta: #If all the metadata field have been filled then there we must check if the data exported already exist in database

        with open(database_file, 'r') as f:
            for i,j in enumerate(f.readlines()):
                filename_database=j.split('\t')[0]
                if meta_var[0].var.get()==filename_database:
                    answer=messagebox.askyesno("WARNING!", "The file already exist are you sure you want to export?")
                    break    
            
            if answer:           
                with open(database_file, 'a') as f:  
                    f.write("\t".join(meta_values))
                    messagebox.showinfo("INFORMATION", "Data successfully exported! \nThank you for your contribution to science!")
                    
            else:
                messagebox.showinfo("INFORMATION", "Data not EXPORTED")
                
export_b= tk.Button(export, text="EXPORT DATA", font=('URW Gothic L','12', 'bold'), width=70, height=5, command= lambda: export_meta(meta_var)).grid(column=0, row=11, rowspan=4, columnspan=4, padx=10, pady=10, sticky=tk.N)
    
export.mainloop()

        