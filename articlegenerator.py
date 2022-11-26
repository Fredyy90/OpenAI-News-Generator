import openai

class ArticleGenerator:

    INTENT_DESCRIPTION = "Schreibe einen neuen Artikel für die Nachrichten, passend zu diesem Thema:"
    INTENT_TITLE = "Schreibe einen neuen Titel für diesen Artikel:"

    def __init__(self, openai_apikey):
        self.openai_apikey = openai_apikey
        openai.api_key = self.openai_apikey

    def generateImage(self, title):
        response = openai.Image.create(
            prompt=title,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return image_url

    def generateTitle(self, description):
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=self.INTENT_TITLE + description,
            temperature=0.9,
            max_tokens=3000,
            top_p=1,
            frequency_penalty=0.13,
            presence_penalty=0.3
        )
        return response.choices[0].text.strip()

    def generateDescription(self, title):
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=self.INTENT_DESCRIPTION + title,
            temperature=0.9,
            max_tokens=3000,
            top_p=1,
            frequency_penalty=0.13,
            presence_penalty=0.3
        )
        return response.choices[0].text.strip()

    def generateArticle(self, title, description):

        article = {}
        article["description"] = self.generateDescription(title)
        article["title"] = self.generateTitle(article["description"])
        article["image"] = self.generateImage(article["title"])

        return article
