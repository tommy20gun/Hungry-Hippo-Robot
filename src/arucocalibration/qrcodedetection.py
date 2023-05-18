import cv2
import numpy as np

# Set the dimensions of the ArUco marker board
aruco_board_size = (4, 5)  # Number of internal corners (rows, columns)
aruco_square_length = 0.0375  # Length of each square in meters

# Set the camera matrix and distortion coefficients for an iPhone 10 camera
camera_matrix = np.array([[2831.25, 0, 1607.5], [0, 2831.25, 1203.5], [0, 0, 1]])
dist_coeffs = np.array([[-0.2028, 0.0712, -0.0011, 0.0009, -0.0145]])

# Prepare object points for the ArUco marker board
object_points = np.zeros((np.prod(aruco_board_size), 3), dtype=np.float32)
object_points[:, :2] = np.mgrid[0:aruco_board_size[0], 0:aruco_board_size[1]].T.reshape(-1, 2) * aruco_square_length

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Open the video capture
cap = cv2.VideoCapture(0)  # You can change the index to use a different camera

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if the frame is successfully captured
    if not ret:
        print("Failed to capture frame")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect ArUco markers
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters()
    corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # If any markers are detected
    if ids is not None and len(ids) > 0 and corners is not None and len(corners) == len(ids):
        # Refine the detected marker corners
        corners = np.array(corners, dtype=np.float32)
        corners = corners.reshape(-1, 1, 2)
        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        # Estimate the pose of the marker
        rvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, aruco_square_length, camera_matrix, dist_coeffs)

        # Draw marker borders and IDs on the frame
        frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Draw axis for each detected marker
        for i in range(len(ids)):
            cv2.aruco.drawAxis(frame, camera_matrix, dist_coeffs, rvecs[i], np.zeros((1, 0, 3), dtype=np.float32), 0.1)

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture
cap.release()
cv2.destroyAllWindows()