.PHONY: help generate fix-input-params apply-schema-patch check-speakeasy clean test test-patch

# Default target
help:
	@echo "Available targets:"
	@echo "  generate           - Run speakeasy generation and apply all fixes"
	@echo "  fix-input-params   - Fix input_ parameter names to input (post-generation)"
	@echo "  apply-schema-patch - Apply schema conversion handling to SDK methods"
	@echo "  test-patch         - Test the schema patch application"
	@echo "  check-speakeasy    - Check if speakeasy CLI is installed"
	@echo "  clean              - Clean generated files and reset to fresh state"
	@echo "  test               - Run tests"
	@echo "  help               - Show this help message"

# Check if speakeasy is installed
check-speakeasy:
	@command -v speakeasy >/dev/null 2>&1 || { \
		echo >&2 "Error: speakeasy CLI is not installed. Please install it first."; \
		echo >&2 "Visit: https://speakeasy.com/docs/getting-started"; \
		exit 1; \
	}
	@echo "✅ Speakeasy CLI is installed"

# Main generation target - runs speakeasy and applies all fixes
generate: check-speakeasy
	@echo "🚀 Running Speakeasy generation..."
	speakeasy run
	@echo "✅ Speakeasy generation completed"
	@echo "🔧 Fixing input parameter names..."
	$(MAKE) fix-input-params
	@echo "🔧 Applying schema conversion patches..."
	$(MAKE) apply-schema-patch
	@echo "✅ Generation and all fixes completed successfully!"

# Fix input_ parameter names to input and type_ to type
fix-input-params:
	@echo "🔧 Fixing input_ parameter names to input and type_ to type..."
	
	# Fix parameter definitions in function signatures
	@find src -name "*.py" -exec sed -i.bak 's/input_: OptionalNullable\[Any\] = UNSET/input: OptionalNullable[Any] = UNSET/g' {} \; -exec rm {}.bak \;
	@find src -name "*.py" -exec sed -i.bak 's/input_: OptionalNullable\[str\] = UNSET/input: OptionalNullable[str] = UNSET/g' {} \; -exec rm {}.bak \;
	@find src -name "*.py" -exec sed -i.bak 's/input_: Union\[models\.Input, models\.InputTypedDict\]/input: Union[models.Input, models.InputTypedDict]/g' {} \; -exec rm {}.bak \;
	@find src -name "*.py" -exec sed -i.bak 's/input_: str/input: str/g' {} \; -exec rm {}.bak \;
	@find src -name "*.py" -exec sed -i.bak 's/input_: Any/input: Any/g' {} \; -exec rm {}.bak \;
	@find src -name "*.py" -exec sed -i.bak 's/type_: OptionalNullable\[str\] = UNSET/type: OptionalNullable[str] = UNSET/g' {} \; -exec rm {}.bak \;
	
	# Fix parameter usage in function calls
	@find src -name "*.py" -exec sed -i.bak 's/input=input_,/input=input,/g' {} \; -exec rm {}.bak \;
	@find src -name "*.py" -exec sed -i.bak 's/type=type_,/type=type,/g' {} \; -exec rm {}.bak \;
	
	# Fix test files
	@if [ -f test.py ]; then \
		sed -i.bak 's/input_=/input=/g' test.py && rm test.py.bak; \
		sed -i.bak 's/input_schema=CountryInput,/input_schema=CountryInput.model_json_schema(),/g' test.py && rm test.py.bak; \
		sed -i.bak 's/output_schema=CapitalOutput,/output_schema=CapitalOutput.model_json_schema(),/g' test.py && rm test.py.bak; \
	fi
	
	# Fix documentation files
	@if [ -f USAGE.md ]; then \
		sed -i.bak 's/input_={/input={/g' USAGE.md && rm USAGE.md.bak; \
	fi
	@if [ -f README.md ]; then \
		sed -i.bak 's/input_={/input={/g' README.md && rm README.md.bak; \
	fi
	@if [ -f README-PYPI.md ]; then \
		sed -i.bak 's/input_={/input={/g' README-PYPI.md && rm README-PYPI.md.bak; \
	fi
	
	# Fix all docs/ directory README files
	@find docs -name "README.md" -exec sed -i.bak 's/input_=/input=/g' {} \; -exec rm {}.bak \;
	@find docs -name "*.md" -exec sed -i.bak 's/input_="/input="/g' {} \; -exec rm {}.bak \;
	@find docs -name "*.md" -exec sed -i.bak 's/type_="/type="/g' {} \; -exec rm {}.bak \;
	
	@echo "✅ Input and type parameter names fixed successfully"

# Apply schema conversion patches to SDK methods
apply-schema-patch:
	@python3 scripts/apply_schema_patch.py

# Clean generated files (requires git)
clean:
	@echo "🧹 Cleaning generated files..."
	@if [ ! -d .git ]; then \
		echo "❌ Error: This is not a git repository. Cannot clean safely."; \
		exit 1; \
	fi
	@git checkout HEAD -- src/ docs/ USAGE.md README.md 2>/dev/null || true
	@git checkout HEAD -- README-PYPI.md 2>/dev/null || true
	@git checkout HEAD -- test.py test_example_app.py 2>/dev/null || true
	@echo "✅ Cleaned successfully - files reset to last committed state"

# Run tests
test:
	@echo "🧪 Running tests..."
	@if [ -f test.py ]; then \
		python test.py; \
	else \
		echo "❌ No test.py file found"; \
		exit 1; \
	fi

# Full workflow: clean, generate, and test
full: clean generate test
	@echo "🎉 Full workflow completed successfully!"

# Test the patch application (for development)
test-patch: apply-schema-patch
	@echo "🧪 Testing schema patch application..."
	@grep -c "# region convert-pydantic-schemas" src/opperai/sdk.py | xargs -I {} echo "Found {} schema conversion blocks"
	@echo "✅ Patch test completed"

# Check what would be changed (dry run)
preview-changes:
	@echo "🔍 Preview of changes that would be made:"
	@echo "Files that contain 'input_:':"
	@find src -name "*.py" -exec grep -l "input_:" {} \; 2>/dev/null || echo "No files found with input_:"
	@echo ""
	@echo "Files that contain 'input=input_,':"
	@find src -name "*.py" -exec grep -l "input=input_," {} \; 2>/dev/null || echo "No files found with input=input_," 