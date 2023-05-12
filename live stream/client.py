import cv2
import socket
import numpy as np

# Network parameters
host = '0.0.0.0'  # Replace with the IP address of the host machine
port = 8000  # Replace with the same port number used in the server

# Initialize socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

while True:
    try:
        # Receive frame bytes from the server
        frame_bytes = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            frame_bytes += chunk

        # Decode the frame bytes
        frame = cv2.imdecode(np.frombuffer(frame_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)

        # Display the frame
        cv2.imshow('Live Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except (socket.error, socket.timeout):
        print('Error occurred while receiving the frame')
        break

# Release the resources
cv2.destroyAllWindows()
sock.close()
