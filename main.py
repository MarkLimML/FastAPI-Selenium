from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from extract import *
import os

SECRET = os.getenv("SECRET")

app = FastAPI()

class Msg(BaseModel):
    msg: str
    secret: str

@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return """
    <html>
        <head>
            <title>Test Site</title>
        </head>
        <body>
            <hr>
            <h1>Input URLs here</h1>
            <form action="" method="get" action="/results>
                <label for="URL">Enter URLs:</label>
                <textarea id="urltext" name="urltext" rows="5" cols="50"></textarea>
                <br>
                <input type="submit" value="submit">
            </form>
        </body>
    </html>
    """
##
#    if request.method == "POST":
#        text = request.form['urltext']
#        print(text)
#        return render_template('results.html', title="TEST RESULT", urltext=text)
#    return render_template('form.html', title='TEST URL')
##

@app.get("/results/{urltext}", response_class=HTMLResponse)
async def demo_get(request: Request, urltext):
    print("Processing")
    urls = urltext
    urllist = urls.split("\n")

    driver=createDriver()

    homepage = getGoogleHomepage(driver)

    results = []
    for url in urllist:
        chkSiteOk,chkReason = doSiteCheck(driver, urltext)
        results.append({url,chkSiteOk,chkReason})
    print(results)
    driver.close()
    return """
    <h1>Results</h1>
    <table>
        <thead>
            <tr>
                <th>URL</th>
                <th>Status</th>
                <th>Reason</th>
            </tr>
        </thead>
        <tbody>
            {% for result in results %}
            <tr>
                <td>{{ result.url }}</td>
                <td>{{ result.status }}</td>
                <td>{{ result.reason }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <br>
    """


    


