# Run server
runserver:
    poetry run python expense_tracker/manage.py runserver

# Run migrate
migrate:
    poetry run python expense_tracker/manage.py migrate

# Run all expense_tracker tests
test:
    poetry run python expense_tracker/manage.py test expense_tracker

# Run test_views for expense_tracker
test_views:
    poetry run python expense_tracker/manage.py test expense_tracker.tests.test_views

# Run test_models for expense_tracker
test_models:
    poetry run python expense_tracker/manage.py test expense_tracker.tests.test_models

# Run coverage
coverage:
    poetry run coverage run --source='.' expense_tracker/manage.py test expense_tracker

# Create coverage report
coverage_report:
    poetry run coverage report

# Create coverage html report
coverage_html:
    poetry run coverage html