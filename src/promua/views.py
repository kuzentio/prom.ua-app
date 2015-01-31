from promua.app import app

from flask import request, redirect, render_template, make_response


@app.route('/', methods=['GET'])
def main():
    assert False, 123
