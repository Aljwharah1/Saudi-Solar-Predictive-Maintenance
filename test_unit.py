import pytest
import pandas as pd
import numpy as np

def maintenace_logic(row):
    if row["dust_level"] > 0.7 or row['module_temp'] > 60:
        return 1 
    else: 
        return 0 

def test_high_temperature_trigger():
    sample_data = {'dust_level': 0.2, 'module_temp': 65} 
    assert maintenace_logic(sample_data) == 1

def test_high_dust_trigger():
    sample_data = {'dust_level': 0.8, 'module_temp': 40} 
    assert maintenace_logic(sample_data) == 1

def test_normal_conditions():
    sample_data = {'dust_level': 0.3, 'module_temp': 35} 
    assert maintenace_logic(sample_data) == 0

def test_dataset_integrity():
    df = pd.read_csv('data/sudair_solar_ready_for_model.csv')
    
    assert df['ambient_temp'].isnull().sum() == 0
    assert df['module_temp'].isnull().sum() == 0
    
    allowed_values = {0, 1}
    assert set(df['needs_maintenance'].unique()).issubset(allowed_values)