# Full Stack Web Development Nanodegree Project #2: Book Catalog
## Overview
The **Book Catalog** is the second project for [Full Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044) provided by Udacity. It requires to build a RESTful web application that provides a list of books within a variety of authros as well as provides a user registration and authentication system.

The project has the following goals:
* Develop a web app with [Flask](https://flask.palletsprojects.com/en/1.1.x/) framework
* Make a web server in Python
* Work with SQLite
* Implement ***CRUD*** (create, read, update, and delete) functionality
* Implement third-party ***OAuth*** auhtentication
* Serialize data
* Create JSON APIs

You can check the project deployment by visiting [http://54.191.192.22.xip.io](http://54.191.192.22.xip.io).
## Features
The **Book Catalog** application has the following features:
* Providing a list of authors
* Providing a list of books of each author
* Implementing a third-party authentication & authorization service via *Google Accounts*
* Allowing registered users to add, edit, and delete their own records
## JSON APIs
The **Book Catalog** application provides access to the following JSON APIs:
* [GET] ```/authors/<int:author_id>/JSON``` – Info about all books of the author
    * id: number
    * title: string(50)
    * description: string(5000)
 
 * [GET] ```/authors/<int:author_id>/<int:book_id>/JSON``` – Info about the book
    * id: number
    * title: string(50)
    * description: string(5000)
    
 * [GET] ```/authors/JSON``` – List of authors
    * id: number
    * name: string(50)
## Getting Started
### Loading Data to the Database
To create database, run the following command:
```sh
python database_setup.py
```
To populate database, run the following command:
```sh
python lotsofbooks.py
```
### Running Locally
To run **Book Catalog** from the terminal, use the following command:
```sh
python application.py
```
To access the application via your browser, visit http://localhost:8000.

## Authors
  + Alexandra Baturina
