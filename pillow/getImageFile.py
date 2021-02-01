import cv2
import PIL
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import os
import time
from openpyxl import load_workbook
import imageio
import re
from gtts import gTTS
from playsound import playsound
from moviepy.editor import *
import html
from google.cloud import texttospeech

import ffmpeg
import natsort

#data_only=Ture로 해줘야 수식이 아닌 값으로 받아온다.
load_wb = load_workbook("C:\excel_file\sampleFile1.xlsx", data_only=True)
#시트 이름으로 불러오기
load_ws = load_wb['Sheet1']
max_row = load_ws.max_row

selectedFont =ImageFont.truetype("HMKMRHD.TTF", 35) #폰트경로과 사이즈를 설정해줍니다.
b,g,r,a = 255,255,255,0

count = 1

soundList = []

def combine_audio(vidname, audname, outname, fps=25):
    import moviepy.editor as mpe
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname,fps=fps)

def ssml_to_audio(ssml_text, outfile):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Sets the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    # Builds the voice request, selects the language code ("en-US") and
    # the SSML voice gender ("MALE")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Selects the type of audio file to return
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Performs the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Writes the synthetic audio to the output file.
    with open(outfile, "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file " + outfile)

def text_to_ssml(inputfile):

    raw_lines = inputfile

    # Replace special characters with HTML Ampersand Character Codes
    # These Codes prevent the API from confusing text with
    # SSML commands
    # For example, '<' --> '&lt;' and '&' --> '&amp;'

    escaped_lines = html.escape(raw_lines)

    # Convert plaintext to SSML
    # Wait two seconds between each address
    ssml = "<speak><prosody rate='90%'>{}</prosody></speak>".format(
        escaped_lines.replace("1 ", '<break time="0.2s"/>').replace("0 ", '<break time="0.8s"/>')
    )
    print(ssml)

    # Return the concatenated string of ssml script
    return ssml


for i in load_ws.rows:
    try:
        target_image = Image.open('C:\image\img2.jpg')  #일단 기본배경폼 이미지를 open 합니다.
        draw = ImageDraw.Draw(target_image) 
        eng = i[3].value
        kor = i[4].value
        imgNm = "C:\image\sample" + str(count) + ".png"
        if len(eng) >= 13 :
            draw.text((80, 310), eng, font=selectedFont, fill=(b,g,r,a))
            eng = eng + "1 " 
        else :
            draw.text((350, 310), eng, font=selectedFont, fill=(b,g,r,a))
            eng = eng + "0 "
        word = eng + " : " + kor
        soundList.append(eng)
        draw.text((700,310), kor, font=selectedFont, fill=(b,g,r,a))
        target_image.save(imgNm) #편집된 이미지를 저장합니다.
        #img_list.append(Image.open(imgNm))
        count = count + 1   
    except: pass
print(soundList)
print(''.join(soundList))
lang = 'en'

ssml = text_to_ssml(''.join(soundList))
ssml_to_audio(ssml, "C:\image\sounds.mp3")

# output = gTTS(text = str(soundList), lang = lang, slow = False)
# output.save("C:\image\sounds.mp3")

path = "C:\image"
paths = [os.path.join(path , i ) for i in os.listdir(path) if re.search(".png$", i )]

store1 = []

for i in paths :
    store1.append(i)

paths = natsort.natsorted(store1)

print(paths)

pathIn= 'C:\image'
pathOut = 'C:\image\words.mp4'
fps = 0.7

frame_array = []
for idx , path in enumerate(paths) : 
    img = cv2.imread(path)
    height, width, layers = img.shape
    size = (width,height)
    frame_array.append(img)
out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
for i in range(len(frame_array)):
    # writing to a image array
    out.write(frame_array[i])
out.release()

# videoclip = VideoFileClip("C:\image\words.mp4")
# audioclip = AudioFileClip("C:\image\sounds.mp3")

# new_audioclip = CompositeAudioClip([audioclip.set_start(5)])
# videoclip.audio = new_audioclip
# videoclip.write_videofile("C:\image\combine.mp4")


if __name__ == "__main__":
	combine_audio("C:\image\words.mp4","C:\image\sounds.mp3","C:\image\ddd.mp4")

