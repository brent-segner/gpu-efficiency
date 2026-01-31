"""
GPU DCGM Metrics Synthetic Data Generator
==========================================
This script generates synthetic DCGM metrics data for GPU efficiency analysis.
It creates realistic scenarios including:
- High utilization with high power (efficient workloads)
- High utilization with low power (data-starved or bottlenecked workloads)
- Low utilization scenarios (idle or lightly loaded GPUs)
- Time series data across multiple days
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# GPU Model Specifications
GPU_SPECS = {
    'NVIDIA A100-SXM4-40GB': {
        'max_power': 400,  # Watts
        'idle_power': 50,
        'memory_total': 40960,  # MB
        'theoretical_tflops_fp16': 312,
        'achievable_tflops_fp16': 102
    },
    'NVIDIA H100 80GB HBM3': {
        'max_power': 700,  # Watts
        'idle_power': 70,
        'memory_total': 81920,  # MB
        'theoretical_tflops_fp16': 1979,
        'achievable_tflops_fp16': 646,
        'theoretical_tflops_fp8': 3958,
        'achievable_tflops_fp8': 1293
    },
    'NVIDIA A10G': {
        'max_power': 300,  # Watts
        'idle_power': 40,
        'memory_total': 24576,  # MB
        'theoretical_tflops_fp16': 125,
        'achievable_tflops_fp16': 35
    }
}

# Workload Scenarios
WORKLOAD_SCENARIOS = {
    'efficient_training': {
        'util_range': (85, 100),
        'power_pct_range': (0.85, 0.98),  # High power efficiency
        'memory_usage_pct': (0.7, 0.95),
        'description': 'Well-optimized training workload'
    },
    'data_starved': {
        'util_range': (80, 100),
        'power_pct_range': (0.35, 0.55),  # Low power despite high util
        'memory_usage_pct': (0.6, 0.85),
        'description': 'High utilization but data bottlenecked'
    },
    'network_bottleneck': {
        'util_range': (70, 95),
        'power_pct_range': (0.40, 0.60),
        'memory_usage_pct': (0.65, 0.90),
        'description': 'Network latency causing GPU stalls'
    },
    'moderate_load': {
        'util_range': (40, 70),
        'power_pct_range': (0.50, 0.75),
        'memory_usage_pct': (0.4, 0.7),
        'description': 'Moderate workload'
    },
    'idle': {
        'util_range': (0, 5),
        'power_pct_range': (0.05, 0.15),
        'memory_usage_pct': (0.05, 0.15),
        'description': 'Idle or minimal activity'
    },
    'inference': {
        'util_range': (30, 60),
        'power_pct_range': (0.45, 0.70),
        'memory_usage_pct': (0.3, 0.6),
        'description': 'Inference workload with bursty patterns'
    }
}

def generate_synthetic_data(num_gpus=50, days=7, samples_per_hour=60):
    """
    Generate synthetic DCGM metrics data
    
    Parameters:
    -----------
    num_gpus : int
        Number of GPU instances to simulate
    days : int
        Number of days of data to generate
    samples_per_hour : int
        Number of samples per hour (default 60 = 1 per minute)
    """
    
    records = []
    start_date = datetime(2026, 1, 20, 0, 0, 0)
    
    # Generate GPU instance configurations
    gpu_configs = []
    for i in range(num_gpus):
        gpu_model = random.choice(list(GPU_SPECS.keys()))
        cluster_num = (i // 20) + 1
        node_num = (i % 20) + 1
        
        # Assign workload scenarios with some persistence
        # 30% efficient, 20% data-starved, 15% network bottleneck, 20% moderate, 10% idle, 5% inference
        scenario_weights = [0.30, 0.20, 0.15, 0.20, 0.10, 0.05]
        primary_scenario = random.choices(
            list(WORKLOAD_SCENARIOS.keys()),
            weights=scenario_weights
        )[0]
        
        gpu_configs.append({
            'gpu_id': i,
            'model': gpu_model,
            'hostname': f'ip-10-247-{cluster_num}-{node_num}.us-west-2.compute.internal',
            'cluster': f'ai-factory-cluster-{cluster_num}',
            'region': 'us-west-2',
            'namespace': random.choice(['ml-training', 'ml-inference', 'research', 'fraud-detection']),
            'pod': f'workload-{i:04d}-{random.randint(1000,9999)}',
            'primary_scenario': primary_scenario,
            'uuid': f'GPU-{random.randint(10000000, 99999999):08x}-{random.randint(1000, 9999):04x}-{random.randint(1000, 9999):04x}'
        })
    
    # Generate time series data
    total_hours = days * 24
    total_samples = total_hours * samples_per_hour
    
    for hour_idx in range(total_hours):
        current_time = start_date + timedelta(hours=hour_idx)
        
        for sample_idx in range(samples_per_hour):
            scrape_time = current_time + timedelta(minutes=sample_idx)
            
            for gpu_config in gpu_configs:
                # Determine current scenario (mostly primary, occasionally switch)
                if random.random() < 0.05:  # 5% chance to temporarily switch scenario
                    current_scenario = random.choice(list(WORKLOAD_SCENARIOS.keys()))
                else:
                    current_scenario = gpu_config['primary_scenario']
                
                scenario = WORKLOAD_SCENARIOS[current_scenario]
                spec = GPU_SPECS[gpu_config['model']]
                
                # Generate utilization
                gpu_util = random.randint(*scenario['util_range'])
                
                # Generate power based on scenario
                power_pct = random.uniform(*scenario['power_pct_range'])
                power_range = spec['max_power'] - spec['idle_power']
                power_usage = spec['idle_power'] + (power_range * power_pct)
                
                # Add some noise
                power_usage += random.gauss(0, spec['max_power'] * 0.02)
                power_usage = max(spec['idle_power'], min(spec['max_power'], power_usage))
                
                # Generate memory usage
                memory_pct = random.uniform(*scenario['memory_usage_pct'])
                memory_used = int(spec['memory_total'] * memory_pct)
                memory_free = spec['memory_total'] - memory_used
                
                # Generate temperature (correlated with power)
                base_temp = 30
                temp_from_power = (power_usage / spec['max_power']) * 50
                gpu_temp = int(base_temp + temp_from_power + random.gauss(0, 3))
                gpu_temp = max(25, min(85, gpu_temp))
                
                # Generate other metrics
                sm_clock = int(1000 + (gpu_util / 100) * 700 + random.gauss(0, 50))
                mem_clock = int(5000 + random.gauss(0, 200))
                
                # Tensor core activity (higher for training workloads)
                tensor_active = 0
                if current_scenario in ['efficient_training', 'data_starved']:
                    tensor_active = int(gpu_util * 0.9 + random.gauss(0, 5))
                    tensor_active = max(0, min(100, tensor_active))
                
                # PCIe traffic (higher when data-starved or network bottlenecked)
                pcie_multiplier = 1.0
                if current_scenario in ['data_starved', 'network_bottleneck']:
                    pcie_multiplier = 2.5
                
                pcie_rx = int(random.randint(50000, 500000) * pcie_multiplier)
                pcie_tx = int(random.randint(50000, 500000) * pcie_multiplier)
                
                record = {
                    'ACTIVITYDATE': current_time.strftime('%m/%d/%y'),
                    'ACTIVITYHOUR': current_time.hour,
                    'HOSTNAME': gpu_config['hostname'],
                    'SCRAPETIME': scrape_time.strftime('%m/%d/%y %H:%M'),
                    'CLOUDREGION': gpu_config['region'],
                    'CLUSTERNAME': gpu_config['cluster'],
                    'MODELNAME': gpu_config['model'],
                    'UUID': gpu_config['uuid'],
                    'NAMESPACE': gpu_config['namespace'],
                    'DCGM_FI_DEV_CORRECTABLE_REMAPPED_ROWS': 0,
                    'DCGM_FI_DEV_DEC_UTIL': 0,
                    'DCGM_FI_DEV_ENC_UTIL': 0,
                    'DCGM_FI_DEV_FB_FREE': memory_free,
                    'DCGM_FI_DEV_FB_USED': memory_used,
                    'DCGM_FI_DEV_GPU_TEMP': gpu_temp,
                    'DCGM_FI_DEV_GPU_UTIL': gpu_util,
                    'DCGM_FI_DEV_MEMORY_TEMP': gpu_temp - 5,
                    'DCGM_FI_DEV_MEM_CLOCK': mem_clock,
                    'DCGM_FI_DEV_MEM_COPY_UTIL': int(gpu_util * 0.6 + random.gauss(0, 5)),
                    'DCGM_FI_DEV_NVLINK_BANDWIDTH_TOTAL': 0,
                    'DCGM_FI_DEV_PCIE_REPLAY_COUNTER': 0,
                    'DCGM_FI_DEV_POWER_USAGE': round(power_usage, 3),
                    'DCGM_FI_DEV_ROW_REMAP_FAILURE': 0,
                    'DCGM_FI_DEV_SM_CLOCK': sm_clock,
                    'DCGM_FI_DEV_TOTAL_ENERGY_CONSUMPTION': round(power_usage * 3600 * hour_idx, 2),
                    'DCGM_FI_DEV_UNCORRECTABLE_REMAPPED_ROWS': 0,
                    'DCGM_FI_DEV_VGPU_LICENSE_STATUS': 0,
                    'DCGM_FI_DEV_XID_ERRORS': 0,
                    'DCGM_FI_PROF_DRAM_ACTIVE': int(gpu_util * 0.7 + random.gauss(0, 5)),
                    'DCGM_FI_PROF_GR_ENGINE_ACTIVE': gpu_util,
                    'DCGM_FI_PROF_PCIE_RX_BYTES': pcie_rx,
                    'DCGM_FI_PROF_PCIE_TX_BYTES': pcie_tx,
                    'DCGM_FI_PROF_PIPE_TENSOR_ACTIVE': tensor_active,
                    'NODEGROUP': None,
                    'POD': gpu_config['pod'],
                    'CONTAINER': 'primary'
                }
                
                records.append(record)
    
    df = pd.DataFrame(records)
    return df

if __name__ == '__main__':
    print("Generating synthetic DCGM metrics data...")
    print("Configuration:")
    print("  - GPUs: 50")
    print("  - Days: 7")
    print("  - Samples per hour: 60 (1 per minute)")
    print("  - Total records: ~504,000")
    
    df = generate_synthetic_data(num_gpus=50, days=7, samples_per_hour=60)
    
    output_file = 'synthetic_dcgm_metrics.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\nData generated successfully!")
    print(f"Output file: {output_file}")
    print(f"Total records: {len(df):,}")
    print(f"\nDataset summary:")
    print(f"  Date range: {df['ACTIVITYDATE'].min()} to {df['ACTIVITYDATE'].max()}")
    print(f"  GPU models: {df['MODELNAME'].unique().tolist()}")
    print(f"  Clusters: {df['CLUSTERNAME'].nunique()}")
    print(f"  Unique GPUs: {df['UUID'].nunique()}")
