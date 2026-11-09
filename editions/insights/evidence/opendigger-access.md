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

## 2026-11-09 再次连接结果

前一次连接超时；本次按作者要求复测，**数据库认证与实际查询成功**，服务版本为 25.3.6.1，数据库为 `opensource`。不需要把连接失败继续作为全部数据库工作的阻碍。

| 检查 | 结果 |
| --- | --- |
| 两份 Skill 与 events 字段参考 | 已成功读取，按文档核对实际表字段 |
| 公开 OpenRank JSON | 成功，样本仓库 X-lab2017/open-digger 返回 73 个月度键，末月 2026-09 |
| 账号认证、数据库与表目录 | 成功；当前可见并获 SELECT 授权的表共 7 张 |
| 报告窗口 OpenRank | 成功读取样本仓库 2025-07 至 2026-06 连续 12 个月 |
| 归一化贡献度 | 成功读取样本仓库 2026-06 的聚合：4 条记录、4 个账号，贡献度合计约 7.1112 |
| events 原始事件表 | 直接查询返回 Code 497 / ACCESS_DENIED，当前账号无所需 SELECT 权限 |
| user_info 用户地理视图 | 直接查询返回 Code 497 / ACCESS_DENIED，当前账号无所需 SELECT 权限 |

已授权的 7 张表：`community_openrank`、`flatten_labels`、`gh_repo_info`、`global_openrank`、`labels`、`name_info`、`normalized_community_openrank`。这是当前账号的权限范围，不是数据库全部表的清单。Skill 的完整表结构也不等于该账号已经获得全部权限。

后续可直接开展 OpenRank、归一化贡献、标签及获授权仓库信息的研究。若需从原始事件重新统计活跃人数、参与人数或关联用户所在地，须由管理员补充所需字段的 SELECT 权限。当前没有尝试提升权限或进行数据写入。授权记录显示按表授予 SELECT；不能仅用 `readonly` 会话设置判断账号实际权限。

说明中的国家标签 ID 示例在本次查询中未匹配记录，不能把空结果解释成国家开发者数量为零；后续先核对实际标签，再读取历史序列。

连接验收与汇总样本见 [access-check-2026-11-09.json](access-check-2026-11-09.json)。第二章 v0.2 仍使用原固定归档，不能因本次连接成功追改为“已由数据库独立核验”。后续新增实证应同步更新数据、图件、正文、附录与主张记录。密码只经隐藏输入用于连接，没有写入文件或 GitHub。
