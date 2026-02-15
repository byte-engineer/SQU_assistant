from modules.speaker import Speaker
from modules.brain import Brain
from modules.visuals import Visuals
# These would be your other files
# from modules.listener import Listener 
# from modules.speaker import Speaker

def main():
    brain = Brain(model="gemma3")
    speaker = Speaker()
    visuals = Visuals()
    
    print("SQU Assistant Starting...")
    
    while True:
        # 1. State: IDLE / Wait for Wake Word
        visuals.show("idle")
        # wake_word_detected = listener.wait_for_keyword()
        
        # 2. State: LISTEN
        # user_text = listener.listen_and_transcribe()
        user_text = input("Temporary Console Input: ") # Mock for testing

        # 3. State: THINK
        visuals.show("thinking")
        response = brain.query(user_text)
        print(f"Assistant: {response}")
        
        
        # 4. State: SPEAK
        visuals.show("speaking")
        speaker.say(response)

if __name__ == "__main__":
    main()