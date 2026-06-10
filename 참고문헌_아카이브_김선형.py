import pandas as pd
import os

# 엑셀(CSV) 파일 이름 설정
file_name = "references.csv"
# 파이썬 파일이 있는 정확한 폴더 위치 찾기
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 그 폴더 안에 references.csv 파일을 만들도록 주소를 합치기
file_name = os.path.join(BASE_DIR, "references.csv")

# 처음 실행할 때 파일이 없으면 빈 파일을 생성
if not os.path.exists(file_name):
    df = pd.DataFrame(columns=['제목', '저자', '키워드', '요약', '파일경로'])
    df.to_csv(file_name, index=False, encoding='utf-8-sig')

# 메인 메뉴
while True:
    print("\n=== 참고문헌 아카이브 ===")
    print("1. 자료 등록")
    print("2. 키워드 검색 및 원본 파일 실행")
    print("3. 전체 목록 조회")
    print("4. 프로그램 종료")
    print("============================")
    
    choice = input("원하는 메뉴 번호를 입력하세요: ")
    
    if choice == '1':
        print("\n[새 자료 등록]")
        title = input("제목: ")
        author = input("저자: ")
        keywords = input("키워드(여러 개일 경우 쉼표로 구분 / 예: 선거, 달러패권): ")
        summary = input("요약: ")
        
        # 문자열 양끝에 따옴표가 들어오면 제거
        file_path = input("파일 경로를 복사해서 입력해주세요: ").strip('"') 
        # Pandas를 활용한 데이터 저장
        df = pd.read_csv(file_name, encoding='utf-8-sig')
        new_data = pd.DataFrame([{'제목': title, '저자': author, '키워드': keywords, '요약': summary, '파일경로': file_path}])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
        
        print("성공적으로 저장되었습니다!")
        
    elif choice == '2':
        print("\n[자료 검색]")
        search_kw = input("검색할 키워드를 입력하세요 (여러 개일 경우 쉼표로 구분: 예: 달러패권, 선거): ")
        
        # 입력받은 여러 개의 키워드를 쪼개기
        keyword_list = search_kw.split(',') # 쉼표 기준으로 자르기
        clean_keywords = [] # 공백을 제거한 깔끔한 단어를 담을 빈 리스트
        for kw in keyword_list:
            clean_keywords.append(kw.strip()) 
            
        df = pd.read_csv(file_name, encoding='utf-8-sig')
        
        # 검색 결과를 담을 빈 리스트
        found_results = []
        
        for index, row in df.iterrows():
            # 빈칸일 경우 에러 방지를 위해 글자(str) 형태로 변환
            saved_keyword = str(row['키워드']) 
            
            # 검색한 여러 개의 키워드 중 하나라도 포함되어 있는지 검사
            for my_kw in clean_keywords:
                if my_kw in saved_keyword:
                    found_results.append(row) # 찾았다면 결과 리스트에 추가
                    break # 한 번이라도 찾았으면 더 찾을 필요 없으니 내부 반복문 종료
                    
        # 검색 결과 출력
        if len(found_results) == 0: #리스트 길이를 구함으로써 검색 결과 여부를 확인
            print("검색 결과가 없습니다.")
        else:
            print(f"\n[검색 결과: '{search_kw}']")
            
            # 순서대로 번호 매겨주기
            for i, row in enumerate(found_results):
                print("-" * 50)
                print(f"번호: {i + 1}")
                print(f"제목: {row['제목']}")
                print(f"저자: {row['저자']}")
                print(f"요약: {row['요약']}")
                print(f"경로: {row['파일경로']}")
            print("-" * 50)
            
            open_choice = input("열고자 하는 파일의 번호를 입력하세요 (열지 않으려면 Enter): ")
            
            if open_choice.isdigit(): # 입력한 게 숫자가 맞는지 확인
                num = int(open_choice) - 1 # 리스트는 0부터 시작하므로 번호에서 1을 뺌
                
                # 입력한 번호가 정상적인 범위 안에 있는지 확인
                if 0 <= num < len(found_results):
                    selected_path = found_results[num]['파일경로']
                    
                    # 파일 열기 에러 방지
                    try:
                        os.startfile(selected_path)
                        print(f"{num + 1}번 파일을 실행했습니다.")
                    except:
                        print("파일을 열 수 없습니다. 경로가 잘못되었거나 파일이 이동되었습니다.")
                else:
                    print("목록에 없는 번호입니다.")

    elif choice == '3':
        print("\n[전체 목록 조회]")
        df = pd.read_csv(file_name, encoding='utf-8-sig')
        if df.empty:
            print("저장된 자료가 없습니다.")
        else:
            print(df)
            
    elif choice == '4':
        print("프로그램을 종료합니다.")
        break
        
    else:
        print("잘못된 번호입니다. 1~4 사이의 숫자를 입력해주세요.")