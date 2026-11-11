from flask import Flask, render_template, request, redirect, url_for
from extensions import db
from models import Customer, Deal

app = Flask(__name__)

app.config['SQLALCHEMY_DATEBASE_URL'] = 'sqlite://crm.db'
app.config['AQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Дальше серверная логика 