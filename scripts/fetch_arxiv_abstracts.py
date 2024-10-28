import arxiv
import re
import json
import os
from pathlib import Path

def extract_arxiv_ids(markdown_content):
    """Extract arXiv IDs from markdown content"""
    # Pattern to match arXiv URLs
    pattern = r'arxiv\.org/abs/(\d{4}\.\d{5})'
    return re.findall(pattern, markdown_content)

def get_paper_info(arxiv_id):
    """Get paper information from arXiv"""
    try:
        # Search for the paper
        search = arxiv.Search(id_list=[arxiv_id])
        paper = next(search.results())
        
        return {
            'title': paper.title,
            'abstract': paper.summary,
            'authors': [author.name for author in paper.authors],
            'arxiv_id': arxiv_id,
            'url': f'https://arxiv.org/abs/{arxiv_id}'
        }
    except Exception as e:
        print(f"Error processing {arxiv_id}: {str(e)}")
        return None

def main():
    # Create output directory
    output_dir = Path('data/abstract')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read the markdown file
    with open('papers/Awesome-LLM-Watermark.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract arXiv IDs
    arxiv_ids = extract_arxiv_ids(content)
    
    # Get paper information for each ID
    papers_info = []
    for arxiv_id in arxiv_ids:
        print(f"Processing {arxiv_id}...")
        paper_info = get_paper_info(arxiv_id)
        if paper_info:
            papers_info.append(paper_info)
    
    # Save to JSON file
    output_file = output_dir / 'papers_info.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(papers_info, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully saved {len(papers_info)} papers' information to {output_file}")

if __name__ == "__main__":
    main()
