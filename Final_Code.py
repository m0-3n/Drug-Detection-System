# this code is the integration of tkinter, dilation of the pupils, graph of it
from tkinter import *
import tkinter.messagebox
import numpy as np
import cv2
import matplotlib.pyplot as plt

window = Tk()
window.geometry("500x500")
window.title("DDS")
window.resizable(False, False)
def Quit_1():
    tkinter.messagebox.showinfo("Attention", "You will be leaving this GUI now.")
    exit()

def dilation():
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    cap = cv2.VideoCapture('Video.mp4')
    blink = False
    kernel = np.ones((5, 5), np.uint8)
    radius = []
    try:
        while 1:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            eyes = eye_cascade.detectMultiScale(gray, 1.1, 20)
            if len(eyes) > 0:

                if blink:
                    blink = False

                cv2.putText(img, "Detecting for Dilation...", (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0),
                            2,
                            cv2.LINE_AA)

                for (x, y, w, h) in eyes:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    roi_gray = gray[y:y + h, x:x + w]
                    roi_img = img[y:y + h, x:x + w]
                    blur = cv2.GaussianBlur(roi_gray, (5, 5), 10)
                    erosion = cv2.erode(blur, kernel, iterations=2)
                    dont_mind_3, thresh3 = cv2.threshold(erosion, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    # printing coordinates
                    # print(x,y,w,h)

                    # Start of drawing circles
                    circles = cv2.HoughCircles(roi_gray, cv2.HOUGH_GRADIENT, 6, 1000, param1=50, param2=30, minRadius=1,
                                               maxRadius=40)
                    if circles is not None:
                        final_circles = []
                        # Obtain rows and columns
                        rows = img.shape[0]
                        cols = img.shape[1]
                        # converting the values to integers
                        circles = np.round(circles[0, :]).astype("int")
                        cv2.circle(img, (rows, cols), radius=0, color=(0, 0, 255), thickness=1)
                        # putting a statement which says that if the radius is below 20 pixels we have to discard them
                        for (ix, iy, r) in circles:
                            if r < 20:
                                continue
                            final_circles.append([ix, iy, r])
                            final_circles = final_circles[0]
                            radius.append(final_circles[2])
            else:
                if not blink:
                    blink = True
                    if blink:
                        cv2.putText(img, "Eye not found", (10, 90), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2,
                                    cv2.LINE_AA)
            cv2.imshow("Dilation", img)

            k = cv2.waitKey(1)
            if k == ord('q'):
                tkinter.messagebox.showwarning("Attention!", "Please Complete the test to show the results...")
                break
        cap.release()
        cv2.destroyAllWindows()

    except:
        # since the video is recorded in 10 fps we can remove 10 continuous readings to plot the radius per time graph
        radius = radius[::10]
        # the radius is in pixels so we need to convert it to millimeters, so we need to multiply each element
        # inside the radius list with -- 1 pixel = 0.2645833333 mm
        # So we need to multiply it with that value
        mm = []
        for i in radius:
            mm.append(round(i * 0.2645833333, 1))
        plt.axis([0, 105, 5, 10])
        plt.plot(mm)
        plt.title("Dilation of the Pupil")
        plt.ylabel("Dilation of the pupil in millimeters")
        plt.xlabel("Time in Seconds")
        plt.show()
        Quit_1()

def start_1():
    tkinter.messagebox.showinfo("Attention!", "The Test Will Begin Now...")
    dilation()

Label(window, text="Drug Detection System", font=("ariel", 20, "italic", "bold"), fg='red', bg='black',
      relief="solid").pack(fill=BOTH, padx=2, pady=2)

Label(window, text="Drug abuse can affect \nseveral aspects of a person's \nphysical and psychological health. "
                   "\nWe can detect this by the small concept of \ndilation of the pupils after taking "
                   "drugs.", font=("ariel", 16, "italic", "bold"), fg='black').pack(padx=12, pady=12)

Label(window, text="The test below shows how \nthis detection can be used \nand plots a graph with the values of "
                   "\nthe radius of the pupil. \nNote that the normal radius of the pupil is \n4 to 8mm in size ",
      font=("ariel", 14, "italic", "bold"), fg='black').pack(padx=5, pady=5)

Button(window, text="Start the test for dilation", font=("ariel", 16, "italic", "bold"),
       fg='blue', bg='yellow', relief=RAISED, command=start_1).place(x= 115, y=340)

Button(window, text="Exit", font=("ariel", 16, "italic", "bold"),
       fg='blue', bg='yellow', relief=RAISED, command=Quit_1).place(x=215, y=400)

window.mainloop()
