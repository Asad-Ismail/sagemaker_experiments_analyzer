# sagemaker_experiments_analyzer
To analyze the sagemaker experiments run without using a sagemaker studio

## Installation


```bash
python setup.py sdist bdist_wheel
pip install dist/sagemaker_experiment_analyzer-0.1.0-py3-none-any.whl
```

```bash
pip install sagemaker_experiment_analyzer
```


## Usage

```python

from sagemaker_experiment_analyzer import SageMakerExperimentAnalyzer

experiment_name = "experiment_name"
analyzer = SageMakerExperimentAnalyzer(experiment_name)
comparison_df = analyzer.compare_runs('MetricName')
analyzer.plot_comparison(comparison_df)
# Normally avg is the most intersting one, but min, max and last are also valid
best_params = analyzer.get_best_parameters(comparison_df, 'Avg', 'min')
print("Best Parameters:", best_params)

```