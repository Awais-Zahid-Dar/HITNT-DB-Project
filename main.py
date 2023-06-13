
import cv2 #face_recognization
import time #date & time
import pymysql #sql connection
import numpy as np #mathematical & arrays & machine learning & fast
from tkinter import * #gui module (graphical user interface) all library
import settings as st #file
import credentials as cr #file
import face_recognition as f
import videoStream as vs #For OPening Cam And Use Video For Recog
import multiprocessing as mp
from datetime import datetime
from tkinter import messagebox # For Messages For Users
from playsound import playsound # FOr Audios
from tkinter import filedialog #Opening Browse For File Selection
from tkinter.filedialog import askopenfile #File Type
import webbrowser #To Access Web Browser And Use It's Services
from PIL import Image, ImageTk #Image Processing
import tkinter as tk #FOr Windows
import requests #Request Session ETC ETC


# The LoginSystem class

uid='';
class LoginSystem:
    def __init__(self, root):
        # Window settings
        self.window = root
        self.window.title("Healthy Is The New Thin (LOGIN PANEL)")
        self.window.geometry("780x480")
        self.window.config(bg=st.color1)
        self.window.resizable(width = False, height = False)

        # Declaring a variable with a default value
        self.status = False

         # Left Frame
        self.frame1 = Frame(self.window, bg='#49545c')
        self.frame1.place(x=0, y=0, width=540, relheight = 1)

        # Right Frame
        self.frame2 = Frame(self.window, bg = '#fffd3d')
        self.frame2.place(x=540,y=0,relwidth=1, relheight=1)

        # Calling the function called buttons()
        self.buttons()

    # A Function to display buttons in the right frame
    def buttons(self):

        AdminRightsButton = Button(self.frame2, text="Admin Panel", font=(st.font3, 12), bd=2, cursor="hand2", width=13, command=self.AdminLoginPanel)
        AdminRightsButton.place(x=50, y=40)

        
        loginButton = Button(self.frame2, text="Login", font=(st.font3, 12), bd=2, cursor="hand2", width=7, command=self.CompareUID)
        loginButton.place(x=74, y=100)

        registerButton = Button(self.frame2, text="Register", font=(st.font3, 12), bd=2, cursor="hand2", width=7, command=self.adminPanel)
        registerButton.place(x=74, y=160)



        


        
        clearButton = Button(self.frame2, text="Clear", font=(st.font3, 12), bd=2, cursor="hand2", width=7, command=self.clearScreen)
        clearButton.place(x=74, y=220)

        exitButton = Button(self.frame2, text="Exit", font=(st.font3, 12), bd=2, cursor="hand2", width=7, command=self.exit)
        exitButton.place(x=74, y=280)


    def CompareUID(self):
        self.clearScreen()
        enterUID = Label(self.frame1, text="Enter User ID:", font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=170)
        self.uidEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.uidEntry.place(x=300,y=200, width=200)

        submitButton = Button(self.frame1, text='Submit', font=(st.font3, 12), bd=2, command=self.loginEmployee, cursor="hand2", bg='#fffd3d',fg='black').place(x=200,y=389,width=100)

        

        
    # A Function to login into the system through face recognition method
    def loginEmployee(self):
        from FetchBlob import readBLOB
        print(self.uidEntry.get())
        iName = str(self.uidEntry.get())
        uid=iName;
        iNameFull = iName + ".jpg"
        readBLOB(self.uidEntry.get(),iNameFull)
        # Clear the screen first
        self.clearScreen()

        

        
        # Call a function called playVoice() to play a sound in a different
        # process
        process = self.playVoice("voice1.mp3")
        time.sleep(6)
        # End the process
        process.terminate()
        
        # Inheriting the class called VideoStream and its
        # methods here from the videoStream module to capture the video stream
        faces = vs.encode_faces()
        encoded_faces = list(faces.values())
        faces_name = list(faces.keys())
        video_frame = True

        # stream = 0 refers to the default camera of a system
        video_stream = vs.VideoStream(stream=0)
        video_stream.start()

        while True:
            if video_stream.stopped is True:
                break
            else :
                frame = video_stream.read()

                if video_frame:
                    face_locations = f.face_locations(frame)
                    unknown_face_encodings = f.face_encodings(frame, face_locations)

                    face_names = []
                    for face_encoding in unknown_face_encodings:
                        # Comapring the faces
                        matches = f.compare_faces(encoded_faces, \
                        face_encoding)
                        name = "Unknown"

                        face_distances = f.face_distance(encoded_faces,\
                        face_encoding)
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = faces_name[best_match_index]

                        face_names.append(name)

                video_frame = not video_frame

                for (top, right, bottom, left), faceID in zip(face_locations,\
                face_names):
                    # Draw a rectangular box around the face
                    cv2.rectangle(frame, (left-20, top-20), (right+20, \
                    bottom+20), (0, 255, 0), 2)
                    # Draw a Label for showing the name of the person
                    cv2.rectangle(frame, (left-20, bottom -15), \
                    (right+20, bottom+20), (0, 255, 0), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    # Showing the face_id of the detected person through 
                    # the WebCam
                    cv2.putText(frame, "Face Detected", (left -20, bottom + 15), \
                    font, 0.85, (255, 255, 255), 2)
                    
                    # Call the function for attendance
                    self.status = self.isPresent(faceID)

            # delay for processing a frame 
            delay = 0.04
            time.sleep(delay)

            cv2.imshow('frame' , frame)
            key = cv2.waitKey(1)
            # If self.status is True(which means the face is identified)
            # a voice will play in the background, the look will be break,
            # and all cv2 window will be closed.
            if self.status == True:
                process = self.playVoice("Voices/voice2.mp3")
                time.sleep(4)
                process.terminate()
                break
        video_stream.stop()

        # closing all windows 
        cv2.destroyAllWindows()
        # Calling a function to show the status after entering an employee
        self.employeeEntered()
        payload = {"uid": "f{self.uidEntry.get()}"}
        r = requests.post('http://localhost/website/',data = payload)
        print(uid)
        
        webbrowser.open('http://localhost/website/index.php?uid='+uid)

      

    # A Function to check if the user id of the detected face is matching 
    # with the database or not. If yes, the function returns the value True.
    def isPresent(self, UID):
        try:
            connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
            curs = connection.cursor()
            curs.execute("select * from user where uid=%s", UID)
            row = curs.fetchone()

            if row == None:
                pass
            else:
                connection.close()
                return True
        except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)

    # A Function to display the entering time of the employee after his/her
    # face is identified.
    def employeeEntered(self):
        # Clear the screen first
        self.clearScreen()
        # Reset the value of self.status varible 
        self.status = False

        heading = Label(self.frame1, text="Login System", font=(st.font4, 30, "bold"), bg='#49545c', fg=st.color3)
        heading.place(x=140, y=30)
        
        # Getting the current time
        now = datetime.now()

        label1 = Label(self.frame1, text="You Entered: ", font=(st.font1, 18, "bold"), bg='#49545c', fg=st.color3)
        label1.place(x=40, y=120)

        # Display the current time on the Tkinter window
        timeLabel = Label(self.frame1, text=now, font=(st.font1, 16), bg='#49545c', fg=st.color3)
        timeLabel.place(x=190, y=123)

    # A Function to play voice in a different process
    def playVoice(self, voice):
        process = mp.Process(target=playsound, args=(voice,))
        process.start()
        return process



    # A Function to display widgets for Admin Login
    def adminPanel(self):
        # Clear the screen first
        self.clearScreen()

        heading = Label(self.frame1, text="Admin Panel", font=(st.font4, 30, "bold"), bg='#49545c', fg=st.color3)
        heading.place(x=140, y=30)

        usernameLabel = Label(self.frame1, text="User Name", font=(st.font1, 18), bg='#49545c', fg=st.color3)
        usernameLabel.place(x=40, y=120)

        self.userName = Entry(self.frame1, font=(st.font2, 15), width=20, bg=st.color4, fg=st.color1)
        self.userName.place(x=160, y=123)

        passwordLabel = Label(self.frame1, text="Password", font=(st.font1, 18), bg='#49545c', fg=st.color3)
        passwordLabel.place(x=40, y=180)

        # Password Entry Box
        self.password = Entry(self.frame1, show="*", font=(st.font2, 15), width=20, bg=st.color4, fg=st.color1)
        self.password.place(x=160, y=183)

        loginButton = Button(self.frame1, text="Login", font=(st.font3, 12), bd=2, cursor="hand2", width=7, bg='#fffd3d', fg='black', command=self.loginAdmin)
        loginButton.place(x=220, y=240)


    def AdminLoginPanel(self):
        # Clear the screen first
        self.clearScreen()

        heading = Label(self.frame1, text="Admin Panel", font=(st.font4, 30, "bold"), bg='#49545c', fg=st.color3)
        heading.place(x=140, y=30)

        usernameLabel = Label(self.frame1, text="User Name", font=(st.font1, 18), bg='#49545c', fg=st.color3)
        usernameLabel.place(x=40, y=120)

        self.userName = Entry(self.frame1, font=(st.font2, 15), width=20, bg=st.color4, fg=st.color1)
        self.userName.place(x=160, y=123)

        passwordLabel = Label(self.frame1, text="Password", font=(st.font1, 18), bg='#49545c', fg=st.color3)
        passwordLabel.place(x=40, y=180)

        # Password Entry Box
        self.password = Entry(self.frame1, show="*", font=(st.font2, 15), width=20, bg=st.color4, fg=st.color1)
        self.password.place(x=160, y=183)

        loginButton = Button(self.frame1, text="Login", font=(st.font3, 12), bd=2, cursor="hand2", width=7, bg='#fffd3d', fg='black', command=self.AdminMenu)
        loginButton.place(x=220, y=240)


    def AdminMenu(self):
        if self.userName.get() == "" or self.password.get() == "":
            messagebox.showerror("Field Missing", "Please fill all the field")
        else:
            try:
                connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
                curs = connection.cursor()
                curs.execute("select * from admin where username=%s and password=%s", (self.userName.get(), self.password.get()))
                row=curs.fetchone()
                
                if row == None:
                    messagebox.showerror("Error!","Please enter the correct information", parent=self.window)
                else:
                    self.AdminScreen()
                    connection.close()
            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)



    def AdminScreen(self):
        self.clearScreen()
        EnterButton = Button(self.frame1, text='Register New Employee', font=(st.font3, 12), bd=2, command=self.registerPage, cursor="hand2", bg='#fffd3d',fg='black').place(x=200,y=100,width=200)
        EditButton = Button(self.frame1, text='Edit Product', font=(st.font3, 12), bd=2, command=self.EditProductUID, cursor="hand2", bg='#fffd3d',fg='black').place(x=200,y=200,width=200)
        DeleteButton = Button(self.frame1, text='Delete Product', font=(st.font3, 12), bd=2, command=self.GETProductUID, cursor="hand2", bg='#fffd3d',fg='black').place(x=200,y=300,width=200)
        EnterNewProductButton = Button(self.frame1, text='Enter New Product', font=(st.font3, 12), bd=2, command=self.EnterProduct, cursor="hand2", bg='#fffd3d',fg='black').place(x=200,y=400,width=200)

        


    def EditPanel(self):
        self.clearScreen()

        name = Label(self.frame1, text="First Name", font=(st.font2, 15, "bold"), bg='#49545c').place(x=40,y=30)
        self.nameEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.nameEntry.place(x=40,y=60, width=200)

        surname = Label(self.frame1, text="Last Name", font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=30)
        self.surnameEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.surnameEntry.place(x=300,y=60, width=200)

        # Calling the function getUID() to get the user id of the last employee
        row = self.getUID()
        
        uid = Label(self.frame1, text="User ID*", font=(st.font2, 15, "bold"), bg='#49545c').place(x=40,y=100)
        # Displaying the current available user id for the new employee
        self.uidLabel = Label(self.frame1, text=f"{row[0]+1}", bg='#49545c', fg=st.color3, font=(st.font2, 15))
        self.uidLabel.place(x=40,y=130)

        eamil = Label(self.frame1, text="Email ID", font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=100)
        self.emailEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.emailEntry.place(x=300,y=130, width=200)

        contact = Label(self.frame1, text="Contact", font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=170)
        self.contactEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.contactEntry.place(x=300,y=200, width=200)

        dob = Label(self.frame1, text="Date of Birth", font=(st.font2, 15, "bold"), bg='#49545c').place(x=40,y=240)
        self.dobEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.dobEntry.place(x=40,y=270, width=200)

        joinningdate = Label(self.frame1, text="Joinning Date", font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=240)
        self.joinningDateEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.joinningDateEntry.place(x=300,y=270, width=200)

        gender = Label(self.frame1, text="Gender", font=(st.font2, 15, "bold"), bg='#49545c').place(x=40,y=310)
        self.genderEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.genderEntry.place(x=40,y=200, width=200)

        address = Label(self.frame1, text="Address", font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=310)
        self.addressEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.addressEntry.place(x=300,y=340, width=200)

        TakePicture = Button(self.frame1,text = 'Take Picture', font = (st.font3,12), bd =2 , command=self.TakePic,cursor = "hand2", bg='#fffd3d',fg='black').place(x=350,y=389,width=100)
        SS = Label(self.frame1, text="Press S To Snap Picture", font=(st.font2, 15, "bold"), bg='#49545c').place(x=175,y=425)

        
        submitButton = Button(self.frame1, text='Submit', font=(st.font3, 12), bd=2, command=self.submitData, cursor="hand2", bg='#fffd3d',fg='black').place(x=200,y=389,width=100)


    
    def CompAdminEdit(self):
        self.clearScreen()
        enterUID = Label(self.frame1, text="Enter User ID:", font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=170)
        self.uidEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.uidEntry.place(x=300,y=200, width=200)
        self.compare = self.uidEntry.get()
        submitButton = Button(self.frame1, text='Submit', font=(st.font3, 12), bd=2, command=self.CheckIfExistUID, cursor="hand2", bg='#fffd3d',fg='black').place(x=200,y=389,width=100)

      
    def CheckIfExistUID(self):
        try:
                connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
                curs = connection.cursor()
                curs.execute("select * from user where uid=%s", (self.compare ))
                row=curs.fetchone()
                
                if row == None:
                    messagebox.showerror("Error!","Please enter the correct information", parent=self.window)
                else:
                    self.registerPage()
                    connection.close()
        except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)
        #cmd.execute(f"SELECT * from accounts WHERE username='{username}'")
