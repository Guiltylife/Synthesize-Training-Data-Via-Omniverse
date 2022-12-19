import os
import shutil
import json
import sys
import numpy as np
import matplotlib.image as mpig


source_data_path = './datasets/ReplicatorData'
destination_data_path = './datasets/COCOData'

if os.path.exists(destination_data_path):
    decision = input('Do you want to delete existed COCO dataset?[Y/N]')
    if decision == 'N' or decision == 'n':
        sys.exit()
    shutil.rmtree(destination_data_path)
os.makedirs(destination_data_path)

os.makedirs(os.path.join(destination_data_path, 'data'))
os.makedirs(os.path.join(destination_data_path, 'depth'))
os.makedirs(os.path.join(destination_data_path, 'semantic'))

data_num_start = 0
data_num_end = 10000
img_size = 1024

coco_json = {'images': [], 'annotations': [], 'categories': []}
bbox_label_name_dict = {}
bbox_id = 0
semantic_json = []
semantic_label_name_dict = {}
for i in range(data_num_start, data_num_end):
    rgb_file = 'rgb_{:04}.png'.format(i)
    bbox_array_file = 'bounding_box_2d_tight_{:04}.npy'.format(i)
    bbox_label_file = 'bounding_box_2d_tight_labels_{:04}.json'.format(i)
    semantic_img_file = 'semantic_segmentation_{:04}.png'.format(i)
    semantic_label_file = 'semantic_segmentation_labels_{:04}.json'.format(i)
    depth_file = 'distance_to_camera_{:04}.npy'.format(i)

    # rgb file
    shutil.copy(os.path.join(source_data_path, rgb_file), os.path.join(destination_data_path, 'data'))

    # bbox file
    coco_json['images'].append({
        "id": i,
        "file_name": rgb_file,
        "width": img_size,
        "height": img_size
    })
    bbox_array = np.load(os.path.join(source_data_path, bbox_array_file))
    with open(os.path.join(source_data_path, bbox_label_file), 'r') as f:
        bbox_label_json = json.load(f)
    for item in bbox_array:
        bbox_label_id = item[0]
        bbox_label_name = bbox_label_json[str(bbox_label_id)]['class']
        if bbox_label_name not in bbox_label_name_dict.keys():
            bbox_label_name_dict[bbox_label_name] = len(bbox_label_name_dict) + 1
            coco_json['categories'].append({
                "supercategory": 'class',
                "id": len(bbox_label_name_dict),
                "name": bbox_label_name
            })
        coco_json['annotations'].append({
            "image_id": i,
            "bbox": [int(item[1]), int(item[2]), int(item[3] - item[1]), int(item[4] - item[2])],
            "category_id": bbox_label_name_dict[bbox_label_name],
            "id": bbox_id
        })
        bbox_id += 1

    # semantic file
    semantic_img = mpig.imread(os.path.join(source_data_path, semantic_img_file)) * 255
    with open(os.path.join(source_data_path, semantic_label_file), 'r') as f:
        semantic_label_json = json.load(f)
    semantic_array = np.zeros((img_size, img_size))
    for j in range(semantic_img.shape[0]):
        for k in range(semantic_img.shape[1]):
            pixel = str((int(semantic_img[j][k][0]), int(semantic_img[j][k][1]),
                         int(semantic_img[j][k][2]), int(semantic_img[j][k][3])))
            label_name = semantic_label_json[pixel]['class']
            if label_name not in semantic_label_name_dict.keys():
                semantic_label_name_dict[label_name] = len(semantic_label_name_dict)
                semantic_json.append({
                    'id': len(semantic_label_name_dict) - 1,
                    'name': label_name
                })
            semantic_array[j][k] = semantic_label_name_dict[label_name]
    np.save(os.path.join(destination_data_path, 'semantic', 'semantic_segmentation_{:04}.npy'.format(i)), semantic_array)

    # depth file
    shutil.copy(os.path.join(source_data_path, depth_file), os.path.join(destination_data_path, 'depth'))

    print('img {} is finished'.format(i))

with open(os.path.join(destination_data_path, 'labels.json'), 'w') as f:
    json.dump(coco_json, f)

with open(os.path.join(destination_data_path, 'semantic', 'semantic_segmentation_labels.json'), 'w') as f:
    json.dump(semantic_json, f)
