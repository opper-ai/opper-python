import sys
from pathlib import Path

from opperai import AsyncOpper
from opperai.functions.async_functions import AsyncStreamingResponse
from opperai.types import FileInput

opper = AsyncOpper()


async def pdf_to_markdown(path: str) -> AsyncStreamingResponse:
    text = await opper.call(
        name="pdf_to_text",
        model="gcp/gemini-2.0-flash",
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
        input=FileInput.from_path(Path(path)),
        stream=True,
    )

    return text


async def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf.py <path_to_pdf>")
        return

    path = sys.argv[1]

    res = await pdf_to_markdown(path)
    async for chunk in res.deltas:
        print(chunk, end="", flush=True)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
