import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'https://www.hct.com.tw/default.aspx'
params = {
    'VIEWSTATE':'YCFdpHOwi8AZvNxsOy7pgcc7XiIyrPwr+gLWtHgFfWAy2jyqB3s3ZIkfYXN19KUIFBCd4UQDl53RYgtWJWvxxQ9ghNL6yU0rZVrDZkVA6fubQLnkch8PmPJy+8Rm7B2X3/ySAX7/B4xO8U+2oNgKR5FMEvPF4nzG3pPNteW+fm/FgK+5Uq69g/drYaW9FstWgnfAf++JXqhrPvad9Iu26GjW3y4L/TZLGKwRqjY9wILG82KUib2ocljUrDLAc1S1gzla8HBxv5pWp7SoTfxKYzbiQJy5m+YR3NrDWky8kr735EllvAecY6WmOvKv9QXxhFVvJZKIkt4q+Fp/0rtPnRoUUl9YtEMTcwV5JWiJUcbJMq4qLMJclwabssAQsqOn3poZgEs6PBJmcxHc3NPQHX0HT53zA1Mk+946qY64ELL9muzFDOeP99s1cnMwdp/NvdLk6q5Mkl4rZLMSixiIydGhXGMMGR9D8qdVqOMxT5EaNeGxQanJkp0532K3j9tfCj/ERVTc8DF3gMKmYMMEm6QIKb2b/ScfpsHN4X3ifCjrBd/9gl4Lg0JZRjHYKCs1OgxX4bJbkUu3nWumlRtrDQQC+ASFeIa3noTOrhf4UbujvSTqhRObhRzdDkEsOPGvF8+9Q3E0agh82chuoAhRdkVHy8YvdcJFtvcSTB/xAT3WE/WHXiPZNN2ehOPbilOWdRcH2nFzYaYXVufDmYi9yrnqqAMTkbpGyzY/v9ZHgnGfownRzRnDXKqrSU2y7+Eb3M/tR+F+GmNw/Pp2SJfV+amCO1NW1st73C+17b8sRuwyRX/Iiib+dAq2v6B6bRzOKNibtm7aeeEKQTquKdFo0KCcCdkZoFkL5U+JOED4FD9nSsd1',
    '__EVENTVALIDATION':'PhEYyHjKlU8hiQMJS8izriAqeCTrF9FfdYtEv9Wj0ob+mhHXXu41GDc5PMp5VigMXw9fr0Cv2njMd2cPEbcarsSPPf1EQ2rI/sbtgjw40hVSVbHzVPwVJgJKmN688BU49j9zYcRDXf7txykXXjBo6aPQh6kbIMwOBVMjEjqp8Ql3G4ia6Fj0uCqls+aqcEamutVjJ8j9pAAx8a0uVx/QOnNbQ6efMiTgWsFbVsWm00uOLs1p',
    'hdnTime':'hp8BnIsNZdrzimQ7tieU+wpT/rXQX/QvZyzZkb5AW1U=',
    'hdnKey':'Hd3NLZPKMYUXvJofOdoReOlspAUVWKwFTDB6REYksMc=',
    'hdnIv':'HtZfTUDLmxadEBSMGVPBvA==',
    'hdnData':'',
    'txtID':'',
    'txtPWD':'',
    'txtCode3':'',
    'TextBox1':'',
    'TextBox2':'',
    'txtCode2':'',
    'txtpKey':'6703093320',
    'txtpKey2':'',
    '2fe94307ac954350bca1603f1fe3cf8b':'9757',
    'Button1':'%E6%9F%A5%E8%A9%A2',

}
res = requests.post(url,data=params)
print res.text