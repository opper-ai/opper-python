# Delta

Incremental content for streaming. Used for both unstructured text streaming (when no output_schema) and structured streaming (when output_schema is provided). For structured streaming, contains actual field values being streamed to the json_path location. Supports all JSON types: strings, numbers, booleans.


## Supported Types

### `str`

```python
value: str = /* values here */
```

### `int`

```python
value: int = /* values here */
```

### `float`

```python
value: float = /* values here */
```

### `bool`

```python
value: bool = /* values here */
```

