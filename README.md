1. Clone the repo
2. In folder "langchain_mistral"
3. run following commands:
	
	poetry env use 3.11
	
	poetry run python --version => It will show python version 3.11.4
	
	poetry install => It will install all required dependent component in a virtual environment

5. rename env_example file to .env
6. open .env file and Add mistral api key and langsmith api key in .env file
7. go to poetry shell by running following command
	
	poetry shell

8. create a new kernel for jupyter notebook.
	
	poetry run python -m ipykernel install --user --name=poetry-env-mistral --display-name=poetry-env-mistral

7. Choose the Kernel in Jupyter: When you open Jupyter Notebook, you should now see an option to select the poetry-env kernel from the Kernel -> Change kernel menu.
	
	poetry run jupyter notebook


