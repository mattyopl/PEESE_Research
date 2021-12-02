from playwright.sync_api import sync_playwright
import pandas as pd
import math
import time

def polymerData(index):
    time.sleep(2)
    if index%10 == 0:
        formNo = 10
    else:
        formNo = index%10
    xpath = "//html/body/table[2]/tbody/tr[5]/td/form[" + str(formNo) + "]/table/tbody/tr/td/b/a"
    page.locator(xpath).click()
    xpathPID = "//html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[1]/td[2]"
    PID = page.locator(xpathPID).inner_text()
    xpathIUPACstruct = "//html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[2]/td[2]"
    IUPACstruct = page.locator(xpathIUPACstruct).inner_text()
    xpathIUPACsource = "//html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[3]/td[2]"
    IUPACsource = page.locator(xpathIUPACsource).inner_text()
    xpathNext = "//html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[4]/td[1]/b"
    if page.locator(xpathNext).inner_text() == "Other name:":
        OtherName = page.locator("//html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[4]/td[2]").inner_text()
        if page.locator("//html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[5]/td[1]/b").inner_text() == "Polymer Class:":
            PClass = page.locator("//html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[5]/td[2]").inner_text()
            CUF = page.locator("//html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[6]/td[2]").inner_text()
            FW = page.locator("//html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[7]/td[2]").inner_text()
        else:
            PClass = page.locator("//html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[6]/td[2]").inner_text()
            CUF = page.locator("//html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[7]/td[2]").inner_text()
            FW = page.locator("//html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[8]/td[2]").inner_text()
    elif page.locator(xpathNext).inner_text() == "Polymer Class:":
        PClass = page.locator("//html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[4]/td[2]").inner_text()
        CUF = page.locator("//html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[5]/td[2]").inner_text()
        FW = page.locator("//html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[6]/td[2]").inner_text()
        OtherName = ""
    else:
        PClass = page.locator("//html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[5]/td[2]").inner_text()
        CUF = page.locator("//html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[6]/td[2]").inner_text()
        FW = page.locator("//html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[7]/td[2]").inner_text()
        OtherName = ""
    tempDF = pd.DataFrame([[PID,IUPACstruct,IUPACsource, OtherName, PClass, CUF, FW ]],columns=["Polymer ID", "IUPAC Structure Based Name", "IUPAC Source Based Name", "Other Name", "Polymer Class", "CU Formula", "Formula Weight"])
    time.sleep(2)
    page.go_back()
    return tempDF

username = "mtgojhvedolbsgymhl@kvhrs.com"
password = "Smoked$almon5tinky"
start = 57
now = start
pageNumber = math.ceil(start/10)
df = pd.DataFrame(columns=["Polymer ID", "IUPAC Structure Based Name", "IUPAC Source Based Name", "Other Name", "Polymer Class", "CU Formula", "Formula Weight"])

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://mdpf-cas.nims.go.jp/cas/login?service=https%3a%2f%2fpolymer.nims.go.jp%2fPoLyInfo%2fcgi-bin%2fp-search.cgi")
    page.fill("input[name='username']", username)
    page.fill('input[name="password"]', password)
    page.click("text=Login")
    time.sleep(7.9)
    page.click("input[type='radio'][value='Homopolymer']")
    page.click("input[type='submit'][value='Search']")
    time.sleep(4.8)
    page.fill("input[name='pagejump']", str(pageNumber))
    page.click("input[type='submit'][value='Go page (1 - 1403)']")
    while now < 14026:
        print(now)
        df = pd.concat([polymerData(now), df], sort = False)
        df.to_excel("C:/Users/matth/OneDrive - Cornell University/Research/Full Scrape/" + str(start) + "-" + str(now)+ ".xlsx")
        now = now + 1
        if math.ceil(now/10) != pageNumber:
            pageNumber = math.ceil(now/10)
            page.fill("input[name='pagejump']", str(pageNumber))
            page.click("input[type='submit'][value='Go page (1 - 1403)']")
    page.close()