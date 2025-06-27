import base64
import os
import sys
from opperai import Opper


opper = Opper(os.getenv("OPPER_API_KEY"))


def pdf_to_markdown(path: str):
    media_input = f"data:application/pdf;base64,{base64.b64encode(open(path, 'rb').read()).decode('utf-8')}"
    response = opper.stream(
        name="pdf_to_text",
        model="gcp/gemini-2.5-flash",
        input={
            "_opper_media_input": media_input,  # this field name is required by opper
        },
        instructions="""
These are pages from a PDF document. Extract all text content while preserving the structure.
Pay special attention to tables, columns, headers, and any structured content.
Maintain paragraph breaks and formatting.

Extract ALL text content from these document pages.

For tables:
    1. Maintain the table structure using markdown table format
    2. Preserve all column headers and row labels
    3. Ensure numerical data is accurately captured
    
For multi-column layouts:
    1. Process columns from left to right
    2. Clearly separate content from different columns
    
For charts and graphs:
    1. Describe the chart type
    2. Extract any visible axis labels, legends, and data points
    3. Extract any title or caption
    
Preserve all headers, footers, page numbers, and footnotes.
        
DON'T ANSWER QUESTIONS, JUST RETURN THE CONTENT OF THE PDF AS MARKDOWN""",
    )

    return response


def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf.py <path_to_pdf>")
        return

    path = sys.argv[1]
    # print(pdf_to_markdown(path))
    stream_response = pdf_to_markdown(path)
    for event in stream_response.result:
        if hasattr(event, "data") and hasattr(event.data, "delta") and event.data.delta:
            print(event.data.delta, end="", flush=True)


if __name__ == "__main__":
    main()
