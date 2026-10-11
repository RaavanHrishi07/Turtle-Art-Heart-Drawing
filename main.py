
import turtle
import math
import random


# Window setup
screen = turtle.Screen()
screen.title("Turtle Art & Heart Drawing")
screen.setup(width=900, height=750)
screen.bgcolor("#101018")
screen.tracer(0)

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.penup()


def draw_heart(size, color, y_offset=0):
    """Draw a filled heart using a parametric curve."""
    points = []

    for step in range(361):
        angle = math.radians(step)
        x = 16 * math.sin(angle) ** 3
        y = (
            13 * math.cos(angle)
            - 5 * math.cos(2 * angle)
            - 2 * math.cos(3 * angle)
            - math.cos(4 * angle)
        )
        points.append((x * size / 32, y * size / 32 + y_offset))

    pen.color(color)
    pen.penup()
    pen.goto(points[0])
    pen.pendown()
    pen.begin_fill()

    for point in points[1:]:
        pen.goto(point)

    pen.goto(points[0])
    pen.end_fill()
    pen.penup()


def draw_stars(count=90):
    """Scatter small stars around the canvas."""
    pen.color("#FFFFFF")

    for _ in range(count):
        x = random.randint(-420, 420)
        y = random.randint(-330, 330)
        pen.goto(x, y)
        pen.dot(random.choice([2, 3, 4]), random.choice(
            ["#FFFFFF", "#B8C7FF", "#FFD6E7", "#A8F0FF"]
        ))


def draw_text():
    """Write a colourful title and subtitle."""
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


def draw_heart_art():
    """Layer hearts to create a colourful glowing-style effect."""
    draw_heart(245, "#4A102A", -35)
    draw_heart(220, "#9E1747", -35)
    draw_heart(190, "#F72568", -35)
    draw_heart(155, "#FF6B8A", -35)
    draw_heart(115, "#FFB3C6", -35)

    # Small decorative highlight
    pen.goto(-52, 55)
    pen.color("#FFFFFF")
    pen.dot(12)

    pen.goto(-28, 42)
    pen.color("#FFE6EE")
    pen.dot(7)


def draw_bottom_message():
    pen.goto(0, -260)
    pen.color("#FFD166")
    pen.write(
        "Made with love  <3",
        align="center",
        font=("Arial", 18, "bold"),
    )


def main():
    draw_stars()
    draw_text()
    draw_heart_art()
    draw_bottom_message()
    screen.update()
    screen.mainloop()


if __name__ == "__main__":
    main()
