import boto3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sagemaker.experiments.experiment import Experiment

class SageMakerExperimentAnalyzer:
    def __init__(self, experiment_name):
        self.sagemaker_client = boto3.client('sagemaker')
        self.experiment_name = experiment_name
        self.runs_data = self._get_runs_data()

    def _get_params(self, trial_component_name):
        trial_component = self.sagemaker_client.describe_trial_component(TrialComponentName=trial_component_name)
        parameters = trial_component.get('Parameters', {})
        extracted_params = {}
        for param_name, param in parameters.items():
            if 'StringValue' in param:
                extracted_params[param_name] = param['StringValue']
            elif 'NumberValue' in param:
                extracted_params[param_name] = param['NumberValue']
        return extracted_params

    def _get_metrics(self, trial_component_name):
        trial_component = self.sagemaker_client.describe_trial_component(TrialComponentName=trial_component_name)
        metrics = trial_component.get('Metrics', [])
        metric_data = []
        for metric in metrics:
            metric_data.append({
                'MetricName': metric['MetricName'],
                'TimeStamp': metric['TimeStamp'],
                'Max': metric['Max'],
                'Min': metric['Min'],
                'Last': metric['Last'],
                'Count': metric['Count'],
                'Avg': metric['Avg'],
                'StdDev': metric['StdDev']
            }) 
        return pd.DataFrame(metric_data)

    def _get_runs_data(self):
        trial_components = self.sagemaker_client.list_trial_components(ExperimentName=self.experiment_name)
        runs_data = {}
        for component in trial_components['TrialComponentSummaries']:
            run_name = component['TrialComponentName']
            metrics_df = self._get_metrics(run_name)
            params_dict = self._get_params(run_name)
            runs_data[run_name] = {
                "metrics": metrics_df,
                "parameters": params_dict
            }
        return runs_data

    def compare_runs(self, metric_name):
        comparison_data = []
        for run_name, data in self.runs_data.items():
            metrics_df = data["metrics"]
            if metric_name not in metrics_df['MetricName'].values:
                print(f"Metric '{metric_name}' does not exist for {run_name}")
                continue
            metric_values = metrics_df[metrics_df['MetricName'] == metric_name]
            if not metric_values.empty:
                params_dict = data["parameters"]
                comparison_data.append({
                    "Run": run_name,
                    "Max": metric_values['Max'].max(),
                    "Min": metric_values['Min'].min(),
                    "Last": metric_values['Last'].iloc[-1],
                    "Avg": metric_values['Avg'].mean(),
                    "StdDev": metric_values['StdDev'].mean(),
                    "Parameters": params_dict
                })

        comparison_df = pd.DataFrame(comparison_data)
        return comparison_df

    def plot_comparison(self, comparison_df, metrics=['Max', 'Min', 'Last', 'Avg', 'StdDev']):
        sns.set(style="whitegrid")
        num_metrics = len(metrics)
        fig, axes = plt.subplots((num_metrics + 2) // 3, 3, figsize=(18, 5 * ((num_metrics + 2) // 3)))
        fig.suptitle('Comparison of Metrics Across Runs')
        axes = axes.flatten()

        for i, metric in enumerate(metrics):
            sns.barplot(x='Run', y=metric, data=comparison_df, ax=axes[i])
            axes[i].set_title(f'{metric} Values')
            axes[i].set_xticklabels(axes[i].get_xticklabels(), rotation=45, ha='right')

        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout()
        plt.subplots_adjust(top=0.95)
        plt.show()

    def get_best_parameters(self, comparison_df, metric_name, criteria='max'):
        if criteria not in ['max', 'min']:
            raise ValueError("Criteria must be either 'max' or 'min'")

        if criteria == 'max':
            best_run = comparison_df.loc[comparison_df[metric_name].idxmax()]
        else:
            best_run = comparison_df.loc[comparison_df[metric_name].idxmin()]

        return best_run['Parameters']
