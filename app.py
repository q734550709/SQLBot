import gradio as gr
from src.plan.content_moderation import *
from src.plan.get_table_info import *
from src.plan.text_to_sql import *
from src.analysis.sql_observation import *
from src.generate.sql_generation import *
from src.study.answer_evaluation import *
from constants.constants import constants

# 解包constant中的常量
locals().update(constants)

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=4):
            gr.Markdown('# SQLBot - 一个基于LLMs的SQL学习和工作平台')
        with gr.Column(scale=1):
            apikey_text = gr.Textbox(type='password',label='请输入api_key:')
    with gr.Tab("通过自然语言生成SQL代码"):
        with gr.Row():
            with gr.Column(scale=4):
                chatbot = gr.Chatbot(bubble_full_width=False,show_label=True,show_copy_button=True)
                input_text = gr.Textbox(lines=6,label="请输入查询语句",show_label=True,show_copy_button=True)
                user_button = gr.Button(value='确认输入')
                clear = gr.ClearButton([input_text, chatbot],value="清除对话")
            with gr.Column(scale=1):
                with gr.Accordion(label='模型设置',open=False):
                    model_select = gr.Dropdown(
                                choices=["gpt-3.5-turbo-16k","gpt-3.5-turbo"],
                                value='gpt-3.5-turbo',
                                label='选择模型'
                                )
                    temperature = gr.Slider(minimum=0, maximum=1,value=0,label='temperature')
                    maxtoken = gr.Slider(minimum=0, maximum=3000, value=300,label='max_token')
                hive_select = gr.Dropdown(
                            choices=["hive","presto","mysql"],
                            value='hive',
                            label='选择SQL语言类型'
                            )
                is_current_table = gr.Checkbox(label='根据现有库表查询',value=True)
                data_definition = gr.Textbox(lines=2,
                                                   max_lines=6,
                                                   value=data_scope_definition,
                                                   label="输入涉及的字段定义")
                gr.Examples(
                        examples=question_examples,
                        inputs=input_text,
                        label='可选例子'
                        )

        with gr.Row():
            with gr.Accordion(label="相关库表信息：",open=False):
                data_df = gr.Dataframe(
                    headers=database_columns,
                    type="array",
                    row_count=9,
                    col_count=(4, "fixed"),
                    max_rows="infinite",
                    value=database_datalist
                )

        user_button.click(fn=process_user_message,
                       inputs=[input_text,
                               chatbot,
                               model_select,
                               temperature,
                               maxtoken,
                               hive_select,
                               is_current_table,
                               data_definition,
                               data_df
                              ],
                       outputs=[input_text,chatbot])

    with gr.Tab("对SQL代码进行文字说明"):
        with gr.Row():

            with gr.Column(scale=2):
                sql_text = gr.Textbox(lines=21,label="输入SQL代码")
                sql_button = gr.Button('确认输入')

            with gr.Column(scale=2):
                output_text = gr.Textbox(lines=24,label="输出",
                                         show_label=True,show_copy_button=True,
                                        )
            with gr.Column(scale=1):
                with gr.Accordion(label='模型设置',open=False):
                    model_select = gr.Dropdown(
                                choices=["gpt-3.5-turbo-16k","gpt-3.5-turbo"],
                                value='gpt-3.5-turbo',
                                label='选择模型'
                                )
                    temperature = gr.Slider(minimum=0, maximum=1,value=0,label='temperature')
                    maxtoken = gr.Slider(minimum=0, maximum=3000, value=300,label='max_token')
                hive_select = gr.Dropdown(
                            choices=["hive","presto","mysql"],
                            value='hive',
                            label='选择SQL语言类型'
                            )
                translate_select = gr.Checkbox(label='需要详细解释')

            sql_button.click(fn=function_select,
                           inputs=[sql_text,
                                   model_select,
                                   temperature,
                                   maxtoken,
                                   translate_select
                                  ],
                           outputs=output_text)

    with gr.Tab("输入prompt模板生成SQL代码"):
        with gr.Row():
            with gr.Column(scale=2):
                merge_text = gr.Textbox(lines=21,label="prompt模板")
                generation_button = gr.Button('确认输入')
            with gr.Column(scale=2):
                output_text = gr.Textbox(lines=24,label="SQL结果",show_label=True,show_copy_button=True)
            with gr.Column(scale=1):
                with gr.Accordion(label='模型设置',open=False):
                    model_select = gr.Dropdown(
                                choices=["gpt-3.5-turbo-16k","gpt-3.5-turbo"],
                                value='gpt-3.5-turbo',
                                label='选择模型'
                                )
                    temperature = gr.Slider(minimum=0, maximum=1,value=0,label='temperature')
                    maxtoken = gr.Slider(minimum=0, maximum=3000, value=300,label='max_token')
                hive_select = gr.Dropdown(
                            choices=["hive","presto","mysql"],
                            value='hive',
                            label='选择SQL语言类型'
                            )

                connect_input = gr.Textbox(lines=2,max_lines=4,label="输入链接词模板")
                select_input = gr.Textbox(lines=2,max_lines=4,label="输入选择词模板")
                filter_input = gr.Textbox(lines=2,max_lines=4,label="输入筛选词模板")
                groupby_input = gr.Textbox(lines=2,max_lines=4,label="输入分组词模板")

        gr.Examples(
                    examples=model_example_list,
                    inputs=[connect_input,select_input,filter_input,groupby_input],
                    label='可选例子'
                    )
        connect_input.change(fn=merge_textbox,
                           inputs=[connect_input,
                                   select_input,
                                   filter_input,
                                   groupby_input],
                           outputs=merge_text)
        select_input.change(fn=merge_textbox,
                           inputs=[connect_input,
                                   select_input,
                                   filter_input,
                                   groupby_input],
                           outputs=merge_text)
        filter_input.change(fn=merge_textbox,
                           inputs=[connect_input,
                                   select_input,
                                   filter_input,
                                   groupby_input],
                           outputs=merge_text)
        groupby_input.change(fn=merge_textbox,
                           inputs=[connect_input,
                                   select_input,
                                   filter_input,
                                   groupby_input],
                           outputs=merge_text)

        generation_button.click(fn=sql_generation,
                           inputs=[merge_text,
                                   model_select,
                                   temperature,
                                   maxtoken,
                                   hive_select],
                           outputs=output_text)

    with gr.Tab("SQL代码练习题"):
        with gr.Row():
            with gr.Column(scale=2):
                title_url_text = gr.Markdown()
                question_text = gr.Textbox(lines=5,max_lines=10,label="题目")
                example_text = gr.Textbox(lines=8,max_lines=10,label="示例")

            with gr.Column(scale=4):
                chatbot = gr.Chatbot(bubble_full_width=False,show_label=True,show_copy_button=True)
                input_text = gr.Textbox(lines=6,label="请输入SQL语句",show_label=True,show_copy_button=True)
                user_button = gr.Button(value='确认输入')
                clear = gr.ClearButton([input_text, chatbot],value="清除对话")

            with gr.Column(scale=1):
                with gr.Accordion(label='模型设置',open=False):
                    model_select = gr.Dropdown(
                                choices=["gpt-3.5-turbo-16k","gpt-3.5-turbo"],
                                value='gpt-3.5-turbo',
                                label='选择模型'
                                )
                    temperature = gr.Slider(minimum=0, maximum=1,value=0,label='temperature')
                    maxtoken = gr.Slider(minimum=0, maximum=3000, value=300,label='max_token')
                difficulty_select = gr.Dropdown(
                            choices=["简单","中等","困难"],
                            label='选择题目难度'
                            )
                with gr.Accordion(label="参考答案：",open=False):
                    answer_text = gr.Textbox(lines=10,label="答案")
                    answer_explain_text = gr.Markdown()

            difficulty_select.change(fn=question_choice,
                               inputs=[difficulty_select],
                               outputs=[title_url_text,
                                        question_text,
                                        example_text,
                                        answer_text,
                                        answer_explain_text])

            user_button.click(fn=answer_evaluation,
                              inputs=[input_text,
                                      chatbot,
                                      question_text,
                                      answer_text,
                                      model_select,
                                      temperature,
                                      maxtoken
                                     ],
                              outputs=[input_text,chatbot]
                             )

    apikey_text.change(fn=get_api_key,inputs= apikey_text)


if __name__ == "__main__":
    demo.launch()
