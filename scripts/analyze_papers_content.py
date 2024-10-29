import json
from collections import Counter
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib.font_manager import findfont, FontProperties
import os

class PaperAnalyzer:
    def __init__(self, file_path='data/abstract/papers_info.json'):
        self.file_path = file_path
        # Download all required NLTK data
        required_packages = ['punkt', 'stopwords']
        for package in required_packages:
            try:
                nltk.data.find(f'tokenizers/{package}')
            except LookupError:
                print(f"Downloading {package}...")
                nltk.download(package)
        self.stop_words = set(stopwords.words('english'))
        
    def load_papers(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def analyze_authors(self, papers):
        """Analyze author statistics"""
        # Count author appearances
        author_counts = Counter()
        papers_per_author = {}
        
        for paper in papers:
            authors = paper['authors']
            for author in authors:
                author_counts[author] += 1
                if author not in papers_per_author:
                    papers_per_author[author] = []
                papers_per_author[author].append(paper['title'])
        
        # Get most prolific authors
        top_authors = author_counts.most_common(10)
        
        print("\n=== Author Analysis ===")
        print(f"Total unique authors: {len(author_counts)}")
        print("\nTop 10 authors by number of papers:")
        for author, count in top_authors:
            print(f"\n{author}: {count} papers")
            print("Papers:")
            for title in papers_per_author[author]:
                print(f"- {title}")
                
    def process_text(self, text):
        """Process text for word frequency analysis"""
        # Remove special characters and convert to lowercase
        text = re.sub(r'[^\w\s]', '', text.lower())
        # Simple word splitting
        words = text.split()
        # Remove stopwords and short words
        words = [word for word in words if word not in self.stop_words and len(word) > 2]
        return words
        
    def analyze_content(self, papers):
        """Analyze title and abstract content"""
        title_words = []
        abstract_words = []
        
        for paper in papers:
            title_words.extend(self.process_text(paper['title']))
            abstract_words.extend(self.process_text(paper['abstract']))
            
        title_freq = Counter(title_words)
        abstract_freq = Counter(abstract_words)
        
        print("\n=== Content Analysis ===")
        print("\nTop 20 words in titles:")
        for word, count in title_freq.most_common(20):
            print(f"{word}: {count}")
            
        print("\nTop 20 words in abstracts:")
        for word, count in abstract_freq.most_common(20):
            print(f"{word}: {count}")
            
        # Generate word clouds
        self.generate_wordcloud(title_freq, "Title Word Cloud", "title_wordcloud.png")
        self.generate_wordcloud(abstract_freq, "Abstract Word Cloud", "abstract_wordcloud.png")
        
    def generate_wordcloud(self, word_freq, title, filename):
        """Generate and save word cloud"""
        try:
            # 使用 matplotlib 的默认字体
            import matplotlib.font_manager as fm
            font_path = fm.findfont(fm.FontProperties(family='DejaVu Sans'))
            
            wordcloud = WordCloud(
                width=1600, 
                height=800, 
                background_color='white',
                font_path=font_path,
                min_font_size=10,
                max_font_size=100
            ).generate_from_frequencies(word_freq)
            
            plt.figure(figsize=(20,10))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(title)
            
            # 确保目录存在
            os.makedirs('results/analysis', exist_ok=True)
            
            plt.savefig(f"results/analysis/{filename}")
            plt.close()
            
        except Exception as e:
            print(f"Warning: Could not generate word cloud due to: {str(e)}")
            # 退回到条形图
            self.visualize_word_freq(word_freq, title, filename.replace('wordcloud', 'barplot'))

    def visualize_word_freq(self, word_freq, title, filename):
        """Generate bar plot for word frequencies"""
        plt.figure(figsize=(15, 8))
        words, counts = zip(*word_freq.most_common(20))
        
        plt.bar(range(len(words)), counts)
        plt.xticks(range(len(words)), words, rotation=45, ha='right')
        plt.title(title)
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.tight_layout()
        
        # 确保目录存在
        os.makedirs('results/analysis', exist_ok=True)
        
        plt.savefig(f"results/analysis/{filename}")
        plt.close()
        
    def analyze(self):
        """Run all analyses"""
        papers = self.load_papers()
        print(f"\nAnalyzing {len(papers)} papers...")
        
        self.analyze_authors(papers)
        self.analyze_content(papers)

if __name__ == "__main__":
    analyzer = PaperAnalyzer()
    analyzer.analyze() 