from fpdf import FPDF
from typing import Type
from pydantic import BaseModel, Field
from crewai_tools import BaseTool
import os
import unicodedata


class TextToPDFToolInput(BaseModel):
    """Input for TextToPDFTool."""

    summary_text: str = Field(
        ..., description="The text summary to be converted into a PDF."
    )
    output_file: str = Field(
        ..., description="The path where the output PDF file will be saved."
    )


class TextToPDFTool(BaseTool):
    name: str = "Text to PDF Converter"
    description: str = "Converts a provided text summary into a formatted PDF document."
    args_schema: Type[BaseModel] = TextToPDFToolInput

    def _run(
        self,
        summary_text: str,
        output_file: str = "output/Youtube_Video_Analysis_Report.pdf",
    ) -> str:
        try:
            # Ensure the directory for the output file exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            def remove_special_characters(text):
                normalized_text = unicodedata.normalize("NFKD", text)
                return normalized_text.encode("latin-1", "ignore").decode("latin-1")

            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            pdf.set_font("Arial", size=12)
            line_height = 6

            for line in summary_text.splitlines():
                line = line.strip()
                line = remove_special_characters(line)

                if line.startswith("#### "):
                    pdf.set_font("Arial", "B", size=12)
                    pdf.cell(0, line_height * 1.8, line[4:], align="C")
                elif line.startswith("### "):
                    pdf.set_font("Arial", "B", size=14)
                    pdf.cell(0, line_height * 1.8, line[3:], align="C")
                elif line.startswith("## "):
                    pdf.set_font("Arial", "B", size=16)
                    pdf.cell(0, line_height * 1.8, line[2:], align="C")
                elif "**" in line:
                    parts = line.split("**")
                    for i, part in enumerate(parts):
                        if i % 2 == 1:
                            pdf.set_font("Arial", "B", size=10)
                        else:
                            pdf.set_font("Arial", size=10)
                        pdf.multi_cell(0, line_height, part)
                    pdf.ln(line_height / 2)
                else:
                    pdf.set_font("Arial", size=10)
                    pdf.multi_cell(0, line_height, line)

            output_path = os.path.abspath(output_file)
            pdf.output(output_path)

            return f"PDF successfully created and saved to {output_path}"
        except Exception as e:
            return f"An error occurred while creating the PDF: {str(e)}"
