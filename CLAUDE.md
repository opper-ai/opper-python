# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Opper AI Python SDK**, an auto-generated client library built using Speakeasy from OpenAPI specifications. The SDK provides type-safe Python bindings for the Opper AI API, supporting functions, knowledge bases, datasets, embeddings, tracing, and analytics.

## Development Commands

### SDK Generation Workflow
```bash
# Full regeneration (recommended)
make generate          # Runs speakeasy, fixes params, applies schema patches

# Individual steps
make check-speakeasy   # Verify speakeasy CLI is installed
make fix-input-params  # Fix input_ parameters to input
make apply-schema-patch # Add Pydantic schema conversion handling
make test-patch        # Verify patches were applied correctly
```

### Testing and Quality
```bash
# Run tests (if test.py exists)
make test

# Lint and type checking
pylint src/            # Lint with project-specific config
mypy src/              # Type checking with mypy
```

### Development Utilities
```bash
make clean             # Reset to clean git state
make full              # Clean + generate + test
make preview-changes   # Show what would change without applying
```

## Architecture and Key Components

### SDK Generation System
This project uses **Speakeasy** to auto-generate SDK code from OpenAPI specs, with a custom **patching system** to preserve important modifications:

1. **Parameter Name Fixing**: Converts `input_` parameters to `input` for API consistency
2. **Schema Conversion Patches**: Adds Pydantic model → JSON schema conversion to SDK methods
3. **Automated Application**: All patches applied via `make generate`

### GitHub Actions Workflows
The project uses custom GitHub Actions workflows (not the standard Speakeasy workflows) due to the custom patching requirements:

- **`generate-sdk.yml`**: Automated SDK generation (manual trigger or weekly schedule)
- **`release.yml`**: Automated PyPI releases when version changes in `pyproject.toml`
- **`validate-pr.yml`**: PR validation and testing

### Core SDK Structure
- **`src/opperai/sdk.py`**: Main SDK entry point with `call`, `call_async`, `stream`, `stream_async` methods
- **`src/opperai/functions.py`**: Function management (create, update, delete, call)
- **`src/opperai/knowledge.py`**: Knowledge base operations
- **`src/opperai/datasets.py`**: Dataset management and querying
- **`src/opperai/spans.py` / `traces.py`**: Observability and tracing
- **`src/opperai/models/`**: Generated Pydantic models for all API types

### Schema Conversion Handling
The patching system adds this code block to SDK methods:
```python
# region convert-pydantic-schemas
if input_schema is not UNSET and hasattr(input_schema, 'model_json_schema'):
    input_schema = input_schema.model_json_schema()
if output_schema is not UNSET and hasattr(output_schema, 'model_json_schema'):
    output_schema = output_schema.model_json_schema()
# endregion convert-pydantic-schemas
```

This allows users to pass either Pydantic model classes (auto-converted) or plain dictionaries.

### Dependency Management
- **Poetry**: Primary dependency management (`pyproject.toml`, `poetry.lock`)
- **UV**: Alternative fast Python package installer (`uv.lock`)
- **Core Dependencies**: httpx, pydantic, httpcore

## Important Files and Locations

### Configuration Files
- **`pyproject.toml`**: Project metadata, dependencies, tool configuration
- **`pylintrc`**: Comprehensive linting rules with custom overrides
- **`.github/workflows/sdk_generation.yaml`**: Automated SDK generation via Speakeasy
- **`Makefile`**: All development automation targets

### Scripts and Automation
- **`scripts/apply_schema_patch.py`**: Python script that applies schema conversion patches
- **`SPEAKEASY_PATCH_README.md`**: Detailed documentation of the patching system

### Generated vs. Custom Code
- **Generated**: Everything in `src/opperai/` (except custom patches)
- **Custom**: Makefile, scripts/, patch system, configuration files
- **Examples**: `examples/` directory with usage patterns for all SDK features

## Release Process

### SDK Updates and Releases
The project follows this workflow for updates and releases:

1. **SDK Generation**: 
   - Manual: Go to GitHub Actions → "Generate SDK" → Run workflow
   - Automatic: Runs weekly on Mondays at 9 AM UTC
   - Creates PR with updated SDK code if changes detected

2. **Version Management**:
   - Speakeasy automatically updates version in `pyproject.toml` during generation
   - Starting from version `2.0.0` (manually set for this custom workflow transition)
   - Future versions managed by Speakeasy following semantic versioning
   - Version changes in merged PRs automatically trigger releases

3. **Automated Release**:
   - Push/merge to `main` with version change triggers `release.yml`
   - Builds package with UV
   - Publishes to PyPI automatically
   - Creates GitHub release with changelog

4. **Manual Release** (if needed):
   - Use "Release to PyPI" workflow in GitHub Actions
   - Typically only needed for hotfixes or urgent releases
   - Most releases happen automatically via SDK generation PRs

### Required Secrets
For the workflows to function, these GitHub secrets must be configured:
- `SPEAKEASY_API_KEY`: For SDK generation
- `PYPI_API_TOKEN`: For publishing to PyPI (use trusted publishing if possible)

## Development Guidelines

### Working with Generated Code
- **Never manually edit** files in `src/opperai/` - changes will be overwritten
- **Always use `make generate`** instead of `speakeasy run` directly
- **Patches are idempotent** - safe to run multiple times
- **Test patches** with `make test-patch` after structural changes

### Schema and Type Handling
- SDK supports both **Pydantic models** and **plain dictionaries** for schemas
- Pydantic models are automatically converted to JSON schema via patches
- Use `MyModel.model_json_schema()` when working with schemas manually

### Project Maintenance
- **Monitor Speakeasy updates** that might change code structure
- **Update patch patterns** in `apply_schema_patch.py` if SDK structure changes
- **Maintain backward compatibility** when modifying patch system
- **Test examples** in `examples/` directory after regeneration