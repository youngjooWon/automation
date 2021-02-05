from mutagen.mp3 import MP3

audio = MP3("C:\\ttsInExcel\\audio_mixed_sounds1.mp3")
print(audio.info.length)