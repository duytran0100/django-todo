# ToDo API
Python 3.10

## Settings environments and database
### On Windows
```shell
copy .env.example .env
```
###  Settings postgres database with information below
- HOST: 'localhost'
- PORT: '5432'
- USER: 'postgres'
- PASSWORD: 'postgres'
- DATABASE_NAME: 'tododb'

## Commands

```shell
cd ToDoAPI
pipenv sync --dev # Install packages
pipenv run make-migrations # Create migrations files
pipenv run migrate # Migrate database
pipenv run init-todo # Init sample todo data
pipenv run createsuperuser --username admin --password admin # Create superuser with username/password (admin/admin)
pipenv run test # Run unittest 
```