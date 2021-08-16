from flask import Flask


def init_app(app: Flask):
    from app.views.upload_view import bp_upload
    app.register_blueprint(bp_upload)

    from app.views.download_view import bp_download
    app.register_blueprint(bp_download)

    from app.views.files_view import bp_files
    app.register_blueprint(bp_files)