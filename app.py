# -*- coding: utf-8 -*-
from wsgiref import validate
from wsgiref.validate import validator
from flask import Flask, render_template, request, flash, Markup, redirect, url_for
from flask_wtf import FlaskForm, CSRFProtect
from wtforms.validators import DataRequired, Length, Regexp, Optional
from wtforms.fields import *
from flask_bootstrap import Bootstrap5, SwitchField
from flask_sqlalchemy import SQLAlchemy
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly
import pandas as pd
import json
from pathlib import Path

from generate_slightly_fake_data import transaction_counts


app = Flask(__name__, static_folder="./static", template_folder="./templates")
app.secret_key = "dev"

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
csrf = CSRFProtect(app)


class CustomerSupportForm(FlaskForm):
    relevant_date = StringField(description="YYYY-MM-DD")
    reason_for_contact = StringField()  # will not autocapitalize on mobile
    freetext_description = TextAreaField()
    image = FileField(validators=(Optional(),))
    email = EmailField(description="We'll never share your email with anyone else.")
    telephone = TelField()
    country = StringField("Country")
    # remember = BooleanField("Remember me")
    submit = SubmitField()


class FetchDataForm(FlaskForm):
    get_card_data = SubmitField()


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
        card_info_json_filepath = Path(__file__).parent / "card_info.json"
        with open(card_info_json_filepath, "r") as f:
            card_data = json.load(f)

        applications = card_data["Applications"]
        # Clean up the AUC tag values
        for app in applications:
            tag = "Application Usage Control"
            auc: str = app[tag]
            begin_strip = "<AUC: "
            end_strip = ">"
            if auc.startswith(begin_strip):
                auc = auc[len(begin_strip) :]
            if auc.endswith(end_strip):
                auc = auc[: -len(end_strip)]
            auc = auc.replace(", ", " <br>")
            app[tag] = auc
        # Clean up the CVM tag values
        for app in applications:
            tag = "Cardholder Verification Method (CVM) List"
            cvm: str = app[tag]
            begin_strip = "<CVM List x: 0, y: 0, rules: "
            end_strip = ">"
            if cvm.startswith(begin_strip):
                cvm = cvm[len(begin_strip) :]
            if cvm.endswith(end_strip):
                cvm = cvm[: -len(end_strip)]
            cvm = cvm.replace(".; ", " ")
            app[tag] = cvm
        app_df = (
            pd.DataFrame.from_dict(applications)
            .set_index("Application Label")
            .T.reset_index()
            .rename(columns={"index": "EMV tag"})
        )
        table = go.Figure(
            layout={
                "title": "Card data",
                "height": 600,
            },
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
            ],
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
                x=date_column, y=since_online, name="consecutive offline transactions"
            ),
            secondary_y=True,
        )
        # Set y-axes titles
        fig.update_yaxes(title_text="total transactions", secondary_y=False)
        fig.update_yaxes(
            title_text="consecutive offline transactions", secondary_y=True
        )
        fig.update_layout(
            title="Transactions recorded for this card identifier: total, offline",
            template="ggplot2",
        )
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


if __name__ == "__main__":
    app.run(debug=True)
