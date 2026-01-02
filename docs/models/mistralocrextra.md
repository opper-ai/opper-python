# MistralOCRExtra

Mistral-specific OCR parameters.


## Fields

| Field                                              | Type                                               | Required                                           | Description                                        |
| -------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------- |
| `extract_header`                                   | *OptionalNullable[bool]*                           | :heavy_minus_sign:                                 | Whether to extract header content from pages       |
| `extract_footer`                                   | *OptionalNullable[bool]*                           | :heavy_minus_sign:                                 | Whether to extract footer content from pages       |
| `table_format`                                     | *OptionalNullable[str]*                            | :heavy_minus_sign:                                 | Format for extracted tables: 'markdown' or 'html'  |
| `bbox_annotation_format`                           | Dict[str, *Any*]                                   | :heavy_minus_sign:                                 | JSON schema for structured bounding box extraction |
| `document_annotation_format`                       | Dict[str, *Any*]                                   | :heavy_minus_sign:                                 | JSON schema for structured document extraction     |