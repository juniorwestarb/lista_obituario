import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import matplotlib.pyplot as plt
from datetime import *
from gtts import gTTS
from playsound import playsound

r_idade = "[0-9]{1,3}"
r_Data = r'\d{2}[-/]\d{2}[-/]\d{4}'

def main():
    url = "https://www.obituarioriomafra.com.br/"
    falecimentos = []
    nomes_falecidos = []
    frase_nomes = ""
    response = requests.get(url)
    html = response.content.decode(encoding="iso-8859-1")
    conteudo = BeautifulSoup(html, "html.parser")
    mortos = conteudo.find_all('div', class_='obitos')

    for morto in mortos:
        falecido = {}
        spans = morto.find_all('span')
        for s in spans:
            if s.text.startswith("Data do Falecimento:"):
                f = re.compile(r_Data)
                falecido["data_falecimento"] = f.findall(s.text)[0] if len(f.findall(s.text)) > 0 else "0"

            if s.text.startswith("Idade:"):
                i = re.compile(r_idade)
                falecido["idade"] = int(i.findall(s.text)[0]) if len(i.findall(s.text)) > 0 else 0

            if s.text.startswith("Dia:"):
                e = re.compile(r_Data)
                falecido["data_enterro"] = e.findall(s.text)[0] if len(e.findall(s.text)) > 0 else "0"

        nome = morto.find('h2', class_="tittle").text
        falecido["nome"] = nome

        if datetime.strptime(falecido["data_falecimento"], '%d/%m/%Y').date() < (datetime.today().date()-timedelta(100)):
            continue
        falecimentos.append(falecido)
    
    pd.set_option('display.expand_frame_repr', False)

    if len(falecimentos) > 0:
        for f in falecimentos:
            frase_nomes = frase_nomes + f["nome"] + " com " + str(f["idade"]) + " anos."
            
        frase_obituario = "Estamos comunicando o falecimento das seguintes pessoas: " + frase_nomes
        print(frase_obituario)
        cria_audio(frase_obituario)

        df = pd.DataFrame(data=falecimentos)
        apresentacao(df)


def apresentacao(df):
    print(df.head())

    df[['idade']].plot(kind='hist',bins=[0,20,40,60,80,100],rwidth=0.8)

    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()


def cria_audio(frase):
    tts = gTTS(frase,lang='pt-br')
    tts.save('audios/falecimento.mp3')
    playsound('audios/falecimento.mp3')


if __name__ == '__main__':
    main()
