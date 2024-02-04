import os
import ffmpeg
from utils import WHERE_IS_CAM, path_from_scenecam
import json

from loguru import logger

image_id: int = 0
bbox_id: int = 0



def extract_frames(cam_id):
    # Extract frames using ffmpeg
    cam_path = path_from_scenecam(cam_id)
    video_path = os.path.join(cam_path, 'video.mp4')
    frame_path = os.path.join(cam_path, 'frames')
    os.makedirs(frame_path, exist_ok=True)
    logger.info(f'Extracting frames from {video_path} to {frame_path}')
    ffmpeg.input(video_path).filter('fps', fps='30').output(frame_path + '/%05d.jpg', start_number=0, **{'qscale:v': 2}).overwrite_output().run(quiet=True)


def prepare_coco_format(cam_id):
    logger.info(f'Preparing coco format from {cam_id}')
    '''
        aic label format:
            frame_id, track_id, x, y, w, h, 1, -1, -1, -1
        coco_format:
            {
                'images'[
                    {
                        file_name: 'frame_id.jpg',
                        id: ,
                        frame_id: frame_id,
                        video_id: video_id,
                        height: 
                    }
                ]
            }
    '''
    
    global image_id, bbox_id
    
    cam_path = path_from_scenecam(cam_id)
    frame_path = os.path.join(cam_path, 'frames')
    out_path = os.path.join(cam_path, 'coco.json')
    
    coco_format = {
        'images': [],
        'annotations': [],
        'categories': [{'id': 1, 'name': 'person'}]
    }
    anno_path = os.path.join(cam_path, 'label.txt')
    
    logger.info(f'Preparing {out_path} from {anno_path}')
    
    if 'test' in cam_path:
        return
    
    with open(anno_path, 'r') as f:
        for line in f:
            frame_id, track_id, x, y, w, h, _, _, _, _ = (int(i) for i in line.strip().split(','))
            coco_format['images'].append({
                'file_name': f'{frame_id}.jpg',
                'id': (image_id := image_id + 1),
                'width': 1920, # assumed 1920*1080
                'height': 1080 # assumed 1920*1080
            })
            
            coco_format['annotations'].append({
                'image_id': image_id,
                'id': (bbox_id := bbox_id + 1),
                'category_id': 1, # since there's only one category (person)
                'bbox': [x, y, w, h],
                'area': w * h,
                'iscrowd': 0
            })
    
    with open(out_path, 'w') as f:
        json.dump(coco_format, f)
                
                
def main():
    # for usage, scenes in WHERE_IS_CAM.items():
    #     for scene, cams in scenes.items():
    #         for cam in cams:
    #             extract_frames((scene, cam))
    #             prepare_coco_format((scene, cam))
    '''
        Only do S002 for now
    '''
    usage = 'train'
    scene = 'S002'
    for cam in WHERE_IS_CAM[usage][scene]:
        extract_frames((scene, cam))
        prepare_coco_format((scene, cam))
    
    
    
if __name__ == '__main__':
    main()