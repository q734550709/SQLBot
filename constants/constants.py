#教师学生班级课堂表
dmd_classroom_student_h  = '''
CREATE TABLE bdp_dmd.dmd_classroom_student_h (
  classroom_student_id INTEGER PRIMARY KEY COMMENT 主键id
  classroom_id INTEGER COMMENT 教室id, -- 学生上课的教室id
  classroom_code STRING COMMENT 教室code,  -- 学生上课的教室code,和教室id一一对应
  course_id INTEGER COMMENT 课程id, -- 课堂归属的课程id
  course_name STRING COMMENT 课程名称, -- 课堂归属的课程名称
  course_type INTEGER COMMENT 课程类型, -- 课堂归属课程的类型,枚举值有<1:短期课,4:试听课,5:系统课>
  course_year INTEGER COMMENT 课程学年, -- 课堂归属课程的学年
  lesson_id INTEGER COMMENT 课次id, -- 课堂归属的课次id
  lesson_duration INTEGER COMMENT 课次时长, -- 课堂归属的课次时长,单位为秒(s)
  lesson_name STRING COMMENT 课次名, -- 课堂归属的课次名称
  classes_id INTEGER COMMENT 班级id,
  teacher_id INTEGER COMMENT 教师id,
  user_id INTEGER COMMENT 用户id,
  open_time TIMESTAMP COMMENT 计划开课时间, -- 课堂的计划开课时间
  start_time TIMESTAMP COMMENT 课程开始时间 -- 课堂的课程开始时间
  data_dt STRING COMMENT 分区字段, -- 数据同步的截止日期
) COMMENT "课堂学生关系表"; --记录了学生每节课的课堂记录
'''

#学生班级信息表
dw_t_classes_student_h = '''
CREATE TABLE bdp_dw.dw_t_classes_student_h (
  id INTEGER PRIMARY KEY COMMENT 主键id
  classes_id INTEGER COMMENT 班级id, -- 学生所在的班级id
  classes_type STRING COMMENT 班级类型, -- 班级类型,枚举值有<1:短期课班,4:试听课班,5:系统课班>
  status STRING COMMENT 状态, -- 用户在班状态,枚举值有<0:无效,100:有效>
  user_id INTEGER COMMENT 用户id,
  join_class_time TIMESTAMP COMMENT 进入班级时间, -- 用户进入班级的时间
  remove_time TIMESTAMP COMMENT 移出班级时间, -- 用户离开班级的时间
  data_dt STRING COMMENT 分区字段, -- 数据同步的截止日期
) COMMENT "学生班级信息表"; --记录了学生所对应的班级信息
'''

#班级信息表
dim_classes_info_h = '''
CREATE TABLE bdp_dim.dim_classes_info_h (
  classes_id INTEGER PRIMARY KEY COMMENT 班级id, -- 主键id
  classes_code STRING COMMENT 班级code, -- 和班级id一一对应
  classes_type STRING COMMENT 班级类型, -- 班级类型,枚举值有<1:短期课班,4:试听课班,5:系统课班>
  teacher_id INTEGER COMMENT 教师id, --班级对应的教师id
  status STRING COMMENT 状态, -- 班级状态,枚举值有<0:无效,100:有效>
  student_count INTEGER COMMENT 学员数量, -- 班级内的学员数量
  is_closed STRING COMMENT 是否关闭状态, --枚举值有<0:未关闭,1:已关闭>
  data_dt STRING COMMENT 分区字段, -- 数据同步的截止日期
) COMMENT "班级信息表"; --记录了班级信息
'''

#课程信息表
dim_course_info_s = '''
CREATE TABLE bdp_dim.dim_course_info_s (
  course_id INTEGER PRIMARY KEY COMMENT 课程id, -- 主键id
  course_code STRING COMMENT 课程code, -- 和课程id一一对应
  course_type INTEGER COMMENT 课程类型, -- 枚举值有<1:短期课,4:试听课,5:系统课>
  course_year INTEGER COMMENT 课程年份,
  subject_type INTEGER COMMENT 学科类型,
  teaching_method STRING COMMENT 授课方式, --枚举值有<1:直播,2:AI>
  business_region INTEGER COMMENT 课程业务线, --枚举值有<101:火花中国,401:对外汉语>
  levels INTEGER COMMENT 年级,
  data_dt STRING COMMENT 分区字段, -- 数据同步的截止日期
) COMMENT "课程信息表"; --记录了课程信息
'''

