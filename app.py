# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, Markup, redirect, url_for
from flask_wtf import FlaskForm, CSRFProtect
from wtforms.validators import DataRequired, Length, Regexp
from wtforms.fields import *
from flask_bootstrap import Bootstrap5, SwitchField
from flask_sqlalchemy import SQLAlchemy
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly
import pandas as pd
import json

from generate_slightly_fake_data import transaction_counts


app = Flask(__name__, static_folder="./static", template_folder="./templates")
app.secret_key = "dev"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

# set default button sytle and size, will be overwritten by macro parameters
app.config["BOOTSTRAP_BTN_STYLE"] = "primary"
app.config["BOOTSTRAP_BTN_SIZE"] = "sm"
# app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'lumen'  # uncomment this line to test bootswatch theme

# set default icon title of table actions
app.config["BOOTSTRAP_TABLE_VIEW_TITLE"] = "Read"
app.config["BOOTSTRAP_TABLE_EDIT_TITLE"] = "Update"
app.config["BOOTSTRAP_TABLE_DELETE_TITLE"] = "Remove"
app.config["BOOTSTRAP_TABLE_NEW_TITLE"] = "Create"

bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)


class CustomerSupportForm(FlaskForm):
    relevant_date = DateTimeField()
    reason_for_contact = StringField()  # will not autocapitalize on mobile
    freetext_description = TextAreaField()
    image = FileField(
        render_kw={"class": "my-class"}, validators=[Regexp(".+\.jpg$")]
    )  # add your class
    email = EmailField(description="We'll never share your email with anyone else.")
    telephone = TelField()
    country_code = IntegerField("Country Code")
    area_code = IntegerField("Area Code/Exchange")
    # remember = BooleanField("Remember me")
    submit = SubmitField()


class HelloForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(1, 20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 150)])
    remember = BooleanField("Remember me")
    submit = SubmitField()


class ButtonForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(1, 20)])
    confirm = SwitchField("Confirmation")
    submit = SubmitField()
    delete = SubmitField()
    cancel = SubmitField()


class FetchDataForm(FlaskForm):
    submit = SubmitField()


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    draft = db.Column(db.Boolean, default=False, nullable=False)
    create_time = db.Column(db.Integer, nullable=False, unique=True)


@app.before_first_request
def before_first_request_func():
    db.drop_all()
    db.create_all()
    for i in range(20):
        url = "mailto:x@t.me"
        if i % 7 == 0:
            url = "www.t.me"
        elif i % 7 == 1:
            url = "https://t.me"
        elif i % 7 == 2:
            url = "http://t.me"
        elif i % 7 == 3:
            url = "http://t"
        elif i % 7 == 4:
            url = "http://"
        elif i % 7 == 5:
            url = "x@t.me"
        m = Message(
            text=f"Message {i+1} {url}",
            author=f"Author {i+1}",
            category=f"Category {i+1}",
            create_time=4321 * (i + 1),
        )
        if i % 4:
            m.draft = True
        db.session.add(m)
    db.session.commit()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/card_info", methods=["GET", "POST"])
def card_info():
    show_card = 0
    form = FetchDataForm()
    df = pd.DataFrame()
    if request.method == "POST":
        show_card = 1
        card_data = dict()
        with open("card_info.json", "r") as f:
            card_data = json.load(f)

        applications = card_data["Applications"]
        app_df = (
            pd.DataFrame.from_dict(applications)
            .set_index("Application Label")
            .T.reset_index()
            .rename(columns={"index": "emv tag"})
        )
        table = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=app_df.columns,
                        fill_color="#005F83",
                        font_color="white",
                        align="left",
                    ),
                    cells=dict(
                        values=app_df.values.T,
                        fill_color="#ecf0f1",
                        align="left",
                    ),
                )
            ]
        )

        txs_counts_n = 100
        card_txs_data = transaction_counts(txs_counts_n)
        df = pd.DataFrame(card_txs_data)
        totals = df[df.columns[0]]
        since_online = df[df.columns[1]]
        date_column = df[df.columns[2]]
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=date_column, y=totals, name="total transactions"),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(
                x=date_column, y=since_online, name="transactions since last online"
            ),
            secondary_y=True,
        )
        # Set y-axes titles
        fig.update_yaxes(title_text="total transactions", secondary_y=False)
        fig.update_yaxes(title_text="transactions since last online", secondary_y=True)
        fig.update_layout(template="ggplot2")
        flash(
            "Anomalous transaction detected: unusual location, multiple failed authentication attempts",
            "danger",
        )
        flash("Your card appears to be expired on 2019-01-31!", "warning")
    else:
        fig = px.bar(template="ggplot2")
        table = px.bar(template="ggplot2")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    tableJSON = json.dumps(table, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        "card_info.html",
        show_card=show_card,
        form=form,
        tableJSON=tableJSON,
        graphJSON=graphJSON,
    )


@app.route("/card_info", methods=["POST"])
def foo():
    card_data = dict()
    with open("card_info.json", "r") as f:
        card_data = json.load(f)
    return card_data


@app.route("/form", methods=["GET", "POST"])
def test_form():
    form = CustomerSupportForm()
    if form.validate_on_submit():
        flash("Form validated!")
        return redirect(url_for("index"))
    return render_template(
        "form.html",
        form=form,
    )


@app.route("/table")
def test_table():
    page = request.args.get("page", 1, type=int)
    # pagination = Message.query.paginate(page, per_page=10)
    pagination = Message.query.paginate(per_page=10)
    messages = pagination.items
    # messages = []
    titles = [
        ("id", "#"),
        ("text", "Message"),
        ("author", "Author"),
        ("category", "Category"),
        ("draft", "Draft"),
        ("create_time", "Create Time"),
    ]
    data = []
    for msg in messages:
        data.append(
            {
                "id": msg.id,
                "text": msg.text,
                "author": msg.author,
                "category": msg.category,
                "draft": msg.draft,
                "create_time": msg.create_time,
            }
        )
    return render_template(
        "table.html", messages=messages, titles=titles, Message=Message, data=data
    )


@app.route("/table/<int:message_id>/view")
def view_message(message_id):
    message = Message.query.get(message_id)
    if message:
        return f'Viewing {message_id} with text "{message.text}". Return to <a href="/table">table</a>.'
    return f'Could not view message {message_id} as it does not exist. Return to <a href="/table">table</a>.'


@app.route("/table/<int:message_id>/edit")
def edit_message(message_id):
    message = Message.query.get(message_id)
    if message:
        message.draft = not message.draft
        db.session.commit()
        return f'Message {message_id} has been editted by toggling draft status. Return to <a href="/table">table</a>.'
    return f'Message {message_id} did not exist and could therefore not be edited. Return to <a href="/table">table</a>.'


@app.route("/table/<int:message_id>/delete", methods=["POST"])
def delete_message(message_id):
    message = Message.query.get(message_id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return f'Message {message_id} has been deleted. Return to <a href="/table">table</a>.'
    return f'Message {message_id} did not exist and could therefore not be deleted. Return to <a href="/table">table</a>.'


@app.route("/table/<int:message_id>/like")
def like_message(message_id):
    return f'Liked the message {message_id}. Return to <a href="/table">table</a>.'


@app.route("/table/new-message")
def new_message():
    return 'Here is the new message page. Return to <a href="/table">table</a>.'


if __name__ == "__main__":
    app.run(debug=True)
