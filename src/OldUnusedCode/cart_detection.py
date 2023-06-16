import cv2
import numpy as np

# Global variable for previous frame to apply a filtering algorithm
prev_rotation_deg = 0
alpha = 0.2  # Smoothing factor for the moving average
degree_threshold = 10
min_matches = 10  # Minimum number of matches required for valid detection

def rescale_frame(frame, scale):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_CUBIC)


def cart_detection(frame):
    # Load the reference image
    ref_image = cv2.imread('qrcode.png', cv2.IMREAD_GRAYSCALE)


    # Detect keypoints and extract descriptors from the reference image
    orb = cv2.ORB_create()
    ref_keypoints, ref_descriptors = orb.detectAndCompute(ref_image, None)

    # Create a BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to the grayscale frame
    _, thresholded_frame = cv2.threshold(gray_frame, 127, 255, cv2.THRESH_BINARY)

    # Detect keypoints and extract descriptors from the thresholded frame
    captured_keypoints, captured_descriptors = orb.detectAndCompute(thresholded_frame, None)

    # Match descriptors of the reference image and captured frame
    matches = bf.match(ref_descriptors, captured_descriptors)

    # Sort the matches by distance (lower is better)
    distance_threshold = 70
    matches = [m for m in matches if m.distance < distance_threshold]


    # Extract the keypoints that have matched
    ref_matched_points = np.float32([ref_keypoints[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    captured_matched_points = np.float32([captured_keypoints[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    # Estimate the homography matrix
    try:
        homography, _ = cv2.findHomography(ref_matched_points, captured_matched_points, cv2.RANSAC, 5.0)
        if homography is None:
            #print("homography is none")
            return frame
    except cv2.error:
        print("cv2 error")
        return frame

    
    global prev_rotation_deg, alpha, degree_threshhold
    # Extract the rotation angle from the homography matrix
    rotation_rad = np.arctan2(homography[1, 0], homography[0, 0])
    rotation_deg = np.degrees(rotation_rad)

    if len(matches) < min_matches:
        # Display "No objects detected" message
        cv2.putText(frame, "No objects detected", (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
    else:
        # Apply the filtering algorithm
        rotation_deg_filtered = alpha * rotation_deg + (1 - alpha) * prev_rotation_deg

        # Update the previous degree value
        prev_rotation_deg = rotation_deg_filtered

        # Check if the degree change exceeds the threshold
        if abs(rotation_deg - prev_rotation_deg) > degree_threshold:
            # Display "No objects detected" message
            cv2.putText(frame, "No objects detected", (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            # Draw rectangles, labels, and perform other operations...
            rect = cv2.boxPoints(cv2.minAreaRect(captured_matched_points))
            rect = np.int0(rect)
            cv2.drawContours(frame, [rect], 0, (0, 255, 0), 2)
            label_background = np.zeros((40, 350, 3), dtype=np.uint8)
            label_background.fill(255)
            frame[10:50, 10:360] = label_background
            label = "Rotation Angle: " + str(int(rotation_deg)) + " degrees"
            cv2.putText(frame, label, (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)

    return frame
