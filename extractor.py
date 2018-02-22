import gc
import requests
from bs4 import BeautifulSoup
import urlsArray

import traceback

for (index, line) in enumerate(urlsArray.urls):
  outputFile = open('titles.tsv', 'a')
  try:
    url = line.strip()
    print(index, url)
    res = requests.get(url, timeout=10)
    if "text/html" in res.headers.get('content-type'):
      soup = BeautifulSoup(res.content, "html5lib")

      if res.status_code > 400:
        outputFile.write(url + "\t" + "" + "\t" + str(res.status_code) + "\t" + "失敗" + "\n")
        print(url, "=>", 'レスポンス有りエラー: ', res.status_code)

      else:
        soup = BeautifulSoup(res.content, "html5lib")
        if soup.title.string is None:
          outputFile.write(url+ "\t" + "" + "\t" + "999" + "\t" + "タイトルがありません" + "\n")
          print(url, "=>", "タイトル無し")

        else:
          title = soup.title.string.replace('\n', '').replace('\t', '')
          outputFile.write(url+ "\t" + title + "\t" + "777" + "\t" + "成功" + "\n")
          print(url, "=>", title)
      del soup
    else:
      outputFile.write(url+ "\t" + "" + "\t" + "888" + "\t" + "Content-Typeがtext/htmlではありません" + "\n")
      print(url + "Content-Typeがtext/htmlではありません" + "\n")

  except Exception as e:
    print(e)
    outputFile.write(url + "\t" + "" + "\t" + "予期せぬエラー" + "\t" + "ネットワークエラー" + "\n")
    print(url, "=>", 'ネットワークエラー: ')

  except UnicodeEncodeError:
    outputFile.write(url + "\t" + "" + "\t" + "予期せぬエラー" + "\t" + "文字コードエラー" + "\n")
    print(url, "=>", '文字コードエラー: ')

  finally:
    outputFile.close()
    gc.collect()
f.close()
