from pathlib import Path
from ultralytics import YOLO


if __name__ == "__main__":

    # Создание кроссплатформенных путей к файлам с помощью pathlib
    BASE_DIR = Path(__file__).resolve().parent
    source_path = BASE_DIR / "assets" / "crowd.mp4"
    output_path = BASE_DIR / "outputs"

    output_path.parent.mkdir(exist_ok=True)

    # Инициализация детектора YOLO и запуск трекинга
    detector = YOLO('yolo11m.pt')
    
    res = detector.track(
        source_path, 
        conf=0.4, 
        iou=0.4, 
        classes=[0], # Класс 0 соответствует людям
        save=True, 
        project=output_path,
        line_width=2 # Толщина линий для аннотаций
    )

    print("Processing complete. Annotated video saved as 'crowd_tracked.mp4'.")
