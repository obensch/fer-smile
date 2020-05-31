# Facial Emotion Recognition
Facial Emotion Recognition is achieved using haar cascade classifiers.
If the detected face does not smile for a specific period, the script asks to do so.

A progress bar shows the progress on smiling. A video and an image can be added to further assist in smiling.

## requirements
Python version: 3.7

The following python packages are required
* numpy
* openCV
* imutils
* time
* tensorflow/keras 

## change settings in the scripts
Webcam is enabled by default in all scripts. 
To enable webstream comment the line
```python
cam = cv2.VideoCapture(0)
```
and uncomment the line
```python
# cam = cv2.VideoCapture("http://192.168.178.21:8080/video?type=some.mjpg")
```
To change the frame settings edit the folling lines in all the scritps:
```python
# set frame size
FrameWidth = 1280
FrameHeight = 720
```
Time to smile and timer to smile can be changed here:
```python
# time to remind the user to smile
smileReminder = 15

# time the user has to smile
timeToSmile = 10
```

## Script: main.py 
Requirements:
The files 'haarcascade_frontalface_default.xml' and 'haarcascade_smile.xml' are required to execute this script. 
The files can be downloaded e.g. from here: https://github.com/opencv/opencv/tree/master/data/haarcascades

This script can be executed using the command:
```python
python main.py
```
Additional settings:
Change debug to False, to disable debug info:
```python
# Show debug info
debug = True
```

### Video and image settings
Create an "image" folder and place an image file "image.png" file inside, as well as an "video" folder with an "video.mp4" inside.
Uncomment lines 27-30 and 118-131.

Change showVideo to False, to show the image instead.
```python
# if false an image of an dog is shown
showVideo = True 
```