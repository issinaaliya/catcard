import project


def test_make_pdf():
    assert project.make_pdf("Aliya", "Asanali", "Wishing you a hearty congratulations on your outstanding achievement. You've earned every bit of this award.", "", "card5.pdf") == True
def test_get_filename():
    assert project.get_filename() == "card6.pdf"
def test_send_myemail():
    assert project.send_myemail("Aliya", "rutatule@gmail.com", "Asanali","card5.pdf") == "Card successfully sended"
