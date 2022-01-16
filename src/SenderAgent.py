import json
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
from textblob import TextBlob

"""
            |                        AGENTE EMISOR:                                     |
            |                Este agente es el encargado de                             |
            |            enviar las peticiones al chatbot y recoger                     |
            |        las respuestas para enviarselas al usuario, también                |
            |    envía respuestas si el chatbot nos pide algún tipo de información.     |

"""

# Load the json file with the crendentials
f = open(f'../credenciales.json',)
data = json.load(f)

def __create_template_user__(protocol):
    template = Template()
    template.sender = data['spade_intro_2']['username']
    template.to = data['spade_intro']['username']
    template.metadata = {"protocol":protocol}

    return template

def __create_template_menu__(protocol):
    template = Template()
    template.sender = data['spade_intro']['username']
    template.to = data['spade_intro']['username']
    template.metadata = {"protocol":protocol}

    return template


class SenderAgent(Agent):
    class Init(OneShotBehaviour):
        async def run(self):
            mess = Message(to=data['spade_intro']['username'], sender=data['spade_intro']['username'])
            mess.set_metadata("protocol", "menu")
            await self.send(mess)
            #print(mess)
    """
    
        Comportamiento Request:
                Este comportamiento recoge los diferentes comandos con los que podemos indicar al chatbot
                lo que el usuario quiere hacer, algunos recogen información directamentes de ellos.
                Si el comando no es reconocido se ha implementado un corrector gramatical.
    
    """
    class Request(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg:
                choice = 0
                command = ''
                flag = False
                while choice == 0:
                    if flag == False:
                        response = input("\nHow can I help you?: ")
                        print("-You say: ", response)
                    if response in "show me the time":
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
                        choice=10
                    elif flag == True:
                        choice = 10
                    else: 
                        print("[User Agent] Commant not recognized," ,
                        "you can type 'help' to show all the possible commands")
                        command = ''
                        if response != str(TextBlob(response).correct()):
                            while command != 'Y' and command != 'N':
                                response = str(TextBlob(response).correct())
                                command = (input(f"Do you want to say <<{response}>> (Y/N): ")).upper()
                        

                        if command == 'Y':
                            flag = True
                        

                if choice == 1:
                    
                    msg = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                    msg.set_metadata("performative", "request")
                    msg.set_metadata("protocol", "current_time")
                    msg.body = "time"

                    await self.send(msg)
                    print(".....")

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
                    print(".....")

                elif choice == 3:
                    msg = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                    msg.set_metadata("performative", "request")
                    msg.set_metadata("protocol", "file")

                    await self.send(msg)
                    print(".....")
                
                elif choice == 4:
                    msg = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                    msg.set_metadata("performative", "request")
                    msg.set_metadata("protocol", "download")

                    url = response.split(" ")[-1]
                    while url[0:23] != 'https://www.youtube.com':
                        url = input('It is needed to introduced youtube url to start the search: ')
                

                    msg.body = url
                    await self.send(msg)
                    print(".....")

                elif choice == 5:
                    msg = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                    msg.set_metadata("performative", "request")
                    msg.set_metadata("protocol", "history")           

                    await self.send(msg)
                    print(".....")

                elif choice == 6:
                    msg = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                    msg.set_metadata("performative", "request")
                    msg.set_metadata("protocol", "faceDetection")           

                    await self.send(msg)
                    print(".....")

                elif choice == 7:
                    
                    msg = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                    msg.set_metadata("performative", "request")
                    msg.set_metadata("protocol", "memeCreator")           

                    await self.send(msg)
                    print(".....")

                elif choice == 9: 
                    msg = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                    msg.set_metadata("performative", "request")
                    msg.set_metadata("protocol", "exit")           

                    print("You shutting down...")
                    await self.send(msg)

                elif choice == 10:
                    print("This is a list with all commands available: "
                        "\n\t - show me the time"
                        "\n\t - who is 'famous person'"
                        "\n\t - file"
                        "\n\t - download or youtube or youtube's urls"
                        "\n\t - history"
                        "\n\t - face detection"
                        "\n\t - meme creator"
                        "\n\t - exit"
                        "\n\t - help")
                    
                    mess = Message(to=data['spade_intro']['username'], sender=data['spade_intro']['username'])
                    mess.set_metadata("protocol", "menu")  
                    await self.send(mess)


    class Responses(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg:
                if msg.metadata["performative"] == "inform":
                    print(msg.body)
                    if msg.metadata["protocol"] != "exit":
                        mess = Message(to=data['spade_intro']['username'], sender=data['spade_intro']['username'])
                        mess.set_metadata("protocol", "menu")  
                        await self.send(mess)
                    else:
                        await self.agent.stop()

                if msg.metadata["performative"] == "failure":
                    print(msg.body)
                    mess = Message(to=data['spade_intro']['username'], sender=data['spade_intro']['username'])
                    mess.set_metadata("protocol", "menu")  
                    await self.send(mess)

                if msg.metadata["performative"] == "request":
                    
                    if msg.metadata["protocol"] == "download":
                        mess = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                        mess.set_metadata("performative", "inform")
                        mess.set_metadata("protocol", "download")           

                        message = (msg.body).split('_')
                        mess.body = f'{input(message[0])} _ {message[1]}'
                        await self.send(mess)

                    if msg.metadata["protocol"] == "memeCreator":
                        mess = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                        mess.set_metadata("performative", "inform")
                        mess.set_metadata("protocol", "memeCreator")           

                        send = input(msg.body)
                        mess.body = send
                        await self.send(mess)
                    
                    if msg.metadata["protocol"] == "file":
                        body_send = ""
                        print(msg.body)

                        route = input("- User asking: Name+path: ")
                        body_send += f'{route} '
                        text = input("- User asking: Text: ")
                        if text != '':
                            body_send += text

                        mess = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                        mess.set_metadata("performative", "inform")
                        mess.set_metadata("protocol", "file")           

                        mess.body = body_send
                        await self.send(mess)


    async def setup(self):
        print("[User Agent] "+str(self.jid)+ " started")
        petis = self.Request()
        init = self.Init()
        self.add_behaviour(init)
        # Msg Templates
        template_time = __create_template_user__("current_time")
        template_whois = __create_template_user__("who_is")
        template_file = __create_template_user__("file")
        template_download = __create_template_user__("download")
        template_history = __create_template_user__("history")
        template_facial = __create_template_user__("faceDetection")
        template_meme = __create_template_user__("memeCreator")
        template_exit = __create_template_user__("exit")

        template_menu = __create_template_menu__("menu")
        # Adding the Behaviour with the template will filter all the msg
        self.add_behaviour(self.Responses(), template_time) #Este comportamiento solo leera mensajes de este tipo
        self.add_behaviour(self.Responses(), template_whois)
        self.add_behaviour(self.Responses(), template_file)
        self.add_behaviour(self.Responses(), template_download)
        self.add_behaviour(self.Responses(), template_history)
        self.add_behaviour(self.Responses(), template_facial)
        self.add_behaviour(self.Responses(), template_meme)
        self.add_behaviour(self.Responses(), template_exit)

        
        self.add_behaviour(petis, template_menu)
