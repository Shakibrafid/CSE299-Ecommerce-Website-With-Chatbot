step 1: python venv : python3 -m venv venv
step 2: to activate py venv: source venv/bin/activate
step 3: install: pip install django djangorestframework djangorestframework-simplejwt django-cors-headers
step 4: django-admin startproject backend .
step 5: create django app:
                python manage.py startapp accounts
                python manage.py startapp store
                python manage.py startapp cart
                python manage.py startapp orders
                python manage.py startapp chat
                python manage.py startapp core
step 6: python manage.py createsuperuser
        Username (leave blank to use 'abumdashrafulrahat'): rahat
        Email address: abumdrahat@gmail.com
        Password: 123
        Password (again): 123
step 7: pip freeze > requirements.txt
        just write :pip install -r requirements.txt
        to install all dependency 
step 8: for docker run --> docker compose up --build
        for docker to stop --> docker compose down
step 9: to work with images i need pillow a python framework to store images to db
step 10: after writing all models:-
        python manage.py makemigrations
        python manage.py migrate
step 11: to see things in django-admin register everything in app/admin:
        register models in django/admin
step 12: now write serizlizers:
        create serizlizers.py file on apps then serizlize
        the models of that app.
step 13: write permissions; first write a global permission.py
        then use it else where.
Step 14: write urls and views
        what views do:
        They take a user's web request in, 
        figure out what to do with the database, 
        and hand a response back.
Step 15: Google Oauth:
        pip install django-allauth dj-rest-auth djangorestframework-simplejwt
        on settings.py:
                on installed apps:
                        'django.contrib.sites',
                        'allauth',
                        'allauth.account',
                        'allauth.socialaccount',
                        'allauth.socialaccount.providers.google',

                        'dj_rest_auth',
                        'dj_rest_auth.registration',


                        # The Google provider
                        'allauth.socialaccount.providers.google',
                also add these:
                        SITE_ID = 1

                        AUTHENTICATION_BACKENDS = [
                        'django.contrib.auth.backends.ModelBackend',
                        'allauth.account.auth_backends.AuthenticationBackend',
                        ]

                        ACCOUNT_EMAIL_REQUIRED = True
                        ACCOUNT_UNIQUE_EMAIL = True
                        ACCOUNT_USERNAME_REQUIRED = False
                        ACCOUNT_AUTHENTICATION_METHOD = 'email'
                        SOCIALACCOUNT_AUTO_SIGNUP = True

                        SOCIALACCOUNT_PROVIDERS = {
                        'google': {
                                'SCOPE': ['profile', 'email'],
                                'AUTH_PARAMS': {'access_type': 'online'},
                        }
                        }
                adding this for auth:
                        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

                        # Google / allauth routes
                        path('api/auth/', include('dj_rest_auth.urls')),
                        path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
                        path('accounts/', include('allauth.urls')),
Step 16: # Migrating Django from SQLite to PostgreSQL (macOS)

        ## 1. Install PostgreSQL

        ```bash
        brew install postgresql@15
        ```

        If already installed:

        ```bash
        brew services start postgresql@15
        ```

        Verify it's running:

        ```bash
        brew services list
        ```

        Expected output:

        ```
        postgresql@15    started
        ```

        ---

        ## 2. Install PostgreSQL Driver

        Activate your virtual environment and install the PostgreSQL adapter.

        ```bash
        pip install psycopg2-binary
        ```

        ---

        ## 3. Export Existing SQLite Data

        Before switching databases, export all existing data.

        ```bash
        python manage.py dumpdata \
        --exclude auth.permission \
        --exclude contenttypes \
        --indent 2 > data.json
        ```

        This creates a `data.json` file containing all project data.

        ---

        ## 4. Start PostgreSQL

        ```bash
        brew services start postgresql@15
        ```

        ---

        ## 5. Open PostgreSQL

        ```bash
        psql postgres
        ```

        ---

        ## 6. Check Existing Roles

        ```sql
        \du
        ```

        Example:

        ```
        abumdashrafulrahat
        postgres
        student_user
        ```

        ---

        ## 7. Check Existing Databases

        ```sql
        \l
        ```

        ---

        ## 8. Create a New Database

        ```sql
        CREATE DATABASE myproject OWNER abumdashrafulrahat;
        ```

        Exit PostgreSQL:

        ```sql
        \q
        ```

        ---

        ## 9. Update Django Database Settings

        Replace SQLite configuration with PostgreSQL.

        ```python
        DATABASES = {
        "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "myproject",
                "USER": "abumdashrafulrahat",
                "PASSWORD": "",
                "HOST": "localhost",
                "PORT": "5432",
        }
        }
        ```

        ---

        ## 10. Test Database Connection

        ```bash
        python manage.py dbshell
        ```

        If successful, you should see:

        ```
        psql (...)
        myproject=#
        ```

        Exit:

        ```sql
        \q
        ```

        ---

        ## 11. Create Database Tables

        Run all Django migrations.

        ```bash
        python manage.py migrate
        ```

        ---

        ## 12. Import SQLite Data into PostgreSQL

        ```bash
        python manage.py loaddata data.json
        ```

        Expected output:

        ```
        Installed 11 object(s) from 1 fixture(s)
        ```

        ---

        ## 13. Verify the Project

        Start the development server.

        ```bash
        python manage.py runserver
        ```

        Verify that:

        - All existing data is present.
        - Admin panel works.
        - CRUD operations work correctly.

        ---

        # Useful PostgreSQL Commands

        Start PostgreSQL

        ```bash
        brew services start postgresql@15
        ```

        Stop PostgreSQL

        ```bash
        brew services stop postgresql@15
        ```

        Restart PostgreSQL

        ```bash
        brew services restart postgresql@15
        ```

        Check PostgreSQL status

        ```bash
        brew services list
        ```

        Open PostgreSQL shell

        ```bash
        psql postgres
        ```

        List databases

        ```sql
        \l
        ```

        List users (roles)

        ```sql
        \du
        ```

        Exit PostgreSQL

        ```sql
        \q
        ```