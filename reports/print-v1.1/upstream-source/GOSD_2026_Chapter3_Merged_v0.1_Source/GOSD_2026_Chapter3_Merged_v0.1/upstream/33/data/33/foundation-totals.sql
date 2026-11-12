SELECT l.id AS id, any(l.name) AS name, round(sum(e.openrank),2) AS openrank, uniqExact(tuple(e.platform,e.repo_id)) AS repositories
FROM global_openrank e
INNER JOIN (SELECT id,platform,name,entity_id,entity_type FROM flatten_labels WHERE type='Foundation') l
ON (l.entity_id=e.repo_id AND l.entity_type='Repo' AND l.platform=e.platform)
OR (l.entity_id=e.org_id AND l.entity_type='Org' AND l.platform=e.platform)
OR (l.entity_id=e.actor_id AND l.entity_type='User' AND l.platform=e.platform)
WHERE e.platform IN ('GitHub','Gitee','GitLab','AtomGit') AND e.type='Repo' AND e.created_at>='2025-07-01' AND e.created_at<'2026-07-01'
GROUP BY l.id ORDER BY openrank DESC SETTINGS max_execution_time=80,max_threads=4;