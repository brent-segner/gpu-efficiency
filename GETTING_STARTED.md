# Getting Started with GPU Efficiency Analytics

## 🚀 Quick Start Guide

### Step 1: Download and Setup

```bash
# Navigate to the project directory
cd gpu_efficiency_analytics

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Explore the Synthetic Data

The dataset is already generated! Check it out:

```bash
# Quick analysis (no Jupyter required)
python quick_start.py
```

This will show you:
- ✅ Fleet-wide efficiency metrics
- ✅ Performance by GPU model
- ✅ Bottlenecked GPU identification
- ✅ ROI potential calculations

**Expected Output:**
```
GPU EFFICIENCY ANALYSIS - QUICK START
========================================
Total GPUs: 50
Average GPU Utilization: 70.4%
Average RFU: 65.5%
Bottlenecked samples: 26.8%
```

### Step 3: Deep Dive with Jupyter

For visualizations and detailed analysis:

```bash
# Launch Jupyter Notebook
jupyter notebook gpu_efficiency_analysis.ipynb
```

**What you'll get:**
- 📊 6 comprehensive visualizations
- 📈 Time series analysis
- 🎯 Bottleneck identification
- 💰 ROI calculations
- 📉 Workload pattern analysis

### Step 4: Customize for Your Environment

#### Add Your GPU Models

Edit `generate_synthetic_data.py` or the notebook:

```python
GPU_SPECS['Your GPU Model'] = {
    'max_power': 500,  # Watts
    'achievable_tflops_fp16': 200
}
```

#### Generate New Data

```bash
# Modify parameters in generate_synthetic_data.py
python generate_synthetic_data.py

# Then run analysis
python quick_start.py
```

## 📁 Project Structure

```
gpu_efficiency_analytics/
│
├── 📊 Data Files
│   └── synthetic_dcgm_metrics.csv (132MB, 504k records)
│
├── 🐍 Python Scripts
│   ├── generate_synthetic_data.py (Data generator)
│   └── quick_start.py (Quick CLI analysis)
│
├── 📓 Jupyter Notebook
│   └── gpu_efficiency_analysis.ipynb (Full analysis)
│
├── 📖 Documentation
│   ├── README.md (Main documentation)
│   ├── PROJECT_SUMMARY.md (Overview)
│   ├── CONTRIBUTING.md (Contribution guide)
│   └── LICENSE (MIT License)
│
└── ⚙️ Configuration
    ├── requirements.txt (Dependencies)
    └── .gitignore (Git ignore rules)
```

## 🎯 Common Use Cases

### Use Case 1: Identify Bottlenecked GPUs

```python
# In Python or Jupyter
import pandas as pd

df = pd.read_csv('synthetic_dcgm_metrics.csv')

# Find GPUs with high utilization but low efficiency
bottlenecked = df[
    (df['DCGM_FI_DEV_GPU_UTIL'] > 70) & 
    (df['power_intensity_factor'] < 0.60)
]

print(f"Found {len(bottlenecked)} bottlenecked samples")
```

### Use Case 2: Calculate Fleet ROI

```python
current_rfu = df['rfu_percent'].mean()
target_rfu = 70
total_gpus = 50

improvement = (target_rfu / current_rfu - 1) * total_gpus
print(f"Equivalent GPUs gained: {improvement:.1f}")
```

### Use Case 3: Monitor Time Series

```python
# Hourly aggregation
hourly = df.groupby(df['SCRAPETIME'].dt.floor('H')).agg({
    'DCGM_FI_DEV_GPU_UTIL': 'mean',
    'rfu_percent': 'mean'
})

hourly.plot()
```

## 🔍 Understanding the Metrics

### Traditional vs New Approach

| Traditional | New Approach |
|-------------|--------------|
| GPU Utilization (0-100%) | Power Intensity Factor (0-1.0) |
| "Is GPU busy?" | "Is GPU productive?" |
| No context on quality | Actual computational work |
| Can't detect bottlenecks | Identifies stalls/bottlenecks |

### Key Formulas

**Power Intensity Factor (PIF)**
```
PIF = Current Power / Max GPU Power
```

**Realized TFLOPS**
```
Realized TFLOPS = Achievable TFLOPS × PIF
```

**Realized TFLOPS Utilization (RFU)**
```
RFU = (Realized TFLOPS / Achievable TFLOPS) × 100%
```

**Efficiency Gap**
```
Gap = GPU Utilization % - RFU %
```

Large gap → GPU is busy but unproductive

## 🎨 Visualization Guide

### 1. Utilization vs Power Scatter
**What it shows:** Relationship between utilization and actual work  
**What to look for:** 
- Green dots (top-right) = Efficient
- Red dots (top-left) = Bottlenecked
- Look for clusters of red dots

### 2. Time Series Plots
**What it shows:** Fleet efficiency over time  
**What to look for:**
- Growing efficiency gap over time
- Time-based patterns (hourly/daily)
- Sudden drops in efficiency

### 3. Model Comparison
**What it shows:** Performance by GPU type  
**What to look for:**
- Which models are most efficient
- Right-sizing opportunities
- Model-specific bottlenecks

## 🐛 Troubleshooting

### Issue: "Module not found"
```bash
pip install -r requirements.txt
```

### Issue: "File not found: synthetic_dcgm_metrics.csv"
```bash
python generate_synthetic_data.py
```

### Issue: Jupyter kernel crashes
- Dataset is 132MB, may need more RAM
- Try sampling: `df.sample(n=50000)`

### Issue: Plots not showing
```python
import matplotlib.pyplot as plt
plt.ion()  # Enable interactive mode
```

## 📚 Next Steps

1. ✅ Run `quick_start.py` - Get familiar with metrics
2. ✅ Open Jupyter notebook - Explore visualizations  
3. ✅ Read `PROJECT_SUMMARY.md` - Understand methodology
4. ✅ Customize for your data - Add your GPU models
5. ✅ Share feedback - Open issues, contribute!

## 🤝 Getting Help

- **Documentation**: Read README.md and PROJECT_SUMMARY.md
- **Issues**: Check existing issues on GitHub
- **Questions**: Open a discussion
- **Contributions**: See CONTRIBUTING.md

## 🎓 Learning Resources

Want to learn more about GPU efficiency?

1. **NVIDIA DCGM Documentation**
   - https://docs.nvidia.com/datacenter/dcgm/

2. **GPU Architecture**
   - Understanding TFLOPS
   - Memory bandwidth
   - Power management

3. **ML Infrastructure**
   - Distributed training
   - Data pipeline optimization
   - GPU scheduling

## ✨ Tips for Success

### For Best Results:
1. **Start small** - Use quick_start.py first
2. **Explore patterns** - Look for time-based trends
3. **Focus on gaps** - Target high efficiency gaps
4. **Iterate** - Generate custom scenarios
5. **Share** - Contribute your findings!

### Performance Tips:
```python
# Sample large datasets
df_sample = df.sample(n=10000)

# Use chunking for processing
for chunk in pd.read_csv('data.csv', chunksize=10000):
    process(chunk)

# Cache computations
df['cached_metric'] = expensive_calculation(df)
```

## 🎉 You're Ready!

You now have everything you need to:
- ✅ Analyze GPU efficiency
- ✅ Identify bottlenecks
- ✅ Calculate ROI
- ✅ Optimize infrastructure

**Start with:** `python quick_start.py`

Happy analyzing! 🚀

---

**Questions?** Open an issue on GitHub  
**Found a bug?** See CONTRIBUTING.md  
**Want to contribute?** We'd love your help!
