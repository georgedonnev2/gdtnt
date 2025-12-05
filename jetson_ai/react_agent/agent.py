import re
import json
from react_agent.LLM import RequestLLM

class ReactAgent:

    def __init__(self, model: RequestLLM) -> None:
        # 提示词
        self.THOUGHT = '✿Thought✿'
        self.ACTION = '✿Action✿'
        self.ACTION_INPUT = '✿Action input✿'
        self.OBSERVATION = '✿Observation✿'
        self.FINAL_ANSWER = '✿Final Answer✿'
        self.FN_STOP_WORDS = [self.OBSERVATION, self.OBSERVATION+':', self.OBSERVATION+':\n']

        self.functions = {}
        self.FN_CALL_TEMPLATE_ZH = """
        尽你所能回答以下问题。如果合适的话,你可以适当地使用一些工具。
        你可以使用以下工具:
        {tool_descs}
        使用以下格式:
        Question: 
        你必须回答的输入问题，由用户输入。
        ✿Thought✿
        你应该始终思考要做什么以及是否使用什么工具。
        ✿Action✿
        要使用的工具名称，应该是[{tool_names}]中的一个
        ✿Action input✿
        工具的输入参数
        ✿Observation✿
        行动的结果
        ... (这个✿Thought✿/✿Action✿/✿Action input✿/✿Observation✿可以重复零次或多次)
        ✿Thought✿
        我现在知道最终答案了
        ✿Final Answer✿
        对原始输入问题的最终答案

        额外要求提示: 
        1. 你回应使用的语言应该与用户使用的语言保持一致。
        """

        self.tool_descs_template = '\n\n工具名称及描述: {func_name}: {description_for_func} || 该工具需要输入参数：{parameters} || 该工具参数的额外要求: {requirement}\n\n'
        self.model = model

    # 注册工具
    def register_tool(self, name, cls):
        self.functions[name] = {
            'function': cls().call,
            'description': cls.description,
            'parameters': cls.parameters,
            'requirement': cls.requirement,
        }

    # 更新sys_message
    def update_system_message(self, messages):
        tool_descs = '\n'.join([
            self.tool_descs_template.format(
                func_name=name,
                description_for_func=tool['description'],
                parameters=json.dumps(tool['parameters'], ensure_ascii=False),
                requirement=tool['requirement']
            ) for name, tool in self.functions.items()
        ])
        tool_names = ', '.join(self.functions.keys())
        sys_message = [
            {
                'role': 'system', 
                'content': self.FN_CALL_TEMPLATE_ZH.format(
                    tool_descs=tool_descs,
                    tool_names=tool_names
                )
            }
        ]
        return sys_message + messages

    # 移除特殊字符
    def remove_special_tokens(self, text, strip=True):
        text = text.replace('✿:', '✿')
        text = text.replace('✿：', '✿')
        out = ''
        is_special = False
        for c in text:
            if c == '✿':
                is_special = not is_special
                continue
            if is_special:
                continue
            out += c
        if strip:
            out = out.lstrip('\n').rstrip()
        return out
    
    def extract_function_and_args(self, input_str):
        # print(input_str)
        # 使用正则表达式提取函数名
        function_match = re.search(r'✿Action✿\s*(\w+)', input_str)
        if not function_match:
            return "", {}
        function_name = function_match.group(1)

        # 使用正则表达式提取参数部分
        args_match = re.search(r'✿Action input✿\s*(\{.*?\})', input_str, re.DOTALL)
        args_str = args_match.group(1)

        try:
            # 解析参数字符串为字典
            args_dict = json.loads(args_str)
        except json.JSONDecodeError as e:
            return function_name, {}

        return function_name, args_dict
    
    # 对话
    def chat(self, messages):
        messages = self.update_system_message(messages)
        while True:
            response = self.model.chat_stream(
                messages=messages,
                stop=self.FN_STOP_WORDS
            )
            
            current_message = ""
            for chunk in response:
                current_message += chunk
                yield chunk.replace('✿', '**')

            fn_name, fn_args = self.extract_function_and_args(current_message)
            if fn_name == "" or "Final Answer" in current_message:
                break  # 如果没有函数调用或已经得到最终答案，退出循环
            
            if fn_name in self.functions:
                res_func = self.functions[fn_name]['function'](**fn_args)
                yield f"""**Observation**:\n{res_func}\n"""

                prompt = f"""
                ✿Action✿: {fn_name}
                ✿Action input✿: {fn_args}
                ✿Observation✿: {res_func}
                """
                messages.append({
                    'role': 'user',
                    'content': prompt
                })
            else:
                yield "**Final Answer**: 调用工具出现异常，请重试"
                break

                