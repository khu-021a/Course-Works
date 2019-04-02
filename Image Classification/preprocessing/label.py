import os
import csv
import json


# encode label IDs with sequential line numbers in CSV document 
def map_label_pos(in_path, out_path):
    labels = set()
    with open(in_path, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for rows in reader:
            labels.add(rows[1])
    label_list = list(labels)
    label_list.sort()
    mapping_gen = ((v, i) for i, v in enumerate(label_list))
    
    with open(out_path, 'w') as f:
        json.dump(dict(mapping_gen), f)

# mapping image IDs with label IDs
def map_img_label(in_path, out_path):
    with open(in_path, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        mapping_gen = ((row[0], row[1]) for row in reader)
        with open(out_path, 'w') as f:
            json.dump(dict(mapping_gen), f)

# summarize labels with IDs and texts
def map_label_text(in_path, out_path):
    with open(in_path, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        mapping_gen = ((row[1], row[2]) for row in reader)
        with open(out_path, 'w') as f:
            json.dump(dict(mapping_gen), f)

# map image IDs with line numbers in CSV document 
def map_img_pos(img_label, label_pos, out_path):
    img_label_json = open(img_label, 'r')
    img_label_dict = json.load(img_label_json)
    label_pos_json = open(label_pos, 'r')
    label_pos_dict = json.load(label_pos_json)
    img_pos = {k: label_pos_dict[v] for k, v in img_label_dict.items()}
    img_label_json.close()
    label_pos_json.close()
    with open(out_path, 'w') as f:
        json.dump(dict(img_pos), f)

# compute the total label number
def label_count(in_path, out_path):
    with open(in_path, encoding='utf-8') as csvfile:
        label_count_dict = {}
        reader = csv.reader(csvfile)
        for row in reader:
            key = row[1]
            if key not in label_count_dict:
                label_count_dict[key] = 0
            label_count_dict[key] += 1

        with open(out_path, 'w') as f:
            json.dump(label_count_dict, f)

# map images in folder to line numbers 
# which act as consecutive labels for computations
# in the single label context
def labels_in_dir(dir, mapping):
    labels = set()
    files = os.listdir(dir)
    map_file = open(mapping, 'r')
    map_dict = json.load(map_file)
    for f in files:
        fid = f.split('.')[0]
        l = map_dict[fid]
        labels.add(l)
    map_file.close()
    return labels
