def draw_data(canvas, data, color_array, canvas_width, canvas_height):
    """
    Draws the array as vertical bars on the Tkinter canvas.

    Args:
        canvas: The canvas widget to draw on.
        data (list): The list of array values to visualize.
        color_array (list): A list of colors for each element.
        canvas_width (int): Width of the canvas.
        canvas_height (int): Height of the canvas.
    """
    # Safety check – if the canvas has been destroyed, silently return
    try:
        canvas.winfo_exists()
    except Exception:
        return

    canvas.delete("all")

    if not data:
        return

    # Calculate bar dimensions
    x_width = canvas_width / (len(data) + 1)
    offset = 10
    spacing = 5

    max_val = max(data)
    normalized = [i / max_val for i in data]

    for i, height_val in enumerate(normalized):
        # Bar x-coordinates
        x0 = i * x_width + offset + spacing
        x1 = (i + 1) * x_width + offset

        # Bar y-coordinates (canvas origin is top-left)
        y0 = canvas_height - (height_val * (canvas_height - 30))
        y1 = canvas_height

        canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i], outline="black")

        # Show value above the bar (only when bars are wide enough)
        if x_width > 14:
            canvas.create_text(
                x0 + 2, y0, anchor="sw",
                text=str(data[i]), font=("Arial", 8),
            )

    # Process pending Tkinter events so the UI stays responsive
    try:
        canvas.update()
    except Exception:
        pass