#学生信息表
dim_stud_info_h = '''
CREATE TABLE bdp_dim.dim_stud_info_h (
  student_id INTEGER PRIMARY KEY COMMENT 学生id, -- 主键id
  user_id INTEGER COMMENT user_id, -- 和学生id一一对应
  nickname STRING COMMENT 学生昵称,
  data_dt STRING COMMENT 分区字段, -- 数据同步的截止日期
) COMMENT "学生信息表"; --记录了学生信息
'''

#教师信息表
dim_teacher_info_h = '''
CREATE TABLE bdp_dim.dim_teacher_info_h (
  teacher_id INTEGER PRIMARY KEY COMMENT 教师id, -- 主键id
  teacher_name STRING COMMENT 教师姓名,
  teacher_nickname STRING COMMENT 教师昵称,
  employee_id INTEGER COMMENT 雇员id,
  introduce STRING COMMENT 教师介绍, -- 教师的个人介绍
  nature_of_work INTEGER COMMENT 工作性质, -- 枚举值有<1:全职,2:兼职,5:小火苗>
  job_type INTEGER COMMENT 工作性质, -- 枚举值有<1:辅导员,2:教研,3:培训师,4:教师,5:未分配>,其中(1,4)为教师,(3,6,7)为教学职能
  status INTEGER COMMENT 状态, -- 枚举值有<1:在职,0:离职>
  entry_date DATE COMMENT 入职日期,
  data_dt STRING COMMENT 分区字段, -- 数据同步的截止日期
) COMMENT "学生信息表"; --记录了学生信息
'''

#雇员信息表
dim_employee_info_h = '''
CREATE TABLE bdp_dim.dim_employee_info_h (
  employee_id INTEGER PRIMARY KEY COMMENT 雇员id, -- 主键id
  department_first STRING COMMENT 一级部门,
  department_second STRING COMMENT 二级部门,
  department_third STRING COMMENT 三级部门,
  department_fourth STRING COMMENT 四级部门,
  department_fifth STRING COMMENT 五级部门,
  department_sixth STRING COMMENT 六级部门,
  data_dt STRING COMMENT 分区字段, -- 数据同步的截止日期
) COMMENT "雇员信息表"; --记录了公司员工的部门信息
'''

connect_model = \
"""- 主表：bdp_dw.dw_t_classes_student_h (别名：classes_student)
- 左连接：bdp_dim.dim_classes_info_h (别名：classes_info)
- 连接条件：classes_student表的data_dt等于classes_info表的data_dt, classes_student表的classes_id等于classes_info表的classes_id
- 左连接：bdp_dim.dim_course_info_s (别名：course_info)
- 连接条件：classes_info表的course_id等于course_info表的course_id
- 左连接：bdp_dim.dim_teacher_info_h (别名：teacher_info)
- 连接条件：classes_info表的teacher_id等于teacher_info表的teacher_id，classes_info表的data_dt等于teacher_info表的data_dt
- 左连接：bdp_dim.dim_employee_info_h (别名：employee_info)
- 连接条件：employee_info表的employee_id等于teacher_info表的employee_id，employee_info表的data_dt等于classes_student表的data_dt
- 左连接：bdp_dim.dim_teacher_info_h (别名：ti)
- 连接条件：ti表的employee_id等于employee_info表的leader_id，ti表的data_dt等于classes_student表的data_dt
- 左连接：bdp_ads_data_ai_engineering.ads_teacher_comment_s (别名：comments)
- 连接条件：comments表的teacher_id等于teacher_info表的teacher_id，comments表的user_id等于classes_student表的user_id, comments表的create_time的日期小于等于classes_student表的data_dt的日期
"""

select_model = \
"""- 查询字段：从teacher_info表中选择teacher_id（别名"教师id"）, teacher_name（别名"教师姓名"）,
 teacher_rank（别名"教师职级"），教师职级使用以下逻辑来计算：
  - 如果教师职级不等于-1，则将教师职级转换为varchar(10)形式并在其前面加上字母"P"；
  - 如果教师职级等于-1，则将职级标记为"无职级"
- 查询字段：使用CASE语句：
  - 根据teacher_info表nature_of_work的取值，对应值为1：全职，2：兼职，3:全职实习，5：小火苗, 不在上述范围置为null（别名"工作性质"）
  - 根据teacher_info表job_type的取值，对应值为：1:辅导员;2:教研;3:培训师;4:教师; 5:未分配;6:课评师;7:年级组长,不在上述范围置为null；（别名"岗位类型"）
- 查询字段：从ti表中选择teacher_name （别名"上级领导姓名"）
- 查询字段：从employee_info表中选择department_first，department_second，department_third，department_fourth，department_fifth，department_sixth，别名分别为："一级部门","二级部门","三级部门","四级部门","五级部门","六级部门"

- 统计字段：
  - 对classes_student.user_id进行去重计数，别名为："在班人次"
  - 对comments.user_id进行去重计数，别名为："学员评价覆盖数量"
  - 对comments.create_time取最大值，别名为："最后一次评价填写时间"
"""

