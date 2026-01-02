# OCRResponseModel

Response model for OCR processing.


## Fields

| Field                                                    | Type                                                     | Required                                                 | Description                                              |
| -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| `id`                                                     | *str*                                                    | :heavy_check_mark:                                       | Unique identifier for this OCR request                   |
| `pages`                                                  | List[[models.OCRPageResult](../models/ocrpageresult.md)] | :heavy_check_mark:                                       | Processed page results                                   |
| `model`                                                  | *str*                                                    | :heavy_check_mark:                                       | The model used for OCR                                   |
| `usage_info`                                             | [models.OCRUsageInfo](../models/ocrusageinfo.md)         | :heavy_check_mark:                                       | Usage information for OCR processing.                    |
| `cost`                                                   | [OptionalNullable[models.OCRCost]](../models/ocrcost.md) | :heavy_minus_sign:                                       | Cost information for this OCR request                    |