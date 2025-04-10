from fpdf import FPDF

def create_resume_match_pdf(email, job_description, analysis):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Resume-JD Match Report", ln=True, align='C')
    pdf.ln(10)

    pdf.multi_cell(0, 10, f"Email: {email}")
    pdf.multi_cell(0, 10, f"Job Description:\n{job_description}")
    pdf.multi_cell(0, 10, f"\nAnalysis:\n{analysis}")

    file_path = f"resume_match_{email.replace('@', '_')}.pdf"
    pdf.output(file_path)
    return file_path