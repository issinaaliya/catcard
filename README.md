    # CATCARD
    #### Video Demo:  <URL HERE>
    #### Description:
    This program produce Postcards using incoming information and image. First card will be named "card1.pdf" and be saved in root directory with project itself. The next will be named "card2.pdf", and so on. If user inputs email address - card will be sent to the address. If email is not provided, the postcard will be created in the root directory but will not be sent.
If user inputs correct path to an image, this image will be used in postcard creation. Otherwise images for making card program get from cataas.com API "https://cataas.com/".

When a Postcard is created, the data associated with it is written to the object. Using the object's functions, the data is checked for validity. Although only one object is created per program session, this simplifies writing and reading the object's attributes.

Three project functions implement the functionality.

get_filename - returns the file name. In order to avoid repeating names, the function numbers  files when creates.

make_pdf - creates a postcard in PDF format using the inputed data and image. The fpdf library is used to create the document.

send_myemail - sends a letter with an attached postcard file to the receiver's email if the address was inputed correctly. For this purpose, the standard library smtplib is imported. Letters are sent using Google SMTP server. email for sending letters was specialy created. Credentials were moved to a separate file config.ini

This three functions are being tested by test_project.py. First test creates number five card, second test compares the name of the next file, which should be number six, and third checks if there are any errors when sending an email with the attached file from the first test.

The program can be used to automate sending of greeting cards. The user does not need to waste time searching and editing pictures in the editor. Everything can be done in one window, without switching to other applications.
