#install<br>
git clone https://github.com/riabow/FastApiTestTask.git<br>
virtualenv env <br>
activate <br>
pip install fastapi pandas uvicorn sqlalchemy <br>
python main.py <br>
<br>
http://127.0.0.1:5000/docs <br>
any questions - riabow@mail.ru +792637727 TWO 8 <br>
have a good day.<br>



# FastApiTestTask
task Design database structure for currency pairs that contains date. Add functionality (script) to populate initial data from file. Create CRUD functionality for currency pairs. Implement endpoint that returns historical data for specified currency pair. Implement endpoint that calculate rate for given currency pair at given date. In case there is no such currency pair, you need to calculate it by using others, for example for input NZD/AUD you can calculate rate by converting NZD -> USD -> AUD. If there are couple of variations we need minimal rate.
