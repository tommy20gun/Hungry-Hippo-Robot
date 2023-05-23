import cv2 as cv
import numpy as np


def plot_axes_on_frame(frame):
    qr = cv.QRCodeDetector()
    # Initialize variables for location and rotation. Set them as None so that the program can tell when there's no QR code.
    center_x, center_y, angle = None, None, None

    ret_qr, points = qr.detect(frame)

    if ret_qr:
        # Selected coordinate points for each corner of QR code.
        qr_edges = np.array([[0, 0, 0],
                             [0, 1, 0],
                             [1, 1, 0],
                             [1, 0, 0]], dtype='float32').reshape((4, 1, 3))

        # Hard-coded camera intrinsic parameters
        cmtx = np.array([[910.1155107777962, 0.0, 360.3277519024787],
                         [0.0, 910.2233367566544, 372.6634999577232],
                         [0.0, 0.0, 1.0]])

        # Hard-coded distortion parameters
        dist = np.array([0.0212284835698144, 0.8546829039917951, 0.0034281408326615323, 0.0005749116561059772, -3.217248182814475])

        # Determine the orientation of QR code coordinate system with respect to camera coordinate system.
        ret, rvec, tvec = cv.solvePnP(qr_edges, points, cmtx, dist)

        # Define unit xyz axes. These are then projected to camera view using the rotation matrix and translation vector.
        unitv_points = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype='float32').reshape((4, 1, 3))
        if ret:
            axis_points, _ = cv.projectPoints(unitv_points, rvec, tvec, cmtx, dist)

            # BGR color format
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]

            # Check if axis points are projected to camera view.
            if len(axis_points) > 0:
                axis_points = axis_points.reshape((4, 2))

                origin = (int(axis_points[0][0]), int(axis_points[0][1]))

                for p, c in zip(axis_points[1:], colors[:3]):
                    p = (int(p[0]), int(p[1]))

                    # Sometimes QR detector will make a mistake and projected point will overflow integer value.
                    # We skip these cases.
                    if origin[0] > 5 * frame.shape[1] or origin[1] > 5 * frame.shape[1]:
                        break
                    if p[0] > 5 * frame.shape[1] or p[1] > 5 * frame.shape[1]:
                        break

                    cv.line(frame, origin, p, c, 5)

                # Calculate the angle of rotation of the QR code
                angle = np.arctan2(axis_points[1][1] - axis_points[0][1], axis_points[1][0] - axis_points[0][0])
                angle = np.degrees(angle)
                if angle < 0:
                    angle += 360

                # Calculate the center of the QR code
                center_x = int((axis_points[0][0] + axis_points[2][0]) / 2)
                center_y = int((axis_points[0][1] + axis_points[2][1]) / 2)

                # Print the angle and center coordinates
                font = cv.FONT_HERSHEY_SIMPLEX
                text = f"Rotation: {int(angle)} degrees"
                cv.putText(frame, text, (origin[0] + 10, origin[1] + 10), font, 1, (255, 255, 255), 2, cv.LINE_AA)

                text = f"({center_x}, {center_y})"
                cv.putText(frame, text, (origin[0] + 10, origin[1] + 40), font, 1, (255, 255, 255), 2, cv.LINE_AA)

    return frame, center_x, center_y, angle


# Example usage
if __name__ == '__main__':
    cap = cv.VideoCapture(0)

    while True:
        ret, img = cap.read()
        if not ret:
            break

        # Plot axes and angle on the frame
        frame_with_axes, center_x, center_y, angle = plot_axes_on_frame(img)

        # Check if an object is detected
        if angle is not None:
            print("QR code rotation angle:", angle)
            print("QR code center: ({}, {})".format(center_x, center_y))

        # Display the frame
        cv.imshow('Frame', frame_with_axes)

        # Wait for the 'Esc' key to exit
        if cv.waitKey(1) == 27:
            break

    cap.release()
    cv.destroyAllWindows()
