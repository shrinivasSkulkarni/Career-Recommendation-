from transformers import pipeline

class ResumeOptimizer:
    def __init__(self):
        # Use PyTorch as the backend
        self.nlp = pipeline("text-generation", model="distilgpt2", framework="pt")

    def optimize(self, text):
        # Generate optimized resume text
        return self.nlp(text, max_length=50)[0]['generated_text']