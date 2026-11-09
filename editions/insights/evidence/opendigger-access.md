# OpenDigger 数据使用入口

2026-11-09，作者补充并授权用于本报告数据核验。这里只记录公开入口与使用边界，不记录账号或连接凭据。

## 公开指标

- [开放指标 Skill](https://github.com/X-lab2017/open-digger/blob/master/skills/open-digger-data-retrieval/SKILL.md)：仓库／用户指标 JSON，无需数据库权限。
- 示例路径模板：`https://oss.open-digger.cn/{platform}/{owner}/{repo}/{metric}.json`。
- 区分原始值、补插值和平台；记录抓取时间、报告窗口与指标定义。不能把各仓库或各月独立人数简单相加作为全国或全球年度人数。

## 数据库

- [ClickHouse 表结构 Skill](https://github.com/X-lab2017/open-digger/blob/master/skills/open-digger-clickhouse-schema/SKILL.md)：使用前核对表结构、字段与平台／时间过滤。
- 只读聚合查询；按需要安装 ClickHouse 连接能力，连接凭据从私密环境注入，不落入报告或源码。
- 当前用户资料视图不是历史位置快照；研究 2022—2026 地理变化时必须核验各年度归属规则。
- 只提取报告需要的汇总，不导出个人邮箱等无关信息。

本轮已阅读两份说明；数据库端点测试超时，尚无成功查询结果。第二章 v0.2 使用固定归档数据，公开指标文档用于术语核对。后续若获得新查询结果，应同时更新数据、图件、正文、附录与主张记录，保留查询及指标版本，不改写旧样稿的核验状态。
