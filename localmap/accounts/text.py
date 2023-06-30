def message(domain, uidb64, token):
    return f"아래 링크를 클릭하면 회원가입 인증이 완료됩니다.\n\n회원가입 링크 : http://{domain}/api/user/activate/{uidb64}/{token}\n\n감사합니다."

def pw_reset_message(random_pw):
    return f"임시 비밀번호 : {random_pw}\n\n로그인 후 비밀번호 변경부탁드립니다.\n\n 감사합니다."