import glob
import cv2
import numpy as np

def detectCorners(img, nx, ny):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)

    # If found, draw corners
    if ret == True:
    # Draw and display the corners
    cv2.drawChessboardCorners(img, (nx, ny), corners, ret)

    return ret, corners

def undistort(img, objpoints, imgpoints):
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img.shape[0:2], None, None)
    dst = cv2.undistort(img, mtx, dist, None, mtx)
    return dst

def calibrate():
    nx = 9
    ny = 6

    # Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((nx*ny, 3), np.float32)
    objp[:,:2] = np.mgrid[0:nx, 0:ny].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d points in real world space
    imgpoints = [] # 2d points in image plane.

    # Get object points and image points and draw points on image
    for file in glob.glob('./camera_cal/calibration*.jpg'):
        cvImage = cv2.imread(file)
        fname = file.split('/')[-1]
        ret, corners = detectCorners(cvImage, nx, ny)
        if (ret == True):
            objpoints.append(objp)
            imgpoints.append(corners)
            cv2.imwrite('./camera_cal_with_points/' + fname, cvImage)

    # Test calibration
    for file in glob.glob('./camera_cal/calibration*.jpg'):
        cvImage = cv2.imread(file)
        fname = file.split('/')[-1]
        dst = undistort(cvImage, objpoints, imgpoints)
        cv2.imwrite('./undistorted/' + fname, dst)

calibrate()
