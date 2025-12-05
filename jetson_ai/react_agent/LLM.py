import openai


# 移除上下文管理
class RequestLLM:

    def __init__(self, base_url, model_name) -> None:
        self.base_url = base_url
        self.model_name = model_name
        self.client = openai.OpenAI(base_url=self.base_url, api_key='EMPTY')

    def chat_nostream(self, messages, stop=[]):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            stream=False,
            stop=stop
        )

        current_content = response.choices[0].message.content
        return current_content
    
    def chat_stream(self, messages, stop=[]):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            stream=True,
            stop=stop
        )
        
        for chunk in response:
            tmp = chunk.choices[0].delta.content
            yield tmp