import os

import cv2

import moviepy
import moviepy.editor as mp
from pydub import AudioSegment

# ファイル名
input_folder = "deer"  # 読み込む動画があるフォルダ
image_out = "image_tmp.mp4"  # 映像のみの出力
sound_out = "sound_tmp.mp3"  # 音声のみの出力
movie_out = "movie_out.mp4"  # 映像と音声の出力


# 元の動画を結合し音声なしで出力
def comb_movie(movies_in, image_out):
    # 形式はmp4
    global frame
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    # 動画情報の取得
    movie = cv2.VideoCapture(movies_in[0])
    fps = movie.get(cv2.CAP_PROP_FPS)
    height = movie.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = movie.get(cv2.CAP_PROP_FRAME_WIDTH)

    # 出力先のファイルを開く
    out = cv2.VideoWriter(image_out, int(fourcc), fps, (int(width), int(height)))

    for movie_in in movies_in:
        # 動画ファイルの読み込み，引数はビデオファイルのパス
        movie = cv2.VideoCapture(movie_in)

        # 正常に動画ファイルを読み込めたか確認
        if movie.isOpened():
            # read():1コマ分のキャプチャ画像データを読み込む
            ret, frame = movie.read()
        else:
            ret = False
            print(movie_in + "：読み込めませんでした")

        while ret:
            # 読み込んだフレームを書き込み
            out.write(frame)
            # 次のフレーム読み込み
            ret, frame = movie.read()

        print("movie input:" + movie_in)


# 元の動画の音声を結合し映像のみの動画に付加
def set_audio(movies_in, movie_out, image_out, sound_out):
    sound = None
    AudioSegment.converter = os.path.abspath("ffmpeg.exe")
    # 元のファイルから音声を一つずつ抽出して結合
    for movie_in in movies_in:
        m_in = os.path.abspath(movie_in.replace(".mp4", ".mp3"))
        if not os.path.exists(m_in):
            audio = moviepy.editor.AudioFileClip(movie_in)
            # .mp3ファイルとして保存
            audio.write_audiofile(m_in, codec='libmp3lame')
            print("done")
        if sound is None:
            sound = AudioSegment.from_file(m_in)
        else:
            sound += AudioSegment.from_file(m_in)

    # 結合した音声を出力
    sound.export(sound_out, format="mp3")

    clip = mp.VideoFileClip(image_out).subclip()

    # 結合した音声を動画に付加
    clip.write_videofile(movie_out, audio=sound_out)


def create(str):
    movies_in = []
    for s in str:
        if s == '\n':
            continue
        movies_in.append("deer\\" + s + ".mp4")
    comb_movie(movies_in, image_out)

    set_audio(movies_in, movie_out, image_out, sound_out)

    # example
    # create(
    """しかのこのここのこのここのここのここのここのこのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのここのここのここのこのここのここのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのこのこのこのこのこのここのこのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのこのこのこのこのこのここのこのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのこのこのこのこのここのこのここのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのこのこのこのこのここのこのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのここのこのここのここのこのここのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのこのこのこのこのここのこのここのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのこのこのこのここのこのこのこのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのこのこのこのこのこのここのこのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのここのここのここのこのここのこのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのここのこのここのここのここのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　"""


# )

# create directory "deer" and put し.mp4 か.mp4 etc....

if __name__ == '__main__':
    s = ''
    i = input()
    while i == '':
        s += i
        i = input()
    create(s)