# if username is '123', then completed command will look like this:
# SELECT * from accounts WHERE username='123'
        #if cmd.fetchall(): # checking if something found with this username
         #   print('Username already exists')

        

                
    # A Function for login into the system for the Admin
    def loginAdmin(self):
        if self.userName.get() == "" or self.password.get() == "":
            messagebox.showerror("Field Missing", "Please fill all the field")
        else:
            try:
                connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
                curs = connection.cursor()
                curs.execute("select * from admin where username=%s and password=%s", (self.userName.get(), self.password.get()))
                row=curs.fetchone()
                
                if row == None:
                    messagebox.showerror("Error!","Please enter the correct information", parent=self.window)
                else:
                    self.registerPage()
                    connection.close()
            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)

    # If the Admin logged in successfully, this function will display widgets
    # to regiter a new employee
    def registerPage(self):
        self.clearScreen()

        name = Label(self.frame1, text="First Name", font=(st.font2, 15, "bold"), bg='#49545c').place(x=40,y=30)
        self.nameEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.nameEntry.place(x=40,y=60, width=200)

        surname = Label(self.frame1, text="Last Name", font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=30)
        self.surnameEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.surnameEntry.place(x=300,y=60, width=200)

        # Calling the function getUID() to get the user id of the last employee
        row = self.getUID()
        
        uid = Label(self.frame1, text="User ID*", font=(st.font2, 15, "bold"), bg='#49545c').place(x=40,y=100)
        # Displaying the current available user id for the new employee
        self.uidLabel = Label(self.frame1, text=f"{row[0]+1}", bg='#49545c', fg=st.color3, font=(st.font2, 15))
        self.uidLabel.place(x=40,y=130)

        eamil = Label(self.frame1, text="Email ID", font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=100)
        self.emailEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.emailEntry.place(x=300,y=130, width=200)


        contact = Label(self.frame1, text="Contact", font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=170)
        self.contactEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.contactEntry.place(x=300,y=200, width=200)

        dob = Label(self.frame1, text="Date of Birth", font=(st.font2, 15, "bold"), bg='#49545c').place(x=40,y=240)
        self.dobEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.dobEntry.place(x=40,y=270, width=200)

        joinningdate = Label(self.frame1, text="Joinning Date", font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=240)
        self.joinningDateEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.joinningDateEntry.place(x=300,y=270, width=200)

        gender = Label(self.frame1, text="Gender", font=(st.font2, 15, "bold"), bg='#49545c').place(x=40,y=310)
        self.genderEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.genderEntry.place(x=40,y=340, width=200)

        address = Label(self.frame1, text="Address", font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=310)
        self.addressEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.addressEntry.place(x=300,y=340, width=200)

        TakePicture = Button(self.frame1,text = 'Take Picture', font = (st.font3,12), bd =2 , command=self.TakePic,cursor = "hand2", bg='#fffd3d',fg='black').place(x=350,y=389,width=100)
        SS = Label(self.frame1, text="Press S To Snap Picture", font=(st.font2, 15, "bold"), bg='#49545c').place(x=175,y=425)

        
        submitButton = Button(self.frame1, text='Submit', font=(st.font3, 12), bd=2, command=self.submitData, cursor="hand2", bg='#fffd3d',fg='black').place(x=200,y=389,width=100)

    # This function returns the last or max user id from the employee_register table
    def getUID(self):
        try:
            connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
            curs = connection.cursor()
            curs.execute("select MAX(uid) from user")
            row = curs.fetchone()
            # Close the connection
            connection.close()
            # Return row
            return row

        except Exception as e:
            messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)
    
    # This function enters the data of the new employee into the employee_register
    # table.

       



 
        
    def submitData(self):

        
        #rowop = self.getUID()
        ##textop=f"{rowop[0]+1}"

        from InsertBlob import convertToBinaryData
        #print('THIS IS UID: ' + str(textop))
        #insertBLOB(textop, 'saved_img.jpg')
        
        if self.nameEntry.get() == "" or self.surnameEntry.get() == "" or self.emailEntry.get() == "" or self.contactEntry.get() == "" or self.dobEntry.get() == "" or self.joinningDateEntry.get() == "" or self.genderEntry.get() == "" or self.addressEntry.get() == "":
            messagebox.showwarning("Empty Field", "All fields are required", parent = self.window)
        else:
            try:
                connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
                curs = connection.cursor()
                empPicture = convertToBinaryData('saved_img.jpg')

                curs.execute("insert into user (f_name,l_name,email,contact,dob,join_date,gender,address,Picture) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                        (
                                            self.nameEntry.get(),
                                            self.surnameEntry.get(),
                                            self.emailEntry.get(),
                                            self.contactEntry.get(),
                                            self.dobEntry.get(),
                                            self.joinningDateEntry.get(),
                                            self.genderEntry.get(),
                                            self.addressEntry.get(),
                                            empPicture,
                                            
                                        ))
                
                connection.commit()
                connection.close()
                messagebox.showinfo('Done!', "The data has been submitted")
                self.resetFields()
            
            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)









    def EnterProduct(self):
        self.clearScreen()

        name = Label(self.frame1, text="Product Name", font=(st.font2, 15, "bold"), bg='#49545c').place(x=40,y=30)
        self.EPnameEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.EPnameEntry.place(x=40,y=60, width=200)

        surname = Label(self.frame1, text="Product Description", font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=30)
        self.EPsurnameEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.EPsurnameEntry.place(x=300,y=60, width=200)

        # Calling the function getUID() to get the user id of the last employee
        row = self.ProductgetUID()
        
        uid = Label(self.frame1, text="Product ID*", font=(st.font2, 15, "bold"), bg='#49545c').place(x=40,y=100)
        # Displaying the current available user id for the new employee
        self.EPuidLabel = Label(self.frame1, text=f"{row[0]+1}", bg='#49545c', fg=st.color3, font=(st.font2, 15))
        self.EPuidLabel.place(x=40,y=130)

        eamil = Label(self.frame1, text="Price", font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=100)
        self.EPemailEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.EPemailEntry.place(x=300,y=130, width=200)
        
       
        TakePicture = Button(self.frame1,text = 'Upload Picture', font = (st.font3,12), bd =2 , command=self.upload_file,cursor = "hand2", bg='#fffd3d',fg='black').place(x=350,y=389,width=120)
        
        #SS = Label(self.frame1, text="Press S To Snap Picture", font=(st.font2, 15, "bold"), bg='#49545c').place(x=175,y=425)

        
        submitButton = Button(self.frame1, text='Submit', font=(st.font3, 12), bd=2, command=self.SubmitProductData, cursor="hand2", bg='#fffd3d',fg='black').place(x=200,y=389,width=100)

        

    def ProductgetUID(self):
        try:
            connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
            curs = connection.cursor()
            curs.execute("select MAX(pid) from product")
            row = curs.fetchone()
            # Close the connection
            connection.close()
            # Return row
            return row

        except Exception as e:
            messagebox.showerror("Error!",f"ErroRRRRRr due to {str(e)}",parent=self.window)
    




    def SubmitProductData(self):
        global img , filename 

        #rowop = self.getUID()
        ##textop=f"{rowop[0]+1}"

        from InsertBlob import convertToBinaryData
        #print('THIS IS UID: ' + str(textop))
        #insertBLOB(textop, 'saved_img.jpg')
        
        if self.EPnameEntry.get() == "" or self.EPsurnameEntry.get() == "" or self.EPemailEntry.get() == "":
            messagebox.showwarning("Empty Field", "All fields are required", parent = self.window)
        else:
            try:
                connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
                curs = connection.cursor()
                fob=open(filename,'rb') # filename from upload_file()
                empPicture = convertToBinaryData(filename)

                fob=fob.read()
                
                curs.execute("insert into product (Name,Description,Price,Pic) values(%s,%s,%s,%s)",
                                        (
                                            self.EPnameEntry.get(),
                                            self.EPsurnameEntry.get(),
                                            self.EPemailEntry.get(),
                                            empPicture,
                                            
                                            
                                        ))


          
                connection.commit()
                connection.close()
                messagebox.showinfo('Done!', "The data has been submitted")
                self.resetProductFields()
            
            except Exception as e:
                messagebox.showerror("Error!",f"EEEError due to {str(e)}",parent=self.window)



    def resetProductFields(self):
        self.EPnameEntry.delete(0, END)
        self.EPsurnameEntry.delete(0, END)
        # Updating the user id label with the next available uid from the table
        row = self.ProductgetUID()
        self.EPuidLabel.config(text=f"{row[0] + 1}")

        self.EPemailEntry.delete(0, END)



    def EditProductUID(self):
        self.clearScreen()
        enterUID = Label(self.frame1, text="Enter Product ID:", font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=170)
        self.EPCuidEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.EPCuidEntry.place(x=300,y=200, width=200)
        self.EPCcompare = self.EPCuidEntry.get()
        
        submitButton = Button(self.frame1, text='Submit', font=(st.font3, 12), bd=2, command=self.CheckIfExistUIDEdit, cursor="hand2", bg='#fffd3d',fg='black').place(x=200,y=389,width=100)
        print("THIS22222:::"+str(self.EPCcompare))

        
    def CheckIfExistUIDEdit(self):
        print("THIS:::"+str(self.EPCcompare))
        try:
                connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
                curs = connection.cursor()
                curs.execute("select * from product where PID=%s", (self.EPCuidEntry.get() ))
                row=curs.fetchone()
                
                if row == None:
                    messagebox.showerror("Error!","Please ERRRRRrrornter the correct information", parent=self.window)
                else:
                    self.DISPLAYID=row[0]
                    self.OLDNAME = row[1]
                    self.OLDDES=  row[2]
                    self.OLDPRICE=  row[3]

                    self.EditProductPanel()
                    connection.close()
        except Exception as e:
                messagebox.showerror("Error!",f"ERRRRRrror due to {str(e)}",parent=self.window)




                
    def EditProductPanel(self):
        self.clearScreen()
        
        name = Label(self.frame1, text="NAME: "+str(self.OLDNAME), font=(st.font2, 15, "bold"), bg='#49545c').place(x=40,y=30)
        self.EPAnameEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.EPAnameEntry.place(x=40,y=60, width=200)

        surname = Label(self.frame1, text="Description: " + str(self.OLDDES), font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=30)
        self.EPAsurnameEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.EPAsurnameEntry.place(x=300,y=60, width=200)

        # Calling the function getUID() to get the user id of the last employee
        row = self.ProductgetUID()
        
        uid = Label(self.frame1, text="Product ID*", font=(st.font2, 15, "bold"), bg='#49545c').place(x=40,y=100)
        # Displaying the current available user id for the new employee
        self.EPuidLabel = Label(self.frame1, text=self.DISPLAYID, bg='#49545c', fg=st.color3, font=(st.font2, 15))
        self.EPuidLabel.place(x=40,y=130)

        eamil = Label(self.frame1, text="Price: "+ str(self.OLDPRICE), font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=100)
        self.EPAemailEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.EPAemailEntry.place(x=300,y=130, width=200)

       
        TakePicture = Button(self.frame1,text = 'Upload Picture', font = (st.font3,12), bd =2 , command=self.upload_file,cursor = "hand2", bg='#fffd3d',fg='black').place(x=350,y=389,width=100)
       # SS = Label(self.frame1, text="Press S To Snap Picture", font=(st.font2, 15, "bold"), bg='#49545c').place(x=175,y=425)

        
        submitButton = Button(self.frame1, text='Submit', font=(st.font3, 12), bd=2, command=self.SubmitEditProductData, cursor="hand2", bg='#fffd3d',fg='black').place(x=200,y=389,width=100)

    def SubmitEditProductData(self):
        #rowop = self.getUID()
        ##textop=f"{rowop[0]+1}"

        from InsertBlob import convertToBinaryData
        #print('THIS IS UID: ' + str(textop))
        #insertBLOB(textop, 'saved_img.jpg')
        
        if self.EPAnameEntry.get() == "" or self.EPAsurnameEntry.get() == "" or self.EPAemailEntry.get() == "":
            messagebox.showwarning("Empty Field", "All fields are required", parent = self.window)
        else:
            try:
                connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
                curs = connection.cursor()
                empPicture = convertToBinaryData(filename)
                
                sql_query = "UPDATE product SET Name = %s ,Description = %s ,Price = %s ,Pic = %s WHERE PID = %s"
                val = (self.EPAnameEntry.get(), self.EPAsurnameEntry.get(),self.EPAemailEntry.get(),empPicture,self.DISPLAYID)

                curs.execute(sql_query,val)
                
                connection.commit()
                connection.close()
                messagebox.showinfo('Done!', "The data has been submitted")
                self.EditProductUID()                

            
            except Exception as e:
                messagebox.showerror("Error!",f"EEEError due to {str(e)}",parent=self.window)


    def GETProductUID(self):
        self.clearScreen()
        enterUID = Label(self.frame1, text="Enter Product ID:", font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=170)
        self.EPCuidEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.EPCuidEntry.place(x=300,y=200, width=200)
        
        submitButton = Button(self.frame1, text='Submit', font=(st.font3, 12), bd=2, command=self.CheckIfExistUIDDel, cursor="hand2", bg='#fffd3d',fg='black').place(x=200,y=389,width=100)
        
    
    def CheckIfExistUIDDel(self):
        try:
                connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
                curs = connection.cursor()
                curs.execute("select * from product where PID=%s", (self.EPCuidEntry.get() ))
                row=curs.fetchone()
                
                if row == None:
                    messagebox.showerror("Error!","Product Not Found", parent=self.window)
                else:
                    self.DISPLAYID=row[0]
                    self.OLDNAME = row[1]
                    self.OLDDES=  row[2]
                    self.OLDPRICE=  row[3]

                    self.DeleteProductPanel()
                    connection.close()
        except Exception as e:
                messagebox.showerror("Error!",f"ERRRRRrror due to {str(e)}",parent=self.window)

    def DeleteProductPanel(self):
        self.clearScreen()
        
        name = Label(self.frame1, text="NAME: "+str(self.OLDNAME), font=(st.font2, 15, "bold"), bg='#49545c').place(x=40,y=30)
       

        surname = Label(self.frame1, text="Description: " + str(self.OLDDES), font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=30)
        

        #
       # row = self.ProductgetUID()
        
        uid = Label(self.frame1, text="Product ID*", font=(st.font2, 15, "bold"), bg='#49545c').place(x=40,y=100)
        # Displaying the current available user id for the new employee
        self.EPuidLabel = Label(self.frame1, text=self.DISPLAYID, bg='#49545c', fg=st.color3, font=(st.font2, 15))
        self.EPuidLabel.place(x=40,y=130)

        eamil = Label(self.frame1, text="Price: "+ str(self.OLDPRICE), font=(st.font2, 15, "bold"), bg='#49545c').place(x=300,y=100)

       

        
        submitButton = Button(self.frame1, text='Delete', font=(st.font3, 12), bd=2, command=self.DeleteProductData, cursor="hand2", bg='#fffd3d',fg='black').place(x=200,y=389,width=100)



    def DeleteProductData(self):
        #rowop = self.getUID()
        ##textop=f"{rowop[0]+1}"

        from InsertBlob import convertToBinaryData
        #print('THIS IS UID: ' + str(textop))
        #insertBLOB(textop, 'saved_img.jpg')
        
        
        
        try:
            connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
            curs = connection.cursor()
            empPicture = convertToBinaryData('saved_img.jpg')
                
            sql_query = "DELETE FROM product WHERE PID = %s"
            val = (self.DISPLAYID)

            curs.execute(sql_query,val)
                
            connection.commit()
            connection.close()
            messagebox.showinfo('Done!', "The data has been DELETED")
            self.GETProductUID()                

            
        except Exception as e:
            messagebox.showerror("Error!",f"EEEError due to {str(e)}",parent=self.window)

    def upload_file(self):
        global filename,img
        f_types =[('Png files','*.png'),('Jpeg Files', '*.jpeg')]
        filename = filedialog.askopenfilename(filetypes=f_types)
        img = ImageTk.PhotoImage(file=filename)
        


    def convertToBinaryDataFP(filename):
    # Convert digital data to binary format
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData





    def TakePic(self):
        import webcamCap
    # This function resets all the fields for register an employee
    def resetFields(self):
        self.nameEntry.delete(0, END)
        self.surnameEntry.delete(0, END)
        # Updating the user id label with the next available uid from the table
        row = self.getUID()
        self.uidLabel.config(text=f"{row[0] + 1}")

        self.emailEntry.delete(0, END)
        self.contactEntry.delete(0, END)
        self.dobEntry.delete(0, END)
        self.joinningDateEntry.delete(0, END)
        self.genderEntry.delete(0, END)
        self.addressEntry.delete(0, END)

    # Function to clear all the widgets from the frame1
    def clearScreen(self):
        for widget in self.frame1.winfo_children():
            widget.destroy()

    # A function to destroy the tkinter window
    def exit(self):
        self.window.destroy()

# The main function
if __name__ == "__main__":
    root = Tk()
    obj = LoginSystem(root)
    root.mainloop()
