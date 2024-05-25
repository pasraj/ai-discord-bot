from config import get_settings
from openai import OpenAI
import json

settings = get_settings()

client = OpenAI(api_key=settings.open_ai_key)
assistant_id = settings.assistant_id

class GPT:
    """
    GPT class to interact with OpenAI's GPT models.
    """

    @staticmethod
    def get_answer(query: str, thread_id: str = None) -> str:
        """
        Get an answer from the GPT model for a given query.
        
        Args:
            query (str): The input query to the GPT model.
            thread_id (str, optional): The thread ID to continue the conversation. Defaults to None.
        
        Returns:
            str: The response from the GPT model.
        """
        try:
            if not thread_id:
                thread = client.beta.threads.create()
                thread_id = thread.id

            # Send the user's message to the thread
            client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=query
            )

            # Create and poll the run
            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=assistant_id
            )

            # If the run is completed, get the response message
            if run.status == 'completed':
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                message_json = messages.model_dump_json()
                response_data = json.loads(message_json)
                response = response_data['data'][0]["content"][0]["text"]["value"]
                return response
            else:
                return "Run did not complete successfully."
        except Exception as e:
            return f"An error occurred: {e}"

