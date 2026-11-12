"""Check the published chart denominators and the joins to frozen source evidence."""
from figures_v2 import *
from datetime import datetime,timezone

checks=[]
def check(name,actual,expected):
    assert actual==expected,(name,actual,expected)
    checks.append({'check':name,'actual':actual,'expected':expected,'passed':True})

check('开放评价记录数',len(Q),889)
check('开放评价唯一模型 ID',len({r['model_id'] for r in Q}),889)
ev=json.loads((LIVE/'grid889.json').read_text())
check('证据明细唯一模型 ID',len({r['model_id'] for r in ev}),889)
check('评价与证据明细 ID 集合一致',{r['model_id'] for r in Q}=={r['model_id'] for r in ev},True)
check('全球开放统计',stats(Q),{'n':889,'open':617,'complete':175,'both':117})
check('中国开放统计',stats(QCN),{'n':415,'open':354,'complete':68,'both':56})
check('地域未知仍在分母',sum(r['country']=='Unknown' for r in Q),64)
check('可识别国家数',len({r['country'] for r in Q if r['country']!='Unknown'}),25)
check('所有可识别国家存在地图映射',all(r['country'] in CNAMES for r in Q if r['country']!='Unknown'),True)
check('全部主体类型映射',all(r['org_type'] in TYPES for r in Q),True)
check('L2 O3 最大单元',sum(r['strict_completeness_num']==2 and r['openness_num']==3 for r in Q),438)
check('中国 L2 O3 单元',sum(r['strict_completeness_num']==2 and r['openness_num']==3 for r in QCN),287)
check('中国任务加总',sum(Counter(r['task_category'] for r in QCN).values()),415)
check('全球主体数',len({r['story_org'] for r in Q}),244)
check('中国主体数',len({r['story_org'] for r in QCN}),61)
byid={r['model_id']:r for r in ev}
keys=['L1_weights','L3_train_code','L3_train_data','L4_eval_code']
for id,expect in [('Qwen/Qwen3-0.6B',['complete','complete','partial','missing']),('deepseek-ai/DeepSeek-R1',['complete','partial','partial','missing']),('BAAI/bge-m3',['complete']*4)]:
    check('案例材料状态 '+id,[byid[id]['indicators'][k] for k in keys],expect)
for asset,expected in [('models',73088),('datasets',12502)]:
    check(asset+' 地域样本与汇总一致',sum(r[asset] for r in S['assets'][asset]['countries']),expected)
    check(asset+' 主体与地域样本一致',sum(r[asset][asset] for r in P),expected)
    cn=s51.country(asset);dr=s51.divisions(asset)
    check(asset+' 中国省级与待补加总',sum(r[asset] for r in dr)+cn['unassignedDivision'][asset],cn[asset])
monthtot={}
for asset,exp,prev in [('models',1126699,1045469),('datasets',520355,258829)]:
    rows=S['global'][asset]['monthlyNew'];m=[r for r in rows if '2025-07'<=r['month']<='2026-06'];p=[r for r in rows if '2024-07'<=r['month']<='2025-06']
    check(asset+' 主期完整 12 个月',len(m),12);check(asset+' 主期合计',sum(r['count'] for r in m),exp)
    check(asset+' 前 12 个月合计',sum(r['count'] for r in p),prev)
    monthtot[asset]={'main_period':exp,'previous_twelve_months':prev,'growth':exp/prev-1}
check('网络节点',len(s52.N),5777);check('网络边',len(s52.E),5111)
check('每条关系双端可见',all(e['source'] in s52.NB and e['target'] in s52.NB for e in s52.E),True)
ni=Counter(e['target'] for e in s52.E);no=Counter(e['source'] for e in s52.E)
both=set(ni)&set(no);multi={k for k,v in ni.items() if v>1}
check('同时连接上下游的版本',len(both),552);check('多上游版本',len(multi),50);check('两类角色重叠',len(both&multi),16)
check('跨国关系表组合数',len(s52.FLOW),186);check('跨国关系计数',sum(r['weight'] for r in s52.FLOW),10943)
ids,agg,out,inc=s52.aggregate_flows();check('桑基保留全量计数',sum(agg.values()),10943)
check('基座来源、派生发布均守恒',sum(out.values())==sum(inc.values())==10943,True)
check('中国到美国',sum(r['weight'] for r in s52.FLOW if r['source']=='CN' and r['target']=='US'),4639)
for row in s52.M:check('ModelRank 席位加总 '+row['month']+' Top'+str(row['k']),sum(row[k] for k in ['china','us','other_known','unknown']),row['k'])

result={'version':'v0.2','checked_utc':datetime.now(timezone.utc).isoformat(),'checks':checks,'monthly_growth':monthtot,
 'limits':['检查源数据的一致性、算术和关联，不等于独立验证模型训练结果。','地域统计保留 2026.10.17 冻结样本，不用新的平台总量更新比例。','源等级与证据字段原样保留；missing 解释为未找到充分证据。']}
(R/'review/data-qa-v0.2.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps({'passed':len(checks),'monthly_growth':monthtot},ensure_ascii=False))
