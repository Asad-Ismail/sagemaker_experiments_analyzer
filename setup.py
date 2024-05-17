from setuptools import setup, find_packages

setup(
    name='SMExpAnalyzer',
    version='0.1.0',
    description='A package to analyze SageMaker experiments',
    author='Your Name',
    author_email='asadismaeel@gmail.com',
    packages=find_packages(include=['SMExpAnalyzer', 'SMExpAnalyzer.*']),
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
