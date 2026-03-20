# FPV Aim Assist

Computer vision-based FPV aim assist prototype for screen input.  
The project detects a target on the screen, tracks it across frames, computes correction commands, mixes them with pilot input, and sends the result to a virtual gamepad.

## Demo 

```text
https://youtu.be/ZKWv6fKPGlQ
```

## Features

- screen capture input
- YOLO-based object detection
- target filtering by class and confidence
- simple nearest-target tracking
- PD-based assist controller for yaw and pitch
- manual / assist flight modes
- pilot input mixing
- virtual Xbox 360 gamepad output
- on-screen visualization of target, frame center, and current mode

## Project structure

```text
.
├── core/
│   ├── controller.py
│   ├── detector.py
│   ├── frame_source.py
│   ├── input_reader.py
│   ├── mixer.py
│   ├── mode_manager.py
│   ├── target_selector.py
│   ├── tracker.py
│   ├── virtual_pad.py
│   └── visualizer.py
├── models/
│   └── yolov8s.pt
├── utils/
│   └── geometry.py
├── config.py
├── main.py
└── requirements.txt
```
## How it works

1. A screen region is captured frame by frame.
2. Every N frames, YOLO runs detection on the current frame.
3. Detections are filtered by target class and confidence threshold.
4. The tracker selects the most relevant target and maintains continuity across frames.
5. The controller computes yaw and pitch corrections based on target offset from the frame center.
6. The mixer combines pilot input with assist commands.
7. The output is sent to a virtual Xbox 360 gamepad.
8. The current state is rendered in a preview window.

## Requirements

- Python 3.10+
- Windows
- connected gamepad
- ViGEm driver

## Installation

```text
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
## Running

```text
python main.py
```

## Configuration

Main parameters are defined in config.py.

## Controls

- left stick → roll / throttle
- right stick → yaw / pitch
- R3 → toggle assist mode

## Output

- target bounding box
- target center
- frame center
- current mode (MANUAL / ASSIST)


## Limitations

- detection is not performed on every frame
- tracking is basic and may switch targets
- only yaw and pitch are assisted
- no real drone integration
- no safety mechanisms
