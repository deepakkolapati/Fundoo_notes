@echo off

rem Run the first Flask application in a separate terminal
start cmd /k "flask --app app:user run --debug"

rem Wait for a moment to allow the first application to start
timeout /t 1

rem Open the Swagger URL for the first application in the default web browser
start http://127.0.0.1:5000/docs

rem Run the second Flask application in a separate terminal
start cmd /k "flask --app app:note run --debug --port 8000"

rem Wait for a moment to allow the second application to start
timeout /t 1

rem Open the Swagger URL for the second application in the default web browser
start http://127.0.0.1:8000/docs

rem Run the third Flask application in a separate terminal
start cmd /k "flask --app app:label run --debug --port 7000"

rem Wait for a moment to allow the third application to start
timeout /t 1

rem Open the Swagger URL for the third application in the default web browser
start http://127.0.0.1:7000/docs
