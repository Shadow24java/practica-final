import speech_recognition as sr

def escuchar_comando():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Calibrando ruido ambiente...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Habla ahora (tienes 5 segundos)...")

            audio = r.listen(source, timeout=5, phrase_time_limit=5)

        texto = r.recognize_google(audio, language="es-ES")
        print("Has dicho:", texto)
        return texto.lower()

    except sr.WaitTimeoutError:
        print("No se ha detectado voz a tiempo")
        return ""
    except sr.UnknownValueError:
        print("No he entendido el audio")
        return ""
    except sr.RequestError as e:
        print("Error con el servicio de reconocimiento:", e)
        return ""
    except OSError as e:
        print("Error con el micrófono:", e)
        return ""
