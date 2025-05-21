from imports import *

class_id = 0
IMG_SIZE = 832
OVERLAP = 0.2

def yolo_format(x1, y1, x2, y2, img_w, img_h):
    x_center = ((x1 + x2) / 2) / img_w
    y_center = ((y1 + y2) / 2) / img_h
    width = (x2 - x1) / img_w
    height = (y2 - y1) / img_h
    return f"{class_id} {x_center} {y_center} {width} {height}"

def slicing_imgs(all_annotations, data_annotations, state):
    for _, row in data_annotations.iterrows():
        img_path = os.path.join(dataset_path, row["image_name"])
        if "train_" not in row["image_name"]:
            continue
        # print(row["image_name"])
        img = Image.open(img_path)
        img_w, img_h = img.size
        # Шаг для слайсинга с перекрытием
        step = int(IMG_SIZE * (1 - OVERLAP))

        for i, y in enumerate(range(0, img_h - IMG_SIZE + 1, step)):
            for j, x in enumerate(range(0, img_w - IMG_SIZE + 1, step)):
                tile = img.crop((x, y, x + IMG_SIZE, y + IMG_SIZE))
                tile_name = f"{os.path.splitext(row['image_name'])[0]}_{i}_{j}.jpg"
                tile.save(f"{main_dir}\\drone_dataset\\images\\{state}\\{tile_name}")
                # print(row["x1"], row["y1"], row["x2"], row["y2"])
                x1_tile = max(int(row["x1"]) - x, 0)
                y1_tile = max(int(row["y1"]) - y, 0)
                x2_tile = min(int(row["x2"]) - x, IMG_SIZE)
                y2_tile = min(int(row["y2"]) - y, IMG_SIZE)
                txt_file_path = f"{main_dir}\\drone_dataset\\labels\\{state}\\{tile_name.replace('.jpg', '.txt')}"
                # print(txt_file_path)
                if x1_tile < IMG_SIZE and y1_tile < IMG_SIZE and x2_tile > 0 and y2_tile > 0:
                    if not os.path.exists(txt_file_path):
                        with open(txt_file_path, "w") as f:
                            # print("WWWWWWWWWWWW")
                            # yolo_line = f"{row["x1"]} {row["y1"]} {row["x2"]} {row["y2"]}"
                            yolo_line = yolo_format(x1_tile, y1_tile, x2_tile, y2_tile, IMG_SIZE, IMG_SIZE)
                            f.write(yolo_line + "\n")
                    else:
                        with open(txt_file_path, "a") as f:
                            # print("AAAAAAAAAAAAAAAAA")
                            # yolo_line = f"{row["x1"]} {row["y1"]} {row["x2"]} {row["y2"]}"
                            yolo_line = yolo_format(x1_tile, y1_tile, x2_tile, y2_tile, IMG_SIZE, IMG_SIZE)
                            f.write(yolo_line + "\n")
                else:
                    if not os.path.exists(txt_file_path):
                        # print("NONONONONONO")
                        open(txt_file_path, "w").close()

    all_imgs = 0
    not_person = 0
    for file in os.listdir(f"{main_dir}\\drone_dataset\\labels\\{state}\\"):
        with open(f"{main_dir}\\drone_dataset\\labels\\{state}\\" + file, "r") as f:
            lines = f.readlines()
            all_imgs += 1
            if len(lines) == 0:
                not_person += 1

    person = all_imgs - not_person
    for file in os.listdir(f"{main_dir}\\drone_dataset\\labels\\{state}\\"):
        if not_person < 0.2 * person:
            break
        # print(os.path.exists(f"{os.path.splitext(row['image_name'])[0]}_{i}_{k}.txt"))
        # print(not_person > (person + 1))
        mark = False
        with open(f"{main_dir}\\drone_dataset\\labels\\{state}\\" + file, "r") as f:
            lines = f.readlines()
            if len(lines) == 0:
                mark = True

        if mark:
            os.remove(f"{main_dir}\\drone_dataset\\images\\{state}\\{file.replace('.txt', '.jpg')}")
            os.remove(f"{main_dir}\\drone_dataset\\labels\\{state}\\{file}")
            not_person -= 1
            print(f"{main_dir}\\drone_dataset\\labels\\{state}\\{file.replace('.jpg', '.txt')}")
        print(person, not_person, "************")



# all_imgs = os.listdir(dataset_path)
# random.shuffle(all_imgs)
# total_size = len(all_imgs)
# train_size = int(total_size * 0.7)
# val_size = int(train_size * 0.15)
# test_size = total_size - train_size - val_size
# train_imgs = all_imgs[:train_size]
# val_imgs = all_imgs[train_size:train_size+val_size]
# test_imgs = all_imgs[train_size + val_size:]
#
annotations = pd.read_csv(csv_path, header=None, names=["image_name", "img_w", "img_h", "class", "x1", "y1", "x2", "y2"])
# train_list = annotations[annotations['image_name'].isin(train_imgs)]
# train_list.to_csv("train_list.csv", index=False)
# val_list = annotations[annotations['image_name'].isin(val_imgs)]
# val_list.to_csv("val_list.csv", index=False)
# test_list = annotations[annotations['image_name'].isin(test_imgs)]
# test_list.to_csv("test_list.csv", index=False)

train_annotations = pd.read_csv(f"{main_dir}\\train_list.csv", header=None, names=["image_name", "img_w", "img_h", "class", "x1", "y1", "x2", "y2"])
train_annotations = train_annotations.sort_values(by="image_name", ascending=True)
val_annotations = pd.read_csv(f"{main_dir}\\val_list.csv", header=None, names=["image_name", "img_w", "img_h", "class", "x1", "y1", "x2", "y2"])
val_annotations = val_annotations.sort_values(by="image_name", ascending=True)
test_annotations = pd.read_csv(f"{main_dir}\\test_list.csv", header=None, names=["image_name", "img_w", "img_h", "class", "x1", "y1", "x2", "y2"])
test_annotations = test_annotations.sort_values(by="image_name", ascending=True)


# slicing_imgs(annotations, train_annotations, "train")
slicing_imgs(annotations, val_annotations, "val")
# slicing_imgs(annotations, test_annotations, "test")