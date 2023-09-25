import openai
from src.get_completion_from_messages import get_completion_from_messages
from src.plan.content_moderation import content_moderation, is_query_question
from constants.constants import constants

# 解包constant中的常量
locals().update(constants)


# 定义一个函数，返回列表中某个值的最后一个出现的索引
def rindex(lst, value):
    """
    返回列表中某个值的最后一个出现的索引。

    lst: 一个列表，我们将在其中搜索。
    value: 一个字符串值，我们要在列表中查找它的最后一个出现的位置。
    """
    try:
        return len(lst) - lst[::-1].index(value) - 1
    except ValueError:
        raise ValueError(f"这个字符`{value}`未出现")

# 定义生成候选补全的函数
def get_candidates(
    messages,
    model = 'gpt-3.5-turbo-16k',
    temperature = 0,
    max_tokens = 3000,
    n = 3,
    stop = [';'],
    ):

    prefix = 'SELECT '

    # 使用 OpenAI 完成接口生成响应
    response = openai.ChatCompletion.create(
        model=model,
        messages = messages,
        temperature=temperature,
        n=n,
        stop=stop,
        max_tokens=max_tokens,
    )
    # 将生成的响应与指定的前缀组合
    responses = [prefix + choice.message.content for choice in response.choices]
    return responses

# 评估候选答案得分
def eval_candidate(
    candidate_answer,
    nl_query,
    engine = 'text-davinci-003',
    ):

    eval_template = "{};\n--上述查询的易于理解的解释为\n-- {}"
    prompt = eval_template.format(candidate_answer, nl_query)

    answer_start_token = "--"

    # 使用 OpenAI 完成接口生成响应
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt, #评估模板，填入生成结果，查询语句
        temperature=0,
        max_tokens=0, #设置为0，不会耗费token
        logprobs=1, #设置为1，是因为只需要判断当前已有prompt的概率，无需生成新结果
        echo=True, #设置为True，可以实现对prompt进行对数概率计算
    )

    # 获取答案开始的索引
    answer_start = rindex(
        response["choices"][0]["logprobs"]["tokens"], answer_start_token
    )

    #计算原始查询语句通过LLM模型计算出的平均对数概率（越大越好）
    logprobs = response["choices"][0]["logprobs"]["token_logprobs"][answer_start + 1 :]
    return sum(logprobs) / len(logprobs)

# 反向翻译，根据自然语言指令生成一系列的SQL查询，并选择最佳的一个。
def backtranslation(
    nl_query,
    messages,
    model = 'gpt-3.5-turbo-16k',
    temperature = 0,
    max_tokens = 3000,
    n = 3,
    stop = [';'],
    ):

    candidates = [] #用于存放待评估项及得分

    responses = get_candidates(messages = messages,
                               model = model,
                               temperature = temperature,
                               max_tokens = max_tokens,
                               n = n,
                               stop = stop
                               )

    for i in range(n):
        quality = eval_candidate(
            responses[i],
            nl_query,
        )
        candidates.append((responses[i], quality))

    # 根据评估得分对候选项进行排序
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[0][0]

# 定义一个处理用户消息的函数
def process_user_message(user_input,
                         all_messages,
                         model = 'gpt-3.5-turbo-16k',
                         temperature = 0,
                         max_tokens = 3000,
                         hive_select='hive',
                         is_current_table = True,
                         data_scope_definition = data_scope_definition,
                         database_datalist = database_datalist
                        ):
    delimiter = "####"  # 定义一个分隔符

    # 步骤1：检查输入是否涉及有害语句或不属于查询问题
    check_error = (content_moderation(user_input) == 1
                    or is_query_question(user_input) == 'N')

    # 如果输入被标记了
    if check_error:
        all_messages+= [(user_input,"对不起，您的问题不是一个查询问题，请重新输入")]
        return "", all_messages  # 返回错误消息

    # 步骤2：从字符串中提取产品列表

    database_df = pd.DataFrame(database_datalist,columns=database_columns)
    database_and_table_str = query_table_info(
                                             user_message = user_input,
                                             model = model,
                                             temperature = temperature,
                                             max_tokens = max_tokens,
                                             database_datalist = database_datalist
                                             )
    database_and_table_list = read_string_to_list(database_and_table_str)

    # 步骤3：如果找到了库表信息，查找表字段信息
    database_and_table_info = generate_table_info(database_and_table_list,database_datalist)
    if database_and_table_info == "" and is_current_table:
        all_messages+= [(user_input,"对不起，未查到相关表信息")]
        return "", all_messages

    # 步骤4：回答用户的问题
    # 定义系统消息
    system_message = f"""
    给定以下SQL表格信息，你的工作是根据用户的请求编写{hive_select} SQL查询,
    相关的口径定义为：{data_scope_definition}

    注意你编写的SQL代码需要符合{hive_select} SQL函数的语法要求
    """

    prefix = 'SELECT '

    nl_query = f"{delimiter}{user_input}{delimiter}"

    history_prompt = []

    for turn in all_messages:
        user_message, bot_message = turn
        history_prompt += [
                {'role': 'user', 'content':user_message},
                {'role': 'assistant', 'content': bot_message}
                         ]

    # 创建消息列表，包括系统消息、用户消息和助手消息
    messages = [
        {'role': 'system', 'content': system_message}] \
        + history_prompt + \
        [{'role': 'assistant', 'content': database_and_table_info},
        {'role': 'user', 'content': nl_query+prefix}
        ]

    # 根据消息生成完成的回复
    final_response = backtranslation(
                nl_query = nl_query,
                messages = messages,
                model = model,
                temperature = temperature,
                max_tokens = max_tokens,
                )

    all_messages+= [(user_input,final_response)]

    return "", all_messages  # 返回最终回复和所有消息
