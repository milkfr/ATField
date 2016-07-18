# -*- coding: utf-8 -*-


from flask import url_for, redirect, render_template
from app.models.documents import Document
from app.decorators.login_required import login_required
from . import document
from .forms import DocumentForm
from app.decorators.role_required import document_required
from app.decorators.permission_required import permission_required


@document.route("/")
@login_required
@document_required
def home():
    headings = ["id", "type", "text", "publish"]
    contents = Document.get_all_documents()
    return render_template("document/home.html", contents=contents, headings=headings)


@document.route("/new", methods=["GET", "POST"])
@login_required
@document_required
@permission_required("DOCUMENT_ADD")
def new():
    form = DocumentForm()
    if form.validate_on_submit():
        Document.add_documents(type=form.type.data,
                               text=form.text.data)
        return redirect(url_for("document.home"))
    return render_template("document/edit.html", form=form)


@document.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@document_required
@permission_required("DOCUMENT_EDIT")
def edit(id):
    form = DocumentForm()
    if form.validate_on_submit():
        Document.update_document_by_id(id=id, type=form.type.data, text=form.text.data)
        return redirect(url_for("document.home"))
    tmp_document = Document.get_document_by_id(id)
    form.type.data = tmp_document.type
    form.text.data = tmp_document.text
    return render_template("document/edit.html", form=form)


@document.route("/publish/<int:id>")
@login_required
@document_required
@permission_required("DOCUMENT_PUBLISH")
def publish(id):
    Document.xor_document_by_id(id)
    return redirect(url_for("document.home"))


@document.route("/delete/<int:id>")
@login_required
@document_required
@permission_required("DOCUMENT_DELETE")
def delete(id):
    Document.delete_document_by_id(id)
    return redirect(url_for("document.home"))
