# streamlink 를 이용한 스트리밍 다운로드

## - 설치 방법

1.  ### python 가상환경 구성

        python3 -m venv venv

2.  ### 가상환경 진입

        source venv/bin/activate

3.  ### streamlink 설치

        pip install --upgrade streamlink

## - 사전 준비 사항

1. ### 스트리머의 url 저장

   다운로드하고 싶은 스트리머의 url을 [target_url.dat](./target_url.dat)에 저장한다.

   ```
   # ./target_url.dat

   https://www.twitch.tv/vo_ine
   https://www.twitch.tv/viichan6
   ```

   - 주의사항 : 'url'만 한 줄씩 입력해야 합니다. 주석처리 없음

## - 실행 방법

1.  ### start 스크립트 실행

        [CENTOS-YW] leeyw@ git:(main) /home/leeyw/Documents/github/streamlink-live-download # ./start.sh
        start streamlink
        ...
        /usr/bin/nohup: redirecting stderr to stdout
        ..
        .
        pids
        3837
        3851
        3853
        done!

2.  ### 로그 확인

    - 스크립트 실행 로그 : `./logs/nohup.log`
    - streamlink 실행 로그 : `./logs/streamlink.log`

3.  ### 영상 저장 확인
    - 영상 저장 경로 :
      ```
              MOUNT_DIR="${HOME}/mnt"
              OUTPUT_DIR="${MOUNT_DIR}/Twitch/recordings"/recordings/{author}`
      ```
    - 영상 이름 규칙 : `[{author}]_{time:%Y-%m-%d-%H%M}_{title}.ts`
      - 스트리머가 방송 시작한 직후 title을 입력하기 때문인지 아니면 다른 이유인지 트위치 어플에서도 방송 시작과 동시에는 title이 뜨지 않음
      - 그런데 author도 못가져오는 이유는 모르겠음.
