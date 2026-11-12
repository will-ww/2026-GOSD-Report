SELECT l.id, any(l.name) AS name, round(sum(e.openrank),2) AS openrank
FROM global_openrank e INNER JOIN
(SELECT DISTINCT id,platform,name,entity_id,entity_type FROM flatten_labels WHERE type='Project' AND entity_type IN ('Repo','Org')) l
ON (l.entity_id=e.repo_id AND l.entity_type='Repo' AND l.platform=e.platform)
OR (l.entity_id=e.org_id AND l.entity_type='Org' AND l.platform=e.platform)
WHERE e.type='Repo' AND e.platform IN ('GitHub','Gitee','GitLab','AtomGit')
AND e.created_at >= '2025-07-01' AND e.created_at < '2026-07-01'
GROUP BY l.id ORDER BY openrank DESC LIMIT 150 FORMAT JSON