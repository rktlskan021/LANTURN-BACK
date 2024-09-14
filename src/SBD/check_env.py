import os

def check_cuda_environment():
    # CUDA 관련 경로 설정 (필요에 따라 수정 가능)
    cuda_bin = "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.6\\bin"
    cuda_libnvvp = "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.6\\libnvvp"

    # 시스템 PATH 환경 변수 가져오기
    system_path = os.environ.get("PATH", "")

    # 경로 확인 결과를 저장할 딕셔너리
    cuda_env_status = {
        "CUDA bin path in PATH": cuda_bin in system_path,
        "CUDA libnvvp path in PATH": cuda_libnvvp in system_path,
    }

    # 결과 출력
    for key, status in cuda_env_status.items():
        if status:
            print(f"{key} is set correctly.")
        else:
            print(f"{key} is NOT set correctly. Please add it to your PATH.")

# CUDA 환경 변수가 올바르게 설정되었는지 확인
check_cuda_environment()
