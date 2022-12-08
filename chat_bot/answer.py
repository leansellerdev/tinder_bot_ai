import requests
import time
counter = 0

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json',
    'Server': 'istio-envoy',
    'Accept-encoding': 'gzip, deflate, br',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.43',
    'Content-Type': 'application/json',
    'Origin': 'https://russiannlp.github.io',
    'Referer': 'https://russiannlp.github.io/',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Accept-Language': 'en-US,en;q=0.9,es-AR;q=0.8,es;q=0.7',
}


def answer_questions(question):
    question = "Парень:" + question + "\nДевушка:"
    response = requests.post("https://api.aicloud.sbercloud.ru/public/v1/public_inference/gpt3/predict",
                             json={"text": question}, headers=headers)
    answer = ""
    if response.status_code == 200:
        try:
            answer = response.json()['predictions'].split('\n')
            new_answer = answer[1]
            new_answer = new_answer.split(':')[1]
            return new_answer
        except:
            print("упс")
    return answer


# def generate_voice(text):
#     var = gTTS(text=text, lang='ru')
#     global counter
#     var.save(f'speech{counter}.mp3')
#     from pygame import mixer  # Load the popular external library

#     mixer.init()
#     mixer.music.load(f'speech{counter}.mp3')
#     mixer.music.play()
#     while mixer.music.get_busy():  # wait for music to finish playing
#         time.sleep(1)
#     counter += 1

    # mixer.music.stop()


# for i in range(10):
#     q = answer_questions(input())
#     print(q)
    # generate_voice(q)
