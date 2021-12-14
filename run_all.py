from datetime import datetime
import pytest
from common import send_email

localconfigEmail = send_email.Email()
if __name__=='__main__':
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    pytest.main(['--html=./report.html'])
    localconfigEmail.send_email()
