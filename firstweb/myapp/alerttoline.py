# alerttoline.py
# q28Plk7483wV4CufUVoYChw7lXqb2Proo4H6diM4WJ0
from songline import Sendline

token = "q28Plk7483wV4CufUVoYChw7lXqb2Proo4H6diM4WJ0"

messenger = Sendline(token)

# test send
# messenger.sendtext('ສະບາຍດີ, ຂ້ອຍຕ້ອງການຊື້ສິນຄ້າ')
# messenger.sticker(4,1, 'ຂ້ອຍຕ້ອງການຊື້ສິນຄ້າ Pizza')
messenger.sendimage('https://fdn.gsmarena.com/imgroot/news/22/03/iphone-13-alpine-green-colors/gallery/-728/gsmarena_001.jpg')