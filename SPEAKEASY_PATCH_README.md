# Speakeasy Patch System

This project uses a custom patching system to preserve important modifications after Speakeasy SDK generation.

## Overview

Speakeasy generates the SDK code from OpenAPI specifications, but overwrites any manual changes during regeneration. To solve this problem, we've implemented an automated patching system that applies necessary fixes after each generation.

## What Gets Patched

### 1. Input Parameter Names
- **Problem**: Speakeasy generates `input_` parameters instead of `input`
- **Solution**: Automatically renamed to `input` for better API consistency

### 2. Schema Conversion Handling  
- **Problem**: Pydantic models need to be converted to JSON schemas before sending to API
- **Solution**: Adds robust `hasattr()` checks and calls `model_json_schema()` when available
- **Location**: All four SDK methods (`call`, `call_async`, `stream`, `stream_async`)

## Usage

### Full Generation Workflow
```bash
make generate
```
This runs:
1. `speakeasy run` - Generate fresh SDK code
2. `make fix-input-params` - Fix parameter naming
3. `make apply-schema-patch` - Add schema conversion handling

### Individual Steps
```bash
# Fix just the input parameter names
make fix-input-params

# Apply just the schema conversion patches
make apply-schema-patch

# Test that patches were applied correctly
make test-patch
```

### Clean and Regenerate
```bash
# Reset to clean state and regenerate everything
make clean
make generate
```

## Files

### Scripts
- `scripts/apply_schema_patch.py` - Python script that intelligently applies schema conversion patches
- `Makefile` - Contains all automation targets

### Generated Files (Modified by Patches)
- `src/opperai/sdk.py` - Main SDK file with schema conversion handling
- Various model files - Fixed input parameter names

## Schema Conversion Details

The patch adds this block to each of the four SDK methods:

```python
# region convert-pydantic-schemas
if input_schema is not UNSET and hasattr(input_schema, 'model_json_schema'):
    input_schema = input_schema.model_json_schema()
if output_schema is not UNSET and hasattr(output_schema, 'model_json_schema'):
    output_schema = output_schema.model_json_schema()
# endregion convert-pydantic-schemas
```

This allows users to pass either:
- Pydantic model classes (automatically converted to JSON schema)
- Plain dictionaries (passed through unchanged)

## Patch Safety

- **Idempotent**: Running patches multiple times is safe
- **Detection**: Script detects existing patches and skips if already applied
- **Targeted**: Uses precise regex patterns to avoid unintended modifications
- **Validation**: Counts applied patches to ensure all methods were updated

## Development

### Testing Patches
```bash
# Test that patches apply correctly
make test-patch

# Preview what would be changed without applying
make preview-changes
```

### Adding New Patches

1. Create/modify the Python script in `scripts/apply_schema_patch.py`
2. Add appropriate regex patterns for your changes
3. Update the Makefile if needed
4. Test with `make test-patch`

## Troubleshooting

### "No insertion points found"
- The SDK structure may have changed
- Update the regex patterns in `apply_schema_patch.py`
- Check that Speakeasy generated the expected code structure

### Wrong number of patches applied
- Check the count in the test output
- Verify all four methods exist in the SDK
- Ensure patterns match the current code structure

### Patches not persisting
- Make sure you're using `make generate` instead of `speakeasy run` directly
- Check that the patch script has execute permissions
- Verify the Makefile includes the patch application step 