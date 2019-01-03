import uuid
import src.models.users.errors as UserErrors
from src.common.database import Database
from src.common.utils import Utils
from src.models.alert.alert import Alert
class User:


    def __init__(self,email,password,_id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id


    def __repr__(self):
        return f"<User {self.email}>"



    @staticmethod
    def is_valid_login(email,password):
        """
        This method verifies that an email/password combo sent by the site forms is valid or not
        Chekcs that the email exists and the password associated to the email
        """
        user_data = Database.find_one('users',{'email': email}) #Password in sha512 -> pbkdf2_sha512
        if user_data is None:
            raise UserErrors.UserNotExistsError("Your user does not exist!")

        if not Utils.check_hashed_password(password,user_data['password']):
            raise UserErrors.InCorrectPasswordError("Your password was wrong.")
    
        
        return True

    @staticmethod
    def register_user(email,password):
        """
        This method registers a user using email and password
        The password already comes hased as sha-512
        :param email: user's email(might be invalid)
        :parm password: sha512-hashed password
        :return: True if registered succesffully, or False otherwise(exceptions can also be raised)

        """

        user_data = Database.find_one("users",{"email": email})

        if user_data is not None:
            #Tell user they are already registered
            raise UserErrors.UserAlreadyRegisteredError("The e-mail you used to register already exists.")


        User(email,Utils.hash_password(password)).save_to_db()

        return True


    def save_to_db(self):
        Database.insert("users",self.json())



    def json(self):
        return {
                "_id": self._id,
                "email": self.email,
                "password": self.password

                }
        

    @classmethod
    def find_by_email(cls,email):

        return cls(**Database.find_one("users",{"email": email}))


    
    def get_alerts(self):
        return Alert.find_by_user_email(self.email)
