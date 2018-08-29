def download_scores(driver, reportID, instructorID, termID):
    driver.get("https://www.applyweb.com/eval/new/showreport/excel?r=2&c=" + reportID + "&i=" + instructorID + "&t=" + termID + "&d=false")

