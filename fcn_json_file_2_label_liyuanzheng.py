# json格式文件批量转换
# import argparse
# import json
# import os
# import os.path as osp
# import warnings
# import PIL.Image
# import yaml
# from labelme import utils
# import base64
#
# def main():
#
#     json_file = "./jiao_file"
#     count = os.listdir(json_file)
#     for i in range(0, len(count)):
#         path = os.path.join(json_file, count[i])
#         if os.path.isfile(path):
#             data = json.load(open(path))
#
#             if data['imageData']:
#                 imageData = data['imageData']
#             else:
#                 imagePath = os.path.join(os.path.dirname(path), data['imagePath'])
#                 with open(imagePath, 'rb') as f:
#                     imageData = f.read()
#                     imageData = base64.b64encode(imageData).decode('utf-8')
#             img = utils.img_b64_to_arr(imageData)
#             label_name_to_value = {'_background_': 0}
#             for shape in data['shapes']:
#                 label_name = shape['label']
#                 if label_name in label_name_to_value:
#                     label_value = label_name_to_value[label_name]
#                 else:
#                     label_value = len(label_name_to_value)
#                     label_name_to_value[label_name] = label_value
#
#             # label_values must be dense
#             label_values, label_names = [], []
#             for ln, lv in sorted(label_name_to_value.items(), key=lambda x: x[1]):
#                 label_values.append(lv)
#                 label_names.append(ln)
#             assert label_values == list(range(len(label_values)))
#
#             lbl = utils.shapes_to_label(img.shape, data['shapes'], label_name_to_value)
#
#             captions = ['{}: {}'.format(lv, ln)
#                         for ln, lv in label_name_to_value.items()]
#             lbl_viz = utils.draw_label(lbl, img, captions)
#
#
#             out_dir = osp.basename(count[i]).replace('.', '_')
#             out_dir = os.path.join("./jiaodata",osp.join(osp.dirname(count[i]), out_dir))
#             print(out_dir)
#             if not osp.exists(out_dir):
#                 os.mkdir(out_dir)
#
#             PIL.Image.fromarray(img).save(osp.join(out_dir, 'img.png'))
#             # PIL.Image.fromarray(lbl).save(osp.join(out_dir, 'label.png'))
#             utils.lblsave(osp.join(out_dir, 'label.png'), lbl)PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir, 'label_viz.png'))
#
#
#             with open(osp.join(out_dir, 'label_names.txt'), 'w') as f:
#                 for lbl_name in label_names:
#                     f.write(lbl_name + '\n')
#
#             warnings.warn('info.yaml is being replaced by label_names.txt')
#             info = dict(label_names=label_names)
#             with open(osp.join(out_dir, 'info.yaml'), 'w') as f:
#                 yaml.safe_dump(info, f, default_flow_style=False)
#
#             print('Saved to: %s' % out_dir)
#
# if __name__ == '__main__':
#     main()



import cv2
import numpy as np
import os
np.set_printoptions(threshold=100000000000000000)


path = r"D:\liuxiang\testpytorch\jiaodata"
all_json_file = os.listdir(path)
count = 0
for i in all_json_file:
    count += 1
    img_path = os.path.join(path,i)
    img_list = os.listdir(img_path)
    for j in img_list:
        if j == "img.png":
            train_data_path = os.path.join(img_path,j)
            train_data = cv2.imread(train_data_path)
            cv2.imwrite(r"D:\liuxiang\testpytorch\bag_data\\"+ str(count) + ".png",train_data)
        if j == "label.png":
            label_path = os.path.join(img_path,j)
            label_data = cv2.imread(label_path,0)
            for x in range(0,label_data.shape[0]):
                for y in range(0,label_data.shape[1]):
                    if label_data[x][y] == 0:
                        label_data[x][y] = 255
                    else:
                        label_data[x][y] = 0
            cv2.imwrite(r"D:\liuxiang\testpytorch\bag_mask\\" + str(count) + ".png", label_data)
