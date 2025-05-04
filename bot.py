
# Dubai AI Bot - Phase 3 Upgrade (placeholder code)
# Improved follow-up handling logic (to be replaced by real bot code)

class DubaiAIBot:
    def __init__(self):
        self.memory = []
    
    def respond(self, user_input):
        # Memory based simple logic simulation
        self.memory.append(user_input)
        if len(self.memory) > 3:
            self.memory.pop(0)
        
        if "price" in user_input.lower() or "cost" in user_input.lower():
            return "The cost may vary based on the options available. Could you please specify more details so I can assist better?"
        elif "where" in user_input.lower():
            return "It is located in Dubai. Can you please specify which place you are referring to?"
        elif "it free" in user_input.lower():
            return "Some attractions are free while others may require tickets. Let me know which one you mean."
        else:
            return "Sure! I can help you with that. Can you please give me a little more detail?"

# End of placeholder bot logic
