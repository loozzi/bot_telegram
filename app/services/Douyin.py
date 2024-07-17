import requests
from bs4 import BeautifulSoup


class DouyinDownloader:
    def __init__(self):
        self.api = "https://savetik.co/api/ajaxSearch"

    def extract_video(self, text: str):
        text_splits = text.split(" ")
        url = text.split(" ")[0]
        for text_split in text_splits:
            if "douyin" in text_split:
                url = text_split
                break

        res = requests.post(self.api, data={"q": url, "lang": "en"})
        if "data" in res.text:
            data = res.json()["data"]
            soup = BeautifulSoup(data, "html.parser")
            cover = soup.find(class_="thumbnail").find("img").get("src")

            username = ""
            description = soup.find(class_="content").text.strip()

            buttons_raw = soup.find_all(class_="tik-button-dl")
            buttons = []
            for button in buttons_raw:
                buttons.append(
                    {
                        "title": button.text.replace("\xa0", ""),
                        "url": button.get("href"),
                    }
                )

            download_photo_btns = soup.find_all(class_="download-items")
            photos = []
            for dp_btn in download_photo_btns:
                photos.append(dp_btn.find("img").get("src"))

            return {
                "status": "success",
                "cover": cover,
                "username": username,
                "description": description,
                "buttons": buttons,
                "photos": photos,
            }
        else:
            return {
                "status": "error",
                "message": "Không thể tải video từ link này!",
            }

    def extract_audio(self):
        # Extract audio from the video
        pass


# if __name__ == "__main__":
#     douyin = DouyinDownloader()
#     url = "https://www.douyin.com/user/MS4wLjABAAAAnR5w1lATOlO-cwRbSBD6TIvabNYbE3SAnIAxa4_mdSA?modal_id=7365391428635069707"
#     data = douyin.extract_video(url)
#     print(data)
