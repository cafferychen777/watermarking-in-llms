import os
from pathlib import Path
import anthropic
import json
from tqdm import tqdm
import logging
from datetime import datetime
import time
import argparse

class PaperAnalyzer:
    def __init__(self, input_dir=None):
        # Setup paths
        self.text_dir = Path(input_dir) if input_dir else Path('data/text')
        self.output_dir = Path('results/analysis')
        self.log_dir = Path('logs')
        
        # Validate input directory
        if not self.text_dir.exists():
            raise ValueError(f"Input directory does not exist: {self.text_dir}")
        
        # Create directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # Initialize Claude client
        self.client = anthropic.Anthropic(
            api_key=os.getenv('ANTHROPIC_API_KEY')
        )
        
        # Log input directory
        self.logger.info(f"Using input directory: {self.text_dir}")

    def setup_logging(self):
        """Setup logging configuration"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = self.log_dir / f'claude_analysis_{timestamp}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def analyze_single_paper(self, text_path):
        """Analyze a single paper using Claude"""
        try:
            # Read the paper text
            self.logger.info(f"Reading file: {text_path}")
            with open(text_path, 'r', encoding='utf-8') as f:
                paper_text = f.read()
            
            self.logger.info(f"Paper text length: {len(paper_text)} characters")
            if len(paper_text) == 0:
                self.logger.error("Paper text is empty!")
                return None

            # Simplified prompt focusing on key aspects
            prompt = f"""Please analyze this LLM watermarking paper for a literature review. Focus on:

1. Core Contribution:
   - Main watermarking approach/technique
   - Key innovations
   - Technical advantages

2. Implementation:
   - Watermarking methodology
   - Detection method
   - Key parameters/requirements

3. Evaluation:
   - Main results
   - Performance metrics
   - Comparison with baselines

4. Research Impact:
   - Limitations
   - Future work
   - Potential applications

Paper text:
{paper_text}

Please provide a concise analysis in JSON format with these four categories."""

            self.logger.info("Sending request to Claude API...")
            # Call Claude API
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            self.logger.info("Received response from Claude API")
            
            # Convert message content to string if it's not already
            content = str(message.content) if message.content else ""
            self.logger.info(f"Response content length: {len(content)}")

            return {
                'paper_name': text_path.stem,
                'analysis': content
            }

        except Exception as e:
            self.logger.error(f"Error analyzing {text_path.name}: {str(e)}")
            import traceback
            self.logger.error(traceback.format_exc())
            return None

    def analyze_papers_batch(self, text_files, batch_size):
        """Analyze multiple papers together focusing on uniqueness"""
        try:
            # Read papers
            papers_content = []
            for text_path in text_files[:batch_size]:
                try:
                    with open(text_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.logger.info(f"Successfully read {text_path.name}, length: {len(content)}")
                        papers_content.append({
                            'name': text_path.stem,
                            'content': content
                        })
                except Exception as e:
                    self.logger.error(f"Error reading {text_path.name}: {str(e)}")

            prompt = """Compare these LLM watermarking papers, focusing specifically on:

1. Key Innovation:
   - What is the unique technical contribution?
   - How does it differ from existing approaches?
   - What novel problem does it solve?

2. Technical Uniqueness:
   - Core technical advantage over other methods
   - Unique implementation features
   - Special capabilities not found in other papers

3. Comparative Strengths:
   - Key advantages compared to baselines
   - Specific improvements over previous work
   - Trade-offs that make it unique

Papers to analyze:
"""
            for i, paper in enumerate(papers_content, 1):
                prompt += f"\nPaper {i}: {paper['name']}\n{paper['content']}\n"

            prompt += """
