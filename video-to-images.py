import cv2
import os
import argparse


def video2images(video, width=None, height=None):
    cap = cv2.VideoCapture(video)
    if cap.isOpened() is False:
        print('Error opening video file: {}'.format(video))
        return

    out_dirname = os.path.basename(video).split('.')[0]
    try:
        os.makedirs(out_dirname, exist_ok=False)
        print('Created directory to store the images: {}'.format(os.path.abspath(out_dirname)))
    except:
        print('Output directory already exists. Skip overwriting: {}'.format(os.path.abspath(out_dirname)))
        return

    seq = 1
    while cap.isOpened() is True:
        ret, frame = cap.read()

        if ret is True:
            if width is not None and height is not None:
                frame = cv2.resize(frame, (width, height), interpolation = cv2.INTER_AREA)

            img_filename = f'{out_dirname}/{seq}.jpg'
            seq += 1
            cv2.imwrite(img_filename, frame)

            key = cv2.waitKey(1)
            if key == ord('q') or key == ord('Q') or key == 27:
                print('Quitting program')
                break



if __name__ == '__main__':
    def validate_file(filename):
        if not os.path.exists(filename):
            raise argparse.ArgumentTypeError('{} does not exist'.format(filename))
        return filename

    parser = argparse.ArgumentParser(description='Video to Images Conversion')
    parser.add_argument("-v", "--video", help='Enter video filename', required=True, dest='video', default=None, type=validate_file, metavar='FILE')
    parser.add_argument('--width', help='Optional resize width', dest='width', default=None, type=int)
    parser.add_argument('--height', help='Optional resize height', dest='height', default=None, type=int)
    args = parser.parse_args()

    if args.video is None:
        print('Video file not provided.')
        exit(1)

    if not os.path.exists(args.video):
        print('Video file {} does not exist.'.format(args.video))
        exit(1)

    print('Converting video {} to images.'.format(args.video))
    video2images(args.video, width=args.width, height=args.height)
    print('Done.')
