from setuptools import setup, find_packages

setup(
    name='sagemaker_experiment_analyzer',
    version='0.1.0',
    description='A package to analyze SageMaker experiments',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'pandas',
        'matplotlib',
        'seaborn',
        'sagemaker-experiments'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
