from fastapi import  Depends, HTTPException, APIRouter
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from selenium import webdriver
import time
from datetime import datetime
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from design_models import MMT

router = APIRouter(
    prefix="/mmt_flights",
    tags=["mmt"],
    responses={404: {"description": "Not Found"}}
)

# print('\n\nScript started on: ', str(datetime.now()))

chromeOptions = webdriver.ChromeOptions()
chrome_options = Options()
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--lang=en_US')
# chrome_options.add_argument("disable-blink-features=AutomationControlled")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36")

capabilities = DesiredCapabilities.CHROME.copy()
capabilities['acceptSslCerts'] = True
capabilities['acceptInsecureCerts'] = True
capabilities = {'browserName': 'chrome'}
ip = 'localhost'

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@router.get("/")
async def read_all(db: Session = Depends(get_db)):
    return {"mmt": "get mmt"}

@router.post("/")
async def read_todo(mmt: MMT, db: Session = Depends(get_db)):
    # print('\n\nScript started on: ', str(datetime.now()))
# async def read_todo(destination: str, origin: str, date: str):
    browser = webdriver.Remote(command_executor='http://' + ip + ':4444', desired_capabilities=capabilities)
    browser.maximize_window()

    org = mmt.origin
    des = mmt.destination
    search_date = mmt.my_date.strftime("%d/%m/%Y")

    url = f"https://www.makemytrip.com/flight/search?itinerary={org}-{des}-{search_date}&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&ccde=IN&lang=eng"
    # print(url)
    browser.get(url)
    org_date = mmt.my_date

    xpath_str = '//*[@id="root"]/div/div[2]/div[2]/div[2]/div/div/div[3]/button'
    wait = WebDriverWait(browser, 10)
    xpath_el = wait.until(EC.presence_of_element_located((By.XPATH, xpath_str)))
    # time.sleep(1)
    xpath_el.click()

    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False

    min_count = 0
    while(match == False):
        lastCount = lenOfPage
        time.sleep(1)
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

        if lastCount == lenOfPage:
            match = True

        if min_count == 1:
            match = True

        min_count += 1

    browser.execute_script("window.scrollTo(0, 0);")

    final = []
    final_model = []
    wait = WebDriverWait(browser, 1)
    xpath_el = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'listingCard')))
    c = 1
    for i in xpath_el:
        j = i.find_element(By.XPATH, ".//div[@class='makeFlex simpleow']")
        j_text = j.text.split('\n')

        try:
            k = j.find_element(By.XPATH,
                               ".//span[@class='plusDisplayText fontSize9 boldFont redText appendLeft5 textCenter']").\
                                text.split('\n')
            for sp in k:
                j_text.remove(sp)
        except:
            pass
        j_text.append(j_text[8].split(' ')[0])
        j_text.append(j_text[8].split(' ')[1])
        j_text.append(int(datetime.now().timestamp()))
        j_text.append(str(datetime.now().date()))
        j_text.append(str(datetime.now().time()))
        j_text.append(org)
        j_text.append(des)
        final.append(j_text)

        c += 1

    df = pd.DataFrame(final,
                      columns=['airline', 'airline_number', 'departure_time', 'origin', 'flight_duration', 'stops',
                               'arrival_time', 'destination', 'fare', 'other', 'currency', 'amount',
                               'capture_timestamp_epoch', 'capture_date', 'capture_timestamp', 'origin_code',
                               'destination_code'])

    browser.quit()

    for index, row in df.iterrows():
        mmt_flights_model = models.Mmt_flights()
        mmt_flights_model.airline= row.airline
        mmt_flights_model.airline_number = row.airline_number
        mmt_flights_model.departure_time = row.departure_time
        mmt_flights_model.origin = row.origin_code
        mmt_flights_model.flight_duration = row.flight_duration
        mmt_flights_model.stops = row.stops
        mmt_flights_model.arrival_time = row.arrival_time
        mmt_flights_model.destination = row.destination_code
        mmt_flights_model.fare = row.fare
        mmt_flights_model.other = row.other
        mmt_flights_model.currency = row.currency
        mmt_flights_model.amount = row.amount.replace(",", '')
        mmt_flights_model.capture_timestamp_epoch = row.capture_timestamp_epoch
        mmt_flights_model.flight_date = org_date
        mmt_flights_model.capture_timestamp = row.capture_timestamp
        mmt_flights_model.currency = row.currency
        mmt_flights_model.capture_date = row.capture_date

        final_model.append(mmt_flights_model)

    db.add_all(final_model)
    db.commit()

    return successful_response(201)


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }

def http_exception():
    return HTTPException(status_code=404, detail="MMT not found")