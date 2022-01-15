import json
import datetime
import scraper # web scrapping
import music as msc
import face_detection as face
import meme_creator as meme
import broker as db
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

"""
            |                        AGENTE RECEPTOR:                               |                    
            |                Este agente es el encargado de                         |   
            |            recoger las peticiones del usuario, elaborar               |     
            |        una respuesta, o pedir al usuario más información para         |
            |    completar su respuesta. También conecta directamente con la base   |
            |    de datos implementada en SQLite.                                   |

"""

# Load the json file with the crendentials
f = open(f'../credenciales.json',)
data = json.load(f)

"""

    Método template:
            Método utilizado por receptor para crear plantillas de mensajes

"""
def __create_template__(protocol):
    template = Template()
    template.sender = data['spade_intro']['username']
    template.to = data['spade_intro_2']['username']
    if protocol != "download" and protocol != "memeCreator" and protocol != "file":
        template.metadata = {"performative": "request", "protocol":protocol}
    else: 
        template.metadata = {"protocol":protocol}

    return template

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

                if msg.metadata["performative"] == "inform":
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
                        await self.send(send)
                    except:
                        send.set_metadata("performative", "failure")
                        send.body = f'-Bot say: something went wrong while creating the file'

                        await self.send(send)
                # ------------------------------------------------------------------------------------------------------------ #
                if msg.metadata["performative"] == "request":
                    try:
                        body_send = "- Bot say: If you want to include a route type the hole path, \
                            if not, the file will be created in the current directory. \
                            \nExample: file.txt | maria/University/Multiagent/file.txt. \
                            \n- Bot say: you also have to include some text in the file (enter if not)."
                        send  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                        send.set_metadata("protocol", "file")
                        send.set_metadata("performative", "request")
                        send.body = body_send
                        await self.send(send)

                    except Exception:
                        error  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                        error.set_metadata("protocol", "file")
                        error.set_metadata("performative", "failure")
                        error.body = f'-Bot say: Something went wrong sending the msg'
                        await self.send(error)

    """
    
        Comportamiento Download:
                Este comportamiento recibe una url de Youtube y descarga el video en el formato indicado
    
    """
    class Download(CyclicBehaviour):
        async def run(self):

            msg = await self.receive() 
            if msg:
                if msg.metadata["performative"] == "request":
                    try:
                        send  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                        send.set_metadata("protocol", "download")
                        send.set_metadata("performative", "request")
                        send.body = f'-Bot say: give me a name with the extension for the file: _ {msg.body}'
                        await self.send(send)

                    except Exception:
                        error  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                        error.set_metadata("protocol", "download")
                        error.set_metadata("performative", "failure")
                        error.body = f'-Bot say: Something went wrong sending the msg'
                        await self.send(error)
            # ------------------------------------------------------------------------------------------------------------ # 
                if msg.metadata["performative"] == "inform":
                    inter_msg  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                    inter_msg.set_metadata("protocol", "download")
                    inter_msg.set_metadata("performative", "inform")
                    inter_msg.body = f'-Bot say: searching url...'
                    await self.send(inter_msg)
                    try:
                        message = (msg.body).split('_')
                        send  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                        send.set_metadata("protocol", "download")
                        send.set_metadata("performative", "inform")

                        flag = msc.download(message[1], message[0][0:-1])
                        if flag == 0:
                            send.body = f'-Bot say: Video store in music folder'
                            await self.send(send)
                        else:
                            send.body = f'-Bot say: Youtube video not found'
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
                    inter_msg.body = f'-Bot say: Beautiful face!'
                    
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
                if msg.metadata["performative"] == "inform":
                
                    if msg.body == "":
                        try:
                            url_random = db.readImage()
                            meme.create_meme(url_random)
                            send  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                            send.set_metadata("protocol", "memeCreator")
                            send.set_metadata("performative", "inform")
                            send.body = f'-Bot say: Meme created randomly and stored in random folder '

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
                            send.body = f'-Bot say: Meme created, stored in random folder and the image has been stored in the database '
                            await self.send(send)

                        except Exception:
                            error = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                            error.set_metadata("protocol", "faceDetection")
                            error.set_metadata("performative", "failure")
                            error.body = f'-Bot say: Something went wrong while detection'

                            await self.send(error)

                # Ascking for an image
                if msg.metadata["performative"] == "request":
                    try:
                        send  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                        send.set_metadata("protocol", "memeCreator")
                        send.set_metadata("performative", "request")
                        send.body = f'-Bot say: Insert image for using that one or enter to get a random image from db: '
                        await self.send(send)

                    except Exception:
                        error  = Message(to=data['spade_intro']['username'], sender=data['spade_intro_2']['username'])
                        error.set_metadata("protocol", "memeCreator")
                        error.set_metadata("performative", "failure")
                        error.body = f'-Bot say: Something went wrong sending the msg'
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
        self.add_behaviour(time, template_time)
        self.add_behaviour(whois, template_whois)
        self.add_behaviour(file, template_file)
        self.add_behaviour(download, template_download)
        self.add_behaviour(history, template_history)
        self.add_behaviour(face, template_facial)
        self.add_behaviour(meme, template_meme)
        self.add_behaviour(exit, template_ShutDown)
