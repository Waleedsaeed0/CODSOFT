import cv2
import time

# Load the Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces_in_image(image_path):
    # Read the image
    img = cv2.imread(image_path)

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Perform face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)

    # Display the image with detected faces
    cv2.imshow('Image with Faces Detected', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Load the Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces_in_video(video_path):
    # Open a video file for face detection
    cap = cv2.VideoCapture(video_path)

    # Variables for FPS calculation
    prev_time = 0
    fps = 0
    frame_interval = 1 / 30  # Target frame interval for 30 FPS

    # Define the desired width and height for resizing
    new_width = 640
    new_height = 480

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (new_width, new_height))


        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Perform face detection
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.6, minNeighbors=7, minSize=(30, 30))

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 3)
            break  # Break after drawing the first rectangle

        # Calculate and display FPS
        current_time = time.time()
        elapsed_time = current_time - prev_time
        if elapsed_time >= frame_interval:
            fps = 1 / elapsed_time
            prev_time = current_time
        cv2.putText(frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


        # Display the frame with detected faces
        cv2.imshow('Video with Faces Detected', frame)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = "video_2.mp4"  # Specify the path to your video
    detect_faces_in_video(video_path)

    #image_path = "test.jpg"  # Specify the path to your image
    #detect_faces_in_image(image_path)

