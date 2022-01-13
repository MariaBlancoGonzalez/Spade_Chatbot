import json
import time
import ReceiverAgent
import SenderAgent


# Load the json file with the crendentials
f = open(f'../credenciales.json',)
data = json.load(f)


"""

    Método main:
        Inicialización de los agentes Emisor (USUARIO) y Receptor (CHATBOT).

"""
def main():
    
    print("Creating Agents... ")

    receiveragent = ReceiverAgent.ReceiverAgent(data['spade_intro_2']['username'], 
                            data['spade_intro_2']['password'])
    future = receiveragent.start()
    future.result()
    

    senderagent = SenderAgent.SenderAgent(data['spade_intro']['username'], 
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
