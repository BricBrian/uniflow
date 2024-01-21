# Backend Interview README
## Setup and installation
1: **Create a Conda Development Environment**\
    First, we need to create a Conda development environment and activate it. If you haven't installed Conda yet, make sure to install it first, and then proceed with the following steps:

```bash
# Create a Conda environment named 'uniflow'
conda create --name myenv

# Activate the newly created environment
conda activate uniflow
```
    
2: **Install Poetry**\
    Next, we'll install Poetry, a tool for managing Python project dependencies. Execute the following command to install Poetry:
    
```bash
# Install Poetry using pip
pip install poetry
```

3: **Install Project Dependencies**\
    Now, we need to install all the dependencies for the project. First, navigate to the root folder of the `uniflow` project:

```bash
# Change directory to the root folder of the uniflow project
cd /path/to/uniflow

# Use Poetry to install all dependencies (excluding the root)
poetry install --no-root
```
    
## Exapmle
1: **Problem**\
It has some problems lead to output wrong answer.
    
The expected output is shown as below:
```
[{'output': [{'a': 1, 'b': 2}],
'root': <uniflow.node.node.Node at 0x140177fa0>},
{'output': [{'c': 3, 'd': 4}],
'root': <uniflow.node.node.Node at 0x140174310>},
{'output': [{'e': 5, 'f': 6}],
'root': <uniflow.node.node.Node at 0x1401772e0>},
{'output': [{'g': 7, 'h': 8}],
'root': <uniflow.node.node.Node at 0x1401e2c20>}]
```
    
However, the actual output is shown as below:
```
[{'output': [[{'a': 1, 'b': 2}]],
'root': <uniflow.node.node.Node at 0x140177fa0>},
{'output': [[{'c': 3, 'd': 4}]],
'root': <uniflow.node.node.Node at 0x140174310>},
{'output': [[{'e': 5, 'f': 6}]],
'root': <uniflow.node.node.Node at 0x1401772e0>},
{'output': [[{'g': 7, 'h': 8}]],
'root': <uniflow.node.node.Node at 0x1401e2c20>}]
```
    
We can find the output should be `List[Mapping[str, Any]]`, but the result is `List[List[Mapping[str, Any]]]`.
    
2: **Solution**\
We can find the problem is in `uniflow/flow/server.py`. As for function  `_divide_data_into_batches`. We defined it to return `List[Mapping[str, Any]]`. Actually, it returned `List[List[Mapping[str, Any]]]`. The code is shown as below:
```python
def _divide_data_into_batches(
    self, input_list: List[Mapping[str, Any]]
) -> List[Mapping[str, Any]]:
    """Divide the list into batches

    Args:
        input_list (List[Mapping[str, Any]]): List of inputs to the flow

    Returns:
        List[Mapping[str, Any]]: List of batches
    """
    # currently only HuggingFace model support batch.
    # this will require some refactoring to support other models.
    batch_size = self._config.model_config.get(
        "batch_size", 1
    )  # pylint: disable=no-member
    if batch_size <= 0:
        raise ValueError("Batch size must be a positive integer.")
    if not input_list:  # Check if the list is empty
        return []

    # Main logic to divide the list into batches
    batched_list = []
    for i in range(0, len(input_list), batch_size):
        batched_list.append(input_list[i : i + batch_size])  # noqa: E203
    return batched_list
```

So I change the data return from this function in `run`. I used index 0 to get the data, the code is shown as below.
```python
output_futures = {
            executor.submit(self._run_flow_wrapper, input_data[0], i): i
            for i, input_data in enumerate(batch_data)
        }
```

## ExpandOp & ReduceOp
Implement `ExtendOp` in `extend_op.py` and `ReduceOp` in `reduce_op.py`.
    
    
## ExpandReduceFlow
Implement `ExpandReduceFlow` inherit `flow` in `expand_reduce_flow.py`.
    
Implement `ExpandReduceConfig' in `config.py`, the code is shown as below:
```python
@dataclass
class ExpandReduceConfig(TransformConfig):
    """Transform Linear Config Class."""

    flow_name: str = "ExpandReduceFlow"
    prompt_template: PromptTemplate = field(
        default_factory=lambda: PromptTemplate(instruction="",             few_shot_prompt=[])
    )
    model_config: ModelConfig = field(default_factory=lambda: {})
```
    
The result is shown as below:
```
Input:
[{"How are you?": "Fine.", "Who are you?": "I am Bob."}, {"Where are you?": "I am at home.", "What are you doing?": "Coding."}]
    
Output:
[{'How are you? Who are you?': 'Fine. I am Bob.'}]
```
    
## Dockerize thr Application
Create `Dockerfile' in root dictory, the configuration is shown as below:
```bash
#Set work dictory
WORKDIR /home/jovyan

# Install Poetry
USER root
RUN pip install poetry
USER jovyan

# Copy pyproject.toml and poetry.lock to docker
COPY pyproject.toml poetry.lock* ./

# Config Poetry
RUN poetry config virtualenvs.create false

# Install requirment package
RUN poetry install --no-dev
    
# Copy project file to docker
COPY . ./
```
    
Use these instructor to build dockerfile and set port.
```bash
docker build -t uniflow-notebook .

docker run -p 9999:8888 uniflow-notebook # Set outside port is 9999 and inside port is 8888 
```
    
Then got token from docker and can use `localhost:9999` to login this application.
    
## Deploy on Kubernetes
Create `uniflow-deployment.yaml` and the configuration is shown as below:
```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: uniflow-deployment
spec:
  replicas: 2  
  selector:
    matchLabels:
      app: uniflow
  template:
    metadata:
      labels:
        app: uniflow
  spec:
    containers:
      - name: uniflow
        image: username/uniflow-notebook:latest  
        ports:
      - containerPort: 8888  
    ```
    
Create `uniflow-service.yaml' and the configuration is shown as below:
```bash
apiVersion: v1
kind: Service
metadata:
  name: uniflow-service
spec:
  type: NodePort
ports:
  - port: 9999
    targetPort: 8888
    selector:
    app: uniflow docker tag uniflow-notebook:latest johndoe/uniflow-notebook:latest docker push johndoe/uniflow-notebook:latest
```

Then, push the local docker to the docker hub and apply these two configuration.
```bash
kubectl apply -f uniflow-deployment.yaml
kubectl apply -f uniflow-service.yaml
```
    
Use the instruction to get the port.
```bash
kubectl describe service pod podname 
```

Use the following instruction to make sure the status is `Running`:
```
kubectl get pods
```
    
Use the port and token to login `http://localhost:port`.
