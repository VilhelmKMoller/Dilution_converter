#!/usr/bin/env python
# coding: utf-8

# In[203]:


import pandas as pd
from scipy.stats import linregress
# from the tkinter library
import tkinter as tk
from tkinter import *

# import filedialog module
from tkinter import filedialog

# to make time stamp
import datetime
from datetime import datetime


# In[174]:


### TO DO ####
#Make an output with the data used and the calculation done and the output created. 

##add on
## python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
## pip install xlrd
## pip install openpyxl


# In[175]:


################################### USER VERIABLES #################################################
## Change the concetration or the initial sample volume by altering the numbers below:
# VolIn = (ConOut * ConOut) / ConIn 
SampleVolume = 5 # uL of sample
FinalConcentration = 2.5 # nG/uL
################################### USER VERIABLES #################################################


# In[176]:


## Creat a browser for extraciting the file position for the pico green file
  
# Function for opening the
# file explorer window
def browseFiles():
    global filename
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.xlsx*"),
                                                       ("all files",
                                                        "*.*")))     
    # Change label contents
    label_file_explorer.configure(text="File Opened: "+filename)

      
def exit():
    window.destroy()
    exit()
                                                                                                  
# Create the root window
window = Tk()
  
# Set window title
window.title('File Explorer')
  
# Set window size
#window.geometry("500x250")
  
#Set window background color
window.config(background = "white")

entry1 = Entry (window)


# Create a File Explorer label
label_file_explorer = Label(window,
                            text = "File Explorer using Tkinter",
                            width = 100, height = 4,
                            fg = "blue")
  
      
button_explore = Button(window,
                        text = "Browse Files",
                        command = browseFiles)
  
button_exit = Button(window,
                     text = "Exit",
                     command = exit)

  
# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column = 1, row = 1, sticky=N)
  
button_explore.grid(column = 1, row = 2, sticky=N)
  
button_exit.grid(column = 1,row = 3, sticky=N)

# Let the window wait for any events
window.mainloop()


# In[178]:


dfInput = pd.read_excel(filename)
#dfInput = pd.read_excel('inputPico2.xlsx')
dfTop = pd.DataFrame(columns=['Source_well', 'Dilution_volume', 'Destination_Well', 'Source_volume' ])

dfExtra = pd.DataFrame(columns=['Source_well', 'Dilution_volume', 'Destination_Well', 'Source_volume' ])


# In[179]:


# extract the wavelengths from Synergy H1 file
pico_raw = dfInput.iloc[29:45,2:26]


# In[180]:


## old method for prompting user for output:
#number_samples = 16 #int(input("Please enter number of samples: "))

## make a text box that user can writ the number of samples in:
root= tk.Tk()

canvas1 = tk.Canvas(root, width = 400, height = 300)
canvas1.pack()

entry1 = tk.Entry (root) 
canvas1.create_window(200, 140, window=entry1)

def number_of_samples ():  
    global number_samples
    number_samples = entry1.get()
    #print(x1)
    label1 = tk.Label(root, text= int(number_samples))
    canvas1.create_window(200, 230, window=label1)
    
# exit function
def close_window():
    root.destroy()
    exit()
    
button1 = tk.Button(text='Number of samples', command=number_of_samples)
canvas1.create_window(200, 180, window=button1)

#x1 = entry1.get()
button2 = tk.Button(text='Exit', command=close_window)
canvas1.create_window(200, 260, window=button2)
root.mainloop()
## Link up with rest of script. call number of samples 

number_samples = int(number_samples)


# In[181]:


# extract the 96 samples from the 384 layout. 


# is the data row by row or column by column ????

## for column by column
count = 0; samples_collect = []
for i in range(pico_raw.shape[1]):
    row = pico_raw.iloc[:,i]
    count += 1

    # go cell by cell in row variable
    for cell in row: 
        # each 384 row is 16 long. Therefor times 4. 
        if len(samples_collect) < 4*number_samples:
            samples_collect.append(cell)

"""
## for row by row
for i in range(pico_raw.shape[0]):
    cell = pico_raw.iloc[i]
    print(cell)
"""


# In[182]:


## delete every second cell starting from the second cell.
del samples_collect[1::2 ]


# In[183]:


## extract all 20 fold dilutions 
dil_20 = samples_collect[0:8] +         samples_collect[2*8:3*8] +         samples_collect[4*8:5*8] +         samples_collect[6*8:7*8] +         samples_collect[8*8:9*8] +         samples_collect[10*8:11*8] +         samples_collect[12*8:13*8] +         samples_collect[14*8:15*8] +         samples_collect[16*8:17*8] +         samples_collect[18*8:19*8] +         samples_collect[20*8:21*8] +         samples_collect[22*8:23*8] 
#print(dil_20)
#print('len(dil_20))', len(dil_20))

