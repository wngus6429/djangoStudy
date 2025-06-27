# Django 질문답변 게시판 프로젝트 분석

## 🚀 프로젝트 개요

이 프로젝트는 Django 3.1.3을 기반으로 한 **질문답변 게시판 시스템**입니다. 사용자들이 질문을 올리고, 답변을 달며, 댓글과 추천 기능을 통해 소통할 수 있는 커뮤니티 플랫폼입니다.

## 📁 프로젝트 구조

```
mysite/
├── config/                 # Django 프로젝트 설정
│   ├── settings.py         # 메인 설정 파일
│   ├── urls.py            # 메인 URL 라우팅
│   ├── wsgi.py            # WSGI 설정
│   └── asgi.py            # ASGI 설정
├── pybo/                  # 메인 앱 (질문답변 기능)
│   ├── models.py          # 데이터 모델
│   ├── forms.py           # 폼 클래스
│   ├── urls.py            # URL 라우팅
│   ├── views/             # 뷰 함수들 (기능별 분리)
│   │   ├── base_views.py      # 기본 뷰 (목록, 상세)
│   │   ├── question_views.py  # 질문 관련 뷰
│   │   ├── answer_views.py    # 답변 관련 뷰
│   │   ├── comment_views.py   # 댓글 관련 뷰
│   │   └── vote_views.py      # 투표 관련 뷰
│   ├── templatetags/      # 커스텀 템플릿 태그
│   └── migrations/        # 데이터베이스 마이그레이션
├── common/                # 공통 기능 앱 (인증)
│   ├── views.py           # 회원가입 뷰
│   ├── forms.py           # 사용자 폼
│   └── urls.py            # 인증 관련 URL
├── templates/             # HTML 템플릿
│   ├── base.html          # 기본 템플릿
│   ├── navbar.html        # 네비게이션 바
│   ├── form_errors.html   # 폼 에러 표시
│   ├── pybo/              # pybo 앱 템플릿
│   └── common/            # 로그인/회원가입 템플릿
├── static/                # 정적 파일 (CSS, JS)
└── db.sqlite3            # SQLite 데이터베이스
```

## 🗄️ 데이터 모델

### 1. Question (질문)

- **author**: 질문 작성자 (User와 외래키 관계)
- **subject**: 질문 제목 (최대 200자)
- **content**: 질문 내용 (텍스트 필드)
- **create_date**: 작성일시
- **modify_date**: 수정일시
- **voter**: 추천한 사용자들 (다대다 관계)

### 2. Answer (답변)

- **author**: 답변 작성자 (User와 외래키 관계)
- **question**: 연결된 질문 (Question과 외래키 관계)
- **content**: 답변 내용
- **create_date**: 작성일시
- **modify_date**: 수정일시
- **voter**: 추천한 사용자들 (다대다 관계)

### 3. Comment (댓글)

- **author**: 댓글 작성자 (User와 외래키 관계)
- **content**: 댓글 내용
- **create_date**: 작성일시
- **modify_date**: 수정일시
- **question**: 연결된 질문 (선택적)
- **answer**: 연결된 답변 (선택적)

## ⚙️ 주요 기능

### 🔍 1. 질문 관리

- **질문 목록 조회**: 페이징 처리 (페이지당 5개)
- **질문 상세 보기**: 질문 내용과 답변들 표시
- **질문 작성**: 로그인한 사용자만 가능
- **질문 수정/삭제**: 작성자만 가능

### 💬 2. 답변 관리

- **답변 작성**: 로그인한 사용자만 가능
- **답변 수정/삭제**: 작성자만 가능
- **답변 목록**: 질문 상세 페이지에서 확인

### 📝 3. 댓글 시스템

- **질문 댓글**: 질문에 대한 댓글 작성/수정/삭제
- **답변 댓글**: 답변에 대한 댓글 작성/수정/삭제
- **댓글 관리**: 작성자만 수정/삭제 가능

