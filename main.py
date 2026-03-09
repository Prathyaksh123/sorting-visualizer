"""
main.py
-------
Entry point for the Sorting Algorithm Visualizer.
Sets up the Tkinter GUI and wires up event handlers.

Features:
  • 6 sorting algorithms selectable from a dropdown
  • Generate Array button to create a new random dataset
  • Custom array input field (comma-separated values)
  • Start Sorting and Stop buttons to control execution
  • Speed and Array-size sliders
  • Elapsed-time display
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time

from utils import generate_array
from visualizer import draw_data
from sorting_algorithms import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    heap_sort,
)


class SortingVisualizer:
    """Main application class."""

    # Map display names → sorting functions
    ALGORITHMS = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort,
        "Heap Sort": heap_sort,
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry("900x700")
        self.root.config(bg="#f0f0f0")
        self.root.resizable(False, False)

        self.data = []
        self.canvas_width = 860
        self.canvas_height = 400
        self.is_sorting = False           # True while a sort is running
        self.stop_requested = False       # Set to True when user clicks Stop

        self._build_ui()
        self.generate()                   # Start with a random array on screen

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self):
        """Create all widgets."""

        # ── Control frame (top section) ──────────────────────────────
        ctrl = tk.Frame(self.root, bg="#e0e0e0", bd=2, relief=tk.GROOVE)
        ctrl.pack(fill=tk.X, padx=10, pady=(10, 5))

        # Row 0 – Algorithm selector & buttons
        tk.Label(ctrl, text="Algorithm:", bg="#e0e0e0",
                 font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.alg_menu = ttk.Combobox(
            ctrl,
            values=list(self.ALGORITHMS.keys()),
            state="readonly",
            width=22,
        )
        self.alg_menu.grid(row=0, column=1, padx=5, pady=5)
        self.alg_menu.current(0)

        self.btn_generate = tk.Button(
            ctrl, text="Generate Array", command=self.generate,
            bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
            activebackground="#1976D2", cursor="hand2",
        )
        self.btn_generate.grid(row=0, column=2, padx=10, pady=5)

        self.btn_start = tk.Button(
            ctrl, text="▶  Start Sorting", command=self.start_sort,
            bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
            activebackground="#388E3C", cursor="hand2",
        )
        self.btn_start.grid(row=0, column=3, padx=5, pady=5)

        self.btn_stop = tk.Button(
            ctrl, text="■  Stop", command=self.stop_sort,
            bg="#f44336", fg="white", font=("Arial", 10, "bold"),
            activebackground="#D32F2F", cursor="hand2",
            state=tk.DISABLED,
        )
        self.btn_stop.grid(row=0, column=4, padx=5, pady=5)

        # Row 1 – Sliders
        tk.Label(ctrl, text="Speed (delay):", bg="#e0e0e0",
                 font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.speed_slider = tk.Scale(
            ctrl, from_=0.01, to=2.0, length=180,
            digits=3, resolution=0.01, orient=tk.HORIZONTAL,
            bg="#e0e0e0", highlightthickness=0,
        )
        self.speed_slider.grid(row=1, column=1, padx=5, pady=5)
        self.speed_slider.set(0.05)

        tk.Label(ctrl, text="Array size:", bg="#e0e0e0",
                 font=("Arial", 10)).grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)

        self.size_slider = tk.Scale(
            ctrl, from_=5, to=80, resolution=1, orient=tk.HORIZONTAL,
            length=180, bg="#e0e0e0", highlightthickness=0,
        )
        self.size_slider.grid(row=1, column=3, columnspan=2, padx=5, pady=5, sticky=tk.W)
        self.size_slider.set(30)

        # Row 2 – Custom array input
        tk.Label(ctrl, text="Custom array:", bg="#e0e0e0",
                 font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        self.array_entry = tk.Entry(ctrl, width=45, font=("Arial", 10))
        self.array_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        self.array_entry.insert(0, "e.g.  34, 12, 90, 5, 67")
        # Clear placeholder text on first click
        self.array_entry.bind("<FocusIn>", self._clear_placeholder)

        self.btn_load = tk.Button(
            ctrl, text="Load Array", command=self.load_custom_array,
            bg="#FF9800", fg="white", font=("Arial", 10, "bold"),
            activebackground="#F57C00", cursor="hand2",
        )
        self.btn_load.grid(row=2, column=3, padx=5, pady=5)

        self.error_label = tk.Label(ctrl, text="", bg="#e0e0e0",
                                    font=("Arial", 9), fg="red")
        self.error_label.grid(row=2, column=4, padx=5, pady=5)

        # ── Status bar (time display) ────────────────────────────────
        status = tk.Frame(self.root, bg="#e0e0e0")
        status.pack(fill=tk.X, padx=10, pady=(0, 5))

        self.time_label = tk.Label(
            status, text="Time: 0.000 s", bg="#e0e0e0",
            font=("Consolas", 11, "bold"), fg="#333",
        )
        self.time_label.pack(side=tk.LEFT, padx=10)

        self.status_label = tk.Label(
            status, text="Ready", bg="#e0e0e0",
            font=("Arial", 10, "italic"), fg="#555",
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)

        # ── Legend (color meanings) ──────────────────────────────────
        legend = tk.Frame(self.root, bg="#f0f0f0")
        legend.pack(fill=tk.X, padx=10, pady=(0, 3))

        for color, label in [("blue", "Normal"), ("yellow", "Comparing"),
                              ("red", "Swapping"), ("green", "Sorted")]:
            tk.Canvas(legend, width=16, height=16, bg=color,
                      highlightthickness=1, highlightbackground="black"
                      ).pack(side=tk.LEFT, padx=(10, 2))
            tk.Label(legend, text=label, bg="#f0f0f0",
                     font=("Arial", 9)).pack(side=tk.LEFT, padx=(0, 8))

        # ── Canvas ───────────────────────────────────────────────────
        self.canvas = tk.Canvas(
            self.root, width=self.canvas_width, height=self.canvas_height,
            bg="white", bd=2, relief=tk.SUNKEN,
        )
        self.canvas.pack(padx=10, pady=(0, 10))

    # ------------------------------------------------------------------
    # Drawing wrapper
    # ------------------------------------------------------------------

    def draw(self, data, color_array):
        """Pass canvas info to the visualizer module."""
        draw_data(self.canvas, data, color_array,
                  self.canvas_width, self.canvas_height)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def generate(self):
        """Generate a new random array and draw it."""
        if self.is_sorting:
            return                       # Don't allow regeneration mid-sort

        size = int(self.size_slider.get())
        self.data = generate_array(size, 10, 150)
        self.draw(self.data, ['blue'] * len(self.data))
        if self.time_label.winfo_exists():
            self.time_label.config(text="Time: 0.000 s")
            self.status_label.config(text="Ready")
            self.error_label.config(text="")

    def load_custom_array(self):
        """Parse the user's comma-separated input and load it as the array."""
        if self.is_sorting:
            return

        raw = self.array_entry.get().strip()
        if not raw or raw.startswith("e.g."):
            if self.error_label.winfo_exists():
                self.error_label.config(text="Enter numbers first!")
            return

        try:
            # Split by commas, strip whitespace, convert to integers
            values = [int(v.strip()) for v in raw.split(",") if v.strip()]
        except ValueError:
            if self.error_label.winfo_exists():
                self.error_label.config(text="Invalid input! Use integers only.")
            return

        if len(values) < 2:
            if self.error_label.winfo_exists():
                self.error_label.config(text="Enter at least 2 numbers.")
            return

        if any(v <= 0 for v in values):
            if self.error_label.winfo_exists():
                self.error_label.config(text="All values must be > 0.")
            return

        self.data = values
        self.draw(self.data, ['blue'] * len(self.data))
        if self.time_label.winfo_exists():
            self.time_label.config(text="Time: 0.000 s")
            self.status_label.config(text=f"Custom array loaded ({len(values)} elements)")
            self.error_label.config(text="")

    def _clear_placeholder(self, event):
        """Remove placeholder text when the entry is clicked."""
        if self.array_entry.get().startswith("e.g."):
            self.array_entry.delete(0, tk.END)

    def start_sort(self):
        """Launch the selected sorting algorithm."""
        if self.is_sorting:
            return                       # Prevent double-start

        alg_name = self.alg_menu.get()
        sort_func = self.ALGORITHMS.get(alg_name)
        if sort_func is None:
            return

        delay = self.speed_slider.get()

        # Lock the UI controls while sorting
        self.is_sorting = True
        self.stop_requested = False
        if not self.btn_start.winfo_exists():
            return
            
        self.btn_start.config(state=tk.DISABLED)
        self.btn_generate.config(state=tk.DISABLED)
        self.btn_load.config(state=tk.DISABLED)
        self.array_entry.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.status_label.config(text=f"Sorting with {alg_name}…")

        # Record start time
        t0 = time.perf_counter()

        # Run the algorithm (blocks the main thread but canvas.update()
        # inside draw_data keeps the GUI responsive)
        sort_func(self.data, self.draw, delay, lambda: self.stop_requested)

        # Record end time
        elapsed = time.perf_counter() - t0

        # Safely attempt to update UI incase window was destroyed
        try:
            if self.time_label.winfo_exists():
                self.time_label.config(text=f"Time: {elapsed:.3f} s")

                if self.stop_requested:
                    self.status_label.config(text="Stopped")
                else:
                    self.status_label.config(text="Done ✓")

                # Unlock the UI
                self.is_sorting = False
                self.btn_start.config(state=tk.NORMAL)
                self.btn_generate.config(state=tk.NORMAL)
                self.btn_load.config(state=tk.NORMAL)
                self.array_entry.config(state=tk.NORMAL)
                self.btn_stop.config(state=tk.DISABLED)
        except Exception:
            pass

    def stop_sort(self):
        """Signal the running algorithm to stop."""
        self.stop_requested = True


# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
