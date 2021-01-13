# Backend API

Launch the backend app

Steps:  

1.  Install python 3.7 or use [pyenv/pyenv windows](https://stackoverflow.com/questions/49794432/how-to-setup-a-pipenv-python-3-6-project-if-os-python-version-is-3-5)  
2.  Install pipenv
    > pip install pipenv or pip3 install pipenv in mac
3.  Run the following command in this directory to activate the virtual environtment
    > pipenv shell  
4.  Install the dependencies
    > pipenv install

5.  Run the app
    > pipenv run uvicorn main:app  --port 5000 --reload

    Or run the python file for debugging  
    > pipenv run python main.py


```  
pipenv install Flask-RESTful
```

[Important things to know about in flask](https://itnext.io/beginning-with-flask-project-the-5-most-important-information-to-know-before-starting-f075e0fb0aec)  

[Use .env files in flask](https://itnext.io/start-using-env-for-your-flask-project-and-stop-using-environment-variables-for-development-247dc12468be)

[Setup configuration files](https://itnext.io/how-and-why-have-a-properly-configuration-handling-file-using-flask-1fd925c88f4c)  

