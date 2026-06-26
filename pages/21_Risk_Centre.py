import streamlit as st

from data.data_engine import DataEngine
from risk.risk_engine import RiskEngine

from core.ui import load_css
from core.ui import app_header
from core.ui import section

from core.components import stat_row

load_css()

app_header(

    "🛡 Risk Centre",

    "Protect your capital before chasing profits."

)

trades = DataEngine.load_trades()

risk = RiskEngine.calculate(trades)

section("Performance")

stat_row([

{

"label":"Daily",

"value":risk["daily"],

"helper":"Recent",

"status":"positive" if risk["daily"]>=0 else "negative"

},

{

"label":"Weekly",

"value":risk["weekly"],

"helper":"Recent",

"status":"positive" if risk["weekly"]>=0 else "negative"

}

])

stat_row([

{

"label":"Monthly",

"value":risk["monthly"],

"helper":"Overall",

"status":"positive" if risk["monthly"]>=0 else "negative"

},

{

"label":"Largest Win",

"value":risk["largest_win"],

"helper":"Best trade",

"status":"positive"

}

])

stat_row([

{

"label":"Largest Loss",

"value":risk["largest_loss"],

"helper":"Worst trade",

"status":"negative"

},

{

"label":"Average Win",

"value":risk["average_win"],

"helper":"Winning trades",

"status":"positive"

}

])

stat_row([

{

"label":"Average Loss",

"value":risk["average_loss"],

"helper":"Losing trades",

"status":"negative"

}

])
