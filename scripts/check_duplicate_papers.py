import re
from collections import Counter

def find_duplicate_papers(readme_path):
    """Find duplicate paper titles in README.md"""
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 提取所有论文标题
    papers = re.findall(r'\["([^"]+)"\]\(papers/[^)]+\)', content)
    
    # 使用 Counter 统计每个标题出现的次数
    paper_counts = Counter(papers)
    
    # 找出出现次数大于1的标题
    duplicates = {title: count for title, count in paper_counts.items() if count > 1}
    
    if duplicates:
        print("\n发现以下重复的论文:")
        for title, count in sorted(duplicates.items()):
            print(f"- '{title}' 出现了 {count} 次")
    else:
        print("\n没有发现重复的论文")

if __name__ == "__main__":
    find_duplicate_papers('README.md') 