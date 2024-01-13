from dotenv import dotenv_values

ENV = dotenv_values()

# ENV VARIABLES
SECRET_KEY = ENV['SECRET_KEY']

DB_HOST = ENV['DB_HOST']
DB_PORT = ENV['DB_PORT']
DB_USER = ENV['DB_USER']
DB_PASSWORD = ENV['DB_PASSWORD']
DB_NAME = ENV['DB_NAME']
