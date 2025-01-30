:: cd ../supabase
REM supabase start

cd ../back

if exist .venv\Scripts\activate (
    call .venv\Scripts\activate
)

python manage.py makemigrations core
python manage.py migrate core

python manage.py makemigrations notifications
python manage.py migrate notifications

python manage.py makemigrations trips
python manage.py migrate trips

python manage.py makemigrations visits
python manage.py migrate visits

python manage.py makemigrations budget
python manage.py migrate budget

:: python manage.py makemigrations
:: python manage.py migrate
