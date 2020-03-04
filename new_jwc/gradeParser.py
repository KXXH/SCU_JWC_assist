import logging


class GradeParser:
    def __init__(self, provider):
        self.provider = provider

    def parse(self, filter=lambda x: True):
        gradeList = self.provider.get_grade()
        grades = sorted(gradeList, key=lambda x: x.term)
        logging.debug(grades)
        res = {}
        for grade in grades:
            if filter(grade):
                res.setdefault(
                    grade.name, (grade.score.to_num(), grade.credit))
        return res
