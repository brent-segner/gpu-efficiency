"""
Quick Start Example: GPU Efficiency Analysis
============================================
This script demonstrates basic usage of the GPU efficiency metrics
on the synthetic dataset without requiring Jupyter.
"""

import pandas as pd
import numpy as np

# GPU Specifications
GPU_SPECS = {
    'NVIDIA A100-SXM4-40GB': {
        'max_power': 400,
        'achievable_tflops_fp16': 102
    },
    'NVIDIA H100 80GB HBM3': {
        'max_power': 700,
        'achievable_tflops_fp16': 646
    },
    'NVIDIA A10G': {
        'max_power': 300,
        'achievable_tflops_fp16': 35
    }
}

def calculate_efficiency_metrics(df):
    """Calculate GPU efficiency metrics"""
    df = df.copy()
    
    # Map GPU specs
    df['max_power'] = df['MODELNAME'].map(lambda x: GPU_SPECS[x]['max_power'])
    df['achievable_tflops'] = df['MODELNAME'].map(lambda x: GPU_SPECS[x]['achievable_tflops_fp16'])
    
    # Calculate Power Intensity Factor (PIF)
    df['power_intensity_factor'] = df['DCGM_FI_DEV_POWER_USAGE'] / df['max_power']
    df['power_intensity_factor'] = df['power_intensity_factor'].clip(0, 1)
    
    # Calculate Realized TFLOPS
    df['realized_tflops'] = df['achievable_tflops'] * df['power_intensity_factor']
    
    # Calculate RFU percentage
    df['rfu_percent'] = (df['realized_tflops'] / df['achievable_tflops']) * 100
    
    # Calculate efficiency gap
    df['efficiency_gap'] = df['DCGM_FI_DEV_GPU_UTIL'] - df['rfu_percent']
    
    return df

def main():
    print("=" * 80)
    print("GPU EFFICIENCY ANALYSIS - QUICK START")
    print("=" * 80)
    
    # Load data
    print("\n1. Loading synthetic dataset...")
    df = pd.read_csv('synthetic_dcgm_metrics.csv')
    print(f"   ✓ Loaded {len(df):,} records")
    print(f"   ✓ Date range: {df['SCRAPETIME'].min()} to {df['SCRAPETIME'].max()}")
    
    # Calculate metrics
    print("\n2. Calculating efficiency metrics...")
    df = calculate_efficiency_metrics(df)
    print("   ✓ Power Intensity Factor (PIF) calculated")
    print("   ✓ Realized TFLOPS calculated")
    print("   ✓ Realized TFLOPS Utilization (RFU) calculated")
    
    # Fleet summary
    print("\n3. Fleet-Wide Metrics:")
    print("-" * 80)
    print(f"   Total GPUs: {df['UUID'].nunique()}")
    print(f"   Average GPU Utilization: {df['DCGM_FI_DEV_GPU_UTIL'].mean():.1f}%")
    print(f"   Average Power Intensity Factor: {df['power_intensity_factor'].mean():.3f}")
    print(f"   Average RFU: {df['rfu_percent'].mean():.1f}%")
    print(f"   Average Efficiency Gap: {df['efficiency_gap'].mean():.1f} percentage points")
    
    # Active GPUs only
    active_df = df[df['DCGM_FI_DEV_GPU_UTIL'] > 1]
    print(f"\n4. Active GPU Analysis (Utilization > 1%):")
    print("-" * 80)
    print(f"   Active samples: {len(active_df):,} ({len(active_df)/len(df)*100:.1f}%)")
    print(f"   Active Average Utilization: {active_df['DCGM_FI_DEV_GPU_UTIL'].mean():.1f}%")
    print(f"   Active Average RFU: {active_df['rfu_percent'].mean():.1f}%")
    print(f"   Active Efficiency Gap: {active_df['efficiency_gap'].mean():.1f} pp")
    
    # Model breakdown
    print("\n5. Performance by GPU Model:")
    print("-" * 80)
    model_stats = df.groupby('MODELNAME').agg({
        'UUID': 'nunique',
        'DCGM_FI_DEV_GPU_UTIL': 'mean',
        'power_intensity_factor': 'mean',
        'rfu_percent': 'mean',
        'efficiency_gap': 'mean'
    }).round(2)
    
    for model in model_stats.index:
        stats = model_stats.loc[model]
        print(f"\n   {model}:")
        print(f"      GPUs: {stats['UUID']}")
        print(f"      Avg Utilization: {stats['DCGM_FI_DEV_GPU_UTIL']:.1f}%")
        print(f"      Avg PIF: {stats['power_intensity_factor']:.3f}")
        print(f"      Avg RFU: {stats['rfu_percent']:.1f}%")
        print(f"      Efficiency Gap: {stats['efficiency_gap']:.1f} pp")
    
    # Bottleneck identification
    bottlenecked = active_df[
        (active_df['DCGM_FI_DEV_GPU_UTIL'] > 70) & 
        (active_df['power_intensity_factor'] < 0.60)
    ]
    
    print("\n6. Bottleneck Detection:")
    print("-" * 80)
    print(f"   Bottlenecked samples (>70% util, <60% PIF): {len(bottlenecked):,}")
    print(f"   Percentage of active samples: {len(bottlenecked)/len(active_df)*100:.1f}%")
    
    if len(bottlenecked) > 0:
        print("\n   Top bottlenecked GPUs by efficiency gap:")
        gpu_bottlenecks = bottlenecked.groupby('UUID').agg({
            'MODELNAME': 'first',
            'HOSTNAME': 'first',
            'efficiency_gap': 'mean',
            'DCGM_FI_DEV_GPU_UTIL': 'mean',
            'power_intensity_factor': 'mean'
        }).sort_values('efficiency_gap', ascending=False).head(5)
        
        for idx, (uuid, row) in enumerate(gpu_bottlenecks.iterrows(), 1):
            print(f"\n   {idx}. {row['MODELNAME']}")
            print(f"      UUID: {uuid}")
            print(f"      Host: {row['HOSTNAME']}")
            print(f"      Avg Util: {row['DCGM_FI_DEV_GPU_UTIL']:.1f}%")
            print(f"      Avg PIF: {row['power_intensity_factor']:.3f}")
            print(f"      Efficiency Gap: {row['efficiency_gap']:.1f} pp")
    
    # ROI Analysis
    print("\n7. ROI Potential:")
    print("-" * 80)
    current_rfu = df['rfu_percent'].mean()
    total_gpus = df['UUID'].nunique()
    
    for target_rfu in [50, 60, 70]:
        if target_rfu > current_rfu:
            improvement = target_rfu - current_rfu
            multiplier = target_rfu / current_rfu
            equivalent_gpus = (multiplier - 1) * total_gpus
            print(f"\n   Improving RFU from {current_rfu:.1f}% to {target_rfu}%:")
            print(f"      Efficiency gain: +{improvement:.1f} percentage points")
            print(f"      Equivalent to adding: {equivalent_gpus:.1f} GPUs")
            print(f"      Additional GPU-hours/day: {equivalent_gpus * 24:.0f}")
    
    print("\n" + "=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print("1. Open gpu_efficiency_analysis.ipynb for detailed visualizations")
    print("2. Review bottlenecked_gpus.csv for specific investigation targets")
    print("3. Analyze hourly_fleet_metrics.csv for time-based patterns")
    print("4. Check README.md for full documentation")
    print("=" * 80)

if __name__ == '__main__':
    main()
