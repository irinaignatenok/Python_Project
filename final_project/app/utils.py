import flask
import flask_mail

from app import db, mail_manager

def send_mail(subject, body, recipients):
    msg = flask_mail.Message(
        subject = subject,
        body = body,
        recipients = recipients,
        sender = flask.current_app.config["MAIL_USERNAME"]
    )
    print(flask.current_app.config["MAIL_USERNAME"])

class ModelMixin():

    id = db.Column(db.Integer(), primary_key = True)

    def save(self):
        db.session.add(self)

        try:
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False



class DeleteItem():

    id = db.Column(db.Integer(), primary_key = True)

    def delete_item(self):
        db.session.delete(self)

        try:
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False


class FormUtils():

    def quick_html(self):

        return """
             <form method="POST">
                {{ form.hidden_tag() }}
                <p>
                    {{ form.username.label }}
                    {{ form.self.username() }}
                </p>
                <p>
                    {{ form.password.label }}
                    {{ form.self.password() }}
                </p>

                {{ form.submit() }}
            </form>
        """
