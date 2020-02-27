import logging


class GradeParser:
    def __init__(self, provider):
        self.provider = provider

    def parse(self, filter=lambda x: True):
        gradeList = self.provider.get_grade()
        grades = sorted(gradeList.get("list", {}).get(
            "records", []), key=lambda x: x[0])
        logging.debug(grades)
        res = {}
        for grade in grades:
            if filter(grade):
                res.setdefault(grade[11], (grade[8], grade[13]))
        return res
