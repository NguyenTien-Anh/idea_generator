import os

from moviepy import VideoFileClip


def convert_video_to_audio(video_path, audio_path=None):
    """
    Chuyển đổi video sang file audio.

    Args:
        video_path (str): Đường dẫn đến file video đầu vào.
        audio_path (str, optional): Đường dẫn đến file audio đầu ra.
                                     Nếu không cung cấp, audio sẽ được lưu cùng thư mục
                                     với video và có cùng tên nhưng với đuôi .mp3.

    Returns:
        str: Đường dẫn đến file audio đã tạo, hoặc None nếu có lỗi.
    """
    try:
        # Load video clip
        video_clip = VideoFileClip(video_path)

        # Nếu audio_path không được cung cấp, tạo đường dẫn mặc định
        if audio_path is None:
            video_dir = os.path.dirname(video_path)
            video_name_without_ext = os.path.splitext(os.path.basename(video_path))[0]
            audio_path = os.path.join(video_dir, f"{video_name_without_ext}.mp3")

        # Trích xuất âm thanh
        audio_clip = video_clip.audio

        # Ghi âm thanh ra file
        audio_clip.write_audiofile(audio_path)

        # Đóng các clip
        audio_clip.close()
        video_clip.close()

        print(f"Chuyển đổi thành công! Audio được lưu tại: {audio_path}")
        return audio_path

    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file video tại '{video_path}'. Vui lòng kiểm tra lại đường dẫn.")
        return None
    except Exception as e:
        print(f"Đã xảy ra lỗi trong quá trình chuyển đổi: {e}")
        return None


if __name__ == "__main__":
    input_video_file = "/home/rb071/Downloads/Japan.mp4"

    convert_video_to_audio(input_video_file)
