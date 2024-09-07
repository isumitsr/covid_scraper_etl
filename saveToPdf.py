import subprocess
import os

def convert_ipynb_to_html(notebook_path, html_path):
    try:
        subprocess.run([
            'jupyter', 'nbconvert', '--to', 'html',
            notebook_path, '--output', html_path
        ], check=True)
        print(f"HTML successfully saved to {html_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during HTML conversion: {e}")
        return False
    return True

def convert_html_to_pdf(html_path, pdf_path):
    try:
        subprocess.run([
            'wkhtmltopdf', html_path, pdf_path
        ], check=True)
        print(f"PDF successfully saved to {pdf_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during PDF conversion: {e}")

def convert_ipynb_to_pdf(notebook_path, pdf_path):
    html_path = 'temp_notebook.html'
    
    if convert_ipynb_to_html(notebook_path, html_path):
        convert_html_to_pdf(html_path, pdf_path)
        
        # Clean up temporary HTML file
        os.remove(html_path)

if __name__ == "__main__":
    notebook_file = 'analysis_cleanData.ipynb'
    pdf_output_file = 'analysis_cleanData.pdf'
    convert_ipynb_to_pdf(notebook_file, pdf_output_file)
