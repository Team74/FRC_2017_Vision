echo "--- Camera 1 ---"
echo "***Brightness 30"
v4l2-ctl --set-ctrl=brightness=30 --device=/dev/video0
echo "Contrast 5"
v4l2-ctl --set-ctrl=contrast=5 --device=/dev/video0
echo "**Saturation 100"
v4l2-ctl --set-ctrl=saturation=100 --device=/dev/video0
echo "***White Balance Temperature Auto 0"
v4l2-ctl --set-ctrl=white_balance_temperature_auto=0 --device=/dev/video0
echo "Power Line Frequency 2 (default don't touch)"
v4l2-ctl --set-ctrl=power_line_frequency=2 --device=/dev/video0
echo "***White Balance Temp 2800"
v4l2-ctl --set-ctrl=white_balance_temperature=2800 --device=/dev/video0
echo "Sharpness 25"
v4l2-ctl --set-ctrl=sharpness=25 --device=/dev/video0
echo "***Backlight_Compensation 0"
v4l2-ctl --set-ctrl=backlight_compensation=0 --device=/dev/video0
echo "***Exposure_Auto 1"
v4l2-ctl --set-ctrl=exposure_auto=1 --device=/dev/video0
echo "***Exposure Absolute 10"
v4l2-ctl --set-ctrl=exposure_absolute=5 --device=/dev/video0
echo "Pan 0"
v4l2-ctl --set-ctrl=pan_absolute=0 --device=/dev/video0
echo "Tilt 0"
v4l2-ctl --set-ctrl=tilt_absolute=0 --device=/dev/video0
echo "Zoom 0"
v4l2-ctl --set-ctrl=zoom_absolute=0 --device=/dev/video0

echo "--- Camera 2 ---"
echo "***Brightness 30"
v4l2-ctl --set-ctrl=brightness=30 --device=/dev/video1
echo "Contrast 5"
v4l2-ctl --set-ctrl=contrast=5 --device=/dev/video1
echo "**Saturation 100"
v4l2-ctl --set-ctrl=saturation=100 --device=/dev/video1
echo "***White Balance Temperature Auto 0"
v4l2-ctl --set-ctrl=white_balance_temperature_auto=0 --device=/dev/video1
echo "Power Line Frequency 2 (default don't touch)"
v4l2-ctl --set-ctrl=power_line_frequency=2 --device=/dev/video1
echo "***White Balance Temp 2800"
v4l2-ctl --set-ctrl=white_balance_temperature=2800 --device=/dev/video1
echo "Sharpness 25"
v4l2-ctl --set-ctrl=sharpness=25 --device=/dev/video1
echo "***Backlight_Compensation 0"
v4l2-ctl --set-ctrl=backlight_compensation=0 --device=/dev/video1
echo "***Exposure_Auto 1"
v4l2-ctl --set-ctrl=exposure_auto=1 --device=/dev/video1
echo "***Exposure Absolute 10"
v4l2-ctl --set-ctrl=exposure_absolute=5 --device=/dev/video1
echo "Pan 0"
v4l2-ctl --set-ctrl=pan_absolute=0 --device=/dev/video1
echo "Tilt 0"
v4l2-ctl --set-ctrl=tilt_absolute=0 --device=/dev/video1
echo "Zoom 0"
v4l2-ctl --set-ctrl=zoom_absolute=0 --device=/dev/video1

