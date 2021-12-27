import json
import time
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
import scraper as ppl

''' 
    User module.

    SPADE API to make requests to the chat module

'''

# Load the json file with the crendentials
f = open('credenciales.json',)
data = json.load(f)

'''
class ReceiverAgent(Agent):
    class RecvBehav(OneShotBehaviour):
        async def run(self):
            print("[Agente Chatbot] Iniciada una llamada al chatbot")

            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            if msg:
                ppl.who_is(msg.body)
                print("Message received with content: {}".format(msg.body))
            else:
                print("Did not received any message after 10 seconds")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("ReceiverAgent started")
        b = self.RecvBehav()

        # Msg Template
        template = Template()
        template.set_metadata("performative", "request")
        template.set_metadata("language", "search")

        # Adding the Behaviour with the template will filter all the msg
        self.add_behaviour(b, template) #Este comportamiento solo leera mensajes de este tipo
'''

class Usuario(Agent):
    class EnviarMensajes(CyclicBehaviour):
        ''' User agent class '''
        async def run(self): # Van con async pq es todo concurrentes
            print("[EnviarMensajes Behaviour]:  Initializing...")
            choice = 0
            response = 'show me the time'
            while choice == 0:
                print('llega')
                #response = 'show me the time'
                    
                if response == "show me the time":
                    choice = 1
                elif "Who is" in response:
                    choice = 2
                elif "help" == response:
                    choice = 3
                else: 
                    print("[User Agent] Commant not recognized," ,
                    "you can type 'help' to show all the possible commands")
                    choice = 0
            
            print('aqui')
            if choice == 1:
                pass
            elif choice == 2:
                # Es como un mensaje ACL
                msg = Message(to=data['spade_intro']['username'])     # Instantiate the message
                msg.set_metadata("performative", "resquest")     # Set the "inform" FIPA performative
                msg.set_metadata("language", "search")
                msg.body = str(response[5:])

                await self.send(msg)
                print("Message sent!")

            elif choice == 3:
                self.behav2 = self.HelpBehaviour()
                self.add_behaviour(self.behav2)

        async def on_end(self):
            await self.agent.stop()

    ''' Help behaviour - feedback with the user'''
    class HelpBehaviour(OneShotBehaviour):
        async def run(self):
            print("[Comportamiento HELP] All commands available:",
                "\n\t-show me the time",
                "\n\t-Who is")
    
    async def setup(self):
        print("[User Agent] Agent starting . . .")
        self.behav = self.EnviarMensajes()
        self.add_behaviour(self.behav)
  
def main():

    # Create the agent
    print("Creating Agents ... ")
    chatbot = Usuario(data['spade_intro']['username'], 
                            data['spade_intro']['password'])
    future1 = chatbot.start()
    future1.result()

    #receiveragent = Usuario(data['spade_intro']['username'], 
    #                        data['spade_intro']['password'])
    #future2 = receiveragent.start(auto_register=True)
    #future2.result()


if __name__ == "__main__":
    main()