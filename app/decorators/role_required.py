# -*- coding: utf-8 -*-


from .permission_required import permission_required


def admin_required(func):
    return permission_required("ADMIN_BASE")(func)


def document_required(func):
    return permission_required("DOCUMENT_BASE")(func)


def user_required(func):
    return permission_required("USER_BASE")(func)
