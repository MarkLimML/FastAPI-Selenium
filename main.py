from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from extract import *
import os
from flask import Flask, request, render_template
from app import app

SECRET = os.getenv("SECRET")

#
app = FastAPI()

class Msg(BaseModel):
    msg: str
    secret: str

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
async def root():
    if request.method == "POST":
        text = request.form['urltext']
        return render_template('results.html', title="TEST RESULT", urltext=text)
    return render_template('form.html', title='TEST URL')


@app.route("/results/{urltext}")
async def demo_get(urltext):
    driver=createDriver()

    homepage = getGoogleHomepage(driver)

    results = []
    for url in urltext:
        chkSiteOk,chkReason = doSiteCheck(driver, urltext)
        results.append({url,chkSiteOk,chkReason})
    
    driver.close()
    return render_template('results.html', title="TEST RESULT", results=results)

@app.post("/backgroundDemo")
async def demo_post(inp: Msg, background_tasks: BackgroundTasks):
    
    background_tasks.add_task(doBackgroundTask, inp)
    return {"message": "Success, background task started"}
    


