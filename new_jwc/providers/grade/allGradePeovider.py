import logging


class AllGradeProvider:
    ALL_SCORES_DATA = "http://zhjw.scu.edu.cn/student/integratedQuery/scoreQuery/allTermScores/data"

    def __init__(self, auth_provider):
        self.session = auth_provider.login()

    def get_grade(self):
        logging.info("正在获取全部成绩信息...")
        r = self.session.post(self.ALL_SCORES_DATA, data={
            "pageNum": 1,
            "pageSize": 999
        })
        logging.debug(r.json())
        return r.json()
