import argparse
import urllib.request
import re
import datetime

def downloadData(url):
    """Downloads data using csv module"""

    """This is the URL we are going to use"""
    # url = 'http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv'

    """Opens the URL"""
    response = urllib.request.urlopen(url)
    weblog = response.read().decode('utf-8')
    return weblog


def processData(weblog):
    weblog_data = weblog.split("\r\n")
    image_hits = total_hits = msie = firefox = chrome = safari = 0
    """Create dictionary with browser type as key and hits as value"""
    browser_counter = {"MSIE": msie, "Firefox": firefox, "Chrome": chrome, "Safari": safari}
    """Create dictionary with hour as key and hits as value"""
    hit_counter = {}

    for line in weblog_data:
        weblog_lines = line.split(",")
        if len(weblog_lines) <5:
            continue
        """assign each column to a variable"""
        path = weblog_lines[0]
        # print(path)
        datetime_accessed = weblog_lines[1]
        browser = weblog_lines[2]
        """other columns in data will not be used
        status = weblog_lines[3]
        request_size = weblog_lines[4]"""

        """loop to find images in path"""
        total_hits += 1
        """way to search for file type without using regex

                extension = path.rpartition(".")[-1]
                if extension in image_counter:
                    image_counter[extension] += 1
                else:
                    image_counter[extension] = 1"""
        """use regex to find images in path"""
        if re.search(r"\.(jpg|jpeg|gif|png)$", path, re.I):
            image_hits += 1
        """use regex to find browser and count hits for each browser"""
        if re.search(r"msie", browser, re.I):
           browser_counter["MSIE"] += 1
        elif re.search(r"firefox", browser, re.I):
           browser_counter["Firefox"] += 1
        elif re.search(r"chrome", browser, re.I):
           browser_counter["Chrome"] += 1
        elif re.search(r"safari", browser, re.I) and not re.search(r"chrome", browser, re.I):
           browser_counter["Safari"] += 1

        """count hits for each hour"""
        hour = datetime.datetime.strptime(datetime_accessed, "%Y-%m-%d %H:%M:%S").hour
        # print(hour)
        if hour in hit_counter:
            hit_counter[hour] += 1
        else:
            hit_counter[hour] = 1

    """create formula for percentage of hits that were image searches"""
    imagePercent = image_hits / total_hits * 100
    print("Image requests account for {0:0.1f}% of all requests".format(imagePercent))
    """find browser with the most hits"""
    popular = max(browser_counter, key=browser_counter.get)
    print("{} is the most popular browser".format(popular))
    """print number of hits for each hour"""
    for hour in hit_counter:
        print("Hour {} has {} hits".format(hour, (hit_counter[hour])))

def main(url):
    print(f"Running main with URL = {url}...")
    try:
        weblog = downloadData(url)
        processData(weblog)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)