from google import genai



class Chat():

    def __init__(self):
        self.client = genai.Client(api_key="AIzaSyDwtxQoFE_SSwugUD42vPfsbVJfa30smNE")

        self.response = self.client.models.generate_content(
            model="gemini-3-flash-preview",
            contents="Explain how AI works in a few words",
        )

    def ask(self, quastion) -> str:
        self.response = self.client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=quastion,
        )

        return self.response.text


if __name__ == "__main__":
    bot = Chat()
    res = bot.ask("What is the colotr of the sky?")
    print(res)
