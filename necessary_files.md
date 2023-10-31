1.

현재 성남 DB(tibero)에는 다음과 같은 스키마들이 존재합니다.

tibero
├ OUTLN
├ SEOUL_IRIS
├ SEOUL_TIBERO
├ SNITS
├ SNITS_IF
├ SNITS_INT
├ SYS
├ SYSCAT
├ SYSGIS
├ TIBERO
└ TIBERO

2.

각 스키마에서 저희 프로젝트와 관련있는 데이터들은 다음과 같습니다.

tibero
├ OUTLN
├ SEOUL_IRIS
├ SEOUL_TIBERO
├ SNITS
  ├ "L_IF_INT_PHASE_CONFIG" : "이력_연계_교차로_현시구성" - 올라와있지 않음
  └ "L_IF_INT_TPLAN" : "이력_연계_교차로_시간계획" - 올라와있지 않음
├ SNITS_IF
├ SNITS_INT
  ├ S_INT_CONFIG : "교차로_제어기" - 올라와있으나 데이터상의 이슈 존재
  ├ "S_INT_PHASE_CONFIG" : "교차로_현시구성" - 올라와있음
  ├ "S_INT_TPLAN" : "교차로_시간계획" - 올라와있지 않음
  ├ "S_SA_DPLAN" : "그룹 일계획" - 올라와있음
  ├ "S_SA_WPLAN" : "그룹 주간계획" - 올라와있음
  └ "S_TOD_HIS" : "신호 TOD 이력" - 올라와있지 않음
├ SYS
├ SYSCAT
├ SYSGIS
├ TIBERO
└ TIBERO

3.

각각의 테이블들에 대한 컬럼 정보와 상세 사항들은 다음과 같습니다.

- "SNITS/L_IF_INT_PHASE_CONFIG" : "이력_연계_교차로_현시구성"
    - 데이터 상태
        - 컬럼명만 올라와있고, 내용이 올라와있지 않습니다.

    - 컬럼명
        - 생성일시 : CRET_DTM
        - 교차로번호 : NT_NO
        - 현시번호 : INT_PHASE_NO
        - 시차제구분 : INT_PLAN_CLSS
        - 링번호 : INT_RING
        - 이동류번호 : INT_FLOW_NO
        - 최소녹색시간 : INT_MIN_SPLIT
        - 최대녹색시간 : INT_MAX_SPLIT
        - 황색시간 : INT_YELLOW
        - MDS제어여부 : INT_MDS_CTRL
        - 주현시지정여부 : INT_MAIN_PHASE
        - 감응 제어여부 : INT_ACT_CTRL
        - 듀얼링 여부 : INT_DUAL_FLAG
        - 차로수 : INT_LANE
        - 고정현시 여부 : INT_FIXED_PHASE
        - 현시확장감응여부 : INT_EXTENDED
        - 시작링크 아이디 : START_LINK_ID
        - 끝 링크 아이디 : END_LINK_ID

- "SNITS/L_IF_INT_TPLAN" : "이력_연계_교차로_시간계획"
    - 데이터 상태
        - 컬럼명만 올라와있고, 내용이 올라와있지 않습니다.
    - 컬럼명
        - 생성일시 : CRET_DTM
        - 교차로번호 : INT_NO
        - 그룹이동여부 : INT_SAMVFLAG
        - 플랜번호 : INT_PLAN_NO
        - 플랜인덱스 : INT_PLAN_INDEX
        - 링A현시1녹색 시간 : INT_ASPLIT1
        - 링A현시2녹색 시간 : INT_ASPLIT2
        - 링A현시3녹색 시간 : INT_ASPLIT3
        - 링A현시4녹색 시간 : INT_ASPLIT4
        - 링A현시5녹색 시간 : INT_ASPLIT5
        - 링A현시6녹색 시간 : INT_ASPLIT6
        - 링A현시7녹색 시간 : INT_ASPLIT7
        - 링A현시8녹색 시간 : INT_ASPLIT8
        - 링B현시1녹색 시간 : INT_BSPLIT1
        - 링B현시2녹색 시간 : INT_BSPLIT2
        - 링B현시3녹색 시간 : INT_BSPLIT3
        - 링B현시4녹색 시간 : INT_BSPLIT4
        - 링B현시5녹색 시간 : INT_BSPLIT5
        - 링B현시6녹색 시간 : INT_BSPLIT6
        - 링B현시7녹색 시간 : INT_BSPLIT7
        - 링B현시8녹색 시간 : INT_BSPLIT8
        - 옵셋값 : INT_OFFSET

