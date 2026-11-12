from pathlib import Path
import csv,json,re,collections,hashlib
R=Path(__file__).resolve().parent;D=R/'data'
def out(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2))
rows=list(csv.DictReader((D/'36/modelrank_2026-06_top100.csv').open(encoding='utf-8-sig')))
evidence=[
 ('Qwen','阿里巴巴 / Qwen','中国','杭州','https://home.alibabagroup.com/en-US/faqs-corporate-information','https://huggingface.co/Qwen'),
 ('google','Google','美国','山景城','https://about.google/company-info/locations/','https://huggingface.co/google'),
 ('openai','OpenAI','美国','旧金山','https://openai.com/policies/terms-of-use/','https://huggingface.co/openai'),
 ('facebook','Meta','美国','门洛帕克','https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm','https://huggingface.co/facebook'),
 ('meta-llama','Meta','美国','门洛帕克','https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm','https://huggingface.co/meta-llama'),
 ('FacebookAI','Meta','美国','门洛帕克','https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm','https://huggingface.co/FacebookAI'),
 ('intfloat','个人账户','未识别','','','https://huggingface.co/intfloat'),
 ('jhu-clsp','约翰斯·霍普金斯大学 CLSP','美国','巴尔的摩','https://www.clsp.jhu.edu/contact/','https://huggingface.co/jhu-clsp'),
 ('krea','Krea','美国','旧金山','https://www.krea.ai/blog/new-krea','https://huggingface.co/krea'),
 ('LiquidAI','Liquid AI','美国','剑桥（马萨诸塞州）','https://www.liquid.ai/privacy-policy','https://huggingface.co/LiquidAI'),
 ('mistralai','Mistral AI','法国','巴黎','https://mistral.ai/fr/legal/','https://huggingface.co/mistralai'),
 ('unsloth','Unsloth AI','美国','旧金山','https://www.ycombinator.com/companies/unsloth-ai','https://huggingface.co/unsloth'),
 ('BAAI','北京智源人工智能研究院','中国','北京','https://www.baai.ac.cn/about-us','https://huggingface.co/BAAI'),
 ('black-forest-labs','Black Forest Labs','德国','弗赖堡','https://bfl.ai/legal/imprint','https://huggingface.co/black-forest-labs'),
 ('cmz1024','个人账户','未识别','','','https://huggingface.co/cmz1024'),
 ('distilbert','Hugging Face','美国','纽约','https://huggingface.co/terms-of-service','https://huggingface.co/distilbert'),
 ('KBlueLeaf','个人账户','未识别','','','https://huggingface.co/KBlueLeaf'),
 ('lerobot','Hugging Face','美国','纽约','https://huggingface.co/terms-of-service','https://huggingface.co/docs/lerobot/index'),
 ('Lightricks','Lightricks','以色列','耶路撒冷','https://www.lightricks.com/contact-us','https://huggingface.co/Lightricks'),
 ('OnomaAIResearch','Onoma AI','韩国','首尔','https://www.onomaai.com/','https://huggingface.co/OnomaAIResearch'),
 ('stabilityai','Stability AI','英国','伦敦','https://find-and-update.company-information.service.gov.uk/company/12295325','https://huggingface.co/stabilityai'),
 ('tiiuae','Technology Innovation Institute','阿联酋','阿布扎比','https://www.tii.ae/contact-us','https://huggingface.co/tiiuae'),
]
ed=[dict(zip(['publisher','organization','country','city','location_source','identity_source'],r),verification_date='2026-11-10',scope='当前组织归属核验，不是贡献者或历史团队地理') for r in evidence]
by={e['publisher']:e for e in ed}
for r in rows:
 r['rank']=int(r['rank']);r['score_normalized']=float(r['score_normalized'])
 r['country']=by[r['author']]['country'];r['organization']=by[r['author']]['organization']
 if r['author']=='Qwen':
  r['family']=re.match(r'(Qwen[\d.]+)',r['name'].split('/')[1]).group(1)
  r['nameplate_params_B']=float(re.search(r'-(\d+(?:\.\d+)?)B',r['name']).group(1))
  r['parameter_band']='≤1B' if r['nameplate_params_B']<=1 else '1—10B' if r['nameplate_params_B']<=10 else '>10B'
