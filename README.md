# Book Catalog
## Overview
The goal of the project is to develop a RESTful web application using the ***Flask*** framework as well as implement third-party ***OAuth*** authentication. It is also intended to get practice with the various HTTP methods and *CRUD*(create, read, update, and delete) operations.

The **Book Catalog** aplication is built as the second project for [Full Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044) provided by Coursera.

## Features

**Book Catalog** (**application.py**) is a Python-based application that provides a list of books within a variety of authors. It implements a third-party authentication & authorization service via *Google Accounts* and allows registered users to add, edit, and delete their own records.

## Getting Started
### Prerequisites
To use Book Catalog application, the following software is required:
  - Git -Download from [here](https://git-scm.com/downloads).
  - *VirtualBox* – software to run the virtual machine. Download from [here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
  - *Vagrant* – software to configure virtual machine. Download the version for your operating system from [here](https://www.vagrantup.com/downloads.html)

### Starting the Virtual Machine
Change to the directory containg virtual machine files. Find the **vagrant** directory and change to it. Inside the **vagrant** directory, run the following command.
```sh
$ vagrant up
```
Once **vagrant up** is finished running, log in to the virtual machine using the following command.
```sh
$ vagrant ssh
```
### Loading the Data to the Database
To populate DB, run the following command.
```sh
$ python database_setup.py
```
Then run:
```sh
$ python lotsofitems.py
```
## Running
To run Book Catalog from the terminal, use the following command.
```sh
$  python application.py
```
To access the application via your browser, visit http://localhost:8000.
## JSON Endpoints
Book Catalog provides access to the following JSON endpoints:
- '/category/<int:category_id>/JSON': id, name, and description of all books of the chosen author
- '/category/<int:category_id>/<int:item_id>/JSON - description, id, and name for chosen book
- '/category/JSON' – a list of all authors with ids and names

## Authors
  + Alexandra Baturina
