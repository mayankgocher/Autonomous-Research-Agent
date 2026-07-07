import os
from agents.state import ResearchState
from agents.llm import get_llm
from langchain_core.messages import HumanMessage
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def report_agent(state: ResearchState) -> ResearchState:
    """Generate final Markdown and PDF report."""
    llm = get_llm(temperature=0.3)
    
    prompt = f"""You are an AI Research Lead.
Based on the following research components, generate a comprehensive final research report in Markdown.
The report MUST include:
1. Executive Summary
2. Detailed Analysis
3. Key Findings
4. Future Research Directions
5. References

Topic: {state['query']}
Subtasks: {state.get('subtasks', [])}
Comparison Table:
{state.get('comparison_table', 'None')}

Fact Check Findings:
{state.get('fact_check_results', 'None')}

Arxiv Results (for references):
{[{'title': r['title'], 'url': r['url']} for r in state.get('arxiv_results', [])]}
"""
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        markdown_content = response.content.strip()
        state['final_report_markdown'] = markdown_content
        
        # Generate PDF
        pdf_path = os.path.abspath(f"./data/reports/report_{state['research_id']}.pdf")
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        generate_pdf_report(markdown_content, pdf_path)
        state['final_report_pdf'] = pdf_path
        
    except Exception as e:
        print(f"Report agent error: {e}")
        state['errors'].append(f"Report error: {e}")
        
    return state

def generate_pdf_report(markdown_text: str, output_path: str):
    """Very basic markdown to pdf conversion."""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    Story = []
    
    for line in markdown_text.split('\n'):
        if not line.strip():
            Story.append(Spacer(1, 12))
            continue
            
        style = styles["Normal"]
        if line.startswith('# '):
            style = styles["Heading1"]
            line = line[2:]
        elif line.startswith('## '):
            style = styles["Heading2"]
            line = line[3:]
        elif line.startswith('### '):
            style = styles["Heading3"]
            line = line[4:]
            
        Story.append(Paragraph(line, style))
        Story.append(Spacer(1, 6))
        
    doc.build(Story)
