import npyscreen
import random

class RandomNumberGeneratorApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', MainForm)

class MainForm(npyscreen.Form):
    def create(self):
        self.add(npyscreen.FixedText, value="Random Number Generator", editable=False)
        self.random_number_display = self.add(npyscreen.TitleText, name="Random Number:", editable=False)
        self.generate_button = self.add(npyscreen.ButtonPress, name="Generate Random Number")
        self.generate_button.whenPressed = self.generate_random_number

    def generate_random_number(self):
        random_number = random.randint(1, 100)
        self.random_number_display.value = str(random_number)
        self.random_number_display.display()

if __name__ == '__main__':
    app = RandomNumberGeneratorApp()
    app.run()