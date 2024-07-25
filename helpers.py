from flask     import redirect, render_template, session
from functools import wraps
from re        import match

def allowed_file(filename):

    if '.' not in filename:
        return False

    parts = filename.rsplit('.', 1)

    name = parts[0]
    ext  = parts[1]

    NamePtrn  = '^m[1-3]ex[0-9][0-9]$'
    nameMatch = match(NamePtrn, name)

    ALLOWED_EXTENSIONS = ['S', 'asm', 'c']

    extMatch = ext in ALLOWED_EXTENSIONS

    return nameMatch and extMatch

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

