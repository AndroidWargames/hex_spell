class BaseGame:
    def wait_for_input(self):
        i = input(self.input_string())
        if i == 'h':
            self.help()
        elif i == "H":
            self.hint()
        elif i == "x":
            return
        else:
            self.guess(i)
        self.wait_for_input()


    def save_game(self):
        with open(f"saved_games/{self.first_word}.redgm", "w+") as f:
            f.write(self.first_word + "\n")
            for word in self.found_words():
                f.write(word + "\n")
