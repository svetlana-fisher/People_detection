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

def slicing_imgs(data_annotations, state):
    for _, row in data_annotations.iterrows():
        img_path = os.path.join(dataset_path, row["image_name"])
        if "train_" not in row["image_name"]:
            continue
        # print(row["image_name"])
        img = Image.open(img_path)
        # img_w, img_h = img.size
        img.save(f"{main_dir}\\drone_dataset\\images\\{state}\\{row["image_name"]}")
        # Шаг для слайсинга с перекрытием

        txt_file_path = f"{main_dir}\\drone_dataset\\labels\\{state}\\{row["image_name"].replace('.jpg', '.txt')}"
        # print(txt_file_path)
        if not os.path.exists(txt_file_path):
            with open(txt_file_path, "w") as f:
                # print("WWWWWWWWWWWW")
                # yolo_line = f"{row["x1"]} {row["y1"]} {row["x2"]} {row["y2"]}"
                yolo_line = f"{row["x1"]} {row["y1"]} {row["x2"]} {row["y2"]}"
                f.write(yolo_line + "\n")
        else:
            with open(txt_file_path, "a") as f:
                # print("AAAAAAAAAAAAAAAAA")
                yolo_line = f"{row["x1"]} {row["y1"]} {row["x2"]} {row["y2"]}"
                # yolo_line = yolo_format(int(row["x1"]), int(row["y1"]), int(row["x2"]), int(row["y2"]), IMG_SIZE, IMG_SIZE)
                f.write(yolo_line + "\n")

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


#
annotations = pd.read_csv(csv_path, header=None, names=["image_name", "img_w", "img_h", "class", "x1", "y1", "x2", "y2"])


test_annotations = pd.read_csv(f"{main_dir}\\test_list.csv", header=None, names=["image_name", "img_w", "img_h", "class", "x1", "y1", "x2", "y2"])
test_annotations = test_annotations.sort_values(by="image_name", ascending=True)


slicing_imgs(test_annotations, "test")