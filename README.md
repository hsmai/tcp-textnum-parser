
# TCP Line Protocol Service (Uppercase + Sum)

작은 TCP 기반 **라인 프로토콜(line-based protocol)** 서비스를 구현한 미니 프로젝트입니다.  

클라이언트가 **문자열 1개 + 정수 1개**를 순서대로 전송하면, 서버는 (1) 문자열 **대문자 변환 결과**와 (2) 서버가 보유한 **기준 숫자와의 합**을 각각 반환합니다.

---

## What this project does

### TCP 서버
- 지정 포트에서 연결을 수락(accept)하고 요청을 처리합니다.
- 클라이언트로부터 문자열(1줄)을 받으면 UPPERCASE로 변환해 응답합니다.
- 이어서 정수(1줄)를 받으면 클라이언트 숫자 + 서버 숫자 결과를 응답합니다.
- 서버 프로세스는 종료되지 않고 다음 연결을 계속 처리합니다(테스트가 여러 번 수행되는 상황을 가정).

### TCP 클라이언트
- 서버에 연결한 뒤, 사용자 입력(문자열/정수)을 “한 줄 단위”로 전송합니다.
- 서버 응답 2개(대문자 결과, 합 결과)를 순서대로 출력합니다.

---

## Repo structure

- server.py : TCP 서버 (Uppercase + Sum 처리)
- client.py : TCP 클라이언트 (입력 2개 전송 + 응답 2개 출력)
- test_example.py : 간단 자동 테스트 스크립트
- main.py : (선택) 로컬 IDE 템플릿 파일 — 프로젝트 동작에는 필요하지 않습니다

---

## How it works (Line-based protocol)

이 프로젝트는 “텍스트 1줄 = 메시지 1개” 규칙을 사용합니다.

    Client connects to Server

    Client → Server: <string>\n
    Server → Client: <string.upper()>\n

    Client → Server: <integer>\n
    Server → Client: <integer + server_number>\n

    Connection close
    (한 요청 처리 후 연결 종료, 서버는 계속 실행)

구현에서는 소켓을 makefile('rwb')로 감싸서 readline() 기반으로 안전하게 라인 단위 송수신을 처리합니다.

---

## Requirements

- Python 3.x
- 별도 외부 라이브러리 없음 (표준 라이브러리만 사용)

---

## Quick start

### 1) Run server

아래 예시는 포트 12000, 서버 기준 숫자 7로 실행합니다.

    python3 server.py --port 12000 --number 7

서버가 준비되면 다음과 같은 로그를 출력합니다.

    Server ready... listening on port 12000, server number=7

### 2) Run client (in another terminal)

    python3 client.py --host 127.0.0.1 --port 12000

입력/출력 예시는 아래와 같습니다.

    Enter your string: hello world
    Enter a number: 5
    From Server: HELLO WORLD
    From Server: 12

---

## Run tests

제공된 테스트 스크립트로 빠르게 동작 확인이 가능합니다.

    python3 test_example.py

성공 시:

    ✅ Test passed.

---

## Implementation highlights

### Server (server.py)
- SO_REUSEADDR 옵션을 사용해 개발 중 재실행 시 “Address already in use”를 완화합니다.
- listen(5)로 대기열(backlog)을 설정합니다.
- while True: 루프에서 지속적으로 accept() 하며, 연결 단위로 요청을 처리하고 소켓을 정리(close) 합니다.  
  (즉, “서버는 계속 살아있고”, “클라이언트 연결은 요청 처리 후 종료” 구조)

### Client (client.py)
- 입력을 2번 받되(문자열 → 정수), 서버와 같은 순서로 전송합니다.
- 각 전송 후 flush()로 즉시 전송되도록 보장합니다.
- 서버 응답도 2번 readline()으로 수신해 출력합니다.

### Test script (test_example.py)
- subprocess.Popen()으로 서버를 백그라운드 실행 후, 클라이언트를 실행합니다.
- 클라이언트 표준 입력에 "문자열\n정수\n" 형태로 테스트 입력을 전달합니다.
- 출력에 기대값(대문자 변환/합산 결과)이 포함되는지 검사합니다.

---

## Troubleshooting

- 포트가 이미 사용 중이라면:
  - 다른 포트로 실행하거나, 기존 프로세스를 종료하세요.
  - 예: --port 12001

- 방화벽/보안 설정으로 로컬 통신이 막히는 경우:
  - 127.0.0.1(loopback)로 먼저 테스트하는 것을 권장합니다.

- 숫자 입력은 “정수 문자열”이어야 합니다.
  - 예: 5는 OK, 5.5는 의도된 동작이 아닙니다.
