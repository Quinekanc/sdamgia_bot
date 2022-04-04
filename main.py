from sdamgia import SdamGIA
import interactions


TOKEN = ""


with open("token.txt", mode='r', encoding='utf8') as f:
    token = f.read()


bot = interactions.Client(token='OTYwNTk1NDg2ODgzMDc0MDU5.YksuQw.mmp0Ac8UD6gHLZ8jYXorO2IpFXY')

sdamgia = SdamGIA()


if __name__ == "__main__":
    bot.start()