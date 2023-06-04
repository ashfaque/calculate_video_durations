def sort_key(filename):
    import re

    match = re.search(r'\d+', filename)  # Extract numeric part of filename
    if match:
        numeric_part = int(match.group())  # Convert to integer
    else:
        numeric_part = 0  # Assign a default value for filenames without numbers

    return numeric_part, filename



if __name__ == "__main__":
    import time
    import os
    import sys
    import ffmpeg    # pip install ffmpeg-python
    from pprint import pprint


    start_time = time.time()

    # start_file_name = input('Enter file name to start calculation of duration from (with extension name): ')
    start_file_name = sys.argv[1] if len(sys.argv) > 1 else None
    vid_dir_path = input('Enter the full path of the dir of videos: ')

    raw_videos_list = os.listdir(vid_dir_path)


    videos_list = []
    for each_video in sorted(raw_videos_list, key=sort_key):    # Sorted in this format: ['lesson1', 'lesson2', 'lesson10'] instead of ['lesson1', 'lesson10', 'lesson2']
        if each_video.endswith('.mp4'):
            videos_list.append(os.path.join(vid_dir_path, each_video))

    start_index = 0
    if start_file_name:
        for index, each_video in enumerate(videos_list):
            if each_video.lower() == str(os.path.join(vid_dir_path, start_file_name)).lower():
                start_index = index
    videos_list = videos_list[start_index:]


    total_video_duration_in_secs = 0.0
    for each_vid_path in videos_list:
        # pprint(ffmpeg.probe(each_vid_path)['streams'])    # [{video_data},{audio_data}]
        # pprint(ffmpeg.probe(each_vid_path))    # dict()
        each_vid_duration_in_secs = ffmpeg.probe(each_vid_path)['streams'][0]['duration']    # Picking video data dict.
        total_video_duration_in_secs += float(each_vid_duration_in_secs)


    # Converting seconds to hrs, mins, secs - Method - 1:-
    import time
    total_duration1 = time.strftime("%H:%M:%S", time.gmtime(total_video_duration_in_secs))

    # Converting seconds to hrs, mins, secs - Method - 2:-
    import datetime
    total_duration2 = str(datetime.timedelta(seconds = total_video_duration_in_secs))

    # Converting seconds to hrs, mins, secs - Method - 3:-
    minutes, seconds = divmod(total_video_duration_in_secs, 60)
    hours, minutes = divmod(minutes, 60)
    total_duration3 = f"{int(hours)}:{int(minutes)}:{int(seconds)}"


    print(total_duration1)
    # print(total_duration2)
    # print(total_duration3)
    
    print("Execution time ---> ", time.time() - start_time)

