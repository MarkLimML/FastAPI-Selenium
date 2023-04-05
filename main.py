from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from extract import *
import os
import uvicorn

SECRET = os.getenv("SECRET")

app = FastAPI()

class Msg(BaseModel):
    msg: str
    secret: str
"""
@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return 
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

@app.get("/", response_class=HTMLResponse)
async def root():
    print("Processing")
    urls = """https://graceful-sunburst-78f35d.netlify.app/www.classcentral.com/index.html
https://ammardab3an99.github.io/
https://heartfelt-lollipop-736861.netlify.app/
https://radiant-hummingbird-697a83.netlify.app/
http://trialserver.rf.gd/trial6/www.classcentral.com/index.html"""
    urllist = urls.split("\n")

    driver=createDriver()
    
    results = []
    for url in urllist:
        print(url)
        chkSiteOk,chkReason = doSiteCheck(url)
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    


