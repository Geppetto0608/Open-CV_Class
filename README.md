# Open-CV Class

OpenCV and ROS computer-vision class materials, including image-processing examples, lane-detection scripts, Gazebo-related examples, sample images, and a reference PDF.

## Repository Status

This repository is currently best understood as class/practice material. It is not yet a polished autonomous-driving or robotics benchmark project.

Current contents:

```text
Open_CV/
  OpenCV.pdf
  images/
  OpenCV example source code/
  Gazebo simulation source code/
```

## Setup

Python examples generally require:

```bash
pip install opencv-python numpy
```

ROS Noetic / Gazebo-related examples may require:

```bash
sudo apt-get install ros-noetic-effort-controllers
sudo apt-get install ros-noetic-ros-controllers
```

## Suggested Validation

Run individual examples from their folder, for example:

```bash
python "Open_CV/OpenCV example source code/show_image.py"
python "Open_CV/OpenCV example source code/hough_lane_detection.py"
```

Gazebo/ROS examples require a ROS Noetic environment and compatible simulation setup.

## Portfolio TODO

- Add screenshots for representative image-processing outputs.
- Add one short explanation for each major example.
- Add exact ROS/Gazebo launch assumptions for lane-detection scripts.
- Mark any missing datasets, bag files, or simulation worlds as `TBD`.
