import tkinter as tk
import cv2
import numpy as np

from config.settings import (
    GREEN_LOWER,
    GREEN_UPPER,
    RED_LOWER_1,
    RED_LOWER_2,
    RED_UPPER_1,
    RED_UPPER_2,
)


def run_tuning_gui():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Keine Kamera erkannt")
        return

    root = tk.Tk()
    root.title("Farb-Tuning Panel")

    after_id = None
    is_running = True

    values = {
        "h_min": tk.IntVar(value=int(RED_LOWER_1[0])),
        "h_max": tk.IntVar(value=int(RED_UPPER_1[0])),
        "s_min": tk.IntVar(value=int(RED_LOWER_1[1])),
        "s_max": tk.IntVar(value=int(RED_UPPER_1[1])),
        "v_min": tk.IntVar(value=int(RED_LOWER_1[2])),
        "v_max": tk.IntVar(value=int(RED_UPPER_1[2])),
    }

    frame_controls = tk.Frame(root)
    frame_controls.pack(side="left", padx=10, pady=10)

    def set_values(lower, upper):
        values["h_min"].set(int(lower[0]))
        values["h_max"].set(int(upper[0]))
        values["s_min"].set(int(lower[1]))
        values["s_max"].set(int(upper[1]))
        values["v_min"].set(int(lower[2]))
        values["v_max"].set(int(upper[2]))

    def add_slider(label, var, min_val, max_val):
        tk.Label(frame_controls, text=label).pack(anchor="w")
        tk.Scale(
            frame_controls,
            from_=min_val,
            to=max_val,
            orient="horizontal",
            variable=var,
            length=300
        ).pack()

    add_slider("Hue min", values["h_min"], 0, 180)
    add_slider("Hue max", values["h_max"], 0, 180)
    add_slider("Saturation min", values["s_min"], 0, 255)
    add_slider("Saturation max", values["s_max"], 0, 255)
    add_slider("Value min", values["v_min"], 0, 255)
    add_slider("Value max", values["v_max"], 0, 255)

    # Presets
    tk.Button(
        frame_controls,
        text="Preset Rot 1",
        command=lambda: set_values(RED_LOWER_1, RED_UPPER_1)
    ).pack(pady=5)

    tk.Button(
        frame_controls,
        text="Preset Rot 2",
        command=lambda: set_values(RED_LOWER_2, RED_UPPER_2)
    ).pack(pady=5)

    tk.Button(
        frame_controls,
        text="Preset Gruen",
        command=lambda: set_values(GREEN_LOWER, GREEN_UPPER)
    ).pack(pady=5)

    # Werte ausgeben
    def print_values():
        print()
        print("Aktuelle Slider-HSV-Werte:")
        print(
            f"LOWER = np.array([{values['h_min'].get()}, "
            f"{values['s_min'].get()}, {values['v_min'].get()}])"
        )
        print(
            f"UPPER = np.array([{values['h_max'].get()}, "
            f"{values['s_max'].get()}, {values['v_max'].get()}])"
        )

    # Für settings übernehmen
    def save_to_settings():
        h_min = values["h_min"].get()
        h_max = values["h_max"].get()
        s_min = values["s_min"].get()
        s_max = values["s_max"].get()
        v_min = values["v_min"].get()
        v_max = values["v_max"].get()

        print()
        print("Für config/settings.py übernehmen:")
        print(f"LOWER = np.array([{h_min}, {s_min}, {v_min}])")
        print(f"UPPER = np.array([{h_max}, {s_max}, {v_max}])")

    def close_all():
        nonlocal is_running, after_id

        if not is_running:
            return

        is_running = False

        if after_id is not None:
            try:
                root.after_cancel(after_id)
            except tk.TclError:
                pass

        cap.release()
        cv2.destroyAllWindows()

        try:
            root.destroy()
        except tk.TclError:
            pass

    tk.Button(
        frame_controls,
        text="Werte ausgeben",
        command=print_values
    ).pack(pady=10)

    tk.Button(
        frame_controls,
        text="In settings übernehmen (ausgeben)",
        command=save_to_settings
    ).pack(pady=5)

    tk.Button(
        frame_controls,
        text="Beenden",
        command=close_all
    ).pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", close_all)

    def opencv_window_closed(name):
        try:
            return cv2.getWindowProperty(name, cv2.WND_PROP_VISIBLE) < 1
        except cv2.error:
            return True

    def update():
        nonlocal after_id

        if not is_running:
            return

        ret, frame = cap.read()

        if not ret:
            close_all()
            return

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Slider Maske
        slider_lower = np.array([
            values["h_min"].get(),
            values["s_min"].get(),
            values["v_min"].get()
        ])

        slider_upper = np.array([
            values["h_max"].get(),
            values["s_max"].get(),
            values["v_max"].get()
        ])

        slider_mask = cv2.inRange(hsv, slider_lower, slider_upper)
        slider_result = cv2.bitwise_and(frame, frame, mask=slider_mask)

        # Settings Maske (echte Projektwerte)
        settings_red_1 = cv2.inRange(hsv, RED_LOWER_1, RED_UPPER_1)
        settings_red_2 = cv2.inRange(hsv, RED_LOWER_2, RED_UPPER_2)
        settings_green = cv2.inRange(hsv, GREEN_LOWER, GREEN_UPPER)

        settings_mask = settings_red_1 + settings_red_2 + settings_green
        settings_result = cv2.bitwise_and(frame, frame, mask=settings_mask)

        cv2.imshow("Original", frame)

        cv2.imshow("Slider Maske", slider_mask)
        cv2.imshow("Slider Ergebnis", slider_result)

        cv2.imshow("Settings Maske Rot Gruen", settings_mask)
        cv2.imshow("Settings Ergebnis Rot Gruen", settings_result)

        key = cv2.waitKey(1)

        if key == 27:
            close_all()
            return

        window_names = [
            "Original",
            "Slider Maske",
            "Slider Ergebnis",
            "Settings Maske Rot Gruen",
            "Settings Ergebnis Rot Gruen",
        ]

        for name in window_names:
            if opencv_window_closed(name):
                close_all()
                return

        after_id = root.after(30, update)

    update()
    root.mainloop()
