from flask import Flask, render_template, request, redirect, url_for, flash, session
from db import get_connection
import os

app = Flask(
    __name__,
    template_folder=os.path.join(
        os.path.dirname(__file__),
        "templates"
    )
)

app.secret_key = "donorconnect_secret_key"


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def admin_login():

    admin_id = request.form.get("admin_id")
    password = request.form.get("password")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT * FROM admins
    WHERE admin_id = %s
    AND password = %s
    """

    cursor.execute(query, (admin_id, password))

    admin = cursor.fetchone()

    cursor.close()
    conn.close()

    if admin:
        session["admin"] = admin["admin_id"]
        return redirect(url_for("dashboard"))

    return render_template(
        "login.html",
        error="Invalid Admin ID or Password"
    )



@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    

    # Total donors
    cursor.execute(
        "SELECT COUNT(*) AS total FROM donors"
    )

    total_donors = cursor.fetchone()["total"]

    # Total donations
    cursor.execute(
        "SELECT SUM(amount_donated)AS total FROM donors"
    )

    total_donations = cursor.fetchone()["total"]

    #Total Campaign
    cursor.execute(
    "SELECT COUNT(*) AS total FROM campaigns"
    )

    total_campaigns = cursor.fetchone()["total"]

    if total_donations is None:
        total_donations = 0

    cursor.execute("""
    SELECT name, amount_donated
    FROM donors
    ORDER BY id DESC
    LIMIT 5
    """)

    recent_donations = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
    "dashboard.html",
    total_donors=total_donors,
    total_donations=total_donations,
    total_campaigns=total_campaigns,
    recent_donations=recent_donations
)


@app.route("/donors")
def donors():

    if "admin" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search", "")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if search:

        cursor.execute("""
            SELECT *
            FROM donors
            WHERE name LIKE %s
               OR email LIKE %s
               OR city LIKE %s
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))

    else:

        cursor.execute("SELECT * FROM donors")

    donors_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "donors.html",
        donors=donors_data,
        search=search
    )



@app.route("/add_donor", methods=["POST"])
def add_donor():

    print("ADD DONOR ROUTE HIT")

    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    city = request.form.get("city")
    amount = request.form.get("amount")
    

    print(name, email, phone, city, amount)
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO donors
        (name,email,phone,city,amount_donated)
        VALUES(%s,%s,%s,%s,%s)
        """,
        (name,email,phone,city,amount)
    )
    conn.commit()

    cursor.close()
    conn.close()
    flash("Donor added successfully!", "success")

    return redirect(url_for("donors"))


@app.route("/delete_donor/<int:id>")
def delete_donor(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM donors WHERE id = %s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()
    flash("Donor deleted successfully!", "danger")

    return redirect(url_for("donors"))


@app.route("/edit_donor/<int:id>")
def edit_donor(id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM donors WHERE id = %s",
        (id,)
    )

    donor = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
    "edit_donor.html",
    donor=donor
)



@app.route("/campaigns")
def campaigns():

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM campaigns")

    campaigns_data = cursor.fetchall()
    
    for campaign in campaigns_data:
        campaign["percentage"] = (
            campaign["raised_amount"] / campaign["target_amount"]
            ) * 100

    cursor.close()
    conn.close()

    return render_template(
        "campaigns.html",
        campaigns=campaigns_data
    )



@app.route("/add_campaign", methods=["POST"])
def add_campaign():

    title = request.form.get("title")
    description = request.form.get("description")
    target_amount = request.form.get("target_amount")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO campaigns
        (
            title,
            description,
            target_amount,
            raised_amount,
            start_date,
            end_date
        )
        VALUES(%s,%s,%s,%s,%s,%s)
        """,
        (
            title,
            description,
            target_amount,
            0,
            start_date,
            end_date
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Campaign added successfully!",
        "success"
    )

    return redirect(
        url_for("campaigns")
    )




@app.route("/delete_campaign/<int:id>")
def delete_campaign(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM campaigns WHERE id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Campaign deleted successfully!",
        "danger"
    )

    return redirect(
        url_for("campaigns")
    )


@app.route("/edit_campaign/<int:id>")
def edit_campaign(id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM campaigns WHERE id=%s",
        (id,)
    )

    campaign = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "edit_campaign.html",
        campaign=campaign
    )



@app.route("/update_campaign/<int:id>", methods=["POST"])
def update_campaign(id):

    title = request.form.get("title")
    description = request.form.get("description")
    target_amount = request.form.get("target_amount")
    raised_amount = request.form.get("raised_amount")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE campaigns
        SET
            title=%s,
            description=%s,
            target_amount=%s,
            raised_amount=%s,
            start_date=%s,
            end_date=%s
        WHERE id=%s
        """,
        (
            title,
            description,
            target_amount,
            raised_amount,
            start_date,
            end_date,
            id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("campaigns"))




@app.route("/architecture")
def architecture():

    if "admin" not in session:
        return redirect(url_for("login"))

    return render_template("architecture.html")


@app.route("/update_donor/<int:id>", methods=["POST"])
def update_donor(id):

    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    city = request.form.get("city")
    amount = request.form.get("amount")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE donors
        SET
            name = %s,
            email = %s,
            phone = %s,
            city = %s,
            amount_donated = %s
        WHERE id = %s
        """,
        (name, email, phone, city, amount, id)
    )

    conn.commit()

    cursor.close()
    conn.close()
    flash("Donor updated successfully!", "info")

    return redirect(url_for("donors"))



@app.route("/reports")
def reports():

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM donors")
    total_donors = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(amount_donated) FROM donors")
    total_donations = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM campaigns")
    total_campaigns = cursor.fetchone()[0]

    avg_donation = 0

    if total_donors > 0:
        avg_donation = total_donations / total_donors

    cursor.close()
    conn.close()

    return render_template(
        "reports.html",
        total_donors=total_donors,
        total_donations=total_donations,
        total_campaigns=total_campaigns,
        avg_donation=avg_donation
    )


@app.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged out successfully!",
        "info"
    )

    return redirect(url_for("login"))




if __name__ == "__main__":
    print("RUNNING THIS APP FILE")
    app.run(host="0.0.0.0", port=5001, debug=True)