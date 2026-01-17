from pathlib import Path
from typing import Tuple
import cv2
import numpy as np
from ultralytics import YOLO


def load_video(video_path: Path) -> Tuple[cv2.VideoCapture, int, int, float]:
    """
    Загружает видео.

    Args:
        video_path (Path): Путь к входному видео.

    Returns:
        Tuple, состоящий из:
        - cv2.VideoCapture объект (cv2.VideoCapture)
        - ширина кадра (int)
        - высота кадра (int)
        - FPS (float)
    """
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise RuntimeError(f"Невозможно открыть видеофайл: {video_path}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    return cap, width, height, fps


def create_video_writer(
    output_path: Path,
    width: int,
    height: int,
    fps: float
) -> cv2.VideoWriter:
    """
    Создает VideoWriter объект для сохранения выходного видео.

    Args:
        output_path (Path): Путь к выходному видео.
        width (int): Ширина кадра.
        height (int): Высота кадра.
        fps (float): FPS.

    Returns:
        cv2.VideoWriter объект.
    """
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    return cv2.VideoWriter(
        str(output_path),
        fourcc,
        fps,
        (width, height)
    )


def draw_detections(
    frame: np.ndarray,
    boxes: np.ndarray,
    scores: np.ndarray,
    color: Tuple[int, int, int] = (255, 0, 0) # Синий цвет
) -> np.ndarray:
    """
    Отрисовывает bounding boxes и labels на кадре.

    Args:
        frame (np.ndarray): Оригинальный кадр видео.
        boxes (np.ndarray): Bounding boxes в xyxy формате.
        scores (np.ndarray): Confidence scores.
        color (Tuple[int, int, int]): Цвет для bounding boxes.

    Returns:
        np.ndarray: Аннотированный кадр.
    """
    for box, score in zip(boxes, scores):
        # Преобразуем координаты в целые числа
        x1, y1, x2, y2 = map(int, box)

        # Рисуем bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness=2)
        
        # Формируем label с confidence score
        label = f"person {score:.2f}"
        
        # Получаем размер текста для отрисовки прямоугольника-фона
        (text_width, text_height), _ = cv2.getTextSize(
            label,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,  # Масштаб шрифта
            2     # Толщина шрифта
        )

        # Координаты прямоугольника-фона
        padding = 4
        x_min = x1
        y_min = y1 - text_height - padding * 2
        x_max = x1 + text_width + padding * 2
        y_max = y1

        # Если текст вылезает за верх кадра
        if y_min < 0:
            y_min = y1
            y_max = y1 + text_height + padding * 2

        # Рисуем прямоугольник-фон
        cv2.rectangle(
            frame,
            (x_min, y_min),
            (x_max, y_max),
            color,
            -1  # заливка
        )

        # Рисуем текст поверх прямоугольника-фона
        cv2.putText(
            frame,
            label,
            (x1, y1 - 8),  # Позиция текста выше bbox'а
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,           # Масштаб шрифта 
            (255,255,255), # Цвет текста
            2,             # Толщина шрифта
            cv2.LINE_AA    # Cглаживание шрифта
        )

    return frame


def process_video(
    input_path: Path,
    output_path: Path,
    model_path: str = "yolo11m.pt",
    conf_threshold: float = 0.4
) -> None:
    """
    Осуществляет детекцию людей на видео и сохраняет результат.

    Args:
        input_path (Path): Путь к входному видео.
        output_path (Path): Путь для сохранения аннотированного видео.
        model_path (str): Путь к весам модели YOLO.
        conf_threshold (float): Confidence threshold для детекций.
    """
    # Загрузка модели YOLO
    model = YOLO(model_path)
    # Загрузка видео
    cap, width, height, fps = load_video(input_path)
    # Создание VideoWriter для сохранения результата
    writer = create_video_writer(output_path, width, height, fps)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # YOLO инференс (class 0 = person)
        results = model(frame, conf=conf_threshold, classes=[0])[0]

        if results.boxes is not None:
            # Извлечение bounding boxes и confidence scores
            boxes = results.boxes.xyxy.cpu().numpy()
            scores = results.boxes.conf.cpu().numpy()
            frame = draw_detections(frame, boxes, scores)

        writer.write(frame)

    cap.release()
    writer.release()


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent

    # Создание кроссплатформенных путей к входному и выходному видео
    input_video = BASE_DIR / "assets" / "crowd.mp4"
    output_video = BASE_DIR / "outputs" / "crowd_annotated.mp4"

    output_video.parent.mkdir(exist_ok=True)

    process_video(
        input_path=input_video,
        output_path=output_video
    )

    print("Processing finished. Annotated video saved as crowd_annotated.mp4.")
