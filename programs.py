from __future__ import unicode_literals
from django.core.files.storage import FileSystemStorage
from django.http import *
from django.shortcuts import *

from django.views.decorators.csrf import *

from templates import *
import speech_recognition as sr
from pdfme import build_pdf
import os
from pydub import AudioSegment
from pytube import YouTube
import moviepy.editor
import os
from pydub.silence import split_on_silence
import cv2


# ------------------------------------------------------------------
def index(request):
    return render(request, "index.html")


def makePdf(videoTitle, linkToVideo, transcript):
    document = {
        "style": {
            "margin_bottom": 15, "text_align": "j",
            "page_size": "a4", "margin": [60, 50]
        },
        "formats": {
            "url": {"c": "blue", "u": 1},
            "title": {"b": 1, "s": 13}
        },
        "running_sections": {
            "header": {
                "x": "left", "y": 20, "height": "top", "style": {"text_align": "r"},
                "content": [{".b": "This is a header"}]
            },
            "footer": {
                "x": "left", "y": 740, "height": "bottom", "style": {"text_align": "c"},
                "content": [{".": ["Page ", {"var": "$page"}]}]
            }
        },
        "sections": [
            {
                # "style": {"page_numbering_style": "roman"},
                # "running_sections": ["footer"],
                "content": [

                    {
                        '.': [videoTitle],
                        'style': {
                            'text_align': 'c',
                            'b': True,
                            'i': True,
                            'u':True,
                            's': 13,
                            # 'bg':'blue',
                            'c':'black',
                        },
                        'label': 'a_important_paragraph',
                        'uri': linkToVideo
                    },

                ]
            },
        ]
    }
    for i in range(0, len(transcript)):
        document["sections"][0]["content"].append({
            "group": [
                {"image": "audios/captures/file_" + str(i + 1) + ".jpg"},
                {".": transcript[i]}
            ]
        })

    with open(videoTitle + '.pdf', 'wb') as f:
        build_pdf(document, f)


r = sr.Recognizer()
def get_large_audio_transcription(path):
    sound = AudioSegment.from_wav(path)
    chunks = split_on_silence(sound,
                              min_silence_len=500,
                              silence_thresh=sound.dBFS - 14,
                              keep_silence=500,
                              )
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    return whole_text


videolength = 70
videoTitle = "YTNotes"


def youtubeVideoToText(link):
    yt = YouTube(link)
    global videolength
    videolength = yt.length
    global videoTitle
    videoTitle = yt.title
    videoTitle = ''.join(e for e in videoTitle if e.isalnum())[:30]
    video = yt.streams.filter()[1]
    video.download(output_path="audios", filename="audio.mp4")
    video = moviepy.editor.VideoFileClip("audios/audio.mp4")
    audio = video.audio
    audio.write_audiofile(r"audios/audio.wav")
    res = get_large_audio_transcription(r"audios/audio.wav")
    return res


def extract_images_from_video(video, folder=None, delay=30, name="file", max_images=20, silent=False):
    vidcap = cv2.VideoCapture(video)
    count = 0
    num_images = 0
    if not folder:
        folder = os.getcwd()
    label = 0
    success = True
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))

    while success and num_images < max_images:
        success, image = vidcap.read()
        num_images += 1
        label += 1
        file_name = name + "_" + str(label) + ".jpg"
        path = os.path.join(folder, file_name)
        try:
            cv2.imwrite(path, image)
        except:
            pass
        if cv2.imread(path) is None:
            os.remove(path)
        else:
            if not silent:
                pass
                # print(f'Image successfully written at {path}')
        count += delay * fps
        vidcap.set(1, count)
    return label


def processIt(transcript):
    transcript = transcript.split('.')
    result = []
    i = 0
    while i < len(transcript):
        temp = ""
        while (i < len(transcript) and len(temp) < 50):
            temp += transcript[i]
            i += 1
        if (len(temp) > 0 and len(temp) > 50):
            result.append(temp)
        print(i, temp)
    print(result)
    return result


