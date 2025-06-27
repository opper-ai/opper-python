#!/usr/bin/env python3
"""
Script to apply schema conversion patches to the Opper SDK after Speakeasy generation.
This script adds Pydantic schema conversion handling to methods in:
- sdk.py: call, call_async, stream, stream_async
- functions.py: create, create_async, update, update_async
"""

import os
import re
import sys


def apply_sdk_schema_conversion_patch(file_path):
    """Apply schema conversion patches to the SDK file."""

    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found")
        return False

    with open(file_path, "r") as f:
        content = f.read()

    # The schema conversion block to insert
    schema_conversion_block = """
        # region convert-pydantic-schemas
        if input_schema is not UNSET and hasattr(input_schema, 'model_json_schema'):
            input_schema = input_schema.model_json_schema()
        if output_schema is not UNSET and hasattr(output_schema, 'model_json_schema'):
            output_schema = output_schema.model_json_schema()
        # endregion convert-pydantic-schemas
"""

    # Pattern to find where to insert the schema conversion
    # Look for the pattern where base_url is set, followed by request creation
    insert_pattern = r"(        else:\n            base_url = self\._get_url\(base_url, url_variables\)\n)\n(        request = models\.AppAPIPublicV2FunctionCallCallFunctionRequest\()"

    # Check if patches are already applied
    if "# region convert-pydantic-schemas" in content:
        print("⚠️  SDK schema conversion patches already exist, skipping...")
        return True

    # Apply the patch - insert the schema conversion block before request creation
    modified_content = re.sub(
        insert_pattern, r"\1" + schema_conversion_block + r"\n\2", content
    )

    # Check if any replacements were made
    if modified_content == content:
        print(
            "⚠️  No insertion points found in SDK - the SDK structure may have changed"
        )
        return False

    # Count how many times the pattern was replaced
    patch_count = len(
        re.findall(r"# region convert-pydantic-schemas", modified_content)
    )

    if patch_count == 0:
        print("❌ No schema conversion blocks were added to SDK")
        return False

    # Write the modified content back
    with open(file_path, "w") as f:
        f.write(modified_content)

    print(f"✅ Applied schema conversion patches to {patch_count} SDK methods")
    return True


def apply_functions_schema_conversion_patch(file_path):
    """Apply schema conversion patches to the functions.py file."""

    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found")
        return False

    with open(file_path, "r") as f:
        content = f.read()

    # The schema conversion block to insert
    schema_conversion_block = """
        # region convert-pydantic-schemas
        if input_schema is not UNSET and hasattr(input_schema, 'model_json_schema'):
            input_schema = input_schema.model_json_schema()
        if output_schema is not UNSET and hasattr(output_schema, 'model_json_schema'):
            output_schema = output_schema.model_json_schema()
        # endregion convert-pydantic-schemas
"""

    # Check if patches are already applied
    if "# region convert-pydantic-schemas" in content:
        print("⚠️  Functions schema conversion patches already exist, skipping...")
        return True

    # Patterns for create and create_async methods
    create_pattern = r"(        else:\n            base_url = self\._get_url\(base_url, url_variables\)\n)\n(        request = models\.CreateFunctionRequest\()"

    # Patterns for update and update_async methods
    update_pattern = r"(        else:\n            base_url = self\._get_url\(base_url, url_variables\)\n)\n(        request = models\.UpdateFunctionFunctionsFunctionIDPatchRequest\()"

    modified_content = content

    # Apply patches for create methods
    modified_content = re.sub(
        create_pattern, r"\1" + schema_conversion_block + r"\n\2", modified_content
    )

    # Apply patches for update methods
    modified_content = re.sub(
        update_pattern, r"\1" + schema_conversion_block + r"\n\2", modified_content
    )

    # Check if any replacements were made
    if modified_content == content:
        print(
            "⚠️  No insertion points found in functions.py - the structure may have changed"
        )
        return False

    # Count how many times the pattern was replaced
    patch_count = len(
        re.findall(r"# region convert-pydantic-schemas", modified_content)
    )

    if patch_count == 0:
        print("❌ No schema conversion blocks were added to functions.py")
        return False

    # Write the modified content back
    with open(file_path, "w") as f:
        f.write(modified_content)

    print(f"✅ Applied schema conversion patches to {patch_count} functions methods")
    return True


def main():
    """Main function."""
    sdk_file = "src/opperai/sdk.py"
    functions_file = "src/opperai/functions.py"

    print("🔧 Applying schema conversion patches...")

    sdk_success = apply_sdk_schema_conversion_patch(sdk_file)
    functions_success = apply_functions_schema_conversion_patch(functions_file)

    if sdk_success and functions_success:
        print("✅ All schema conversion patches applied successfully!")
        sys.exit(0)
    else:
        print("❌ Failed to apply some schema conversion patches")
        sys.exit(1)


if __name__ == "__main__":
    main()
