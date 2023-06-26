def message(domain, uidb64, token):
    return f"아래 링크를 클릭하면 회원가입 인증이 완료됩니다.\n\n회원가입 링크 : http://{domain}/api/user/activate/{uidb64}/{token}\n\n감사합니다."

def pw_reset_message(domain, uidb64, token):
    return f"아래 링크를 클릭하면 비밀번호 재설정할 수 있는 페이지로 이동합니다.\n\n비밀번호 재설정 링크 : http://{domain}/api/user/reset/{uidb64}/{token}\n\n 비밀번호 재설정을 요청하지 않았다면 이 이메일을 무시하셔도 됩니다.\n\n 감사합니다."