### 👍 4. 추천 시스템

- **질문 추천**: 사용자가 질문에 추천 가능
- **답변 추천**: 사용자가 답변에 추천 가능
- **중복 추천 방지**: 같은 사용자의 중복 추천 불가

### 🔐 5. 사용자 인증

- **회원가입**: 사용자명, 이메일, 비밀번호
- **로그인/로그아웃**: Django 내장 인증 시스템 사용
- **자동 리다이렉트**: 로그인 후 메인 페이지로 이동

### 🔍 6. 검색 및 정렬

- **통합 검색**: 제목, 내용, 작성자명으로 검색
- **정렬 옵션**:
  - **최신순** (기본): 작성일 기준 내림차순
  - **추천순**: 추천 수 기준 내림차순
  - **인기순**: 답변 수 기준 내림차순

### 📄 7. 페이징

- **페이지 네비게이션**: 페이지당 5개씩 표시
- **URL 파라미터**: `?page=1` 형태로 페이지 처리

## 🌐 URL 구조

### 메인 URL (`config/urls.py`)

```python
urlpatterns = [
    path('pybo/', include('pybo.urls')),     # 질문답변 기능
    path('common/', include('common.urls')), # 인증 기능
    path('admin/', admin.site.urls),         # 관리자
    path('', base_views.index),              # 메인 페이지
]
```

### Pybo 앱 URL (`pybo/urls.py`)

- **기본**: `/`, `/<int:question_id>/`
- **질문**: `/question/create/`, `/question/modify/<id>/`, `/question/delete/<id>/`
- **답변**: `/answer/create/<id>/`, `/answer/modify/<id>/`, `/answer/delete/<id>/`
- **댓글**: `/comment/create/question/<id>/`, `/comment/modify/question/<id>/` 등
- **투표**: `/vote/question/<id>/`, `/vote/answer/<id>/`

### Common 앱 URL (`common/urls.py`)

- **로그인**: `/common/login/`
- **로그아웃**: `/common/logout/`
- **회원가입**: `/common/signup/`

## 🎨 프론트엔드 구성

### 템플릿 구조

- **base.html**: 기본 레이아웃 (Bootstrap 사용)
- **navbar.html**: 네비게이션 바 (로그인/로그아웃 상태 표시)
- **form_errors.html**: 폼 에러 메시지 표시

### 정적 파일

- **Bootstrap 4**: CSS/JS 프레임워크
- **jQuery 3.4.1**: JavaScript 라이브러리
- **custom CSS**: 추가 스타일링

## ⚡ 주요 특징

### 1. 모듈화된 구조

- 뷰 함수들을 기능별로 분리 (`views/` 디렉토리)
- 앱 기반 구조로 기능별 분리 (`pybo`, `common`)

### 2. 사용자 친화적 기능

- 페이징 처리로 성능 최적화
- 검색 및 정렬 기능
- 직관적인 UI/UX

### 3. 보안 기능

- CSRF 보호
- 사용자 인증 기반 권한 관리
- 작성자만 수정/삭제 가능

### 4. 데이터베이스 최적화

- 외래키 관계를 통한 정규화
- 인덱싱 활용 (작성일 기준)

## 🚀 실행 방법

1. **가상환경 활성화**

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **의존성 설치**

```bash
pip install django
```

3. **마이그레이션 실행**

```bash
python manage.py migrate
```

4. **개발 서버 실행**

```bash
python manage.py runserver
```

5. **접속**: `http://localhost:8000`

## 📋 추가 개발 가능 기능

- 파일 첨부 기능
- 이메일 알림 시스템
- 카테고리 분류
- 관리자 페이지 커스터마이징
- API 엔드포인트 추가
- 소셜 로그인 연동

---

이 프로젝트는 Django의 핵심 기능들을 잘 활용한 완성도 높은 질문답변 게시판 시스템으로, 웹 개발 학습에 매우 적합한 예제입니다.
