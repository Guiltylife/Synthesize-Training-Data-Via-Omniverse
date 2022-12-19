import fiftyone as fo


if __name__ == "__main__":
    name = "COCO"
    dataset_dir = "./datasets/COCOData"

    # Create the dataset
    dataset = fo.Dataset.from_dir(
        dataset_dir=dataset_dir,
        dataset_type=fo.types.COCODetectionDataset,
        name=name,
    )

    session = fo.launch_app(dataset, desktop=True)
    session.wait()

    # name = "YOLO"
    # dataset_dir = "./datasets/YOLOData"
    #
    # # Create the dataset
    # dataset = fo.Dataset.from_dir(
    #     dataset_dir=dataset_dir,
    #     dataset_type=fo.types.YOLOv5Dataset,
    #     name=name,
    # )
    #
    # session = fo.launch_app(dataset, desktop=True)
    # session.wait()
