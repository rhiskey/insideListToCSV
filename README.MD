1. Go to https://github.com/mozilla/geckodriver/releases/ and place geckodriver to proj folder
or add it to system env Path `C\Python\Python39` or default `C:\Users\USERNAME\AppData\Local\Programs\Python\Python38`
2. Install requirements `pip install -r requirements.txt`
3. (Optional) Pass connection to MongoDB in env file, paste .env:
   ```
   URL=https://www.cbr.ru/inside/BlackList/datasource/?page=0&dateFrom=&dateTo=&SPhrase=&PageSize=5000&Thema=-1&_=1622632910146
   ```
4. Run `main.py`
5. Or compile executable with `auto-py-to-exe` + add binary `driver/geckodriver.exe`

`pip freeze > requirements.txt`