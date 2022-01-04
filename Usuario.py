import json
import time
import datetime # time
import scraper # web scrapping
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import asyncio

# Load the json file with the crendentials
f = open('credenciales.json',)
data = json.load(f)

class SenderAgent(Agent):

    class Peticiones(CyclicBehaviour):
        async def run(self):
            choice = 0

            while choice == 0:
                response = input("\nHow can I help you?: ")
                print("-You say ", response)
                if response in "show me the time":
                    choice = 1
                    
                elif "who is" in response:
                    choice = 2
                elif "file" == response:
                    choice = 3
                    
                elif "help" == response:
                    print("This is a list with all commands available: "
                    "\n\t - show me the time"
                    "\n\t - who is 'famous person'"
                    "\n\t - file"
                    "\n\t - help")
                elif "exit" == response:
                    pass
                else: 
                    print("[User Agent] Commant not recognized," ,
                    "you can type 'help' to show all the possible commands")
            
            if choice == 1:
                
                msg = Message(to=data['spade_intro_2']['username'], sender=data['spade_intro']['username'])
                msg.set_metadata("performative", "request")
                msg.set_metadata("protocol", "current_time")
                msg.body = "time"

                await self.send(msg)
                
                print("..................................................................................................")
                

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
                            "\n Example: file.txt | maria/University/Multiagent/file.txt \nType: ")

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
            await asyncio.sleep(1)

    async def setup(self):
        print("[User Agent] "+str(self.jid)+ " started")
        petis = self.Peticiones()
        self.add_behaviour(petis)

class ReceiverAgent(Agent):
    class TimeBehav(CyclicBehaviour):
        ''' 
        
        '''
        async def run(self):

            msg = await self.receive()
            if msg:
                print("-Bot say: The time is ",datetime.datetime.now())
                print("..................................................................................................")

    class WhoIs(CyclicBehaviour):
        ''' 
        
        '''
        async def run(self):

            msg = await self.receive()
            if msg:
                print("-Bot say: ", scraper.who_is(msg.body))
                print("..................................................................................................")
        
    class CreateFile(CyclicBehaviour):
        ''' 
        
        '''
        async def run(self):

            msg = await self.receive() 
            if msg:
                print("-Bot say: writing file...")
                body = (msg.body).split(" ")
                file = open(f'{body[0]}', "w")
                file.write(' '.join(body[1:]))
                file.close()
                print("-Bot say: File created successfully")
                print("..................................................................................................")

    async def setup(self):

        def __create_template__(protocol):
            template = Template()
            template.sender = data['spade_intro']['username']
            template.to = data['spade_intro_2']['username']
            template.metadata = {"performative": "request", "protocol":protocol}

            return template

        print("[Receiver Agent] "+str(self.jid)+ " started")
        time = self.TimeBehav()
        whois = self.WhoIs()
        file = self.CreateFile()
        # Msg Template
        template_time = __create_template__("current_time")
        template_whois = __create_template__("who_is")
        template_file = __create_template__("file")
        #print(template)
        # Adding the Behaviour with the template will filter all the msg
        self.add_behaviour(time, template_time) #Este comportamiento solo leera mensajes de este tipo
        self.add_behaviour(whois, template_whois)
        self.add_behaviour(file, template_file)
'''

    Método main:
        Inicialización de los agentes Emisor y Receptor.

'''
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
