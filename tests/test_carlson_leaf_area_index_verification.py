import os
import numpy as np
import pandas as pd
import pytest

from carlson_leaf_area_index import carlson_leaf_area_index, inverse_carlson_NDVI

def test_carlson_leaf_area_index_against_verification():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    verification_path = os.path.join(repo_root, 'carlson_leaf_area_index', 'verification.csv')
    df = pd.read_csv(verification_path)
    ndvi = df['NDVI'].values
    expected_lai = df['LAI'].values
    calculated_lai = carlson_leaf_area_index(ndvi)
    np.testing.assert_allclose(calculated_lai, expected_lai, rtol=1e-5, atol=1e-8)

def test_inverse_carlson_NDVI_against_verification():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    verification_path = os.path.join(repo_root, 'carlson_leaf_area_index', 'verification.csv')
    df = pd.read_csv(verification_path)
    lai = df['LAI'].values
    expected_ndvi = df['inverted_NDVI'].values
    calculated_ndvi = inverse_carlson_NDVI(lai)
    np.testing.assert_allclose(calculated_ndvi, expected_ndvi, rtol=1e-5, atol=1e-8)
