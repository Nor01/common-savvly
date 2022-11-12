import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
from common.util.logging_helper import get_logger
from common.util.config_wrapper import get_config_string_param
from common.util.utility_functions import utils_get_image_dir, utils_get_path_base_name
from common.email.email_template import *

# ---------------------------------------------------
# A class to send emails
# ---------------------------------------------------
class SendEmail():
    _notification_email_list = ["danny@savvly.com", "tony@savvly.com", "yuval@savvly.com"]
    #_notification_email_list = ["danny@savvly.com"]
    _subj_user_signeup = "Savvly User Registreation"
    _subj_client_contract = "Savvly Client Contract"

    # ---------------------------------------------------
    # Constructor
    # SendGrid Account: danny@savvly.com/SavvlyEmailer$@$
    # ---------------------------------------------------
    def __init__(self):
        self.glogger = get_logger("email")
        self.server = get_config_string_param("outgoing_email_server")
        self.server_port = get_config_string_param("outgoing_email_server_port")
        self.sender_email = get_config_string_param("outgoing_email_user")
        self.password = get_config_string_param("outgoing_email_password")
        ###password = AzureKeyVaultWrapper.instance().get_secret("email_password")

    # ----------------------------------------------------------------------------
    # Create attachement object
    # ----------------------------------------------------------------------------
    def _create_attachment(self, filepath, maintype, subtype, attach_id):
        try:
            fname = utils_get_path_base_name(filepath)
            with open(filepath, 'rb') as fh:
                mime = MIMEBase(maintype, 'png', filename=fname) # set attachment mime and file name, the image type is png
                mime.add_header('Content-Disposition', 'attachment', filename=fname) # add required header data:
                mime.add_header('X-Attachment-Id', str(attach_id))
                mime.add_header('Content-ID', '<' + str(attach_id) + '>')
                mime.set_payload(fh.read()) # read attachment file content into the MIMEBase object
                encoders.encode_base64(mime)   # encode with base64
                return mime
        except Exception as err:
            self.glogger.error("Failed to create an attachement with file:%s err=%s", filepath, err)
            return None

    # ---------------------------------------------------
    # Create a BASE email Message
    # ---------------------------------------------------
    def _create_email_base_message(self, recipients: list, subject: str, body_text: str, body_html: str):
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = get_config_string_param("outgoing_email_sender")
            message["To"] = ", ".join(recipients)   #to_email
            # Turn these into plain/html MIMEText objects
            if body_text:
                part1 = MIMEText(body_text, "plain")
                message.attach(part1)
            if body_html:
                part2 = MIMEText(body_html, "html")
                message.attach(part2)
        except Exception as err:
            self.glogger.error("Failed to prepare the email message err=%s", err)
            return None
        self.glogger.info("Sending email To=%s Subject=%s", recipients, subject)
        return message

    # ---------------------------------------------------
    # Create an email Message
    # ---------------------------------------------------
    def _attach_file_to_message(self, message, filepath, maintype, subtype, attach_id = 0):
        mime = self._create_attachment(filepath, maintype, subtype, attach_id)
        if mime is None:
            return False
        message.attach(mime)  # add MIMEBase object to MIMEMultipart object
        return True

    # ---------------------------------------------------
    # Create an email Message
    # ---------------------------------------------------
    def _attach_logo_to_message(self, message):
        attach_id= 0
        filepath = utils_get_image_dir() + "savvly-logo.png"
        return self._attach_file_to_message(message, filepath, 'image', 'png', attach_id)

    # ---------------------------------------------------
    # Send an email
    # ---------------------------------------------------
    def _send_email(self, recipients: list, subject: str, body_text: str, body_html: str):
        message = self._create_email_base_message(recipients, subject, body_text, body_html)
        if message is None:
            return False
        self._attach_logo_to_message(message)
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.server, int(self.server_port), context=context) as server:
                server.login(self.sender_email, self.password)
                server.sendmail( self.sender_email, recipients, message.as_string())
                server.quit()
        except Exception as err:
            self.glogger.error("Failed to send email via SMTP. err=%s", err)
            return False
        return True
#
    # ----------------------------------------------------------------------------
    # Send an email to admin to let him know that a new user has signed up
    # ----------------------------------------------------------------------------
    def send_email_to_admin_on_user_signup(self, user_name : str, user_email:str, user_idx:str):
         dic = {'name' : user_name, 'email' : user_email, 'userid' : user_idx }
         body_html = EmailTemplate().build_html("user_registration.html", dic)
         if body_html:
            self._send_email(self._notification_email_list, self._subj_user_signeup, None, body_html)

    # ----------------------------------------------------------------------------
    # Send an email to admin to let him know that a client has signed a contract
    # client_info = {'firstname': 'YYY', 'lastname': 'YYYYYY', 'email': 'YYY@leupus.com', 'address': 'YYYYYY',
    #                    'zip_code': '21121', 'birthdate': '1998-07-03', 'sex': 'M', 'is_US_citizen': 'Y', 'is_married': 'Y',
    #                    'ssn': '123-12-3123',
    #                    'spouse_firstname': 'YYY', 'spouse_lastname': 'YYY', 'spouse_birthdate': '1999-07-11',
    #                    'spouse_sex': 'F',
    #                    'spouse_ssn': '123-12-3123', 'spouse_is_US_citizen': 'Y', 'spouse_address': 'YYYYYYYYY',
    #                    'spouse_email': 'YYY@leupus.com', 'investment_start_date': '2022-07-11', 'payout_ages': [70],
    #                    'ETF': 'VOO Vanguard', 'funding': '100000', 'purchaser_type': 'Qualified Purchaser'}
    # ----------------------------------------------------------------------------
    def send_email_to_admin_on_client_contract_sign(self, client_info : dict):
        body_html = EmailTemplate().build_html("contract_signed.html", client_info)
        if body_html:
            self._send_email(self._notification_email_list, self._subj_client_contract, None, body_html)