filter_model = \
"""- 筛选条件：
classes_info表的status不等于0，
classes_student表的status不等于0，
classes_info表的is_closed等于0，
classes_info表的student_count大于0，
course_info表的subject_type等于2，
course_info表的course_type等于5，
course_info表的teaching_method等于1，
course_info表的teaching_mode不等于'2'，
teacher_info表的job_type不在(0,5)，
teacher_info表的status等于1，
teacher_info表的teacher_name不包含'测试'，
teacher_info表的teacher_nickname不包含'测试'，
teacher_info表的introduce不包含'测试'，
teacher_info表的grade_name不包含'测试'，
classes_student表的data_dt等于'2023-06-27'
"""

groupby_model = \
"""- 分组：teacher_info表的teacher_id, teacher_name, teacher_rank，teacher_rank使用以下逻辑来计算：
  - 如果teacher_rank不等于-1，则将teacher_rank转换为varchar(10)形式并在其前面加上字母"P"；
  - 如果teacher_rank等于-1，则将teacher_rank标记为"无职级"
- 分组：使用CASE语句：
  - teacher_info表nature_of_work的取值，对应值为1：全职，2：兼职，3:全职实习，5：小火苗, 不在上述范围置为null
  - teacher_info表job_type的取值，对应值为：1:辅导员;2:教研;3:培训师;4:教师; 5:未分配;6:课评师;7:年级组长,不在上述范围置为null；
- 分组：ti表的teacher_name
- 分组：employee_info表的department_first，department_second，department_third，department_fourth，department_fifth，department_sixth
"""

#设置常量
constants = {

    # 创建列名称
    'database_columns': ["database", "table", "tableinfo", "tabledetail"],

    #添加库表信息
    'database_datalist' : [
                ['bdp_dmd',
                'dmd_classroom_student_h',
                '课堂班级课程学生教师对应关系表',
                dmd_classroom_student_h
                ],
                ['bdp_dw',
                'dw_t_classes_student_h',
                '学生班级信息表',
                dw_t_classes_student_h
                ],
                ['bdp_dim',
                'dim_stud_info_h',
                '学生信息表',
                dim_stud_info_h
                ],
                ['bdp_dim',
                'dim_classes_info_h',
                '班级信息表',
                dim_classes_info_h
                ],
                ['bdp_dim',
                'dim_course_info_s',
                '课程信息表',
                dim_course_info_s
                ],
                ['bdp_dim',
                'dim_teacher_info_h',
                '教师/老师信息表',
                dim_teacher_info_h
                ],
                ['bdp_dim',
                'dim_employee_info_h',
                '雇员/员工信息表',
                dim_employee_info_h
                ]
            ],

    #口径定义说明
    'data_scope_definition' : '''在班学员: bdp_dim.dim_classes_info_h中的status=100;''',

    #设置SQL模板
    'model_example_list' : [
        [
            '''- 主表：Customers (别名：c)
            - 左连接：Orders (别名：o)
            - 连接条件：c的id等于o表的customerId''',
            '''- 查询字段：从c表中选择name（别名"Customers"）''',
            '''- 筛选条件：o表的customerId不为null;''',
            ''
        ],
        [
            '- 主表：Scores',
             '''- 查询字段：从Scores表中选择Score,
             - 统计字段：对Score进行密集排名(排名不跳过)，排名顺序为对Score倒序，别名为：Rank''',
             '',
             ''
        ],
        [connect_model,select_model,filter_model,groupby_model]

    ],

    #自然语言问题例子
    'question_examples' : [
        "今天天气怎么样？",
        "查询老师的入职日期，以及距今天数",
        "查询每个老师的第一节试听课的上课时间",
        "查询每个老师至今上课次数，以及上课的小时数",
        "查询当前公司每个部门的人数，并给出一级部门到六级部门的名称",
        "查询当前每个系统班班级的在班学员人数",
        "查询当前在职教师的id、昵称、一级到六级部门名称、入职时间",
        "我想知道最近一次订单的付款时间"
        ]
}
