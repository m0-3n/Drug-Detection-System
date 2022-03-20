# just the eye detection and graph
import numpy as np
import cv2
import matplotlib.pyplot as plt

eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
cap = cv2.VideoCapture('Video.mp4')
blink = False
kernel = np.ones((5, 5), np.uint8)
radius = []
try:
    while 1:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(gray, 1.1, 16)
        if len(eyes) > 0:

            if blink:
                blink = False

            cv2.putText(img, "Detecting for Dilation...", (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2,
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
        cv2.imshow("output", img)

        k = cv2.waitKey(1)
        if k == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

except:
    # since the video is recorded in 10 fps we can remove 10 continuous readings to plot the radius per time graph
    radius = radius[::10]
    # the radius is in pixels so we need to convert it to millimeters so we need to multiply each element
    # inside the radius list with -- 1 pixel = 0.2645833333 mm
    # So we need to multiply it with that value
    mm = []
    for i in radius:
        mm.append(round(i * 0.2645833333, 1))
    plt.axis([0, 105, 20, 40])
    plt.plot(radius)
    plt.title("Dilation of the Pupil")
    plt.ylabel("Dilation of the pupil in Centimeter")
    plt.xlabel("Time in Seconds")
    plt.show()
    print("Program Run Successfully 1")
