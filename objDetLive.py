import cv2

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Create a tracker object
tracker = cv2.TrackerCSRT_create()

# Read the first frame
ret, frame = cap.read()
bbox = cv2.selectROI("Tracking", frame, False)

# Initialize the tracker on the first frame and bounding box
tracker.init(frame, bbox)

while True:
    ret, frame = cap.read()
    
    # Update the tracker
    success, bbox = tracker.update(frame)
    
    if success:
        # Draw a rectangle around the tracked object
        x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    else:
        cv2.putText(frame, "Tracking failed", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    
    # Display the frame
    cv2.imshow("Tracking", frame)
    
    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()