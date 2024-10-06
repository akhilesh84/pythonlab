#!/bin/bash

# Check if conda is installed
if ! command -v conda &> /dev/null
then
    echo "conda could not be found. Please install conda first."
    exit 1
fi

# Get the current conda environment name
ENV_NAME=$(conda info --envs | grep '*' | awk '{print $1}')

# Export the conda environment to environment.yml
echo "Exporting conda environment to environment.yml..."
conda env export -n env > environment.yml

# Extract pip dependencies from environment.yml and create requirements.txt
echo "Generating requirements.txt from environment.yml..."
python - <<EOF
import yaml

def convert_conda_to_requirements(yaml_file, requirements_file):
    with open(yaml_file, 'r') as file:
        env_data = yaml.safe_load(file)

    dependencies = env_data.get('dependencies', [])
    pip_dependencies = []

    for dep in dependencies:
        if isinstance(dep, str):
            pip_dependencies.append(dep)
        elif isinstance(dep, dict) and 'pip' in dep:
            pip_dependencies.extend(dep['pip'])

    with open(requirements_file, 'w') as file:
        for dep in pip_dependencies:
            file.write(f"{dep}\n")

convert_conda_to_requirements('environment.yml', 'requirements.txt')
EOF

echo "Files generated:"
echo "- environment.yml"
echo "- requirements.txt"