def videoToNotes(link):
    print("Generating Transcript")
    transcript = youtubeVideoToText(link)
    # transcript = "Share back again and i know you are pretty excited about this new series that i can get started. This series is gonna be a little bit fast-paced so that you can understand what type step test and i totally understand. Excitement. The. Enthusiasm to learn all about typhoid fever i have. The right now that our world is formed by javascript people are loving it allow people hating it but regardless the fact. Happy birthday is writing jealous dad. Andhra plethora of tutorials available on javascript including mine and i am also determined to add more videos in the hostel series. What is new kid on the town known as types that allow people are loving it those who start writing a script. Just plain that i don't want to go back into writing javascript so what's this all about typescript i be missing anything that i ball. Prema starting a brand new series on the typescript and eventually as we go further you will have the full knowledge and full writable skill so that you can transform from javascript to typescript. Before going further there i would like to just give you an introduction what type today and schedule be even writing typescript at all on the first place. There is a lot of her in the market that i just want to jump into typescript i don't even want to learn javascript but that is not the case that is not how it should be started. It should be started with javascript and there is a reason behind it i walk you through with that. And also what it will that why it is important and why even you should be writing javascript in the first place or shouldn't be that is the big question that will answering. Subah to the series on the typescript and we will be running the series into a fast paced nodal the pushing a lot of videos so go ahead buckle up and let's get started with typescript. Rajkot highway 31 learnet. An everybody knows one thing about typekit temperature in case you are living unless and until under a rock you have heard about that this is a javascript the classic yellow i can this is a typescript. Often called as the typescript is a superset of javascript that means everything that you can do in javascript that is only available in typescript and a lot more is available to that. Bada tej. Find the true statement but not accurately being contextualize by a lot of people. Yes you have an accurate statement that i feed is a superset of javascript. But it's not like it is adding more features to javascript no it doesn't give you more of call back it doesn't give you more of arrow function in just allows you to write javascript in a much precise manner so that your code faces a lot less error in the run time. If there is any error it is already being displayed to you while writing the code and the kind of when you are just helping them out in the your favourite editor maybe vs code or something. That is where we want to just catch those error and find that we shouldn't be doing something like that. That is all your typescript it is not going to give you and you look it is not going to give you a classes on you module it is not going to give you anything new. In fact all the code that you're right in the typed it is finally compiled into javascript not only that. Even though you are chordata might be yelling at you with some squiggly line about that code. Still you are allowed to compile that code in the javascript and it might one witherrors but it might run. Strong thing that you need to understand that is not like typescript is the ultimate way of writing the pure javascript is not going to give you any quality behaviour it might sell so you are round off somewhere and that is exactly what we are going to learn in this series. The first yes i understand that you know the statement that there is a javascript there is a typescript and circles the entire chavakkad. In the sweet by walk through all the details in depth of the type steps don't you worry about that i'll cover that are. But first farmers should be even learning typescript that is the big question. Rajkot is not about reinventing the entire javascript language it is not. Adjust is asking that you write javascript with a little bit more accurate behaviour that you just do anything just try to write a javascript in a more precise manner so that errors are less. And i honestly would say you shouldn't be using that safe if your project is just to file long and there in each file their ages 5 to 10 lines of code. It is not compulsory that having a place you need to write pfx or ts for typescript. I've seen a lot of people who use typescript but all the places the use any which is the keyboard will talk about that later on. Using typescript you need to use the super power of typescript to make your code much more powerful and much more error-prone. And if you are using just a script for the fanciness of writing ts. A properly not using it correctly. After watching this series. Watching tested in a much more powerful manner. It is all about type safety nothing more. Just this world. Repeating this word for william milian time in this entire series that what is the site safety typescript is all about type safety and nothing else. So what is the type safety let me give you a couple of covid-19 apples. Sometimes it is nothing that javascript allows us to do some on behaviour for example i can go ahead and just add to with the string of 2. Which i shouldn't be allowed to do it gives me a odd result of 22. This is happening because the type safety was missing. On the very first place it should have stopped me from doing. Addition of number with string. It doesn't stop you tries to do its own behaviour which have discussed on the tibetan my other videos but registry right now take care. Pradesh west india. That is all miss matching of the type if you have been consistent with a type this error shouldn't be there. And it allows you to just stop this behaviour that's all it does. For example whether you have now you are allowed to add two values to the null and on top of that there is an define and you are allowed to add to to undefined and get another thing like to end and not a number. This is all not the quality behaviour of javascript but rather your way of you haven't been concerned about the types of javascript. There is an explanation in the documentation of javascript that what behaviour is going to kick in a what behaviour is going to super power and power that but apart from the end we haven't read the documentation of javascript which are being the language specification given by atmospheric they are all right here. But the idea is high should be reading that much on the first lady should be focused on building my application with the type safety. And that is where the title comes into the picture in the series mastering the typescript. Subscribe the channel and can be walking through in fact rolling costing through this ride of type safety with the ties that i hope you all excited all videos are coming and get prescribed let's catch you up in xvideo."
    print(transcript)
    print("Transcript Done")
    transcript = processIt(transcript)
    totalPages = len(transcript)
    print(videolength, totalPages)
    totalDelay = int(videolength / totalPages)
    print(totalDelay)
    # tl = int(len(transcript) / totalPages)
    print("Getting Screenshots from Video")
    cnt = extract_images_from_video("audios/audio.mp4", folder="audios/captures/", delay=totalDelay, name="file",
                                    max_images=totalPages, silent=False)
    # print(cnt)
    print("Done with Screenshots")

    print("Making the PDF")
    makePdf(videoTitle, link, transcript)
    print("PDF Done")


# link = "https://www.youtube.com/watch?v=j89BvWz8Eag"
# videoToNotes(link)
def makenotes(request):
    link = request.GET["url"]
    # try:
    videoToNotes(link)
    # except:
    #     return HttpResponse("error")
    return HttpResponse("success")

def downloadpdf(request):
    filename=videoTitle + '.pdf'
    response = FileResponse(open(filename, 'rb'))
    return response
def getlength(request):
    link = request.GET["url"]
    yt = YouTube(link)
    ln=yt.length
    return render(request,"makenotes.html",{"len":str(ln),"link":link})
