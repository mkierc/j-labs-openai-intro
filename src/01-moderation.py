from openai import OpenAI

client = OpenAI(api_key=open('openai-api.key').readline())

topic_list = [
    "Python to gówniany język, dla idiotów, którzy nie umieją stawiać średników",
    "Zabiję kiedyś tych wszystkich lemingów, którzy nie potrafią szybko ruszyć ze świateł",
    "Kiedy oglądam polską piłkę nożną, to mam ochotę się zabić",

    # "Python is a shitty language, for idiots who can't use semicolons",
    # "One day I'm going to kill all those lemmings, who can't quickly move from traffic lights",
    # "When I'm watching Polish football, I want to kill myself",
]

for line in topic_list:
    moderation = client.moderations.create(input=line, model='text-moderation-latest')

    filtered_categories = [name for name, value in moderation.results[0].categories if value is True]
    print('flagged:', moderation.results[0].flagged, ', categories:', filtered_categories)
    # print(moderation.results[0])

