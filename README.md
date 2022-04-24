# 격자 관리

## 문제
- m x n 크기의 격자를 생성한다.
    - m과 n은 2와 10,000 사이의 정수이다.
- `generate_dots(n)`: n개의 점을 격자의 좌표에 삽입한다.
    - 한 좌표에 한 번만 삽입할 수 있다.
    - 실제 할당된 개수를 반환한다.
    - 여러 번 호출 할 수 있다.
- `remove_dots(n)`: n개 만큼의 좌표에서 점을 제거한다.
    - 남은 섬 만큼만 제거할 수 있다.
    - 실제 삭제된 개수를 반환한다.
    - 여러 번 호출 할 수 있다.
- 격자와 점의 좌표를 파일 형태로 저장하고 읽는다.

## 풀이

### 구조
책 ["파이썬으로 살펴보는 아키텍처 패턴"](https://book.naver.com/bookdb/book_detail.naver?bid=20554246)에서 기본 구조를 가져와 이 문제에 적합한 방식으로 변경했다. DDD 방법론을 최대한 따라서 설계했다.

- Application
    - Service: 점을 삽입하거나 제거하기 위한 서비스
    - Unit of Work: 작업 단위
- Domain
    - Model: 격자, 격자 관리 모델
    - Dependency: 점 관리자, 격자 생성기, 쿼리 처리기
- Infrastructure
    - Repository: 파일 저장소

## 환경
Python 3.10+


## 테스트

### 실행
```shell
$ pytest --cov
```

### 결과
```
platform linux -- Python 3.10.4, pytest-7.1.2, pluggy-1.0.0
plugins: cov-3.0.0
collected 14 items

tests/integration/test_application_unit_of_works.py ..
tests/unit/test_application_services.py .
tests/unit/test_domain_dependencies.py ......
tests/unit/test_domain_models.py ....

---------- coverage: platform linux, python 3.10.4-final-0 -----------
Name                                                           Stmts   Miss  Cover
----------------------------------------------------------------------------------
src/grid_management/__init__.py                                    0      0   100%
src/grid_management/application/__init__.py                        0      0   100%
src/grid_management/application/services.py                       20      0   100%
src/grid_management/application/unit_of_works.py                  27      2    93%
src/grid_management/common/models.py                              13      1    92%
src/grid_management/common/utils.py                                4      0   100%
src/grid_management/constants.py                                   2      0   100%
src/grid_management/domain/__init__.py                             0      0   100%
src/grid_management/domain/dependencies/__init__.py                0      0   100%
src/grid_management/domain/dependencies/grid_dot_managers.py      78      7    91%
src/grid_management/domain/dependencies/grid_generators.py        18      3    83%
src/grid_management/domain/dependencies/query_processors.py       43      5    88%
src/grid_management/domain/models/__init__.py                      0      0   100%
src/grid_management/domain/models/grid_managements.py             18      0   100%
src/grid_management/domain/models/grids.py                        30      3    90%
src/grid_management/infrastructure/__init__.py                     0      0   100%
src/grid_management/infrastructure/repositories.py                18      2    89%
----------------------------------------------------------------------------------
TOTAL                                                            271     23    92%
```
