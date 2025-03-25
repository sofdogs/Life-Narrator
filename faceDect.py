import cv2 

# load the pre-trained Haar Cascade 
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Read THE IMAGE 
img = cv2.imread('./human_face.jpeg')
# convert to grayscale 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces 
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize = (30,30)) # optimizing detection 

# Draw rectangles around the faces 
for(x, y, w, h) in faces: 
    cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2)

# Display the output 
cv2.imshow('Face Detection', img) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 