from src.plan.sql_generation import *

if __name__ == "__main__":
    user_input = '查询教师id'
    result, context = process_user_message(user_input,[])
    print(result,'\n',context)
