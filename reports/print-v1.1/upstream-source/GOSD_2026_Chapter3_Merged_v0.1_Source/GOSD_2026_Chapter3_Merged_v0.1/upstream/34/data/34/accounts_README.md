# Chapter 3.4 public-account evidence reproduction

## Finding

All supplied Page headline values reproduce exactly from the saved public inputs. No numerical divergence was found.

| Repository | Annual sample union | 1–2 months | 3–5 months | 6–8 months | 9–12 months | 9–12 month share |
|---|---:|---:|---:|---:|---:|---:|
| pytorch/pytorch | 369 | 242 | 68 | 23 | 36 | 9.76% |
| vllm-project/vllm | 514 | 396 | 71 | 22 | 25 | 4.86% |
| sgl-project/sglang | 507 | 384 | 74 | 26 | 23 | 4.54% |
| langchain-ai/langchain | 885 | 862 | 15 | 2 | 6 | 0.68% |
| langgenius/dify | 665 | 594 | 45 | 17 | 9 | 1.35% |
| kubernetes/kubernetes | 430 | 307 | 58 | 35 | 30 | 6.98% |

The vLLM–SGLang annual intersection is 36 logins, including 21 unique logins present in both samples in at least one same month. The corresponding PyTorch–vLLM values are 22 and 16. Summing the monthly intersection sizes instead gives 22 and 41 account-month incidences; these are different measures and must not be called 21/16 occurrences.

## Reproduction method

1. Use only the twelve exact monthly keys July 2025 through June 2026 inclusive from each repository's `https://oss.open-digger.cn/github/{owner}/{repo}/activity_details.json`. Ignore annual, quarterly, other monthly and aggregate keys. All 72 requested repository-month keys exist.
2. For every returned `[login, activity_score]`, trim whitespace and normalize the login to lowercase. Exclude empty logins, any login containing `[bot]`, and any normalized login present among the GitHub users in `labeled_data/bot/index.yml` at commit `ead4515179ae93a3bcbb151707a90fe7e1750f49`. The pinned file contains 928 distinct normalized GitHub bot names. There is no extra heuristic based on the words `bot`, `ci`, or `robot` in ordinary login names.
3. Deduplicate within each repository-month after filtering. Do not backfill filtered entries: the source sample is already capped before this analysis removes bots.
4. A repository's annual set is the union of its twelve monthly sets. For each login, count the number of monthly sets containing it. Bin that count into 1–2, 3–5, 6–8 or 9–12. The last bin is the stated high-frequency measure; the proportion uses the annual sample union as denominator.
5. For each repository pair, intersect their annual sets. Separately, intersect their monthly sets for each matching calendar month and union those twelve intersections. The latter is the unique-account same-month overlap. Also retain the sum of the twelve intersection sizes as an explicitly separate account-month measure.

## The 100-entry limit

The pinned [implementation, lines 227–286](https://github.com/X-lab2017/open-digger/blob/ead4515179ae93a3bcbb151707a90fe7e1750f49/src/metrics/indices.ts#L227-L286) defines `getRepoActivity`. Its [line 263](https://github.com/X-lab2017/open-digger/blob/ead4515179ae93a3bcbb151707a90fe7e1750f49/src/metrics/indices.ts#L263) contains:

```
arraySlice(arraySort(x -> -tupleElement(x, 2), groupArray((actor_login, ROUND(activity, 2)))), 1, 100) AS details
```

This takes at most 100 entries after descending ordering by the rounded activity score, and monthly aggregation is visible at line 267. The relevant event types in this function are issues, issue comments, pull requests and pull-request review comments, not a census of all GitHub participation or all code authors.

The [pinned bot directory](https://github.com/X-lab2017/open-digger/tree/ead4515179ae93a3bcbb151707a90fe7e1750f49/labeled_data/bot) was resolved with the GitHub connector and contains one file, [index.yml](https://github.com/X-lab2017/open-digger/blob/ead4515179ae93a3bcbb151707a90fe7e1750f49/labeled_data/bot/index.yml). Both this YAML and the implementation are saved locally.

All twelve raw monthly samples have 100 entries for PyTorch, vLLM and SGLang. LangChain has 80 in May 2026 and 33 in June 2026; Dify has 98 and 36, respectively; Kubernetes has 83 in June 2026. All other selected raw months have 100. These observations alone do not establish why a sample is shorter or whether the underlying event collection is complete.

## Interpretation limits

- These are bot-filtered monthly leading-activity samples, not full contributor censuses. The annual union and persistence bins describe appearing in those samples, not all project participation or retention.
- Bot filtering is label/name based and is not a guarantee that all remaining accounts represent humans. The current public data gives logins, not immutable account IDs, so case normalization does not reconcile account renames or establish person identity.
- Cross-repository overlap establishes observed reuse of the same normalized login. It does not establish migration, collaboration, affiliation, causal knowledge transfer or an individual's skills.
- The source code and bot labels are pinned to a commit, but the OSS activity JSON URLs are mutable and are not tied to that commit. The source manifest records the exact downloaded bytes with SHA-256 hashes. A future `--refresh` may produce different results.
- Local file modification timestamps in `source_manifest.json` are recorded by the execution environment, not claimed to be the upstream dataset's publication or update dates.

## Files and reuse

Run `python reproduce.py` from this folder to regenerate all derived files. Python with PyYAML is required. `python reproduce.py --refresh` redownloads the public inputs, which can change with time. It performs no remote writes.

- Six `{owner}_{repo}.json` files: complete raw OSS responses.
- `indices.ts`, `bot_labels.yml`: pinned source and labels.
- `source_manifest.json`: source URLs, pinned commit, file sizes, timestamps and input SHA-256 hashes.
- `repository_summary.csv`: annual unions and frequency bins.
- `monthly_audit.csv`: raw and retained sizes plus exclusion counts per month.
- `excluded_accounts.csv`: every excluded account-month record and its reason.
- `account_months.csv`: each repository/login and its exact observed monthly membership.
- `normalized_monthly_accounts.json`: all post-filter monthly account sets.
- `pairwise_intersections.csv`: all 15 repository pairs and three distinct overlap metrics.
- `pairwise_accounts.json`: exact annual, same-month and monthly-intersection login lists.
- `bot_logins_normalized.txt`: 928 normalized GitHub bot labels.
- `results.json`, `previous_page_comparison.json`: machine-readable results and supplied-headline comparison.

## Suggested Chinese methods note

本节使用 OpenDigger `activity_details.json` 中 2025 年 7 月至 2026 年 6 月的 12 个月度公开账号列表。固定版本实现将每个统计期的账号明细按活跃度降序截取至多 100 条，因此以下结果是“月度高活跃账号公开样本”的观察值，不是项目全部贡献者人数。分析将 login 转为小写，剔除空值、含 `[bot]` 的账号及固定版本机器人标签表中的 GitHub 账号，再计算年度去重并集、出现月份数分组及项目间交集。“同月重叠账号”指至少在一个相同自然月同时进入两个项目样本的去重账号数，不是账号月份次数，也不直接证明人才流动或协作关系。
