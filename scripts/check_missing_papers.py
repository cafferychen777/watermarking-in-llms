import json
import re

def extract_papers_from_readme(readme_path):
    """Extract paper titles from README.md"""
    papers = set()
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # 使用正则表达式匹配所有 ["Title"](papers/xxx.pdf) 格式的标题
        matches = re.findall(r'\["([^"]+)"\]\(papers/[^)]+\)', content)
        papers.update(matches)
    return papers

def extract_papers_from_json(json_path):
    """Extract paper titles from papers_info.json"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return {paper['title'] for paper in data}

def find_missing_papers():
    """Find papers that are in JSON but not in README"""
    readme_papers = extract_papers_from_readme('README.md')
    json_papers = extract_papers_from_json('data/abstract/papers_info.json')
    
    missing_papers = json_papers - readme_papers
    
    print(f"\n发现 {len(missing_papers)} 篇论文在 JSON 中但不在 README 中:")
    for i, paper in enumerate(sorted(missing_papers), 1):
        print(f"{i}. {paper}")

if __name__ == "__main__":
    find_missing_papers() 