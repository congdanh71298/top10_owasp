
# Login form template
LOGIN_FORM = '''
<form method="post">
    Username: <input name="username"><br>
    Password: <input name="password" type="password"><br>
    <input type="submit" value="Login">
</form>
'''

# Registration form template
REGISTER_FORM = '''
<form method="post">
    Username: <input name="username"><br>
    Password: <input name="password" type="password"><br>
    <input type="submit" value="Register">
</form>
'''

# Checkout form template
CHECKOUT_FORM = '''
<form method="post">
    Item ID: <input name="item_id"><br>
    Quantity: <input name="quantity" type="number"><br>
    <input type="submit" value="Checkout">
</form>
'''

# File upload form template
UPDATE_FORM = '''
<form method="post" enctype="multipart/form-data">
    File: <input type="file" name="file"><br>
    <input type="submit" value="Upload">
</form>
'''