import cv2
import numpy as np
import os
from scipy.signal import argrelextrema


def extract_keyframes(videopath, output_dir='./extractimg/', len_window=50, frame_interval=1):
    def smooth(x, window_len=13, window='hanning'):
        """ Helper function to smooth the signal. """
        if x.size < window_len:
            window_len = x.size
        if window_len < 3:
            return x
        s = np.r_[2 * x[0] - x[window_len:1:-1], x, 2 * x[-1] - x[-1:-window_len:-1]]
        if window == 'flat':  # moving average
            w = np.ones(window_len, 'd')
        else:
            w = getattr(np, window)(window_len)
        y = np.convolve(w / w.sum(), s, mode='same')
        return y[window_len - 1:-window_len + 1]

    # Check if video file exists
    if not os.path.isfile(videopath):
        print(f"Error: Video file {videopath} not found.")
        return

    # Create directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load video and get FPS
    cap = cv2.VideoCapture(videopath)
    if not cap.isOpened():
        print(f"Error: Could not open video {videopath}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_skip = int(fps * frame_interval)  # Process every `frame_interval` seconds

    print(f"Target video: {videopath}")
    print(f"Frame save directory: {output_dir}")
    print(f"Video FPS: {fps}")
    print(f"Processing every {frame_skip} frames ({frame_interval} seconds)")

    curr_frame = None
    prev_frame = None
    frame_diffs = []
    frames = []
    success, frame = cap.read()
    i = 0

    # Read and process video frames
    while success:
        if i % frame_skip == 0:  # Process every `frame_interval` seconds
            luv = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
            curr_frame = luv
            if curr_frame is not None and prev_frame is not None:
                # Compute frame difference
                diff = cv2.absdiff(curr_frame, prev_frame)
                diff_sum = np.sum(diff)
                diff_sum_mean = diff_sum / (diff.shape[0] * diff.shape[1])
                frame_diffs.append(diff_sum_mean)
                frames.append(i)
            prev_frame = curr_frame
        i += 1
        success, frame = cap.read()
    cap.release()

    # Exit if no differences were found
    if len(frame_diffs) == 0:
        print("No frame differences calculated. Please check the video file and parameters.")
        return

    # Compute keyframes
    print("Computing keyframes using local maxima.")
    diff_array = np.array(frame_diffs)
    sm_diff_array = smooth(diff_array, len_window)
    frame_indexes = np.asarray(argrelextrema(sm_diff_array, np.greater))[0]
    keyframe_ids = [frames[i] for i in frame_indexes]

    # Save keyframes as images
    cap = cv2.VideoCapture(videopath)
    success, frame = cap.read()
    idx = 0
    while success:
        if idx in keyframe_ids:
            name = f"keyframe_{idx}.jpg"
            cv2.imwrite(os.path.join(output_dir, name), frame)
            keyframe_ids.remove(idx)
        idx += 1
        success, frame = cap.read()
    cap.release()

    print("Keyframe extraction completed.")


# Example usage:
extract_keyframes('information/86Gy035z_KA.mp4', './extractimg/', len_window=50, frame_interval=1)