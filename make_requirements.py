import subprocess

def generate_requirements_txt():
    # pip list 명령어 실행하여 패키지 목록 가져오기
    result = subprocess.run(['pip', 'list', '--format=freeze'], stdout=subprocess.PIPE)
    
    # 명령어 출력 결과를 문자열로 변환
    packages = result.stdout.decode('utf-8')
    
    # requirements.txt 파일 생성 및 패키지 목록 기록
    with open('requirements.txt', 'w') as file:
        file.write(packages)
    
    print("requirements.txt 파일이 생성되었습니다.")

# 함수 실행
generate_requirements_txt()
