import json
import datetime
from collections import defaultdict

def analyze_papers():
    """Analyze papers from papers_info.json"""
    try:
        with open('data/abstract/papers_info.json', 'r', encoding='utf-8') as f:
            papers = json.load(f)
            
        # Count total papers
        total_papers = len(papers)
        
        # Group papers by year-month
        papers_by_date = defaultdict(list)
        for paper in papers:
            arxiv_id = paper['arxiv_id']
            # Extract year and month from arxiv ID (format: YYMM.xxxxx)
            year = '20' + arxiv_id[:2]
            month = arxiv_id[2:4]
            date_key = f"{year}-{month}"
            papers_by_date[date_key].append({
                'title': paper['title'],
                'arxiv_id': paper['arxiv_id']
            })
        
        # Sort dates
        sorted_dates = sorted(papers_by_date.keys(), reverse=True)
        
        # Print results
        print(f"\nTotal number of papers: {total_papers}\n")
        print("Papers by month:")
        print("-" * 50)
        
        for date in sorted_dates:
            papers_in_month = papers_by_date[date]
            print(f"\n{date} ({len(papers_in_month)} papers):")
            for paper in papers_in_month:
                print(f"- {paper['title']} (arxiv:{paper['arxiv_id']})")
                
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    analyze_papers() 