
# Item Catalog

Item Catalog is a web application that provides a list of items
within a variety of categories and integrates third party
user registration and authentication. Authenticated users
should have the ability to post, edit, and delete their own items.

## Installation

Download the Latest version of Python

- Download Python [here](https://www.python.org/downloads/)

### Install Dependencies

To run this project, you will need to run the requirements.txt file
listed in **dependencies** section below.

### Dependencies

```
pip install -r requirements.txt
```

## Create & Populate Database

```
export FLASK_APP=itemCatalog.py
```

```
flask shell
```

```
import itemCatalog
```

```
db.create_all()
```

```
import populateDB
```

## Run the Application

```
python itemCatalog.py
```