Please provide a focused analysis in JSON format, highlighting only the unique and innovative aspects of each paper. Support your points with specific examples from the papers."""

            self.logger.info("Sending request to Claude API...")
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            self.logger.info("Received response from Claude API")
            
            # Extract content from TextBlock
            content = message.content
            if hasattr(content, 'text'):  # If content is a TextBlock
                content = content.text
            elif isinstance(content, list) and content and hasattr(content[0], 'text'):  # If content is a list of TextBlocks
                content = content[0].text
            else:
                content = str(content)

            # Try to parse the JSON string if it's escaped
            try:
                if content.startswith('"') and content.endswith('"'):
                    content = json.loads(content)
            except:
                pass

            self.logger.info(f"Processed content length: {len(str(content))}")
            
            result = {
                'papers': [p['name'] for p in papers_content],
                'analysis': content
            }
            
            return result

        except Exception as e:
            self.logger.error(f"Error in batch analysis: {str(e)}")
            import traceback
            self.logger.error(traceback.format_exc())
            return None

    def get_paper_path(self, paper_identifier):
        """Get paper path from identifier (can be name or index)"""
        text_files = list(self.text_dir.glob('*.txt'))
        self.logger.info(f"Looking for paper: {paper_identifier}")
        self.logger.info(f"Available files: {[f.stem for f in text_files]}")
        
        if paper_identifier.isdigit():
            # If identifier is a number, use it as index
            idx = int(paper_identifier)
            if 0 <= idx < len(text_files):
                self.logger.info(f"Found paper at index {idx}: {text_files[idx]}")
                return text_files[idx]
        else:
            # If identifier is a name, find matching file
            for file in text_files:
                if paper_identifier in file.stem:
                    self.logger.info(f"Found paper matching name: {file}")
                    return file
        
        self.logger.error(f"Paper not found: {paper_identifier}")
        return None

    def analyze_papers(self, mode='single', batch_size=3, paper_ids=None):
        """Analyze papers based on specified mode and paper identifiers"""
        text_files = list(self.text_dir.glob('*.txt'))
        self.logger.info(f"Found {len(text_files)} text files to analyze")
        
        analyses = []
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if mode == 'single':
            # If specific papers are requested
            if paper_ids:
                papers_to_analyze = []
                for pid in paper_ids:
                    paper_path = self.get_paper_path(pid)
                    if paper_path:
                        papers_to_analyze.append(paper_path)
                    else:
                        self.logger.error(f"Paper not found: {pid}")
                text_files = papers_to_analyze
            
            # Process each paper individually
            for text_file in tqdm(text_files, desc="Analyzing papers"):
                start_time = time.time()
                self.logger.info(f"Starting analysis of: {text_file.name}")
                
                analysis = self.analyze_single_paper(text_file)
                
                if analysis:
                    analyses.append(analysis)
                    processing_time = time.time() - start_time
                    self.logger.info(f"Successfully analyzed {text_file.name} "
                                   f"(Processing time: {processing_time:.2f}s)")
                    
                    # Save individual analysis with unique filename
                    paper_output_file = self.output_dir / f"analysis_{text_file.stem}_{timestamp}.json"
                    try:
                        with open(paper_output_file, 'w', encoding='utf-8') as f:
                            json.dump({
                                'paper_name': str(analysis['paper_name']),
                                'analysis': str(analysis['analysis'])
                            }, f, indent=2, ensure_ascii=False)
                        self.logger.info(f"Saved analysis to: {paper_output_file}")
                    except Exception as e:
                        self.logger.error(f"Error saving analysis for {text_file.name}: {str(e)}")
                else:
                    self.logger.error(f"Failed to analyze {text_file.name}")
            
            # Save combined analyses if multiple papers were analyzed
            if len(analyses) > 1:
                combined_output_file = self.output_dir / f"combined_analysis_{timestamp}.json"
                try:
                    with open(combined_output_file, 'w', encoding='utf-8') as f:
                        json_data = [{
                            'paper_name': str(analysis['paper_name']),
                            'analysis': str(analysis['analysis'])
                        } for analysis in analyses]
                        json.dump(json_data, f, indent=2, ensure_ascii=False)
                    self.logger.info(f"Saved combined analysis to: {combined_output_file}")
                except Exception as e:
                    self.logger.error(f"Error saving combined analysis: {str(e)}")
            
        else:  # batch mode
            if paper_ids:
                # Create batches from specified papers
                papers_to_analyze = []
                for pid in paper_ids:
                    paper_path = self.get_paper_path(pid)
                    if paper_path:
                        papers_to_analyze.append(paper_path)
                    else:
                        self.logger.error(f"Paper not found: {pid}")
                text_files = papers_to_analyze
            
            # Process papers in batches
            for i in tqdm(range(0, len(text_files), batch_size), desc="Analyzing paper batches"):
                batch_files = text_files[i:i + batch_size]
                start_time = time.time()
                
                paper_names = [f.stem for f in batch_files]
                batch_name = '_'.join(paper_names)
                self.logger.info(f"Starting analysis of batch: {paper_names}")
                
                analysis = self.analyze_papers_batch(batch_files, batch_size)
                
                if analysis:
                    analyses.append(analysis)
                    processing_time = time.time() - start_time
                    
                    # Save batch analysis with unique filename
                    batch_output_file = self.output_dir / f"batch_analysis_{batch_name}_{timestamp}.json"
                    try:
                        with open(batch_output_file, 'w', encoding='utf-8') as f:
                            json.dump(analysis, f, indent=2, ensure_ascii=False)
                        self.logger.info(f"Saved batch analysis to: {batch_output_file}")
                    except Exception as e:
                        self.logger.error(f"Error saving batch analysis: {str(e)}")
                else:
                    self.logger.error(f"Failed to analyze batch: {paper_names}")
        
        return analyses

def list_available_papers(input_dir=None):
    """List all available papers with their indices"""
    text_dir = Path(input_dir) if input_dir else Path('data/text')
    if not text_dir.exists():
        print(f"Error: Directory not found: {text_dir}")
        return
        
    text_files = list(text_dir.glob('*.txt'))
    if not text_files:
        print(f"\nNo text files found in {text_dir}")
        return
        
    print(f"\nAvailable papers in {text_dir}:")
    for i, file in enumerate(text_files):
        print(f"[{i}] {file.stem}")

def main():
    parser = argparse.ArgumentParser(description='Analyze research papers using Claude')
    parser.add_argument('--mode', choices=['single', 'batch'], default='single',
                      help='Analysis mode: single paper or batch analysis')
    parser.add_argument('--batch-size', type=int, default=3,
                      help='Number of papers to analyze together in batch mode')
    parser.add_argument('--papers', nargs='*',
                      help='Specific papers to analyze (by index or name)')
    parser.add_argument('--list', action='store_true',
                      help='List available papers')
    parser.add_argument('--input-dir', type=str,
                      help='Directory containing text files to analyze')
    parser.add_argument('--output-name', type=str,
                      help='Custom name for output file (without extension)')
    args = parser.parse_args()

    # List available papers if requested
    if args.list:
        list_available_papers(args.input_dir)
        return

    # Check for API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("Please set your ANTHROPIC_API_KEY environment variable")
        return

    try:
        analyzer = PaperAnalyzer(input_dir=args.input_dir)
        
        # Log start time
        start_time = time.time()
        analyzer.logger.info(f"Starting paper analysis in {args.mode} mode")
        
        # Analyze papers
        analyses = analyzer.analyze_papers(
            mode=args.mode, 
            batch_size=args.batch_size,
            paper_ids=args.papers
        )
        
        # Custom output filename if provided
        if args.output_name:
            output_file = analyzer.output_dir / f"{args.output_name}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(analyses, f, indent=2, ensure_ascii=False)
            analyzer.logger.info(f"Results saved to: {output_file}")
        
        # Log completion
        total_time = time.time() - start_time
        analyzer.logger.info(f"Analysis completed. Total time: {total_time:.2f}s")
        analyzer.logger.info(f"Successfully analyzed {len(analyses)} {'papers' if args.mode == 'single' else 'batches'}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return

if __name__ == "__main__":
    main() 