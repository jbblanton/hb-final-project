"""Models for the Shower Buddy app"""

import os
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()


################# Models & Info ##################################

class User(db.Model):
    """A User, aka: a Caregiver"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    #caregiver_name =db.Column(db.String(25),)
    email = db.Column(db.String(50), unique = True, nullable = False,)
    password = db.Column(db.String(25), nullable = False,)
    telephone = db.Column(db.String(12),)

    client = db.relationship('Client')

    def get_id(self):
        """Return caregiver's ID, to satisfy login requirements;
            For use with the Flask Login """

        return self.user_id

    def is_authenticated(self):
        """Return True if user is authenticated;
            For use with the Flask Login """

        return self.authenticated

    def is_anonymous(self):
        """No anonymous use allowed!
            For use with the Flask Login """

        return False

    def __repr__(self):
        return f'<Caregiver user_id={self.user_id}, email={self.email}, phone={self.telephone}>'

    def check_if_registered(email):
        """Check if a caregiver is already registered"""

        # Query a given email address; 
        #   If exists in db, alert('this email already has an account, plz log in')
        #   Else: create account
        return User.query.filter(User.email == email).first()


class Client(db.Model):
    """A Client, aka: the end-User"""

    __tablename__ = "clients"

    client_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    client_name = db.Column(db.String(50), nullable = False,)
    client_body = db.Column(db.String(16),)
    caregiver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    caregiver = db.relationship('User')
    flow = db.relationship('Flow')

    def __repr__(self):
        return f'<Client client_name={self.client_name} client_id={self.client_id} user_id={self.caregiver_id}>'


    def check_if_client():
        """Look for the combo of user name & body + caregiver
            Goal: prevent duplication; redirect to "add a flow" """

        pass


class Flow(db.Model):
    """A user's shower routine"""

    __tablename__ = "flows"

    flow_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    title = db.Column(db.String(60),)
# default title = 'daily'
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'))


    client = db.relationship('Client')

    def __repr__(self):
        return f'<Flow flow_id={self.flow_id}, title={self.title}, client={self.Client.client_name}>'
        # I don't know if I can write that last bit like that... FIND OUT


class Flow_Activity(db.Model):
    """Connector table between Flow & Activities"""

    __tablename__ = "flow_acts"

    flow_act_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    seq_step = db.Column(db.Integer, nullable = False,)
    flow_id = db.Column(db.Integer, db.ForeignKey('flows.flow_id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'))

    flow = db.relationship('Flow')
    activity = db.relationship('Activity')

    def __repr__(self):
        return f'<Flow_Activity flow_act_id={self.flow_act_id},  step in sequence={self.seq_step}>'


class Activity(db.Model):
    """Activities that occur during a shower sequence or 'flow' """

    __tablename__ = "activities"

    activity_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    activity_name = db.Column(db.String(30))
    description = db.Column(db.Text,)
    activity_video = db.Column(db.Text,)

    flow_act = db.relationship('Flow_Activity')
    #act_prod_id = db.relationship('Activity_Product')

    def __repr__(self):
        return f'<Activity id={self.activity_id}, description={self.description}, video={self.activity_video}>'



## Deactivated this table on 6/5 based on a conversation with mentor R. 
## Since one activity (shampooing) can have many products due to the number of 
## unique users (Bob uses Pert, Lola uses Suave, Pickle uses Pantene, etc.), 
## this was a messy connection.
## This table is being replaced by Flow_Product which will tuple a 
## flow_act_id and product_id to allow the unique combo of user + product.
##
# class Activity_Product(db.Model):
#     """Connector table between Activities & Products """

#     __tablename__ = "activity_products"

#     act_prod_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
#     activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'))
#     product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))

#     activity = db.relationship('Activity')
#     product = db.relationship('Product')

#     def __repr__(self):
#         return f'<Act_Prod id={self.act_prod_id}, activity_id={self.activity_id}, \
#                 product_id={self.product_id}>' 


# class Flow_Product(db.Model):
#     """Tying a unique flow to the necessary products"""

#     __tablename__ = "flow_products"

#     fa_id = db.Column(db.Integer, db.ForeignKey('flow_acts.flow_act_id'), primary_key = True,)
#     prod_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), primary_key = True, )

#     flowacts = db.relationship('Flow_Activity')
#     products = db.relationship('Product')


# REFERENCE:
#    CREATE TABLE my_association (
#   user_id INTEGER REFERENCES user(id),
#   account_id INTEGER REFERENCES account(id),
#   PRIMARY KEY (user_id, account_id)
# )

class Product(db.Model):
    """Info on Products used for a Shower """

    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    product_img = db.Column(db.String(75),)
    product_name = db.Column(db.String(25), nullable = False,)
    product_label_color = db.Column(db.String(20),)

    # act_prod_id = db.relationship('Activity_Product')

    def __repr__(self):
        return f'<Product id={self.product_id}, name={self.product_name}, label color={self.product_label_color}>'


################ end of models ##################################





def connect_to_db(flask_app, db_uri='postgresql:///testing', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)


if __name__ == '__main__':
    from server import app

    connect_to_db(app)
    print("Connected to DB.")