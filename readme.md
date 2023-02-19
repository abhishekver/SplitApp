# Bill Split App

## Project setup
- Make sure venv is already install on the system, if not follow the steps here: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
- Since the virtual environment is already included, run `source venv/bin/activate`
- Once the venv is activated, run `pip install -r requirements.txt` to install all the dependencies


## Migrations
Can skip this step as latest migration and db is already included with the code
- To make the migrations, run: `./manage.py makemigrations`
- Following that run: `./manage.py migrate`


## Running the project
- Use `./manage.py runserver` to run the server, it'll start the server on port: 8000
- If wanting to use custom port, ude `./manage.py runserver {port-number}`, it will start the application on given port


## Using the app
Project is basically divided into 3 sets of API:
- User: To create user, view user and to view user's balance sheet
- Transaction: To create transaction, to settle balance between users and view balances


## Playing Around (All APIs are part of postman collection)

### User Interactions
- **Create User:** User Create Use API to create a few users
- **View User:** Use this api to view details of the given user
- **View Balance Sheet:** Shows the summary of the user's transactions and the total amount he owes or is receivable to him

### Group Interactions
- **Create Group**: Use this to create a group of users
- **Add Members To Group:** Use this to add additional members to the group
- **View Group:** This shows the list of members, total amount and group name
- **View Balance Sheet:** This shows the summary of amount owed or payable for individual members of the group
- **View Transactions:** This shows all the transactions that have happened within the group

### Transaction Interactions
- **Create Transaction:** This API allows one to create an activity, taking into consideration individual expenses and contributions
- **Settle Balance:** This API allows one to settle the amount between two users
- **View Transaction:** It allows to view the details of individual transactions


## NOTE
The given database already contains superuser credentials. Use `(admin, admin)` to login to http://127.0.0.1:8000/admin/
Here one can view all the existing database entries and can use it to get the respective `ids`, as those are auto-generated
uuids an tough to remember