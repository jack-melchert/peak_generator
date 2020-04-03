import pytest
import magma.backend.coreir_


@pytest.fixture(autouse=True)
def peak_generator_test():
    magma.backend.coreir_.CoreIRContextSingleton().reset_instance()

