from nomic import atlas
import inspect

# Check the signature of AtlasDataset
print("AtlasDataset signature:")
try:
    sig = inspect.signature(atlas.AtlasDataset.__init__)
    print(sig)
except Exception as e:
    print(f"Error getting signature: {e}")

# Try to understand what parameters AtlasDataset expects
print("\nAtlasDataset docstring:")
try:
    print(atlas.AtlasDataset.__doc__)
except Exception as e:
    print(f"Error getting docstring: {e}")

# Test different parameter combinations
print("\nTesting different AtlasDataset parameter combinations:")

ATLAS_ORGANIZATION_NAME = "talon-pro-se"
ATLAS_PROJECT_ID = "stephen-boerner-divorce-case-data-test-upload"

# Test 1: Try with name parameter
try:
    print("Testing with 'name' parameter...")
    dataset = atlas.AtlasDataset(name=ATLAS_PROJECT_ID, organization_name=ATLAS_ORGANIZATION_NAME)
    print("Success with 'name' parameter")
except Exception as e:
    print(f"Failed with 'name': {e}")

# Test 2: Try with identifier parameter
try:
    print("Testing with 'identifier' parameter...")
    dataset = atlas.AtlasDataset(identifier=ATLAS_PROJECT_ID, organization_name=ATLAS_ORGANIZATION_NAME)
    print("Success with 'identifier' parameter")
except Exception as e:
    print(f"Failed with 'identifier': {e}")

# Test 3: Try with just organization_name
try:
    print("Testing with only 'organization_name' parameter...")
    dataset = atlas.AtlasDataset(organization_name=ATLAS_ORGANIZATION_NAME)
    print("Success with only 'organization_name' parameter")
except Exception as e:
    print(f"Failed with only 'organization_name': {e}")

# Test 4: Try with no parameters
try:
    print("Testing with no parameters...")
    dataset = atlas.AtlasDataset()
    print("Success with no parameters")
except Exception as e:
    print(f"Failed with no parameters: {e}")