from pydub import AudioSegment

sound = AudioSegment.from_mp3("000002.mp3")

sound.export("", format="wav")