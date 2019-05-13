# IONBot
# Code written by Raunak Daga

from tkinter import *
from tkinter.ttk import *
from selenium import webdriver
import time
import os

classToID = {}
classToID['Library Study Hall'] = '940'
classToID['Weight Room'] = '751'
classToID['Volleyball'] = '22'
classToID['Biotech'] = '762'

IDtonames = {}
IDtonames['940'] = 'Library'
IDtonames['22'] = 'Volleyball'
IDtonames['751'] = 'Weight'
IDtonames['762'] = 'Biotec'

dir_path = os.path.dirname(os.path.realpath(__file__))

global status_label

def beginProcess():
    status_label.configure(text='Searching') # Not Working
    signup(username.get(), password.get(), classToID.get(classCombo.get()), selected.get(), customClassInfo.get())

def getBlockText(driver, blockRequested):
    current_day = driver.find_element_by_class_name('current-day')
    blocks = current_day.find_elements_by_class_name('block')
    if(blockRequested == 1):
        blockElement = blocks[0]
    else:
        blockElement = blocks[1]

    blockWanted = blockElement.find_element_by_class_name('selected-activity')
    return blockWanted

def ifCustomGetName(driver, customID):
    driver.get('https://ion.tjhsst.edu/eighth/?activity=' + customID)
    className = driver.find_element_by_class_name('activity-detail-link')
    return className.text

def signup(username, password, activity, blockRequested, customID):
    driver = webdriver.Chrome(dir_path + r'\chromedriver.exe')
    driver.get('https://ion.tjhsst.edu/') # Go to ion

    # Gets Past Login Page
    id_box = driver.find_element_by_name('username')
    id_box.send_keys(username)
    pass_box = driver.find_element_by_name('password')
    pass_box.send_keys(password)
    login = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/form/input[4]")
    login.click()

    if 'Upcoming' not in driver.page_source:
        status_label.configure(text='Incorrect Login')
        return 'Terminated' # Does nothing

    # Gets Past 8th Period Page
    eighth = driver.find_element_by_xpath('/html/body/div[3]/ul/li[2]/a')
    eighth.click()

    # Finds Current Day and Blocks Elements
    current_day = driver.find_element_by_class_name('current-day')
    blocks = current_day.find_elements_by_class_name('block')

    # A or B block
    if(blockRequested == 1):
        blockElement = blocks[0]
    else:
        blockElement = blocks[1]

    # Clicks on block link to actually get to that block's activities
    blockParent = blockElement.find_element_by_xpath('..')
    blockParent.click()

    if customID:
        activitySliver = ifCustomGetName(driver, customID).strip()
        activity = customID
    else:
        activitySliver = IDtonames.get(activity)

    blockWanted = getBlockText(driver, blockRequested)
    timesTried = 0
    while(activitySliver not in blockWanted.text):
        driver.get('https://ion.tjhsst.edu/eighth/?activity=' + activity)
        try:
            signup_button = driver.find_element_by_id('signup-button')
            signup_button.click()
        except Exception:
            timesTried += 1
            status_label.configure(text='Times tried:' + str(timesTried))

        blockWanted = getBlockText(driver, blockRequested)
        time.sleep(8)

    status_label.configure(text="Succesfully found spot.")
    driver.close()


root = Tk()
root.title('IONBot')
root.geometry('210x180')
root.configure(background='white')

username = Entry(root, width=20)
userlabel = Label(root, text = 'Username:', background='white')
password = Entry(root, show="*", width=20)
passwordlabel = Label(root, text = 'Password:', background='white')
userlabel.place(x = 10, y = 10)
username.place(x = 70, y = 10)
passwordlabel.place(x = 10, y = 35)
password.place(x = 70, y = 35)
username.focus()

classlabel = Label(root, text='Activity:', background='white')
classlabel.place(x = 10, y = 60)
classCombo = Combobox(root)
classCombo['values'] = ('Volleyball', 'Weight Room', 'Library Study Hall', 'Biotech')
classCombo.place(x = 62, y = 60)

customClassLabel = Label(root, text='Custom:', background='white')
customClassLabel.place(x = 10, y=85)
customClassInfo = Entry(root, width=20)
customClassInfo.place(x=70, y = 85)

selected = IntVar()
rad1 = Radiobutton(root, text='A', value=1, variable=selected)
rad2 = Radiobutton(root, text='B', value=2, variable=selected)
rad1.place(x = 76, y = 110)
rad2.place(x = 116, y = 110)

doProcess = Button(root, text="Begin Searching", command=beginProcess)
doProcess.place(x = 65, y = 135)

status_label = Label(root, text = 'Not Searching', background='white')
status_label.place(x = 75, y = 160)

root.mainloop()
beginProcess()
