# OCRPageImage

An image extracted from a page.


## Fields

| Field                                                    | Type                                                     | Required                                                 | Description                                              |
| -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| `id`                                                     | *str*                                                    | :heavy_check_mark:                                       | Unique identifier for the image                          |
| `top_left_x`                                             | *OptionalNullable[int]*                                  | :heavy_minus_sign:                                       | X coordinate of top-left corner                          |
| `top_left_y`                                             | *OptionalNullable[int]*                                  | :heavy_minus_sign:                                       | Y coordinate of top-left corner                          |
| `bottom_right_x`                                         | *OptionalNullable[int]*                                  | :heavy_minus_sign:                                       | X coordinate of bottom-right corner                      |
| `bottom_right_y`                                         | *OptionalNullable[int]*                                  | :heavy_minus_sign:                                       | Y coordinate of bottom-right corner                      |
| `image_base64`                                           | *OptionalNullable[str]*                                  | :heavy_minus_sign:                                       | Base64-encoded image data (if include_image_base64=True) |