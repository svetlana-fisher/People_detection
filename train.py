from ultralytics import YOLO


model = YOLO("yolov8m.pt")

def main():
    results = model.train(
        data="data.yaml",
        imgsz=832,
        epochs=1000,
        batch=15,
        patience=50,
        device=0,
        lr0=0.01,
        cos_lr=True,
        augment=True,
        optimizer="auto",
        seed=42,
        # cache=True,
        name="yolov8m_drone_human",
        val=True,
        pretrained = "/home/jovyan/work/people_detection/yolov8m.pt"
    )

    metrics = model.val()
    print(f"mAP50: {metrics.box.map50}")
    print(f"Recall: {metrics.box.r}")
    print(f"Precision: {metrics.box.p}")

if __name__ == '__main__':
    main()