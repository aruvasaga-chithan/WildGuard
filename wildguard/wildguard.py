# TITLE: WILDGUARD
# OBJECTIVES: Detect elephants in real-time and alert an alarm to notify people near the forest side
# AUTHOR: A.ARUVASAGA CHITHAN

# Import all requirements
import cv2
import numpy as np
from playsound import playsound
import threading
import time
from datetime import datetime
from twilio.rest import Client
import mysql.connector


# Logging detection into MySQL database
def log_to_db(detection_info):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # XAMPP default username
            password="",  # Leave blank for default setup
            database="wildguard_db"
        )
        cursor = conn.cursor()
        timestamp = datetime.now()
        cursor.execute('''INSERT INTO detections (timestamp, info) VALUES (%s, %s)''', (timestamp, detection_info))
        conn.commit()
    except Exception as e:
        print(f"Error logging to database: {e}")
    finally:
        conn.close()


# Load YOLOv3 network
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")  # load pretrained YOLO models along with configuration
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]  # store layer indexes

# Load COCO class labels
with open("coco.names", "r") as f:  # open coco.names file for label names
    classes = [line.strip() for line in f.readlines()]  # read label names and store in class list[]

# Initialize video capture (0, 1, or 2 based on the index of the camera)
cap = cv2.VideoCapture(1)

# Set lower resolution to reduce CPU load (640x480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # adjust the video frame display size
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():  # if error in opening video, exit the function
    print("Error: Cannot access the camera or video file.")
    exit()

# Global flag for sound and thread control
elephant_alert_flag = False
exit_flag = False  # Flag to close sound alert when ESC is pressed

# Logging function: create a log about elephant detection and send log via SMS
def log_detection():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # get current date and time
    log_to_db(f"Elephant detected at {current_time}")  # log detection in the database
    with open("elephant_detection_log.txt", "a") as log_file:  # open the log file and append detection logs
        log_file.write(f"Elephant detected at {current_time}\n")
    send_sms_notification(current_time)


# SMS notification function using Twilio
def send_sms_notification(detection_time):
    try:
        # Twilio account_sid and auth_token for activating and sending SMS via Twilio
        account_sid = "YOUR_ACCOUNT_SSID"
        auth_token = "YOUR_AUTH_TOKEN"
        client = Client(account_sid, auth_token)

        # Send SMS
        message = client.messages.create(
            body=f"Elephant detected at {detection_time}. Please take necessary action.",
            from_="+1010101101",  # Your Twilio number
            to="+919999999999"      # The recipient's phone number
        )
        print("SMS sent successfully to forest officers")
    except Exception as e:
        print(f"Failed to send SMS: {e}")


# Define the sound alert using playsound
def sound_alert():
    global elephant_alert_flag, exit_flag
    while elephant_alert_flag:
        if exit_flag:
            break  # Stop the sound alert if exit flag is set
        print("Elephant detected, sounding alarm!")  # Debug print
        try:
            playsound('alert.mp3')  # Ensure the file path is correct
        except Exception as e:
            print(f"Error playing sound: {e}")
        time.sleep(1)  # Delay between repeated alerts, if needed


# Function to trigger alert sound and log detection
def trigger_alert():
    global elephant_alert_flag
    if not elephant_alert_flag:
        elephant_alert_flag = True
        # Start sound alert in a separate thread
        sound_thread = threading.Thread(target=sound_alert)
        sound_thread.start()

        # Log detection and send SMS in a separate thread
        log_thread = threading.Thread(target=log_detection)
        log_thread.start()


# Process each frame
def process_frame(frame):
    height, width, channels = frame.shape

    # Detecting objects and convert into blob format for matching to YOLO model
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Initialization
    class_ids = []
    confidences = []
    boxes = []

    # Processing detected objects
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Reduce the confidence threshold for testing
            if confidence > 0.3 and classes[class_id] == "elephant":  # Lowered from 0.5 to 0.3
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])  # Draw a box
                confidences.append(float(confidence))  # Add confidence score
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)

    elephant_detected = False
    if indexes is not None and len(indexes) > 0:
        for i in indexes.flatten():  # flatten function returns the index
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence_score = confidences[i]  # Get the confidence score for the label
            color = (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

            # Display label with confidence score
            label_with_confidence = f"{label} {confidence_score:.2f}"  # e.g., 'elephant 0.92'
            cv2.putText(frame, label_with_confidence, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            # Check if an elephant is detected in the current frame
            if label == "elephant":
                elephant_detected = True

    # Trigger sound alert if an elephant is detected
    if elephant_detected and not elephant_alert_flag:
        trigger_alert()

    return frame


# Main loop for capturing video
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Ensure frame is not None before processing
    if frame is not None:
        frame = process_frame(frame)

        # Display the output frame
        cv2.imshow("WildGuard - Elephant Detection", frame)

    # Check if 'ESC' is pressed to exit
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'ESC' to exit
        exit_flag = True  # Set flag to stop sound thread
        break

    # Sleep to lower the frame rate and reduce CPU usage
    time.sleep(0.05)

# Cleanup and exit
elephant_alert_flag = False  # Stop the sound alert
cap.release()
cv2.destroyAllWindows()
