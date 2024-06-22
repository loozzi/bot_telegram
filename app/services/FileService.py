import os
import uuid

import aiohttp


class FileService:
    def __init__(self):
        self.files_path = "./files"
        if not os.path.exists(self.files_path):
            os.makedirs(self.files_path)

    async def save(self, url: str, filename=None):
        if filename is None:
            filename = self.random_filename()
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(os.path.join(self.files_path, filename), "wb") as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            f.write(chunk)

        return filename

    def delete(self, filename: str):
        os.remove(os.path.join(self.files_path, filename))

    def random_filename(self, type: str = "mp4"):
        return str(uuid.uuid4()) + "." + type
