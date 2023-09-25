import openai
from src.get_completion_from_messages import get_completion_from_messages
#详细解释
def sql_explain(user_input,
                model="gpt-3.5-turbo-16k",
                temperature=0,
                max_tokens=3000):
    system_message = """
    详细解释用户提供的SQL语句：
    """

    messages =  [
        {'role':'system', 'content': system_message},
        {'role':'user', 'content': user_input},
        ]

    response = get_completion_from_messages(messages,
                    model,
                    temperature,
                    max_tokens)

    return response

#自然语言解释
def sql_translate(user_input,
                  model="gpt-3.5-turbo-16k",
                  temperature=0,
                  max_tokens=3000):
    system_message = """
    将下面的SQL语句翻译为自然语言：
    """

    messages =  [
        {'role':'system', 'content': system_message},
        {'role':'user', 'content': user_input},
        ]

    response = get_completion_from_messages(messages,
                    model,
                    temperature,
                    max_tokens)

    return response

#模型选择函数
def function_select(input_text,
                    model,
                    temperature,
                    max_token,
                    flag = False):
    if flag:
        response = sql_explain(input_text,model,temperature,max_token)
        return response
    else:
        response = sql_translate(input_text,model,temperature,max_token)
        return response
