import os
import random
import shutil
import json
import sys
import yaml


def convert(size, box, label):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[0] + box[2]) / 2.0
    y = (box[1] + box[1] + box[3]) / 2.0
    w = box[2]
    h = box[3]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return str(label) + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h) + '\n'


train_val_percent = 0.9
train_percent = 0.9
image_source_path = './datasets/COCOData/data'
label_source_path = './datasets/COCOData/labels.json'
txt_dst_path = './datasets/YOLOData'
image_dst_path = './datasets/YOLOData/images'
label_dst_path = './datasets/YOLOData/labels'

if os.path.exists(txt_dst_path):
    decision = input('Do you want to delete existed YOLO dataset?[Y/N]')
    if decision == 'N' or decision == 'n':
        sys.exit()
    shutil.rmtree(txt_dst_path)
os.makedirs(txt_dst_path)

os.makedirs(image_dst_path)
os.makedirs(os.path.join(image_dst_path, 'train'))
os.makedirs(os.path.join(image_dst_path, 'val'))
os.makedirs(os.path.join(image_dst_path, 'test'))

os.makedirs(label_dst_path)
os.makedirs(os.path.join(label_dst_path, 'train'))
os.makedirs(os.path.join(label_dst_path, 'val'))
os.makedirs(os.path.join(label_dst_path, 'test'))

num = 10000
list_index = range(num)
train_val_num = int(num * train_val_percent)
train_num = int(train_val_num * train_percent)
train_val_list = set(random.sample(list_index, train_val_num))
train_list = set(random.sample(train_val_list, train_num))

file_test = open(txt_dst_path + '/test.txt', 'w')
file_train = open(txt_dst_path + '/train.txt', 'w')
file_val = open(txt_dst_path + '/val.txt', 'w')

for i in list_index:
    image_name = 'rgb_{:04}.png'.format(i)
    if i in train_val_list:
        if i in train_list:
            shutil.copy(os.path.join(image_source_path, image_name), os.path.join(image_dst_path, 'train'))
            file_train.write(image_dst_path + '/train/' + image_name + '\n')
        else:
            shutil.copy(os.path.join(image_source_path, image_name), os.path.join(image_dst_path, 'val'))
            file_val.write(image_dst_path + '/val/' + image_name + '\n')
    else:
        shutil.copy(os.path.join(image_source_path, image_name), os.path.join(image_dst_path, 'test'))
        file_test.write(image_dst_path + '/test/' + image_name + '\n')
    if i % 100 == 0:
        print('image {} is finished'.format(i))

file_train.close()
file_val.close()
file_test.close()

with open(label_source_path, 'r') as f:
    src_label = json.load(f)
annotations = src_label['annotations']
categories = src_label['categories']

pre_image_id = 0
pre_image_label = []
for item in annotations:
    image_id = item['image_id']
    bbox = item['bbox']
    label = item['category_id']
    if image_id != pre_image_id:
        data_separate = ''
        if pre_image_id in train_val_list:
            if pre_image_id in train_list:
                data_separate = 'train'
            else:
                data_separate = 'val'
        else:
            data_separate = 'test'
        if data_separate != '':
            with open(os.path.join(label_dst_path, data_separate, 'rgb_{:04}.txt'.format(pre_image_id)), 'w') as f:
                f.writelines(pre_image_label)
        pre_image_label.clear()
        pre_image_id = image_id
        if pre_image_id % 100 == 0:
            print('image {} label is finished'.format(pre_image_id))
    pre_image_label.append(convert((1024, 1024), bbox, label))

yaml_dict = {
    'train': './images/train/',
    'val': './images/val/',
    'test': './images/test/',
    'nc': len(categories),
    'names': {i + 1: categories[i]['name'] for i in range(len(categories))}
}
yaml_dict['names'][0] = 'unlabeled'
with open(os.path.join(txt_dst_path, 'dataset.yaml'), 'w') as f:
    yaml.dump(yaml_dict, f)
