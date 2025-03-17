import requests
import json
import csv  # CSV 파일 작업을 위한 라이브러리

def get_api_data(url, api_key, offset=0, limit=100):
    """
    API에서 데이터를 가져오는 함수

    Args:
        url (str): API 엔드포인트 URL
        api_key (str): API 인증을 위한 키
        offset (int, optional): 데이터 요청 시작 위치. Defaults to 0.
        limit (int, optional): 한번에 가져올 데이터 개수. Defaults to 100.

    Returns:
        dict: API로부터 받은 JSON 데이터를 파이썬 딕셔너리 형태로 반환, 오류 발생 시 None 반환
    """
    try:
        # API 요청 헤더 설정 (X-Redmine-API-Key 사용)
        headers = {'X-Redmine-API-Key': api_key}
        # API 요청 파라미터 설정 (offset, limit)
        params = {'offset': offset, 'limit': limit}
        # API에 GET 요청 보내기
        response = requests.get(url, headers=headers, params=params)
        # 응답 상태 코드가 200 OK가 아니면 예외 발생 (예: 401 Unauthorized, 404 Not Found 등)
        response.raise_for_status()
        # JSON 응답을 파이썬 딕셔너리로 변환하여 반환
        return response.json()
    except requests.exceptions.RequestException as e:
        # API 요청 중 오류 발생 시 오류 메시지 출력
        print(f"Error fetching data from API: {e}")
        # 오류 발생 시 None 반환
        return None

def save_data_to_csv(data, filename='api_data.csv'):
    """
    JSON 데이터를 CSV 파일에 저장하는 함수

    Args:
        data (list): JSON 데이터 리스트
        filename (str): 저장할 CSV 파일 이름
    """
    if not data:
        print("No data to save.")
        return

    # CSV 파일에 쓸 필드 이름(헤더) 정의 (원하는 필드만 선택적으로 추가 가능)
    fieldnames = [
        'id', 'name',
        'manager_name',
        'status',
        'start_date', 'due_date',
        'parent_id','parent_name'
    ]
    
    # custom_fields 를 위한 필드 이름 추가
    for item in data:
        if 'custom_fields' in item:
            for custom_field in item['custom_fields']:
                if custom_field['name'] not in fieldnames:
                    fieldnames.append(custom_field['name'])

    try:
        with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()  # 헤더 쓰기

            for item in data:
                row = {}
                # 기본 필드 값 추출
                for field in fieldnames:
                    if field in item:
                        row[field] = item[field]
                    elif field == 'author_id' and 'author' in item:
                        row[field] = item['author']['id']
                    elif field == 'author_name' and 'author' in item:
                        row[field] = item['author']['name']
                    elif field == 'manager_id' and 'manager' in item:
                        row[field] = item['manager']['id']
                    elif field == 'manager_name' and 'manager' in item:
                        row[field] = item['manager']['name']
                    elif field == 'owner_id' and 'owner' in item:
                        row[field] = item['owner']['id']
                    elif field == 'owner_name' and 'owner' in item:
                        row[field] = item['owner']['name']
                    elif field == 'parent_id' and 'parent' in item:
                        row[field] = item['parent']['id']
                    elif field == 'parent_name' and 'parent' in item:
                        row[field] = item['parent']['name']
                    else:
                        row[field] = ''
                
                # custom_fields 값 추출
                if 'custom_fields' in item:
                    for custom_field in item['custom_fields']:
                        row[custom_field['name']] = custom_field['value']

                writer.writerow(row)

        print(f"Data saved to {filename}")

    except Exception as e:
        print(f"Error saving data to CSV: {e}")

if __name__ == "__main__":
    # API 엔드포인트 URL 정의
    api_url = "https://dxlandt.easyredmine.com/projects.json"
    # API 키 정의 (실제 API 키로 변경 필요)
    api_key = "b9ee97bf1e7f430f8e57a7d6381838317fb1e176"
    # 데이터 요청 시작 위치
    offset = 0
    # 한번에 가져올 데이터 개수
    limit = 100
    # 가져온 모든 데이터를 저장할 리스트
    all_data = []

    # 데이터가 없을 때까지 반복해서 데이터 가져오기
    while True:
        # API에서 데이터 가져오기
        data = get_api_data(api_url, api_key, offset, limit)
        
        # 가져온 데이터가 없거나 "projects" 키가 없거나 "projects" 키 안의 데이터가 0개이면 반복문 종료
        if data is None or "projects" not in data or len(data["projects"]) == 0:
            break

        # "projects" 키에 있는 데이터를 all_data 리스트에 추가
        all_data.extend(data["projects"])

        # 다음 데이터 요청을 위해 offset 증가
        offset += limit

    # 모든 데이터를 CSV 파일에 저장
    save_data_to_csv(all_data)