dil_100 = samples_collect[8:2*8] +         samples_collect[3*8:4*8] +         samples_collect[5*8:6*8] +         samples_collect[7*8:8*8] +         samples_collect[9*8:10*8] +         samples_collect[11*8:12*8] +         samples_collect[13*8:14*8] +         samples_collect[15*8:16*8] +         samples_collect[17*8:18*8] +         samples_collect[19*8:20*8] +         samples_collect[21*8:22*8] +         samples_collect[23*8:24*8] 


# # Start Data processing

# In[184]:


## extract the dilution ladder
pico_ladder = dfInput.iloc[44:45,21:26]


# In[185]:


# subtract Zero from sample(Pos Z44 excel) OPS OPS This will be W44 in the future
standard_zero = pico_ladder.iloc[0][0]
d20_standard = []; d100_standard = []
for i in range(len(dil_20)):
    cell_d20 = dil_20[i]
    cell_d100 = dil_100[i]
    d20_standard.append(cell_d20 - standard_zero)
    d100_standard.append(cell_d100 - standard_zero)


# In[186]:


## Find the ladder reads used to make the standard curve and subtract the background noise. 
ladder_reads = list(pico_ladder.iloc[0][0:]) - standard_zero

## know concentrations of ladder read
ng_pr_ul = [0,10,100,1000,10000]


# In[187]:


## linear regression using ladder read
slope = linregress(ng_pr_ul, ladder_reads)[0]
intercept = linregress(ng_pr_ul, ladder_reads)[1]
Rvalue = linregress(ng_pr_ul, ladder_reads)[2]
std_err = linregress(ng_pr_ul, ladder_reads)[4]


# In[188]:


d20_curve = []; d100_curve = [];
for num in range(len(d20_standard)):
    ## find the dna concentration by using the ladder_reads. Times with the volume / dilution factor 
    d20_curve.append( ((d20_standard[num] + intercept) / slope) * 20/1000 )
    d100_curve.append( ((d100_standard[num] + intercept) / slope) * 100/1000 )
    


# In[189]:


## find the mean of the two dilutions
dna_concentrations = []
for num in range(len(d100_curve)):
    dna_concentrations.append( round( (d100_curve[num] + d20_curve[num]) / 2 ,2))


# In[ ]:





# # Text boxes. Will work on later

# In[190]:


"""
## Boiler plate for extracting files 
import pandas as pd
# Python program to create
# a file explorer in Tkinter
  
# import all components
# from the tkinter library
from tkinter import *
  
# import filedialog module
from tkinter import filedialog
  
# Function for opening the
# file explorer window
def browseFiles():
    global filename
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.xlsx*"),
                                                       ("all files",
                                                        "*.*")))     
    # Change label contents
    label_file_explorer.configure(text="File Opened: "+filename)

      
def exit():
    window.destroy()
    exit()
                                                                                                  
# Create the root window
window = Tk()
  
# Set window title
window.title('File Explorer')
  
# Set window size
#window.geometry("500x250")
  
#Set window background color
window.config(background = "white")

entry1 = Entry (window)


# Create a File Explorer label
label_file_explorer = Label(window,
                            text = "File Explorer using Tkinter",
                            width = 100, height = 4,
                            fg = "blue")
  
      
button_explore = Button(window,
                        text = "Browse Files",
                        command = browseFiles)
  
button_exit = Button(window,
                     text = "Exit",
                     command = exit)

  
# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column = 1, row = 1, sticky=N)
  
button_explore.grid(column = 1, row = 2, sticky=N)
  
button_exit.grid(column = 1,row = 3, sticky=N)



# Let the window wait for any events
window.mainloop()
print(filename)
dftestinpout = pd.read_excel(filename)
print('hello')
display(dftestinpout)
"""


# In[ ]:





# In[191]:


