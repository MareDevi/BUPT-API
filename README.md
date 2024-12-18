# BPUT API for ucloud
注：bupt_auth来自于https://github.com/Lynnette177/BUPT-AUTH

## 接口信息

### get_courses()

获取当前学生的课程列表。

---

### get_course_detail(course_id)

获取指定课程的详细信息。

**参数：**

- `course_id`：课程ID。

---

### get_course_files(course_id)

获取指定课程的文件列表。

**参数：**

- `course_id`：课程ID。

---

### get_assignments(course_id)

获取指定课程的作业列表。

**参数：**

- `course_id`：课程ID。

---

### get_assignment_detail(assignment_id)

获取指定作业的详细信息。

**参数：**

- `assignment_id`：作业ID。

---

### get_todo_list()

获取当前学生的待办列表。

---

### download_file(file_name, storage_id, file_format)

下载指定的文件。
注：参数要与get_course_files等接口返回的信息一致

**参数：**

- `file_name`：要保存的文件名。
- `storage_id`：文件的存储ID。
- `file_format`：文件格式。

