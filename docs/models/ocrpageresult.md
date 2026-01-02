# OCRPageResult

Result for a single processed page.


## Fields

| Field                                                                        | Type                                                                         | Required                                                                     | Description                                                                  |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `index`                                                                      | *int*                                                                        | :heavy_check_mark:                                                           | Page index (0-based)                                                         |
| `markdown`                                                                   | *str*                                                                        | :heavy_check_mark:                                                           | Extracted text in markdown format                                            |
| `dimensions`                                                                 | [OptionalNullable[models.OCRPageDimensions]](../models/ocrpagedimensions.md) | :heavy_minus_sign:                                                           | Page dimensions                                                              |
| `images`                                                                     | List[[models.OCRPageImage](../models/ocrpageimage.md)]                       | :heavy_minus_sign:                                                           | Extracted images from the page                                               |