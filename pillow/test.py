# def combine_audio(vidname, audname, outname, fps=25):
#     import moviepy.editor as mpe
#     my_clip = mpe.VideoFileClip(vidname)
#     audio_background = mpe.AudioFileClip(audname)
#     final_clip = my_clip.set_audio(audio_background)
#     final_clip.write_videofile(outname,fps=fps)

# if __name__ == "__main__":
# 	combine_audio("C:\image\words.mp4","C:\image\sounds.mp3","C:\image\ddd.mp4")

import html
from google.cloud import texttospeech
import os
from pydub import AudioSegment

def ssml_to_audio(ssml_text, outfile):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Sets the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    # Builds the voice request, selects the language code ("en-US") and
    # the SSML voice gender ("MALE")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.MALE
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
    ssml = "<speak><prosody rate='80%'>{}</prosody></speak>".format(
        escaped_lines.replace("**", '<lang xml:lang="ko-KR">').replace("*", '</lang>')
    )
    print(escaped_lines)
    print(ssml)
    # Return the concatenated string of ssml script
    return ssml

def list_voices():
    """Lists the available voices."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices()

    for voice in voices.voices:
        # Display the voice's name. Example: tpc-vocoded
        print(f"Name: {voice.name}")

        # Display the supported language codes for this voice. Example: "en-US"
        for language_code in voice.language_codes:
            print(f"Supported language: {language_code}")

        ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)

        # Display the SSML Voice Gender
        print(f"SSML Voice Gender: {ssml_gender.name}")

        # Display the natural sample rate hertz for this voice. Example: 24000
        print(f"Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}\n")


text = """**버려지다* contract intrude  be accustomed to ing  show off  oversee  entrust  dispatch  initiate  """

print(text)
ssml = text_to_ssml(text)
ssml_to_audio(ssml, "test.mp3")

sound1 = AudioSegment.from_mp3("C:\image\sounds.mp3")
sound2 = AudioSegment.from_mp3("C:\image\sounds_ko.mp3")

# sound1, with sound2 appended (use louder instead of sound1 to append the louder version)
combined = sound1 + sound2

# save the result
combined.export("C:\image\mixed_sounds.mp3", format="mp3")
