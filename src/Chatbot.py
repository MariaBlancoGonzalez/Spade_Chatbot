import json
import asyncio
import time
import datetime # time
import scraper # web scrapping
import music as msc
import face_detection as face
import meme_creator as meme
import broker as db
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
from textblob import TextBlob


# Load the json file with the crendentials
f = open(f'../credenciales.json',)
data = json.load(f)


"""

    Métodos templates:
            Métodos utilizados por el emisor y receptor para crear plantillas de mensajes

"""
def __create_template__(protocol):
    template = Template()
    template.sender = data['spade_intro']['username']
    template.to = data['spade_intro_2']['username']
    if protocol != 'download':
        template.metadata = {"performative": "request", "protocol":protocol}
    else: 
        template.metadata = {"protocol":protocol}

    return template

def __create_template_user__(protocol):
    template = Template()
    template.sender = data['spade_intro_2']['username']
    template.to = data['spade_intro']['username']
    template.metadata = {"protocol":protocol}

    return template

"""
            |                        AGENTE EMISOR:                                     |
            |                Este agente es el encargado de                             |
            |            enviar las peticiones al chatbot y recoger                     |
            |        las respuestas para enviarselas al usuario, también                |
            |    envía respuestas si el chatbot nos pide algún tipo de información.     |

"""
class SenderAgent(Agent):

    """
    
        Comportamiento Request:
                Este comportamiento recoge los diferentes comandos con los que podemos indicar al chatbot
                lo que el usuario quiere hacer, algunos recogen información directamentes de ellos.
                Si el comando no es reconocido se ha implementado un corrector gramatical.
    
    """
    class Request(CyclicBehaviour):
        async def run(self):
            choice = 0
            command = ''
            flag = False
            while choice == 0:
                if flag == False:
                    response = input("\nHow can I help you?: ")
                    print("-You say: ", response)
                if response in "show time":
                    choice = 1
                elif "who is" in response:
                    choice = 2
                elif "file" in response:
                    choice = 3
                elif "download" in response or "youtube" in response:
                    choice = 4
                elif "history" in response:
                    choice = 5
                elif "face detection" == response:
                    choice = 6
                elif "meme creator" in response:
                    choice = 7
                elif "exit" == response:
                    choice = 9
                elif "help" == response:
                    print("This is a list with all commands available: "
                    "\n\t - show me the time"
                    "\n\t - who is 'famous person'"
                    "\n\t - file"
                    "\n\t - download 'url'"
                    "\n\t - history"
                    "\n\t - face detection"
                    "\n\t - meme creator"
                    "\n\t - exit"
                    "\n\t - help")
                else: 
                    print("[User Agent] Commant not recognized," ,
                    "you can type 'help' to show all the possible commands")
                    command = ''
                    while command != 'Y' and command != 'N':
                        response = str(TextBlob(response).correct())
                        command = input(f"Do you want to say <<{response}>> (Y/N): ")
                        

                    if command == 'Y':
                        flag = True
            
            if choice == 1:
                
                msg = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                msg.set_metadata("performative", "request")
                msg.set_metadata("protocol", "current_time")
                msg.body = "time"

                await self.send(msg)
                

            elif choice == 2:
                msg = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                msg.set_metadata("performative", "request")
                msg.set_metadata("protocol", "who_is")

                response_splitted = response.split()
                index = response_splitted.index('is')
                people = response_splitted[index+1:]
                body = ' '.join(people)

                msg.body = body
                await self.send(msg)
                print("..................................................................................................")

            elif choice == 3:

                body = ""
                route = input("If you want to include a route type the hole path, "
                            "if not, the file will be created in the current directory. "
                            "\nExample: file.txt | maria/University/Multiagent/file.txt \nType: ")

                body = f'{route} '

                text = input("If you want to include some text in the file write it here (press enter if not): ")

                if text != '':
                    body += text

                msg = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                msg.set_metadata("performative", "request")
                msg.set_metadata("protocol", "file")
                msg.body = body

                await self.send(msg)
                print("..................................................................................................")

            elif choice == 4:
                msg = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                msg.set_metadata("performative", "request")
                msg.set_metadata("protocol", "download")

                url = response.split(" ")[-1]
                while url[0:23] != 'https://www.youtube.com':
                    url = input('It is needed to introduced youtube url to start the search: ')
                

                msg.body = url
                await self.send(msg)
                print("..................................................................................................")

            elif choice == 5:
                msg = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                msg.set_metadata("performative", "request")
                msg.set_metadata("protocol", "history")           

                await self.send(msg)
                print("..................................................................................................")

            elif choice == 6:
                msg = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                msg.set_metadata("performative", "request")
                msg.set_metadata("protocol", "faceDetection")           

                await self.send(msg)
                print("..................................................................................................")

            elif choice == 7:
                
                msg = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                msg.set_metadata("performative", "request")
                msg.set_metadata("protocol", "memeCreator")           

                msg.body = input("Insert image for using that one or enter to get a random image from db: ")
                await self.send(msg)
                print("..................................................................................................")

            elif choice == 9: 
                msg = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                msg.set_metadata("performative", "request")
                msg.set_metadata("protocol", "exit")           

                print("You shutting down...")
                await self.send(msg)

            
            await asyncio.sleep(1)

    class Responses(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg:
                if msg.metadata["performative"] == "inform":
                    print(msg.body)
                if msg.metadata["performative"] == "failure":
                    print(msg.body)
                if msg.metadata["performative"] == "request":
                    mess = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                    mess.set_metadata("performative", "inform")
                    mess.set_metadata("protocol", "download")           

                    message = (msg.body).split('_')
                    mess.body = f'{input(message[0])} _ {message[1]}'
                    await self.send(mess)


    async def setup(self):
        print("[User Agent] "+str(self.jid)+ " started")
        petis = self.Request()

        # Msg Templates
        template_time = __create_template_user__("current_time")
        template_whois = __create_template_user__("who_is")
        template_file = __create_template_user__("file")
        template_download = __create_template_user__("download")
        template_history = __create_template_user__("history")
        template_facial = __create_template_user__("faceDetection")
        template_meme = __create_template_user__("memeCreator")
        template_exit = __create_template_user__("exit")

        # Adding the Behaviour with the template will filter all the msg
        self.add_behaviour(self.Responses(), template_time) #Este comportamiento solo leera mensajes de este tipo
        self.add_behaviour(self.Responses(), template_whois)
        self.add_behaviour(self.Responses(), template_file)
        self.add_behaviour(self.Responses(), template_download)
        self.add_behaviour(self.Responses(), template_history)
        self.add_behaviour(self.Responses(), template_facial)
        self.add_behaviour(self.Responses(), template_meme)
        self.add_behaviour(self.Responses(), template_exit)
        
        self.add_behaviour(petis)

"""
            |                        AGENTE RECEPTOR:                               |                    
            |                Este agente es el encargado de                         |   
            |            recoger las peticiones del usuario, elaborar               |     
            |        una respuesta, o pedir al usuario más información para         |
            |    completar su respuesta. También conecta directamente con la base   |
            |    de datos implementada en SQLite.                                   |

"""


class ReceiverAgent(Agent):

    """
    
        Comportamiento TimeBehav:
                Este comportamiento nos muestra la hora de la forma %d/%m/%Y %H:%M:%S
    
    """
    class TimeBehav(CyclicBehaviour):
        async def run(self):

            msg = await self.receive()
            if msg:
                
                send = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                send.set_metadata("performative", "inform")
                send.set_metadata("protocol", "current_time")           
                
                date = datetime.datetime.now()
                date_parser = date.strftime("%d/%m/%Y %H:%M:%S")
                send.body = f'-Bot say: The current time is: {date_parser}'
                await self.send(send)


    """
    
        Comportamiento WhoIs:
                Este comportamiento busca en Wikipedia información sobre una persona y la almacena en la bbdd,
                si esta persona ha sido buscada con anterioridad y almacenada en nuestra base de datos, 
                nos muestra la información almacenada. Suma 1 por cada busqueda.

    """
    class WhoIs(CyclicBehaviour):
        async def run(self):
            
            msg = await self.receive()
            if msg:

                search = db.readRows()
                urls = db.readURL()

                send = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                send.set_metadata("protocol", "who_is")           

                description = None
                times = 0
                name = scraper.parse_name(msg.body)

                for i in search:
                    if i[0] == name:
                        description = i[1]
                        times = i[2]
                        break

                if description == None:
                    text = scraper.who_is(name, urls[0][0])
                    no_encontrado = scraper.who_is("dnasjkdnas", urls[0][0])

                    if text != no_encontrado:
                        send.set_metadata("performative", "inform")
                        send.body = f'-Bot say: {name}: {text} \nPerson store in our database'
                        db.insertRow(name, text,1)
                    else:
                        send.set_metadata("performative", "failure")
                        send.body = f'-Bot say: Fail, this person is not famous'
                else:
                    send.set_metadata("performative", "inform")
                    send.body = f'-Bot say: This person is already in our database: {description}'
                    db.updatePeople(name, times+1)

                await self.send(send)
                

    """
    
        Comportamiento CreateFile:
                Este comportamiento crea un fichero, con la información y nombre (con o sin ruta) indicados.
    
    """
    class CreateFile(CyclicBehaviour):
        async def run(self):
            msg = await self.receive() 
            if msg:
                send = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                send.set_metadata("protocol", "file")
                try:
                    inter_msg  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                    inter_msg.set_metadata("protocol", "file")
                    inter_msg.set_metadata("performative", "inform")
                    inter_msg.body = f'-Bot say: I am creating the file...'
                    await self.send(inter_msg)

                    body = (msg.body).split(" ")
                    file = open(f'{body[0]}', "w")
                    file.write(' '.join(body[1:]))
                    file.close()
           
                    send.set_metadata("performative", "inform")
                    send.body = f'-Bot say: file created in {body[0]}, with content: {body[1]}'

                except:
                    send.set_metadata("performative", "failure")
                    send.body = f'-Bot say: something went wrong while creating the file'

                await self.send(send)


    """
    
        Comportamiento Download:
                Este comportamiento recibe una url de Youtube y descarga el video en el formato indicado
    
    """
    class Download(CyclicBehaviour):
        async def run(self):

            msg = await self.receive() 
            if msg:
                if msg.metadata["performative"] == "request":
                    inter_msg  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                    inter_msg.set_metadata("protocol", "download")
                    inter_msg.set_metadata("performative", "inform")
                    inter_msg.body = f'-Bot say: searching url...'
                    await self.send(inter_msg)
                    try:
                        send  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                        send.set_metadata("protocol", "download")
                        send.set_metadata("performative", "request")
                        send.body = f'-Bot say: give me a name with the extension for the file _ {msg.body}'
                        await self.send(send)

                    except Exception:
                        error  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                        error.set_metadata("protocol", "download")
                        error.set_metadata("performative", "failure")
                        error.body = f'-Bot say: Something went wrong sending the msg'
                        await self.send(error)
            # ------------------------------------------------------------------------------------------------------------ # 
                if msg.metadata["performative"] == "inform":
                    try:
                        message = (msg.body).split('_')
                        msc.download(message[1], message[0][0:-1])
                        send  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                        send.set_metadata("protocol", "download")
                        send.set_metadata("performative", "inform")
                        send.body = f'-Bot say: Video store in music folder'
                        await self.send(send)

                    except Exception:
                        error  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                        error.set_metadata("protocol", "download")
                        error.set_metadata("performative", "failure")
                        error.body = f'-Bot say: Something went wrong sending the msg'
                        await self.send(error)
                

    """
    
        Comportamiento History:
                Este comportamiento busca en la base de datos la persona más buscada y nos ofrece información
                al respecto.

    """
    class History(CyclicBehaviour):
        async def run(self):

            msg = await self.receive() 
            if msg:
                try:
                    people = db.readOrderedPeople()
                    inter_msg  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                    inter_msg.set_metadata("protocol", "history")
                    inter_msg.set_metadata("performative", "inform")
                    inter_msg.body = f'-Bot say: The most search person is: {people[0]}, '
                    inter_msg.body += f'\n-Bot say: Result of this search:  {people[1]},'
                    inter_msg.body += f' \n-Bot say: Times this person has been search: {people[2]}'
                    await self.send(inter_msg)

                except Exception:
                    error = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                    error.set_metadata("protocol", "history")
                    error.set_metadata("performative", "failure")
                    error.body = f'-Bot say: Something went wrong while accessing database'

                    await self.send(error)
                
    """
    
        Comportamiento Facial:
                Este comportamiento activa la cámara del ordenador host para identificar una cara.

    """
    class Facial(CyclicBehaviour):
        async def run(self):

            msg = await self.receive() 
            if msg:
                try:
                    inter_msg  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                    inter_msg.set_metadata("protocol", "faceDetection")
                    inter_msg.set_metadata("performative", "inform")
                    inter_msg.body = f'-Bot say: to close this windows press space bar'
                    
                    await self.send(inter_msg)
                    face.detect()

                except Exception:
                    error = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                    error.set_metadata("protocol", "faceDetection")
                    error.set_metadata("performative", "failure")
                    error.body = f'-Bot say: Something went wrong while detection'

                    await self.send(error)
                
    """
    
        Comportamiento MemeCreator:
                Este comportamiento crea un meme con la cara random si no se le entrega ruta 
                un meme con la imagen pasada.

    """
    class MemeCreator(CyclicBehaviour):
        async def run(self):

            msg = await self.receive() 
            if msg:
                
                if msg.body == "":
                    try:
                        url_random = db.readImage()
                        meme.create_meme(url_random)
                        send  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                        send.set_metadata("protocol", "memeCreator")
                        send.set_metadata("performative", "inform")
                        send.body = f'-Bot say: Meme created randomly and stored in meme folder '

                        await self.send(send)

                    except Exception:
                        error = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                        error.set_metadata("protocol", "faceDetection")
                        error.set_metadata("performative", "failure")
                        error.body = f'-Bot say: Something went wrong while reading random image'

                        await self.send(error)
                else:
                    try:
                        url = msg.body
                        meme.create_meme(url)
                        name = ((url.split("/"))[-1].split("."))[-2]
    
                        db.insertImage(name, url)

                        send  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                        send.set_metadata("protocol", "memeCreator")
                        send.set_metadata("performative", "inform")
                        send.body = f'-Bot say: Meme created, stored in meme folder and the image has been stored in the database '

                        await self.send(send)

                    except Exception:
                        error = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                        error.set_metadata("protocol", "faceDetection")
                        error.set_metadata("performative", "failure")
                        error.body = f'-Bot say: Something went wrong while detection'

                        await self.send(error)

    """
    
        Comportamiento Shutdown:
                Apaga el agente chatbot y manda una señal al usuario

    """
    class ShutDown(CyclicBehaviour):
        async def run(self):
            msg = await self.receive() 
            if msg:
                send  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                send.set_metadata("protocol", "exit")
                send.set_metadata("performative", "inform")
                send.body = f'Bot shutting down...'

                await self.send(send)                

                await self.agent.stop()


    """
    
        Inicialización de los comportamientos y agente chatbot o receptor
    
    """
    async def setup(self):
        print("[Receiver Agent] "+str(self.jid)+ " started")

        print("Loading responses...")
        
        time = self.TimeBehav()
        whois = self.WhoIs()
        file = self.CreateFile()
        download = self.Download()
        history = self.History()
        face = self.Facial()
        meme = self.MemeCreator()
        exit = self.ShutDown()

        # Msg Templates
        template_time = __create_template__("current_time")
        template_whois = __create_template__("who_is")
        template_file = __create_template__("file")
        template_download = __create_template__("download")
        template_history = __create_template__("history")
        template_facial = __create_template__("faceDetection")
        template_meme = __create_template__("memeCreator")
        template_ShutDown = __create_template__("exit")


        # Adding the Behaviour with the template will filter all the msg
        self.add_behaviour(time, template_time) #Este comportamiento solo leera mensajes de este tipo
        self.add_behaviour(whois, template_whois)
        self.add_behaviour(file, template_file)
        self.add_behaviour(download, template_download)
        self.add_behaviour(history, template_history)
        self.add_behaviour(face, template_facial)
        self.add_behaviour(meme, template_meme)
        self.add_behaviour(exit, template_ShutDown)

"""

    Método main:
        Inicialización de los agentes Emisor (USUARIO) y Receptor (CHATBOT).

"""
def main():
    
    print("Creating Agents... ")

    receiveragent = ReceiverAgent(data['spade_intro_2']['username'], 
                            data['spade_intro_2']['password'])
    future = receiveragent.start()
    future.result()
    

    senderagent = SenderAgent(data['spade_intro']['username'], 
                        data['spade_intro']['password'])
    f = senderagent.start()
    f.result()
    
    
    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            receiveragent.stop()
            break
    
    print("Agents finished")

if __name__ == "__main__":
    main()
