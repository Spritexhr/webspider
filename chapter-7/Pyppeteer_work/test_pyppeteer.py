import pyppeteer.chromium_downloader

print(pyppeteer.chromium_downloader.chromiumExecutable.get("win64"))
print(pyppeteer.chromium_downloader.downloadURLs.get("win64"))

#无法解决连接https://storage.googleapis.com/ 下载文件的问题