import os
import numpy as np
from pathlib import Path
import cv2
import supervision as sv
from ultralytics import YOLO

detector = YOLO('yolo11m.pt')
tracker = sv.ByteTrack()
box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

def callback(frame: np.ndarray, _: int) -> np.ndarray:
    """
        Обработчик кадров для детекции и трекинга людей.

        Args:
        frame (np.ndarray): Входной кадр видео.
        _: Номер кадра (не используется).

        Returns: 
        np.ndarray: Аннотированный кадр 
        с детекциями и трекингом людей.
    """
    results = detector(frame)[0]
    
    # Преобразовать результаты детекции в формат Supervision
    detections = sv.Detections.from_ultralytics(results)

    # Выбрать только детекции людей (class_id == 0)
    person_mask = detections.class_id == 0
    detections = detections[person_mask]
    
    # Обновить трекер с новыми детекциями
    detections = tracker.update_with_detections(detections)

    labels = [
        f"person #{tracker_id} {confidence:.2f}"
        for tracker_id, confidence
        in zip(detections.tracker_id, detections.confidence)
    ]

    # Аннотировать кадр с помощью боксов и меток
    annotated_frame = box_annotator.annotate(
        scene=frame.copy(),
        detections=detections
    )
    annotated_frame = label_annotator.annotate(
        scene=annotated_frame,
        detections=detections,
        labels=labels
    )

    return annotated_frame


def track_video(src_path, trgt_path):
    sv.process_video(
        source_path=src_path,
        target_path=trgt_path,
        callback=callback
    )


if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent

    source_path = BASE_DIR / "assets" / "crowd.mp4"
    target_path = BASE_DIR / "outputs" / "crowd_annotated.mp4"

    track_video(
        src_path=str(source_path),
        trgt_path=str(target_path)
    )
    print("Processing complete. Annotated video saved as 'crowd_annotated.mp4'.")
