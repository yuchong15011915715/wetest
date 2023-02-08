import pprint
from findit import FindIt
from stagesepx.classifier import SVMClassifier
from stagesepx.cutter import VideoCutter
from stagesepx.video import VideoObject

if __name__ == '__main__':
    fi = FindIt()
    fi.load_template('wechat_logo', pic_path='pic/Snipaste_2.png')

    result = fi.find(
        target_pic_name='screen',
        target_pic_path='pic/Snipaste_1.png',
    )

    pprint.pprint(result)

    video_path = "pic/456.mp4"
    video = VideoObject(video_path)
    video.load_frames()

    # --- cutter ---
    cutter = VideoCutter()
    res = cutter.cut(video)
    stable, unstable = res.get_range()
    data_home = res.pick_and_save(stable, 5)

    # --- classify ---
    cl = SVMClassifier()
    cl.load("2021112315014431")
    cl.train()
    classify_result = cl.classify(video, stable, keep_data=True)
    result_dict = classify_result.to_dict()

    pprint.pprint(result_dict)