from imports import *

class_id = 0
IMG_SIZE = 832
OVERLAP = 0.2

annotations = pd.read_csv(csv_path, header=None, names=["image_name", "img_w", "img_h", "class", "x1", "y1", "x2", "y2"])

# train, tmp = train_test_split(annotations, test_size=0.3, random_state=42)
# val, test = train_test_split(annotations, test_size=0.63, random_state=42)
#
# train.to_csv("train_list.csv", index=False)
# val.to_csv("val_list.csv", index=False)
# test.to_csv("test_list.csv", index=False)

train_annotations = pd.read_csv(f"{main_dir}\\train_list.csv", header=None, names=["image_name", "img_w", "img_h", "class", "x1", "y1", "x2", "y2"])
val_annotations = pd.read_csv(f"{main_dir}\\val_list.csv", header=None, names=["image_name", "img_w", "img_h", "class", "x1", "y1", "x2", "y2"])
test_annotations = pd.read_csv(f"{main_dir}\\test_list.csv", header=None, names=["image_name", "img_w", "img_h", "class", "x1", "y1", "x2", "y2"])


def yolo_format(x1, y1, x2, y2, img_w, img_h):
    x_center = ((x1 + x2) / 2) / img_w
    y_center = ((y1 + y2) / 2) / img_h
    width = (x2 - x1) / img_w
    height = (y2 - y1) / img_h
    return f"{class_id} {x_center} {y_center} {width} {height}"

def slicing_imgs(data_annotations, state, person=0, not_person=0):
    for _, row in data_annotations.iterrows():
        img_path = os.path.join(dataset_path, row["image_name"])
        if "train_" not in row["image_name"]:
            continue
        if not os.path.exists(img_path):
            continue
        # print(row["image_name"])
        img = Image.open(img_path)
        img_w, img_h = img.size
        # person = 0
        # not_person = 0
        imgs_cnt = 0
        # Шаг для слайсинга с перекрытием
        step = int(IMG_SIZE * (1 - OVERLAP))

        for i, y in enumerate(range(0, img_h - IMG_SIZE + 1, step)):
            imgs_cnt = 0
            for j, x in enumerate(range(0, img_w - IMG_SIZE + 1, step)):
                tile = img.crop((x, y, x + IMG_SIZE, y + IMG_SIZE))
                tile_name = f"{os.path.splitext(row['image_name'])[0]}_{i}_{j}.jpg"
                if not os.path.exists(f"{main_dir}\\drone_dataset\\images\\{state}\\{tile_name}"):
                    tile.save(f"{main_dir}\\drone_dataset\\images\\{state}\\{tile_name}")
                    imgs_cnt += 1

                # Обработка аннотаций для текущего тайла
                txt_file_path = f"{main_dir}\\drone_dataset\\labels\\{state}\\{tile_name.replace('.jpg', '.txt')}"
                with open(txt_file_path, "w") as f:
                    # print(txt_file_path, "***********************")
                    x1_tile = max(int(row["x1"]) - x, 0)
                    y1_tile = max(int(row["y1"]) - y, 0)
                    x2_tile = min(int(row["x2"]) - x, IMG_SIZE)
                    y2_tile = min(int(row["y2"]) - y, IMG_SIZE)

                    # Проверка, что бокс попадает в тайл
                    if x1_tile < IMG_SIZE and y1_tile < IMG_SIZE and x2_tile > 0 and y2_tile > 0:
                        yolo_line = yolo_format(x1_tile, y1_tile, x2_tile, y2_tile, IMG_SIZE, IMG_SIZE)
                        f.write(yolo_line + "\n")
                        person += 1
                    else: not_person += 1

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


slicing_imgs(train_annotations, "train")
slicing_imgs(val_annotations, "val")
slicing_imgs(test_annotations, "test")