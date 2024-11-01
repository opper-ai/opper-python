import importlib.util
import os

import pytest


def import_module_from_file(file_path):
    spec = importlib.util.spec_from_file_location("module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pytest_generate_tests(metafunc):
    if "example_file" in metafunc.fixturenames:
        example_files = []
        for root, _, files in os.walk("examples"):
            for file in files:
                if file.endswith(".py"):
                    example_files.append(os.path.join(root, file))
        metafunc.parametrize("example_file", example_files)


@pytest.mark.asyncio
async def test_example(example_file):
    module = import_module_from_file(example_file)

    if hasattr(module, "run_sync"):
        print(f"running sync function from {example_file}")
        module.run_sync()

    if hasattr(module, "run_async"):
        print(f"running async function from {example_file}")
        await module.run_async()

    # If neither run_sync nor run_async is present, the test passes silently
    assert True
