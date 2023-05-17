from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Arial", 24, "normal")


class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        with open("data.txt", mode="r") as file:
            self.highscore = int(file.read())
        self.goto(0, 270)
        self.color("white")
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(
            f"Score:{self.score} High score:{self.highscore}",
            align=ALIGNMENT,
            font=FONT,
        )

    def reset_scoreboard(self):
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.update_scoreboard()

    def increase_score(self):
        self.score += 1
        # To clear previous screen, previous score
        self.update_scoreboard()
        if self.score > self.highscore:
            with open(
                "data.txt", mode="w"
            ) as file:
                file.write(str(self.score))
