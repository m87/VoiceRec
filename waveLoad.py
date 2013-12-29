import os
import wave
def waveLoader(path):
    out=[]
    for f in os.listdir(path):
        out.append([f[-5:-4],wave.open(os.path.join(path,f))])


    return out


if __name__ == "__main__":
    out=waveLoader("train")
    print(out)
