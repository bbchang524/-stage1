"""AI Study Assistant demo: offline extractive NLP, clearly labeled baseline."""
import gradio as gr
from pypdf import PdfReader
from engine import summarize, answer

def load_file(file):
    if file is None:return '', 'Upload a PDF or TXT file.'
    path=file.name
    try:
        if path.lower().endswith('.pdf'):
            reader=PdfReader(path)
            text='\n'.join(page.extract_text() or '' for page in reader.pages[:30])
        elif path.lower().endswith('.txt'):
            with open(path,'r',encoding='utf-8',errors='replace') as f:text=f.read()
        else:return '', 'Only PDF and TXT files are supported.'
        text=text[:120000]
        if not text.strip():return '', 'No selectable text found (scanned PDFs are not supported).'
        return text, f'Loaded {len(text):,} characters.'
    except Exception as e:return '', f'Could not read file: {type(e).__name__}: {e}'

with gr.Blocks(title='AI Study Assistant') as demo:
    gr.Markdown('# AI Study Assistant\nOffline extractive NLP prototype. **No LLM is used in this version.**')
    file=gr.File(label='Upload PDF or TXT',file_types=['.pdf','.txt'])
    status=gr.Textbox(label='Status',interactive=False)
    doc=gr.State('')
    file.change(load_file,inputs=file,outputs=[doc,status])
    with gr.Tab('Summarize'):
        summary=gr.Textbox(label='Key sentences',lines=9)
        gr.Button('Extract summary').click(summarize,inputs=doc,outputs=summary)
    with gr.Tab('Ask document'):
        question=gr.Textbox(label='Question',placeholder='What is the main benefit?')
        result=gr.Textbox(label='Relevant excerpts',lines=9)
        gr.Button('Find answer passages').click(answer,inputs=[doc,question],outputs=result)
    gr.Markdown('**Limitations:** extractive matching only; English text; no OCR; no hallucinated answers. Planned future work: LLM-based generation and Intel Arc Pro B70 validation.')
if __name__=='__main__':demo.launch(inbrowser=True)
