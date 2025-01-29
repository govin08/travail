from PIL import ImageGrab
import pytesseract
lef = 1045
top = 945
rig = 1072
bot = 973
def read_digit(lef, top, rig, bot, Display=False):
    # 이미지 캡쳐
    capture = ImageGrab.grab(bbox=(lef, top, rig, bot))
    # 이미지 보이기
    if Display:
        display(capture)
    num = pytesseract.image_to_string( # the number of wins / losses
        capture,
        config='--psm 7 -c tessedit_char_whitelist=0123456789'  # PSM 모드 추가
        ).strip()
    return int(num)
num = read_digit(lef, top, rig, bot)