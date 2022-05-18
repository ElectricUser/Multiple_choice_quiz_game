class Question:
    def __init__(self, question_text, answers, correct_answer, points):
        self.question_text = question_text
        self.answers = answers
        self.correct_answer = correct_answer
        self.points = points

    def get_question_text(self):
        return self.question_text

    def get_answers(self):
        return self.answers

    def get_correct_answer(self):
        return self.correct_answer

    def get_points(self):
        return self.points

    def get_answers_str(self):
        answers_string = ""
        for a in self.answers:
            answers_string = answers_string + " " + a
        return answers_string

    def __str__(self):
        attributes = f"\n Question: {self.question_text}, \n Answers: {self.get_answers_str()}, \n Correct answer: {self.correct_answer}, \n Points: {self.points}"
        return attributes
