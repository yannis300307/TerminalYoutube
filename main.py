import cv2
import yt_dlp
import sys
import time
from ffpyplayer.player import MediaPlayer
import shutil


def play_video(url: str):
    width = 128

    # TODO: Reduce the quality to reduce bw
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet': True,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        stream_url = info['url']
    
    #stream_url = "video.mp4"
    cap = cv2.VideoCapture(stream_url)
    player = MediaPlayer(stream_url)

    frame_time = 1. / cap.get(cv2.CAP_PROP_FPS);

    while True:
        start_time = time.time()
        ret, frame = cap.read()
        _, _ = player.get_frame()
        if ret is None:
            break

        shape = frame.shape

        height = int(width * shape[0] / shape[1])

        term_size = shutil.get_terminal_size((80, 20))

        position = (term_size[0] - width - 2, 2)

        resize = cv2.resize(frame, (width, height))

        converted_frame = []
        converted_frame.append(f"\x1b7\x1b[{position[1]};{position[0]}H")
        for y in range(0, height, 2):
            for x in range(0, width):
                b1, g1, r1 = resize[y, x]
                if y < height - 1:
                    b2, g2, r2 = resize[y + 1, x]
                    converted_frame.append(f'\x1b[38;2;{r2};{g2};{b2};48;2;{r1};{g1};{b1}m▄')
                else:
                    converted_frame.append(f'\x1b[49;38;2;{r1};{g1};{b1}m▀')

            converted_frame.append(f"\x1b[1B\x1b[{position[0]}G")

        converted_frame.append(f"\x1b8")
        sys.stdout.write("".join(converted_frame))
        sys.stdout.flush()
        delta = time.time() - start_time
        time.sleep(max(frame_time - delta, 0.))
    

    cap.release()
    cv2.destroyAllWindows()

def main():
    url = input("Youtube URL > ")
    play_video(url)

if __name__ == "__main__":
    main()
