# SCU_JWC_toolkit
一个简单的四川大学教务处工具包

目前支持：

- 分数查询
  - 加权均分计算
  - 总学分计算
  - 任意条件过滤器
- 课表处理
  - 转换为`icalendar`对象，以提供标准日历格式的访问

改进和交流请联系zjm97@outlook.com

---
2020年2月24日更新：

彻头彻尾地重构了两年前的代码：

- 随着教务处评教系统的改革，一键评教已经没有存在下去的必要了，因此移除了一键评教功能。
- 随着一键评教的移除，目前仅剩课表导入日历的功能。
- 区分了具有不同功能的模块，将认证和主体流程模块解耦。目前提供三种登陆器：
  - 用户名密码登陆器，需要提供用户名密码，并填写验证码
  - `sessionId`登陆器，提供`JSESSIONID`即可，适用于短期内无密码登录
  - 记住密码登陆器，需提供`SPRING_SECURITY_REMEMBER_ME_COOKIE`，该值需要通过特殊方法获取
- 修正了部分函数的功能