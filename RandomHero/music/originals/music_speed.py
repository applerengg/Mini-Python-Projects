from pydub import AudioSegment
from pydub.playback import play
from argparse import ArgumentParser 

print(0)
parser = ArgumentParser()
parser.add_argument("-a", dest="audio", type=str, required=True)
parser.add_argument("-s", dest="speed", type=float, default=1.0)
args = parser.parse_args()

print(1)
ost : AudioSegment = AudioSegment.from_wav(args.audio)
speed = args.speed

print(2)
modified = ost._spawn(ost.raw_data, overrides={"frame_rate": int(ost.frame_rate * speed)})
modified = modified.set_frame_rate(ost.frame_rate)

print(3)
play(modified)

print(4)
