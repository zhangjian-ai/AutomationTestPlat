# AutomationTestPlat  自动化测试平台
> 持续更新

## 已实现功能
- 登录注册
  - 登陆实现：账号密码、手机验证码、钉钉扫码(需要配置自己真实的钉钉应用，具体配置百度就有)
  - 账号注册：直接注册、钉钉用户首次登陆时需绑定账号
- 用例管理
  - 用例创建
  - xmind 批量导入用例
  - 用例查询列表
- 任务管理
  - 测试任务创建
  - 测试任务列表及任务分配
- 工作台
  - 工作台就是具体对测试过程进行管理的模块
  - 统计针对登录账号已完成、待完成的测试任务
  - **测试记录不会自动保存** 后续会修复
- 资源原理
  - 资源列表。基于 websocket 实现资源的上传下载功能
  - 此次更新后，后端 django 的部署方式新增 asgi服务，以实现 websocket 连接。
