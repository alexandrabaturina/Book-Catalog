# Full Stack Web Development Nanodegree Project #2: Book Catalog
## Overview
The **Book Catalog** is the second project for [Full Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044) provided by Udacity. It requires to build a RESTful web application that provides a list of books within a variety of authros as well as provides a user registration and authentication system.

The project has the following goals:
* Web development with [Flask](https://flask.palletsprojects.com/en/1.1.x/) framework
* Make a web server in Python
* Implement ***CRUD*** (create, read, update, and delete) functionality
* Implement third-party ***OAuth*** auhtentication
* Serialize data
* Create JSON APIs

You can check the project deployment by visiting [http://54.191.192.22.xip.io](http://54.191.192.22.xip.io.).
## Features
The **Book Catalog** application has the following features.
* Providing a list of books within a variety of authors
* Implementing a third-party authentication & authorization service via *Google Accounts*
* Allowing registered users to add, edit, and delete their own records
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
