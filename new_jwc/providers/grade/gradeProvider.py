import logging
from typing import Iterable
from abc import abstractmethod
from ...entity.gradeRecord import GradeRecord, CourseType
from ...entity.score import NumericScore, LevelScore, FormerLevelScore, FormerNumericScore
from ...entity.exam import ExamType


class GradeFilter:
    @abstractmethod
    def validate(self, grade_record: GradeRecord)->bool:
        """判断该成绩是否应该被视为有效的记录
        True表示应该被列为记录
        """


class DefaultFilter(GradeFilter):
    def validate(self, grade_record):
        return True


class FirstFilter(GradeFilter):
    """该过滤器在初始化后，仅允许第一次出现的课程号的成绩
    """

    def __init__(self):
        self.s = set()

    def validate(self, grade_record):
        if grade_record.course_num not in self.s:
            self.s.add(grade_record.course_num)
            return True
        return False


class AllGradeProvider:
    '''提供全部的成绩数据，包括多次选修
    '''
    ALL_SCORES_DATA = "http://zhjw.scu.edu.cn/student/integratedQuery/scoreQuery/allTermScores/data"

    def __init__(self, auth_provider):
        self.session = auth_provider.login()

    def get_grade(self)->Iterable:
        logging.info("正在获取全部成绩信息...")
        r = self.session.post(self.ALL_SCORES_DATA, data={
            "pageNum": 1,
            "pageSize": 999
        })
        grade_info = r.json()
        logging.debug(grade_info)
        try:
            for grade in grade_info["list"]["records"]:
                term = grade[0]
                yield GradeRecord(
                    term=grade[0],
                    course_num=grade[1],
                    course_index=grade[2],
                    name=grade[11],
                    en_name=grade[12],
                    credit=grade[13],
                    hour_num=grade[14],
                    score_num=grade[8],
                    score_level=grade[17],
                    course_type=CourseType(grade[15]),
                    exam_type=ExamType(grade[16])
                )
        except KeyError as e:
            raise e


class GradeProvider(AllGradeProvider):
    def __init__(self, auth_provider, filter=DefaultFilter(), *args, **kwargs):
        super().__init__(auth_provider, *args, **kwargs)
        self.filter = filter

    def get_grade(self):
        all_grades = super().get_grade()
        for grade in all_grades:
            if self.filter.validate(grade):
                yield grade


class OrderedGradeProvider(GradeProvider):
    '''有序的成绩清单。默认为按照学期排序
    '''

    def __init__(self, auth_provider, filter=DefaultFilter(), key=lambda x: x.term, *args, **kwargs):
        super().__init__(auth_provider, filter=DefaultFilter(), *args, **kwargs)
        self.key = key

    def get_grade(self) -> Iterable:
        all_grades = sorted(super().get_grade(), key=self.key)
        for grade in all_grades:
            if self.filter.validate(grade):
                yield grade


class FirstGradeProvider(OrderedGradeProvider):
    '''按照教务处核算均分时的标准，所有成绩以第一次修读为准，同一课程号只能出现一次
    '''

    def __init__(self, auth_provider, filter=DefaultFilter(), key=lambda x: x.term, *args, **kwargs):
        super().__init__(auth_provider, filter=FirstFilter(), *args, **kwargs)
        self.key = key
