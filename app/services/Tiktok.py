import requests
from bs4 import BeautifulSoup


class TiktokDownloader:
    def __init__(self):
        self.api = "https://snaptik.gg/check/"

    def extract_video(self, text: str):
        url = text.split(" ")[0]
        res = requests.post(self.api, data={"url": url})
        if "html" in res.text:
            data = res.json()["html"]
            soup = BeautifulSoup(data, "html.parser")

            cover = soup.find(id="thumbnail").get("src")
            username = soup.find(class_="user-username").text
            description = soup.find(class_="user-fullname").text

            buttons = soup.find_all(class_="btn-main")
            result_buttons = [
                button
                for button in buttons
                if "btn-back" not in button.get("class", [])
            ]

            buttons = []
            for button in result_buttons:
                buttons.append(
                    {
                        "title": button.text,
                        "url": button.get("href"),
                    }
                )

            return {
                "status": "success",
                "cover": cover,
                "username": username,
                "description": description,
                "buttons": buttons,
                "photos": [],
            }
        else:
            return {
                "status": "error",
                "message": "Không thể tải video từ link này!",
            }

    def extract_audio(self):
        # Extract audio from the video
        pass

    def save(self):
        # Save the video
        pass


if __name__ == "__main__":
    tiktok = TiktokDownloader()
    # url = "https://www.tiktok.com/@lingg2809/video/7375115624269335824"
    url = "https://vt.tiktok.com/ZSY5SWgtq/"
    data = tiktok.extract_video(url)
    print(data)
