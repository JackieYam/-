import requests

url = 'https://clear.twse.com.tw/fileDownload/TwseServlet/downloadFile'
r = requests.post(url, data={'fileAddr':'/home/tseweb/index/datafile/T30'}, allow_redirects=True)
open(r'C:\AuroraQuantitative\ForeignDataConverter\T30.TSE', 'wb').write(r.content)
open(r'C:\AuroraQuantitative\TWCmdTrasfer\T30.TSE', 'wb').write(r.content)

url = 'https://clear.twse.com.tw/fileDownload/TwseServlet/downloadFile'
r = requests.post(url, data={'fileAddr':'/home/tseweb/index/datafile/T32'}, allow_redirects=True)
open(r'C:\AuroraQuantitative\ForeignDataConverter\T32.TSE', 'wb').write(r.content)
open(r'C:\AuroraQuantitative\TWCmdTrasfer\T32.TSE', 'wb').write(r.content)

url = 'https://dsp.tpex.org.tw/storage/mops/home/java/t30.dat'
r = requests.get(url, allow_redirects=True)
open(r'C:\AuroraQuantitative\ForeignDataConverter\T30.OTC', 'wb').write(r.content)
open(r'C:\AuroraQuantitative\TWCmdTrasfer\T30.OTC', 'wb').write(r.content)
