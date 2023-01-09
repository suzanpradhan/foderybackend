
from django.core.mail import EmailMultiAlternatives
from views import encrypt


def smtp(payload, email):
    token = encrypt({"user": payload})
    subject = "Welcome to Sweed."
    message = (
        "Hello, "
        + " Please click on this link to activate your account: "
        + "http://127.0.0.1:8000/user/activate/?token="
        + str(token)
    )
    html_context='<img src="https://www.google.com/imgres?imgurl=https%3A%2F%2Fimage6.uhdpaper.com%2Fwallpaper%2F2b-lollipop-nier-automata-uhdpaper.com-4K-6.603.jpg&imgrefurl=https%3A%2F%2Fwww.uhdpaper.com%2F2020%2F01%2F2b-lollipop-nier-automata-4k-6603.html&tbnid=QMVN03W9ftEHeM&vet=12ahUKEwicx5bXlNb0AhU1t2MGHSFsA7UQMygVegUIARDXAQ..i&docid=IRq0UPX4CNxpbM&w=3840&h=2160&itg=1&q=nier%202b%20pixel%20live%20wallpaper&ved=2ahUKEwicx5bXlNb0AhU1t2MGHSFsA7UQMygVegUIARDXAQ" >'
    recepient = email
    msg=EmailMultiAlternatives(subject,message,'no-reply@kurmatechnepal.com',[recepient])
    msg.attach_alternative(html_context)
    msg.send()

smtp(1,'ranaxmond@gmail.com')