import time
import pytest
from common import send_email

localconfigEmail = send_email.Email()

if __name__=='__main__':
    pytest.main(['--html=./result/report.html'])
    localconfigEmail.send_email()