"""
from tkinter import *

# key down function
def click():
    entered_text=textentry.get() # collect text from text box
    output.delete(0.0, END)
    try:
        definition = my_compdictionary[entered_text]
    except:
        definition = 'sorry there is no word like that please try again'
    output.insert(END, definition)

# exit function
def close_window():
    window.destroy()
    exit()

window = Tk()
window.title("My Computer science")
window.configure(background='black')

# create label
Label (window, text='Enter the word you would like a definition of:', bg='black', fg='white', font='none 12 bold') .grid(row=0, column=0, sticky=W)

# creeate a text entry box
textentry = Entry(window, width=20, bg='white')
textentry.grid(row=2, column=0, sticky=W)

#add a submit button
Button(window, text='SUBMIT', width=6, command=click) .grid(row=3, column=0, sticky=W)

# create another label
Label (window, text='\nDefinition:', bg='black', fg='white', font='none 12 bold') .grid(row=4, column=0, sticky=W)

# create a text box 
output = Text(window, width=75, height=6, wrap=WORD, background='white')
output.grid(row=5, column=0, columnspan=2, sticky=W)

my_compdictionary = {
    'algorithem': 'step by step instructions to complete a task', 'bug': 'pice of code that causes a program to fail'
}

# exit label
Label (window, text='click to exit:', bg='black', fg='white', font='none 12 bold') .grid(row=6, column=0, sticky=W)

#add a exit button
Button(window, text='Exit', width=14, command=close_window) .grid(row=7, column=0, sticky=W)

## run the main loop
window.mainloop()
"""


# In[192]:


"""
import tkinter as tk

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 400, height = 300)
canvas1.pack()

entry1 = tk.Entry (root) 
canvas1.create_window(200, 140, window=entry1)

def number_of_samples ():  
    global x1
    x1 = entry1.get()
    #print(x1)
    label1 = tk.Label(root, text= float(x1))
    canvas1.create_window(200, 230, window=label1)
    
# exit function
def close_window():
    root.destroy()
    exit()
    
    
button1 = tk.Button(text='Number of samples', command=number_of_samples)
canvas1.create_window(200, 180, window=button1)

#x1 = entry1.get()
button2 = tk.Button(text='Exit', command=close_window)
canvas1.create_window(200, 260, window=button2)
root.mainloop()

print(x1)
"""


#    # Make the dilution calculations
#     

# In[193]:


# Fill waterList with water amount needing to be added to 10uL sample to ubtain concentration of 2.5ng/uL
# number rounded to 2 decimal places. 
waterList = []
for i in range(len(dna_concentrations)):
    SampleConcetration = dna_concentrations[i]
    WaterAdded = round( ((SampleVolume * SampleConcetration) / FinalConcentration ) - SampleVolume) # change from uL to nL
    waterList.append(WaterAdded)
    #print(WaterAdded)
#print(waterList)


# In[194]:


