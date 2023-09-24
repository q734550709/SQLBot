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


# 创建列名称
database_columns=["database", "table", "tableinfo", "tabledetail"]

#添加信息
database_datalist = [
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
        ]

#口径定义说明
data_scope_definition = \
'''在班学员: bdp_dim.dim_classes_info_h中的status=100;'''
