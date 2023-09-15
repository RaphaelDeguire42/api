import cv2
import os
import sys

def extract_frames(fileName, workspacePath):
    file_name = fileName

    file_path = os.path.join(workspacePath, file_name)
    folder_name = os.path.splitext(file_name)[0]
    folder_path = os.path.join(workspacePath, folder_name)

    # Check if the folder path exists; if not, create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    unlabelled_path = os.path.join(folder_path, 'unlabelled')
    labelled_path = os.path.join(folder_path, 'labelled')

    if not os.path.exists(unlabelled_path):
        os.makedirs(unlabelled_path)

    if not os.path.exists(labelled_path):
        os.makedirs(labelled_path)

    capture = cv2.VideoCapture(file_path)
    frame_count = 0

    while frame_count < 50:  # Change '50' to 'True' to extract the entire video
        success, frame = capture.read()
        if not success:
            break

        frame_filename = f"frame{frame_count}.webp"
        frame_path_1 = os.path.join(unlabelled_path, frame_filename)
        frame_path_2 = os.path.join(labelled_path, frame_filename)

        if os.path.exists(frame_path_1) or os.path.exists(frame_path_2):
            print(f"Frame {frame_count} already exists in one of the paths. Skipping...")
            frame_count += 1
            continue

        cv2.imwrite(frame_path_1, frame, [cv2.IMWRITE_WEBP_QUALITY, 75])

        print(f"Frame {frame_count} extracted.")
        frame_count += 1

    capture.release()

def main():
    if len(sys.argv) < 3:
        print("Usage: python extraction.py <filename> <workspacePath>")
        return

    fileName = sys.argv[1]
    workspacePath = sys.argv[2]

    extract_frames(fileName, workspacePath)

# Call the main function
main()
