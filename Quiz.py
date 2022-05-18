# module imports
import pprint
import Question
import Player


class Quiz:
    def __init__(self):
        self.player_name = ""
        self.questions = []
        self.players = []

        # Constant message strings
        self.START_MESSAGE = "\nWelcome to the quiz! Good luck!"
        self.QUIT_WARNING = "\nYou may quit the game any time you want by typping the word \"quit\""
        self.END_OF_GAME_POINTS = "\nYour final score was {} points"
        self.WRONG_ANSWER = "\nWRONG!"
        self.RIGHT_ANSWER = "\nCORRECT!"
        self.END_OF_GAME = "\nThank you for playing!\n"
        self.NUMBER_OF_PLAYERS = "\nHow many people will be playing > "
        self.NAME_OF_PLAYER = "\nWhat's your name > "
        self.PLAYER_X_TURN = "\nPlayer {} turn\n"
        self.WINNER = "\nCongratulations {} you won with a total of {} points!\n"

    def import_questions(self, filename):
        file_dump = []
        with open(f"{filename}.txt", "r", encoding="utf-8") as f:
            file_dump = f.readlines()
        return file_dump

    def load_questions_answers(self, dump_data):
        cleaner_data = dump_data.copy()
        try:
            while True:
                cleaner_data.remove("\n")
        except ValueError:
            pass

        # counters
        counter_questions = 0
        couter_points = 5

        # data structures
        questions = []
        points = []
        answers = []
        for index, data in enumerate(cleaner_data):
            if index == counter_questions:
                questions.append(data)
                counter_questions = counter_questions + 6
            elif index == couter_points:
                points.append(data)
                couter_points = couter_points + 6
            else:
                answers.append(data)

        self.load_game(self.clear_questions(questions), self.clear_answers(
            answers), self.clear_correct_answers(answers), self.clear_points(points))

    def clear_points(self, points):
        int_points = []
        for p in points:
            clear_point = p.replace("\n", "")
            clear_point = clear_point.strip()
            int_points.append(int(clear_point[len(clear_point) - 1]))
        return int_points

    def clear_questions(self, questions_list):
        questions = []
        for question in questions_list:
            clear_question = question.replace('\n', "")
            clear_question = clear_question.strip()
            questions.append(clear_question)

        return questions

    def clear_correct_answers(self, answers_list):
        correct_answers = []
        for answer in answers_list:
            if "[CORRECT]" in answer:
                cleanned_answer = answer.replace("[CORRECT]", "")
                cleanned_answer = cleanned_answer.replace('\n', "")
                cleanned_answer = cleanned_answer.strip()
                correct_answers.append(cleanned_answer)

        return correct_answers

    def clear_answers(self, answers_list):
        answers_no_clues = []  # answers without clues

        for answer in answers_list:
            if "[CORRECT]" in answer:
                cleanned_answer = answer.replace("[CORRECT]", "")
                cleanned_answer = cleanned_answer.replace('\n', "")
                cleanned_answer = cleanned_answer.strip()
                answers_no_clues.append(cleanned_answer)
            else:
                cleanned_answer = answer.replace('\n', "")
                cleanned_answer = cleanned_answer.strip()
                answers_no_clues.append(cleanned_answer)

        return answers_no_clues

    def load_game(self, clear_questions, clear_answers, clear_correct_answers, clear_points):
        index = 0  # +1
        counter_answer1 = 0  # +4
        counter_answer2 = 4

        questions = clear_questions
        answers = clear_answers
        correct_answers = clear_correct_answers
        points = clear_points

        # gives the number of questions since every question has 4 possible answers
        questions_left = len(answers) / 4
        try:
            while questions_left != 0:

                self.questions.append(Question.Question(
                    questions[index], answers[counter_answer1:counter_answer2], correct_answers[index], points[index]))
                index += 1
                counter_answer1 += 4
                counter_answer2 += 4

                questions_left -= 1
        except:
            return print("There was an error loading the questions")
        return print("Questions loaded successfully")

    def ask_question(self, index_question):
        while True:
            question = self.questions[index_question]  # Question object
            answers = ""
            print(question.get_question_text())

            for answer in question.get_answers():
                answers += "\n" + answer

            print(answers)
            answer = input("\nChoose the correct option > ")
            if answer.lower() not in ['a', 'b', 'c', 'd']:
                print("\nWARNING! You need to enter a valid option (a, b, c, d)\n")
            else:
                break
        return answer

    def check_result(self, index_question, answer):
        question = self.questions[index_question]
        correct_answer = question.get_correct_answer()[0]
        points = question.get_points()

        # if the user answers correctly it returns the number of
        if answer[0] == correct_answer:
            return points
        else:
            return 0

    def start_game(self):
        print(self.START_MESSAGE)
        self.ask_player_input()
        print(self.QUIT_WARNING)
        number_of_questions = len(self.questions)
        total_players = len(self.players)
        current_player_index = 0
        while number_of_questions != 0:
            for index, value in enumerate(self.questions):
                current_player = self.players[current_player_index]
                print(
                    f"\n{current_player.get_name()} has {current_player.get_points()} points")
                answer = self.ask_question(index)
                if answer == "quit":
                    break
                points = self.check_result(index, answer)
                if points != 0:
                    print(self.RIGHT_ANSWER)
                    print(f"\n +{points} POINTS!\n")
                else:
                    print(self.WRONG_ANSWER)
                self.players[current_player_index].add_points(points)
                current_player_index += 1
                # when the index of the current_player is equal to the len(self.players) means
                if current_player_index == total_players:
                    current_player_index = 0
                number_of_questions -= 1
        winner = self.quiz_winner()
        print(self.WINNER.format(winner.get_name(), winner.get_points()))
        print(self.all_players_points())
        self.export_file_results()
        print(self.END_OF_GAME)
        return quit()

    def create_player(self, player_name):
        try:
            self.players.append(Player.Player(player_name))
            print("Player created")
        except:
            print("There was an error creating the player")

    def ask_player_input(self):
        while True:
            try:
                number_of_players = int(input(self.NUMBER_OF_PLAYERS))
                while number_of_players != 0:
                    player_name = input(self.NAME_OF_PLAYER)
                    self.create_player(player_name)
                    number_of_players -= 1
            except ValueError as err:
                print(err)
                print("\nWARNING! Please enter a valid number!\n")
            else:
                break

    def quiz_winner(self):
        players = self.players
        highest_points_player = Player.Player("Random")
        for player in players:
            if player.get_points() > highest_points_player.get_points():
                highest_points_player = player
        return highest_points_player

    def all_players_points(self):
        result = "\nFINAL RESULT\n"
        sorted_players = sorted(
            self.players, key=lambda x: x.points, reverse=True)
        for player in sorted_players:
            result += f"{player.get_name()} > {player.get_points()} points\n"
        return result

    def export_file_results(self):
        players = self.players
        players_sorted_by_score = sorted(
            players, key=lambda x: x.points, reverse=True)
        with open('results.txt', "w", encoding="utf-8") as f:
            f.write("Final results of the quiz\n")
            f.write("\n{:<8} {:<8} {:<8}\n".format(
                "Position", "Player", "Points"))
            for index, player in enumerate(players_sorted_by_score):
                f.write("{:<8} {:<8} {:<8}\n".format(
                    (index + 1), player.get_name(), player.get_points()))


quiz1 = Quiz()
quiz1.load_questions_answers(quiz1.import_questions("questions"))
quiz1.start_game()