- "SNITS_INT/S_INT_CONFIG" : "교차로_제어기"
    - 데이터 상태
        - 잘 올라와있습니다.
        - 그런데 교차로 X좌표, Y좌표 (경도, 위도)가 각각 37, 127로 고정되어 있어 아무 쓸모가 없는 데이터입니다.
    - 컬럼명
        - 제어기번호 : INT_NO
        - 교차로명 : INT_NAME
        - 그룹번호 : SA_NO
        - 교차로 X좌표 : INT_LAT
        - 교차로 Y좌표 : INT_LNG
        - 스마트교차로 여부 : IS_SMART


- "SNITS_INT/S_INT_PHASE_CONFIG" : "교차로_현시구성"
    - 데이터 상태
        - 잘 올라와있습니다.
    - 컬럼명
        - 제어기번호 : INT_NO
        - 현시번호 : INT_PHASE_NO
        - 시차제구분 : INT_PLAN_CLSS
        - 링번호 : INT_RING
        - 이동류번호 : INT_FLOW_NO
        - 최소녹색시간 : INT_MIN_SPLIT
        - 최대녹색시간 : INT_MAX_SPLIT
        - 황색시간 : INT_YELLOW
        - 주현시지정여부 : INT_MAIN_PHASE
        - 차로수 : INT_LANE
        - 현시좌표1 X : INT_PHASE_LAT1
        - 현시좌표1 Y : INT_PHASE_LNG1
        - 현시좌표2 X : INT_PHASE_LAT2
        - 현시좌표2 Y : INT_PHASE_LNG2
        - 현시좌표3 X : INT_PHASE_LAT3
        - 현시좌표3 Y : INT_PHASE_LNG3

- "SNITS_INT/S_INT_TPLAN" : "교차로_시간계획"
    - 데이터 상태
        - 잘 올라와있습니다.
        - 그런데 데이터가 네 줄밖에 없어서 사용할 수 없습니다.
    - 컬럼명
        - 제어기번호 : INT_NO
        - 교차로 시간계획 플랜번호 : INT_PLAN_NO
        - 교차로 시간계획 플랜인덱스 : INT_PLAN_INDEX
        - 링A 현시1 녹색시간 : INT_ASPLIT1
        - 링A 현시2 녹색시간 : INT_ASPLIT2
        - 링A 현시3 녹색시간 : INT_ASPLIT3
        - 링A 현시4 녹색시간 : INT_ASPLIT4
        - 링A 현시5 녹색시간 : INT_ASPLIT5
        - 링A 현시6 녹색시간 : INT_ASPLIT6
        - 링A 현시7 녹색시간 : INT_ASPLIT7
        - 링A 현시8 녹색시간 : INT_ASPLIT8
        - 링B 현시1 녹색시간 : INT_BSPLIT1
        - 링B 현시2 녹색시간 : INT_BSPLIT2
        - 링B 현시3 녹색시간 : INT_BSPLIT3
        - 링B 현시4 녹색시간 : INT_BSPLIT4
        - 링B 현시5 녹색시간 : INT_BSPLIT5
        - 링B 현시6 녹색시간 : INT_BSPLIT6
        - 링B 현시7 녹색시간 : INT_BSPLIT7
        - 링B 현시8 녹색시간 : INT_BSPLIT8
        - 옵셋 : INT_OFFSET

- "SNITS_INT/S_SA_DPLAN" : "그룹 일계획"
    - 데이터 상태
        - 잘 올라와있습니다.
    - 컬럼명 : 생략

- "SNITS_INT/S_SA_WPLAN" : "그룹 주간계획"
    - 데이터 상태
        - 잘 올라와있습니다.
    - 컬럼명 : 생략

- "SNITS_INT/S_TOD_HIS" : "신호 TOD 이력"
    - 데이터 상태
        - 올라와있지 않습니다.
    - 컬럼명 : 생략

"S_SA_DPLAN" : "그룹 일계획"
"S_SA_WPLAN" : "그룹 주간계획"
"S_TOD_HIS" : "신호 TOD 이력"
