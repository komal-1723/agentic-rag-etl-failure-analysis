"""
ollama_client.py

Handles communication with the local Ollama Llama3 model.

Requirements:
    pip install ollama

Before running:

    ollama serve
    ollama pull llama3

Author: Komal K Project
"""

import ollama


class OllamaClient:
    """
    Wrapper around Ollama chat API.
    """

    def __init__(
        self,
        model: str = "llama3",
        temperature: float = 0.2,
    ):
        self.model = model
        self.temperature = temperature

    def generate(self, prompt: str) -> str:
        """
        Sends prompt to Ollama and returns response text.
        """

        try:

            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                options={
                    "temperature": self.temperature,
                },
            )

            return response["message"]["content"]

        except Exception as e:
            raise RuntimeError(
                f"Ollama request failed: {str(e)}"
            )

    def health_check(self) -> bool:
        """
    Checks whether Ollama is running and the model exists.
    """

        try:

            models = ollama.list()

            print(models)      # Temporary debugging

            return True

        except Exception as e:

            print(e)

            return False


# ----------------------------------------------------
# Test
# ----------------------------------------------------

if __name__ == "__main__":

    client = OllamaClient()

    print("=" * 60)
    print("Checking Ollama...")
    print("=" * 60)

    if not client.health_check():

        print("\nERROR")
        print("Ollama is not running or llama3 is not installed.")
        print("\nRun:")
        print("    ollama serve")
        print("    ollama pull llama3")
        exit()

    print("SUCCESS")
    print("Ollama is ready.")

    print("\nSending prompt...\n")

    prompt = """
You are an ETL expert.

Current Error:
Unable to connect to database.

Give:
Pipeline Status
Category
Severity
Confidence
Root Cause
Recommendations
"""

    answer = client.generate(prompt)

    print("=" * 60)
    print("LLAMA RESPONSE")
    print("=" * 60)
    print(answer)