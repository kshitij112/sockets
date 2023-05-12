import cv2
import numpy as np
import socket

# Camera parameters
camera_ip = '0.0.0.0'  # Replace with the IP address of your camera
camera_port = 0  # Replace with the port number of your camera (e.g., 0 for default)

# Network parameters
host = '0.0.0.0'  # Replace with the IP address of the host machine
port = 8000  # Replace with the desired port number for streaming

# Initialize socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(1)

# Accept a client connection
print('Waiting for a client to connect...')
client_socket, client_address = sock.accept()
print('Client connected:', client_address)

# Initialize camera
cap = cv2.VideoCapture(camera_ip + ':' + str(camera_port))

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Encode the frame as JPEG
    _, encoded_frame = cv2.imencode('.jpg', frame)

    # Convert the encoded frame to bytes
    frame_bytes = np.array(encoded_frame).tobytes()

    try:
        # Send the frame to the client
        client_socket.sendall(frame_bytes)
    except (socket.error, socket.timeout):
        print('Error occurred while sending the frame')
        break

    # Break the loop if the client has disconnected
    if not client_socket.recv(1):
        print('Client disconnected')
        break

# Release the resources
cap.release()
client_socket.close()
sock.close()