DestinationArray = []; start = 1; addressPositionList = []
for num in range(start, len(dna_concentrations)+1):
    ## Converts destinations into plate format A1, B1 .. A2 ..B2 .. H12. Column by column. 96 well PCR plate
    platePosition = 'ABCDEFGH'[((num - 1) % 8+1) - 1] + '%1d' % ((num - 1) // 8+1,) #UPPERCASE
    DestinationArray.append(platePosition)

    ## Converts destinations into plate format A1, B1 .. A2 ..B2 .. H12. Column by column. 96 well PCR plate
    plateSourcePosition = 'ABCDEFGH'[((num - 1) % 8+1) - 1] + '%1d' % ((num - 1) // 8+1,) #UPPERCASE
    addressPositionList.append(plateSourcePosition)


# In[195]:


# load all the data into the df
dfTop['Source_well'] = addressPositionList
dfTop['Destination_Well'] = DestinationArray
dfTop['Dilution_volume'] = waterList
dfTop['Source_volume'] = [str(SampleVolume)] * len(dna_concentrations)
# create SampleVolumeList
SampleVolumeList = [10] * len(dna_concentrations)
#print(dfTop)


# # Screen data for negative values

# In[196]:


## find all negative values in the df and insert them in another df
#dfTop


# In[197]:


## if Dilution_volume is less than 0 in list then call true
cond = dfTop.Dilution_volume < 0
## get position for all rows containing Dilution_volume < 0 
rows = dfTop.loc[cond, :]
## append those rows to dfExtra
dfExtra = dfExtra.append(rows, ignore_index=True)
## drop the rows in dfExtra from dfTop
dfTop.drop(rows.index, inplace=True)


# In[ ]:





# # Output the data to be used

# In[216]:


#from datetime import datetime
#generate date
#today = datetime.date.today()

from datetime import date

today = date.today()

# generate time 
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
# convert to tab seprated file(.txt). 
dfTop.to_csv(str(today) + '_DilutionForFelix.txt', index = False, sep="\t") 

if dfExtra.shape[0] > 0:
    dfExtra.to_csv(str(today) + '_DilutionForFelix_negative_positions.txt', index = False, sep="\t") 


# In[199]:


pico_raw.shape


# In[218]:


# Writing to an excel 
# sheet using Python
import xlwt
from xlwt import Workbook
  
# Workbook is created
wb = Workbook()
  
# add_sheet is used to create sheet.
sheet1 = wb.add_sheet('Sheet 1')

# Specifying style
bold_style = xlwt.easyxf('font: bold 1')
  

"""
## (row, column, text)
sheet1.write(1, 0, 'ISBT DEHRADUN')

"""

## date 
sheet1.write(1, 0, 'Date:', bold_style)
sheet1.write(1, 1, today)
## time for experiment
sheet1.write(2, 0, 'Time:', bold_style)
sheet1.write(2, 1, current_time)

## number_samples
sheet1.write(3, 0, 'Number of samples:', bold_style)
sheet1.write(3, 1, number_samples)


###standard_zero
sheet1.write(5, 0, 'standardizing zero value:', bold_style)
sheet1.write(5, 1, standard_zero)

#slope
sheet1.write(6, 0, 'Linear slope:', bold_style)
sheet1.write(6, 1, slope)
#intercept
sheet1.write(7, 0, 'Linear intercept:', bold_style)
sheet1.write(7, 1, intercept)
#Rvalue
sheet1.write(8, 0, 'Linear R^2:', bold_style)
sheet1.write(8, 1, Rvalue)
#std_err
sheet1.write(9, 0, 'Linear std error:', bold_style)
sheet1.write(9, 1, std_err)

#Sample volume defined in top of script
sheet1.write(9, 4, 'SampleVolume:', bold_style)
sheet1.write(9, 5, SampleVolume)

#Final concentration defined in top of script
sheet1.write(10, 4, 'Final Concentration:', bold_style)
sheet1.write(10, 5, FinalConcentration)

##pico_ladder
##ladder_reads
##ng_pr_ul
sheet1.write(1, 4, 'Pico laddder', bold_style)
sheet1.write(2, 4, 'ng/uL', bold_style)
sheet1.write(2, 5, 'ladder read', bold_style)
sheet1.write(2, 6, 'standardized laddder', bold_style)
for i in range(len(ladder_reads)):
    sheet1.write(i+3, 4, ng_pr_ul[i])
    sheet1.write(i+3, 5, pico_ladder.iloc[0][i])
    sheet1.write(i+3, 6, ladder_reads[i])
    

# Specifying column
sheet1.write(12, 0, 'Raw data from Pico', bold_style)
for row in range(pico_raw.shape[0]):
    for col in range(pico_raw.shape[1]):
        sheet1.write(row+13, col, pico_raw.iloc[row][col])

    
## dil_20 
sheet1.write(31, 0, 'Dilution 20x', bold_style)
for i in range(number_samples):
    row = (i + 1) % 8
    col = (i + 0) // 8   
    sheet1.write(row+32, col, dil_20[i])

## dil_100
sheet1.write(31, 13, 'Dilution 100x', bold_style)
for i in range(number_samples):
    row = (i + 1) % 8
    col = (i + 0) // 8   
    sheet1.write(row+32, col+13, dil_100[i])

##d20_standard
sheet1.write(42, 0, 'Dilution 20x standardized', bold_style)
for i in range(number_samples):
    row = (i + 1) % 8
    col = (i + 0) // 8   
    sheet1.write(row+43, col, d20_standard[i])


##d100_standard
sheet1.write(42, 13, 'Dilution 100x standardized', bold_style)
for i in range(number_samples):
    row = (i + 1) % 8
    col = (i + 0) // 8   
    sheet1.write(row+43, col+13, d100_standard[i])

##d20_curve
sheet1.write(53, 0, 'Dilution 20x curves', bold_style)
for i in range(number_samples):
    row = (i + 1) % 8
    col = (i + 0) // 8   
    sheet1.write(row+54, col, d20_curve[i])

##d100_curve
sheet1.write(53, 13, 'Dilution 100x curves', bold_style)
for i in range(number_samples):
    row = (i + 1) % 8
    col = (i + 0) // 8   
    sheet1.write(row+54, col+13, d100_curve[i])

##dna_concentrations
sheet1.write(64, 0, 'DNA concentration results', bold_style)
for i in range(number_samples):
    row = (i + 1) % 8
    col = (i + 0) // 8   
    sheet1.write(row+65, col, dna_concentrations[i])


##dilutions sent as csv to felix
sheet1.write(75, 0, 'DNA concentration results', bold_style)
for i in range(number_samples):
    row = (i + 1) % 8
    col = (i + 0) // 8   
    sheet1.write(row+76, col, dna_concentrations[i])

wb.save(str(today) + '_Diagnostic_output.xls')


# In[212]:


#pico_raw.iloc[row][col]
print(ng_pr_ul)
print(pico_ladder.iloc[0:])
print(ladder_reads)


# In[213]:


print(pico_ladder.iloc[0][0])
print(pico_ladder.iloc[0][1])


# In[214]:


pico_raw


# In[ ]:




