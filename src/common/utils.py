from passlib.hash import pbkdf2_sha512


class Utils:


    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: THe sha512 passwordf rom the login/register form
        :return: A sha512->pbkdf2_sha512 encrypte dpassword
        """

        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password,hashed_password):
        """
        Checks that the password the user sent matches that of the database
        The database password is encrypted more than the user's passowrd at this stage.
        :param hashed password: pbkdf2.sha512 encrypted passwor
        : return: Ture if passwords match, Flase otherwise


        """


        return pbkdf2_sha512.verify(password,hashed_password)
