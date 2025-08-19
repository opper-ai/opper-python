<!-- Start SDK Example Usage [usage] -->
```python
# Synchronous Example
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.call(name="add_numbers", instructions="Calculate the sum of two numbers", input_schema={
        "properties": {
            "x": {
                "title": "X",
                "type": "integer",
            },
            "y": {
                "title": "Y",
                "type": "integer",
            },
        },
        "required": [
            "x",
            "y",
        ],
        "title": "OpperInputExample",
        "type": "object",
    }, output_schema={
        "properties": {
            "sum": {
                "title": "Sum",
                "type": "integer",
            },
        },
        "required": [
            "sum",
        ],
        "title": "OpperOutputExample",
        "type": "object",
    }, input={
        "x": 4,
        "y": 5,
    }, examples=[
        {
            "input": {
                "x": 1,
                "y": 3,
            },
            "output": {
                "sum": 4,
            },
            "comment": "Adds two numbers",
        },
    ], parent_span_id="123e4567-e89b-12d3-a456-426614174000", tags={
        "project": "project_456",
        "user": "company_123",
    }, configuration={})

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from opperai import Opper
import os

async def main():

    async with Opper(
        http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
    ) as opper:

        res = await opper.call_async(name="add_numbers", instructions="Calculate the sum of two numbers", input_schema={
            "properties": {
                "x": {
                    "title": "X",
                    "type": "integer",
                },
                "y": {
                    "title": "Y",
                    "type": "integer",
                },
            },
            "required": [
                "x",
                "y",
            ],
            "title": "OpperInputExample",
            "type": "object",
        }, output_schema={
            "properties": {
                "sum": {
                    "title": "Sum",
                    "type": "integer",
                },
            },
            "required": [
                "sum",
            ],
            "title": "OpperOutputExample",
            "type": "object",
        }, input={
            "x": 4,
            "y": 5,
        }, examples=[
            {
                "input": {
                    "x": 1,
                    "y": 3,
                },
                "output": {
                    "sum": 4,
                },
                "comment": "Adds two numbers",
            },
        ], parent_span_id="123e4567-e89b-12d3-a456-426614174000", tags={
            "project": "project_456",
            "user": "company_123",
        }, configuration={})

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->