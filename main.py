
import turtle
import math
import random
import time
import os
import tempfile
from tkinter import Tk, colorchooser, filedialog, messagebox

from PIL import Image


def choose_color(title, initial_color):
    """Open a colour picker dialog."""
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    selected = colorchooser.askcolor(
        color=initial_color,
        title=title,
        parent=root,
    )
    root.destroy()
    return selected[1] if selected and selected[1] else initial_color


# Select artwork colours.
heart_color = choose_color("Choose Heart Colour", "#F72568")
background_color = choose_color("Choose Background Colour", "#101018")

# Set up the drawing window.
screen = turtle.Screen()
screen.title("Turtle Art & Animated Heart")
screen.setup(width=900, height=750)
screen.bgcolor(background_color)
screen.tracer(0)

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.penup()

heart_pen = turtle.Turtle()
heart_pen.hideturtle()
heart_pen.speed(0)
heart_pen.penup()


def draw_stars(count=90):
    """Draw decorative stars in the background."""
    for _ in range(count):
        x = random.randint(-420, 420)
        y = random.randint(-330, 330)
        colour = random.choice(
            ["#FFFFFF", "#B8C7FF", "#FFD6E7", "#A8F0FF"]
        )
        pen.goto(x, y)
        pen.dot(random.choice([2, 3, 4]), colour)


def draw_text():
    """Draw the title, subtitle and footer."""
    pen.goto(0, 275)
    pen.color("#FFD166")
    pen.write(
        "A LITTLE PIECE OF ART",
        align="center",
        font=("Arial", 24, "bold"),
    )

    pen.goto(0, 230)
    pen.color("#C9B6FF")
    pen.write(
        "Made with Python Turtle",
        align="center",
        font=("Arial", 14, "normal"),
    )

    pen.goto(0, -290)
    pen.color("#FFD166")
    pen.write(
        "Made with love <3",
        align="center",
        font=("Arial", 18, "bold"),
    )


def heart_points(size, y_offset=-35, steps=240):
    """Calculate points along a mathematical heart curve."""
    points = []

    for step in range(steps + 1):
        angle = 2 * math.pi * step / steps
        x = 16 * math.sin(angle) ** 3
        y = (
            13 * math.cos(angle)
            - 5 * math.cos(2 * angle)
            - 2 * math.cos(3 * angle)
            - math.cos(4 * angle)
        )
        points.append(
            (x * size / 32, y * size / 32 + y_offset)
        )

    return points


def draw_animated_layer(size, colour, y_offset=-35):
    """Draw and fill one animated heart layer."""
    points = heart_points(size, y_offset)

    heart_pen.clear()
    heart_pen.color(colour)
    heart_pen.pensize(2)
    heart_pen.penup()
    heart_pen.goto(points[0])
    heart_pen.pendown()

    for index, point in enumerate(points[1:], start=1):
        heart_pen.goto(point)

        if index % 4 == 0:
            screen.update()
            time.sleep(0.02)

    heart_pen.penup()
    heart_pen.goto(points[0])
    heart_pen.pendown()
    heart_pen.begin_fill()

    for point in points[1:]:
        heart_pen.goto(point)

    heart_pen.goto(points[0])
    heart_pen.end_fill()
    heart_pen.penup()
    screen.update()


def draw_animated_heart():
    """Draw layered hearts using the selected colour."""
    layers = [
        (245, "#4A102A"),
        (220, "#9E1747"),
        (190, heart_color),
        (155, heart_color),
        (115, "#FFB3C6"),
    ]

    for size, colour in layers:
        draw_animated_layer(size, colour)

    heart_pen.goto(-52, 55)
    heart_pen.dot(12, "#FFFFFF")
    heart_pen.goto(-28, 42)
    heart_pen.dot(7, "#FFE6EE")
    screen.update()


def save_artwork():
    """Export the finished Turtle canvas as a PNG image."""
    filename = filedialog.asksaveasfilename(
        title="Save Artwork",
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png")],
        initialfile="turtle_heart_art.png",
    )

    if not filename:
        return

    if not filename.lower().endswith(".png"):
        filename += ".png"

    postscript_file = None

    try:
        canvas = screen.getcanvas()
        canvas.update()

        with tempfile.NamedTemporaryFile(
            suffix=".ps", delete=False
        ) as temporary_file:
            postscript_file = temporary_file.name

        canvas.postscript(
            file=postscript_file,
            colormode="color",
        )

        with Image.open(postscript_file) as source:
            source.load()
            image = source.convert("RGB")
            image.save(filename, format="PNG")

        messagebox.showinfo(
            "Artwork Saved",
            f"Your artwork was saved successfully:\n{filename}",
            parent=screen.getcanvas().winfo_toplevel(),
        )

    except Exception as error:
        messagebox.showerror(
            "Save Error",
            "Could not save the artwork.\n\n"
            f"Details: {error}\n\n"
            "On Windows, PostScript export may require Ghostscript.",
            parent=screen.getcanvas().winfo_toplevel(),
        )

    finally:
        if postscript_file and os.path.exists(postscript_file):
            try:
                os.remove(postscript_file)
            except OSError:
                pass


def main():
    draw_stars()
    draw_text()
    screen.update()

    draw_animated_heart()

    # Add a clickable Save Artwork button to the Turtle window.
    save_button = turtle.Turtle()
    save_button.hideturtle()
    save_button.penup()
    save_button.goto(0, -340)
    save_button.color("#FFFFFF")
    save_button.write(
        "SAVE ARTWORK (click here)",
        align="center",
        font=("Arial", 12, "bold"),
    )
    screen.update()

    # Make the save text clickable.
    canvas = screen.getcanvas()
    canvas.bind("<Button-1>", lambda event: save_artwork(), add="+")

    screen.mainloop()


if __name__ == "__main__":
    main()
