**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./writeup-images/calibration.png "Calibrated"
[image2]: ./writeup-images/undistorted.png "Undistorted"
[image3]: ./writeup-images/thresholds.png "Binary Example"
[image4]: ./writeup-images/warped.png "Warp Example"
[image5]: ./writeup-images/lines.png "Fit Visual"
[image6]: ./writeup-images/lanes.png "Output"
[video1]: ./out.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the first code cell of the IPython notebook located in "./project.ipynb".

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result:

![alt text][image1]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

To undistort the image, I used the outputs from the previous step as parameters to apply cv2.undistort to the image. Example output below:

![alt text][image2]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I used a combination of color and gradient thresholds to generate a binary image (see the section of "./project.ipynb" 'create a thresholded binary image').

I first started by creating a copy of the image converted to HLS color space. I then selected pixels that had a saturation value between 160 - 255.

Then I added some Gaussian blur to remove noise.

Next, I converted the image to grayscale and applied the Sobel operator to get the gradient in the X direction and select pixels with a sobelx between 10 - 255.

Using Sobel again, I found the magnitude of the gradient and applied a threshold of 40 - 255.

Again, using Sobel, I found the direction of the gradient and applied a threshold of 0.65 - 1.05 radians.

I combined all of those thresholds together, then selected an area of interest on the image where lane lines might appear.

Here's an example of my output for this step.

![alt text][image3]


#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform is in "./project.ipynb" under Perspective Transform (perspectiveCorrection function).  The `perspectiveCorrection()` function takes as inputs an image (`img`).  I chose to hardcode the source and destination points in the following manner:

```python
	region = [[580, 460],[710, 460],[1150,720],[150,720]]
	offset = 200
	# Grab the image shape
	img_size = (img.shape[1], img.shape[0])
	# For source points I'm grabbing the outer four detected corners
	src = np.float32(region)
	# For destination points, I'm arbitrarily choosing some points to be
	# a nice fit for displaying our warped result
	dst = np.float32([[offset, 0],
					  [img_size[0]-offset, 0],
					  [img_size[0]-offset, img_size[1]],
					  [offset, img_size[1]]])
```

This resulted in the following source and destination points:

| Source        | Destination   |
|:-------------:|:-------------:|
| 580, 460      | 200, 0        |
| 710, 460      | 1080, 0      	|
| 1150, 720     | 1080, 720     |
| 150, 720      | 200, 720      |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image4]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Using the combined binary image from step two I was able to select only the pixels that are lane lines. After warping the image I could fit a polynomial to each line by identifying the peaks in a histogram to determine the lane line locations and identify all nonzero pixels around the peaks.

![alt text][image5]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

After finding the lane lines I calculated the position of the vehicle within the lane lines by calculating the average of the x intercepts from each of the two lane lines.
Then I got the distance from center by taking the absolute value of the vehicle position and subtracting the midpoint. To convert this to meters I multiplied the number of pixels by 3.7/700.

This is done in "./project.ipynb" toward the bottom of the drawLanes() function.

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in the section "Draw Lanes" in "./project.ipynb"  in the function `drawLanes()`.  Here is an example of my result on a test image:

![alt text][image6]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./out.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?
The pipeline I created did a fairly good job of detecting lane lines, however in less ideal conditions it would probably have a difficult time. For example, rain, snow, etc. Even shadows and changing road coloration gave my pipeline a little bit of trouble. I could make this more robust by adding better sanity checking and averaging the lines detected from a range of frames together. I could also improve and change the thresholding techniques and experiment with different ways to detect the lines.
