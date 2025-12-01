from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app import db
from app import Event, User
from . import admin_bp

# ---------- Access Control ----------
def admin_only():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash("Admins only!", "danger")
        return redirect(url_for("index"))
    return None

# ---------- ADMIN HOME ----------
@admin_bp.route("/")
@login_required
def dashboard():
    block = admin_only()
    if block:
        return block

    events = Event.query.order_by(Event.start_time).all()
    users = User.query.order_by(User.id).all()
    return render_template("admin/dashboard.html", events=events, users=users)

# ---------- CREATE EVENT ----------
@admin_bp.route("/event/create", methods=["GET", "POST"])
@login_required
def create_event():
    block = admin_only()
    if block:
        return block

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        venue = request.form.get("venue")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        capacity = request.form.get("capacity")

        image_file = request.files.get("image")
        filename = None

        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            upload_path = os.path.join("static", "uploads", filename)
            image_file.save(upload_path)

        new_event = Event(
            title=title,
            description=description,
            venue=venue,
            start_time=start_time,
            end_time=end_time,
            capacity=capacity,
            image_filename=filename
        )
        db.session.add(new_event)
        db.session.commit()
        flash("Event created successfully!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/create_event.html")

# ---------- EDIT EVENT ----------
@admin_bp.route("/event/edit/<int:event_id>", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    block = admin_only()
    if block:
        return block

    event = Event.query.get_or_404(event_id)

    if request.method == "POST":
        event.title = request.form.get("title")
        event.description = request.form.get("description")
        event.venue = request.form.get("venue")
        event.start_time = request.form.get("start_time")
        event.end_time = request.form.get("end_time")
        event.capacity = request.form.get("capacity")

        image_file = request.files.get("image")
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            upload_path = os.path.join("static", "uploads", filename)
            image_file.save(upload_path)
            event.image_filename = filename

        db.session.commit()
        flash("Event updated successfully!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/edit_event.html", event=event)

# ---------- DELETE EVENT ----------
@admin_bp.route("/event/delete/<int:event_id>", methods=["POST"])
@login_required
def delete_event(event_id):
    block = admin_only()
    if block:
        return block

    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()

    flash("Event deleted!", "warning")
    return redirect(url_for("admin.dashboard"))

# ---------- USER MANAGEMENT ----------
@admin_bp.route("/users")
@login_required
def manage_users():
    block = admin_only()
    if block:
        return block

    users = User.query.all()
    return render_template("admin/users.html", users=users)

# ---------- TOGGLE ADMIN ----------
@admin_bp.route("/user/<int:user_id>/toggle-admin", methods=["POST"])
@login_required
def toggle_admin(user_id):
    block = admin_only()
    if block:
        return block

    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    flash("User admin status updated.", "success")
    return redirect(url_for("admin.manage_users"))