cn=[r.copy() for r in rows if r['country']=='中国']
for i,r in enumerate(cn):r['china_subset_rank']=i+1
q=[r for r in rows if r['author']=='Qwen']
summary={'n':len(rows),'country_counts':dict(collections.Counter(r['country'] for r in rows)),
 'publishers':dict(collections.Counter(r['author'] for r in rows)),
 'tasks':dict(collections.Counter(r['category'] or '未标注' for r in rows)),
 'country_rank_bands':{c:[sum(r['country']==c and a<=r['rank']<=b for r in rows) for a,b in [(1,10),(11,30),(31,100)]] for c in ['美国','中国','法国','德国','英国','韩国','以色列','阿联酋','未识别']},
 'china_n':len(cn),'china_top20':sum(r['rank']<=20 for r in cn),'china_tasks':dict(collections.Counter(r['category'] for r in cn)),
 'qwen_family':dict(collections.Counter(r['family'] for r in q)),
 'qwen_size':dict(collections.Counter(r['parameter_band'] for r in q)),
 'qwen_family_size':{f:{b:sum(r['family']==f and r['parameter_band']==b for r in q) for b in ['≤1B','1—10B','>10B']} for f in ['Qwen2.5','Qwen3','Qwen3.5','Qwen3.6']},
 'deepseek_top100':sum(r['author']=='deepseek-ai' for r in rows)}
assert len(rows)==100 and len(by)==22 and sum(summary['country_counts'].values())==100
assert summary['country_counts']=={'德国':1,'英国':1,'中国':37,'美国':50,'韩国':1,'法国':2,'阿联酋':1,'未识别':6,'以色列':1}
out(D/'publisher-geography.json',ed);out(D/'models100.json',rows);out(D/'china37.json',cn);out(D/'summary.json',summary)
out(R/'review/data-checks.json',{'main_window':'2025-07-01/2026-06-30','ranking_snapshot':'2026-06','original_rank_preserved':True,'no_synthetic_values':True,'geography_coverage':'94/100; 6 unknown personal-account models','source_csv_sha256':hashlib.sha256((D/'36/modelrank_2026-06_top100.csv').read_bytes()).hexdigest(),'summary':summary})
out(D/'external-evidence.json',[
 {'source':'ATOM Report v1, 2026-04-08','url':'https://arxiv.org/html/2604.07190v1','window':'2023-11 to 2026-03','sample':'约1500个重点开放权重语言模型；衍生模型筛选与本节不同','facts':{'qwen_under10B_download_share':44,'deepseek_250Bplus_download_share':47,'deepseek_openrouter_token_share_2026_01':31.1},'locator':'Figure 12; Figure 9; §2.1 and §5.1','limits':'OpenRouter只覆盖逐月前十开放模型；下载不等于独立用户；仅引用研究原值，未重新计算。'},
 {'source':'HF Summer 2026, fixed 2026-08-17 version','url':'https://github.com/huggingface/blog/blob/9e982d5f2ff0c93248a897bf1e0c59c9828c5ab8/state-of-open-models-summer-2026.md','window':'2026年1—7月活动，8月补充发布；本节使用文中累计库存观察','facts':{'qwen_derivatives':151448,'qwen_gguf_conversions':28531,'qwen_official_gguf':54,'non_qwen_gguf':28477},'locator':'§4','limits':'衍生仓库不是独立原创模型、用户或部署；GGUF转换数与总衍生数不相加。'},
 {'source':'DeepSeek R1 official model card','url':'https://huggingface.co/deepseek-ai/DeepSeek-R1','facts':{'distills_qwen':4,'distills_llama':2},'locator':'§3 Model Downloads','limits':'基础权重继承与推理样本传递分开表达，不把蒸馏画成R1权重缩小。'},
 {'source':'DeepSeek R1 0528 official model card','url':'https://huggingface.co/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B','fact':'DeepSeek-R1-0528的思维链样本用于后训练Qwen3-8B-Base','locator':'§2 DeepSeek-R1-0528-Qwen3-8B'}])
print(json.dumps(summary,ensure_ascii=False,indent=2))
