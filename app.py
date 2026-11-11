import os
import sys
import streamlit as st
import urllib.request
import urllib.parse
import json
import hmac
import hashlib
import time
import datetime
import base64

# ==============================================================================
# CONFIGURACIÓN Y SEGURIDAD BORA DESIGN // ADOBE CREATIVE SUITE ADMIN CLOUD
# ==============================================================================
FIREBASE_URL = os.environ.get("BORA_FIREBASE_URL", "https://bora-design-nestpro-default-rtdb.firebaseio.com")
SECRETO_MAESTRO_BORA = b"BoraDesign_Angelo_SecretKey_2026_Pro_V3_Monthly"
EPOCA_BASE_DIAS = 19723
FIREBASE_SECRET_DEFAULT = "UKSc4y38ZoRp0WSJ4eA3ub9nlXIefv4WDDHv2tvz"

PRESETS_ETIQUETAS = ["Poseidon", "Ocampo", "Heidy lee Sport", "Sublimación Express", "Taller Central"]
CLAVE_ADMINISTRADOR = os.environ.get("BORA_ADMIN_PASSWORD", "Bora2026Admin*")
MAX_INTENTOS_LOGIN = 5
SEGUNDOS_BLOQUEO_LOGIN = 60

# Logo Oficial Bora Design (Blanco alta resolución incrustado)
LOGO_BORA_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAA4cAAAF8CAYAAAB8J85lAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAOdEVYdFNvZnR3YXJlAEZpZ21hnrGWYwAASchJREFUeAHt3e913DbWx/Gfn7Pv460gdAVxKli6AjsVhK4gSgVhKohSQZgKolRgpoLIFZhbQbwV6ME1QXssS8OZ4R9ckN/POThyPGPHGpEgLnBx8eQuELx5H9tjv+7if3eHv37y5Ml/BeBBoav7Onx5Glpx8LWIL9//ev/XDzm8N7t7v9fd/8r9uQ/hOvstfKmEKQ7vLdPd+/379xn3GLCA0J/9EL5caz11uI9/FpJ6QnC4Od29dqv+oflWwMaF7syCPgsCn8dWxK9PY0vN7sf38WsXv74N9+d7YRMIDpMb7q/D+8wa9xlwptCfvdP4ROmcbLz6TEiK4HBfDgekrXhYImMxEPyP+gdXqU/BYI6Ge7MVAWPWCA5dGwLGj42JU+BhoS+zZ+rfWl8Z7su/hGQIDjE8JFtrpOXAqxgMvlQfBL5SvoHgqVr19+aNCBazQXCYpVafnoO3PAeBD33ZL+HLldZHamliBIe4r1P/gGyYuUFKMRj8Rn0guIdgcEyrPlBsWe3wi+BwE4ZJU7vf/mJiBnuUIKV0QGppYgSHOMYeiG1oN+FG/V3Awg5WByt92iuIL3ViEsclgsNNakNrRHYNdiJhSumA1NKE/k/A42xgbis2Tego/rFBT2j/ETAjCwhD+z60N+E/baayUb+HkMDwcYX6AKS12d14b34jAEso1fdLXbjP/rYKjrH6MbBV3yutUkiGlUNcogutFrOomCBONNjkQyUCwbl04t5MipXDXWnVB41/knqKLUmYUjp4H+6pfwtJEBxiik79w7FmIIpTxLRROzfJgsLnwpIakXa6OoLDXbLA0PYnXrMfGLmLE7et0iO1NJEnh/8RLogi/tK+DsUgDs8KAx7TiCARj2CVMKlO/b3JvuEE7j1XzTf69ExlX+32tOonZbjfkCVHE1w22fKjsLonp74xPuCGAd4rAQ+rQ/uVFBuYGBTWYv+AB51IOXXn4NlaiftkSzoxKYMMOUgpHZBamsjJweGh+DD7SaTO4GGdeCjuGkGha50+pZwSJDrCs3WTOvE8RCYcpZQOSC1N4KJqpeEHZWeQvA6/tHNIOgGfK9RXOP2Nim77Yg+WWHW0FYGhV4XiCmL4Wf0U94HCgYNnay1sRaH+eWhVhVNXgATGVPKFTMUELlo5PBRnOv8QexLxsE7Mmm4eK4VZ68Q96o4F7iJI3KI2tIpVe3jkKKV0QGppApPPObSZzvDlO7GCiIcV6mdNfxI2xyaHQrPJoVYEhrkqxMqGO+HZ+rN8pXdhHqX68xJ5JsKVOMlbyJennK+9vsnBoYkBYiXgcXU8PJg00w2IB9fb4OZvkfaxFYX6IPEP7lM3amGrau41OFPJJ8YYK5ucVnoo7jUqBTyuU7/BmJSaTMVZvEb+ZhgxrzquXiGhcL/9I4672LJOPBPhgMOU0gGppSubOzj0VuXoKrQcDqR9qk8P/2EWsdCn8yYLbWtw0ImHYXbi/uJftJ1ZPDtupQvtNn79b/y9h45h2ds9OuhCuwr36p9CEo7OHDNtaGtMGBzeb18d/LrQp8Hr4a9z14X2KtxnOYxXsEEOx+/3UbV0Rf/SvKxjs4GVl0HS23AxtdqAWFHQiv58o0+HJ+daBKhQXymRADET4Wf1g/oUt5wDIAsCW/X9VBvT4Wdz7x4ttI1DzovQbsL31qhfSeR+XZ8NiCr50Hl7poZrc7jH7L4r9eney0mhT89EAkSkUMk3m5QmOFzJrCuHxllq6YutBIcPORiMWhGJUvnNonahfRt+Ru8Fl+Jqoa1clMpPF9qN+gdKm+o6i4NXm5UtY8s1WOzEKuLq4vXzt3xo4lEb7lmgpc/vuxxYH0WAiNU5Tikd2L3xjPHiOpYIDi3t7Eo+bDo4vC8OIixQtBmWQnmwQfsLwZ1wPb1Uv7cwp2Cmje33uVcG5xIHrfbZ2tccV/+vw2f7o7CKOAn4j3zIJjg8FD9Du+deyX9afCe2XWBF8Vl/I/9ILV3JLNVK72HGK5Fw09zaoC20Z+qPF2nlX0lJb19iJVKb5LGHRQ6Boc0k1upXoW1C6GevgaGxCat4n34b/tPuVZtM65SPq3jsBVUWV8BM+XT2Gdo5nqHZc9HuuUp+77lCfYrpFvcwwyfvEyaDSljFEsGhlxnOXQsPwZu4ImcD0Fa+1Zxj40NMI7XUcC+r/8e06rMD/h0DwltlxoLY0H6NEzp2vzbKQ6H+rLYfhDV0wiziPfd7vOcq+fxsC/Xp/MAacgkOXzFpso4lgkNmOR2Jq4k26Kzke4DRcNOnFQ9At71NnlMdrX+51qdVwlYbEVcULWXP+8rGoWtbZebeRY4OgsRa/rxi8gVLiymlufTfQ+EpLGyJ4BAOOX8ImiI00ksTiWmkjfw+JIbU0WcxJTO7VcJTZbKycchWmf8mzRS5iud52v3WyZea+woLy2XVcFAJiyM43Jn4ECzlc8Bpe5mYFVpR3F/oPY3UVgqfxdTRXWUmZBQkFur3Sb0UkKE4KWP32rX8sMm6RsBycgsOSS1dAcHhDsVqT5Zq2skfTw/mTYv7Cy2NtJRPbWhFXCncdbp6JkFiof5MRDIAkK1YibeWH2VM+QdmFa+r3AKtofIwFkRwuFOxmqPHALGkOM3y4gqtBYaF/OnUF5p5QTn3z1mQKP+Fa2oCROQsZtg08qNmtQQLyG3VcFAJiyI43LGDANHbqkwtLCbOFrbyN2P4YV+hrZBtqdDM3GL621C4ppNPNpj9gwEtMmYriF72NhehUZwGs4l9c67B4XOeLcsiONy5GCBW8oXVw4XEFZ1G/gLDNrTnccYeJzjYI1XLJxt4UKgGWYqp7HYuopfJ0ysGxJhRzqmZpJYujOAQ9hD8U/72+uU6o+VWDAxr+XNFCunlHFdaNIX6QjUEiMhOnDz18my0ATGrh5jLlDFWp/T3RSUshuAQAxtgekovrZglnY/TwLBTv1r4qzCJ00qLg0IEiMiX9U9eno2VgIlmSCltQ7tRWqSWLojgEB/EFBpvJbyp0DYDp4HhcJD9W2E2sdJiJX/7iAv1ASJH1SArzp6NBVsuMIOpKZm/x6r3KZ8zjBEXRHCIQ55mSA2ppROFgcRv8hcYXnE8xXJiRdNv5S/NtBABIvLk6dlYC5im0uXeHxSMa5QWY8SFEBziI4erhyVpA5cLn90v8pWG1Ik00lXEvVIWIKZO/bnP7mcCRGTF2bOR5yIuFs83LnW5m0d+nQL3wkIIDnGft4E7FakuEFNJr+THbWglaaTrsQFtaFZtsZYvBIjI0Z/yg3Q6XGpqWvLHgNBBaqnhXlgAwSE+E2dIW/lRCmdxuMewUX+oPdVIE4jVTGv5QoCIrIT7yCa4WvlAOh0uVely72N1+0ON0uJeWADBIR7yu/zgxj+Dw8Dw2g5sZ39hWjFA9LSSbIYAkSqmyEUrH0inw9lmTik99ntr4l5YAMEhHuJpn9JTBo+ncRgY1rF6JhyIez0r+UKAiJy08oMtFzjXbCmlA1JLt4ngEF8gtTQ/YXBtnWMtP+q4WgVHYiXTSr4UIkBEBpwMhAfPBZyn0uUeSikdNEqLDLOZERziMa384CF4RNy35anKLIGhY84DRNKD4F0rHxgQ42QLpZSe8toaSC2dGcEhHtPKD4LDR8QO3zpmLx0jgWEGHAeIfwjwrZUPBQNinGH2lNIBqaXbQ3CIx3g6coDg8AFxYPBG/aDaAwLDjDgNEMt4PifgVSc/2HeIU1W63LGU0kGjtFhJnxHBIR4U9x128uEpM6QP+k0EhpggBoi1fLmKxZUAj5g4RVYWTik95z1LIrV0RgSHOOZWfhTCR3Hw7GWmjMAwY07PQaxjkSXAlXC/dKIoDfKyWErpAZs0SX1f/CDMguAQx3Tyg0qGURg0WypRLR8IDDcg/gwb+XJNBVM41ckHgkOcYsoZt6eklA7ZZslXD4VZEBziGE/pM6QL6GN6iJfKpDcEhptiZ1J6yhYYzkDk3oc3Xu4TtlzgqDhmmDKJcE7A1yitkgnFeRAc4ph/5EchGKvmWCg9Gxy9FjYjzvx+J18ZA4X6vbWAJ17SSk0h4HFTixadExx6SC2thMkIDnHMf+XH7mdH4z5DD2lEXWivYjCBDYn7qbxVfXsVrn32ksCTTn58I+BxlS53UkrpgNTS7SA4xDGeBv+7Dg7D4Ng2lNdKz66JMjwEPE0cYEbhZ2uzv1P2qCzhOt4DgAf/kx+FgAfMkFLa6nweqpYyYTIRwSEeFVcRkFjs4Bv5cEVguH3hZ/yr/OxtHTTsr4IT7+RHIeBhUys+XxLo/aX0Cwvesl+yQ3CIXBTaL0snLZReHc/Fwz5YsaFOfhSh/SIgPVYOkYNK05ycUjqIqaWpCzZVwiQEhxjTCcnEs94qpXdLZdJ9iQ/5F/KVXl7Fo1yAlChIA9dCP2nppIUudzOhrkDqSeSCbQjTEBwCTsUUulrpdSJNY5dianktXxrKlQPAUSlSSg//bOoJlFK4GMEh4JendFL2Ge5U3H/Yyg+bNGkEJOJsP34h4EtTJ3TPTikdkFqaP4JDwKFYhMZDxciGfYZQf/6hp1S6kvRSoEehJhxKnFI6ILU0YwSHgE9vlF4nfymFSCAOFCr5QvVSoPeVgE+mngs7x3EUqY+0MGyHuRDBIeBMLEJTKD3SSfFRPAzZwwN/YIHhTwIAHCo1zcUppYM4odgqrUq4CMEhctFpB2I6aa30SCfFQ17LV3rpFalDgJ4J0IcxhPWHhS43R0rpx79LaT3l+XAZgkPAFzerhgLuiYOGWr7UAgCYStPMGdB5mGAmtfQCBIfIhafVikU4WjUknRSPcli91IrTTN1jAwBbUGqaySmlA1JL80VwiDFeCj5sPjiUj/1TnTgmAONq+VJTnAbAnjlLKf34dyotUksvQHCIMQSHK4irhpXSY9UQo8I18lf4ci0/rJ9i9RDAnlWaZolAjtTSDBEc4lHOZuK3vnLoYtWQIjQ4w8/yV5yG1UMAe1VqmtlSSgekluaJ4BDHeBpobXY1y9OqoYATxYc+q4fYHSYh4I3TlNKPf7fSIrX0TASHOOZr+bHllUNWDZErK07TyQ9bPfTUb2GbCA7hTaVplgzgSC3NDMEhjvH0AOy0QawaImcOj7awPutKALAvpaZptRBSS/NDcIhjCvnwfsF0h9RYNUTW4rXTyY+KtD8sjOsLbsyQUtquUIiO1NKMEBzimEI+3GqD4qqhh1SHWsA0tfxg7yGW9pV82cNRT3hcpWkaLW/2YjcXqISTEBzimOfyYasPPpvF8jAD3QqYwOHqIZVLsSf/CHs2dZK51cLCM6JT+rHGK54LpyE4xDFegsNNrhzKx2pLw7mGmEktP1g9xJKeyZf/CbsUgp2XmjbJ3K44BmiVln1O3wijCA7xoDi74mWGZXPB4Qx7BObyq4B5WNqQq3MPBSzDVUXcDe/Jx7ipq4aN1uOhtkEljCI4xGM8za5scWWrUnq3YVCx1VVZrMzjuYcUIMBCPKWmERjum/uU0gGppfkgOMRjSvnwfmsBjKPjKzwN5LENthLtabBaC5hfIT86YZcySyn9+P9UWqSWnoDgEI8p5cMWV7a8rGa0AmYUVw8b+VGGARQDAcyNlUN4kFNK6cBDamktHEVwiC/EJfdSPrTaHg97oW4oRIOFpD7P6j4Px8VgWwr5QXC4Q3GcVmmaViuLqaWd0npOaulxBId4iKd9On9pQ2JKqYcqsN4G8NiI8PC3e7aVHxSmwdwK+cG+8X16qWnahBPEjdKywHDq57dpBId4iJeZdttv2GpbvHRIHg6kxXZ5mnygMA1mE64lL0c8DVg53KccU0oHrdKrhEcRHOIhXoLDVttTKb2W0udYmO0r8XSNVQLm8ZV8eSvsSkyJzKZK6X0xu6RTWqSWHkFwiM+Em+V7+dlsv6nUR0cppY2ABTksTEP5csyFlUOklnNK6aBRWqSWHkFwiPsq+dFqW7x0RK2A5blKLRXlyzEPT8Hh5o56wklyTikdtEqvEh5EcIiP4spWKR88zGzNzUO67i1VSrGGmDpEaim2ppAfBIY7E8dp2aaUDpw8H0oySh5GcIhDP8mPRhvi6HiQVsB6GvnBkRaYQyk/OmFvphbX8jTx3ii974Uv/EuAPs5GVfKhC52Xh4NS57T5g+/vpK/H3vNEYtUykbs+tXKsmMb/nsw7m2uppV6OkvhQtTTOWANnc1j1lpXD/ak0TSM/PDwfbNLwV+EzBIcY/CI/Wm2Pl1WLJQfGjUZm1UOA8uIJq5ep2DX428h7mtBeayYWiIUBtQWbXlJ37DMgOMSlvBWj4VrekZm2/rRywsnz4UNqKRXcP0daKYYKpZ5Srmptj4dBxS0dIBJo5Ecp4HKl/KAYzf5sKaV00Cg9UkvvITjcuTgTVcuPZmsFUxwdYeFhIDGaeorFpPrsPVUt5WwrTFHKDwLD/ak0TSN/PDwf2I9+D8EhLM2skB+1tsdLCf1W6TEw3x87pNvTijVnW+Fscb+hp/5rU+cA47itpZQOqFrqE8HhjoWbwaqTlvJjc6uGUSkf3io9b3t29iTJZx9TmT2tcnAN4hKVfGG/4b5sMaV00Cg9UksPEBzuVAwMa/lhA8ha2+RhMOplfwoD83QKpeNplYMUIlyilB8d+w13p9I0jfwitdQZgsMdchgYmusNH85eKj0vA4nnd6SWri5+5ikDc0+rHAUpRDhHTCkt5Ecr7MZWU0oHpJb6Q3C4M+HityMravlis6A/a4McnYvlaZaZPV/rS7rvNa5yeNp36GUfMPJQyZetnQOM47acUjpolB6ppRHB4U7YzFNob+TnQOqBDRhLbVchHzr5UQlrq5ReKz9Ib8ZJ4qpNJT9sMrUV9qTSNI38I7XUEYLDHQgPN1up+Vs+g7B6w+mkxssg1EMxmkF5N30mFCe66ycoKqXXyo9SwGl+ki+tsBtbTykdOEot5bgtERxu2sFqoc3IeMyltsDwV22bl+DQW/GCWliLl1QZKpYiKw5XDU0t7MnUbRg5pJQOPKweVgLB4RbFoNDOL3wnvzPkN1vdZ3iPl0qlnvZ7GVs9/EFYVFw1rOWDp/MOKUqDU7hbNdx4pg2+VGmaRvlolF4pEBxuiRU/Ce0P9UFhJb9sBeG1Ni4OPj0MQDv5dH1HYZDFxMDwjZyIExSd/CgEPCIWE6vkSyPsRly5njrB3CofHiYQSS0VwWH27CK2oylCsz2FrfxvqLXA8IXDlawleAl8PH/WLfsP5xc/UwsMC/nSyg8mJvCgOChv5IsVoqFK6b5MTSm9zWmlOY4LSS11gOAwMzEY/N6OpAjNVgg79WljOeyhabWfwNB4SVvzfFiyfUYWIHpL38qSnWcYmh1X08rnylgnP9h3iMfYPVTIl1rYm0rTNMpPo/RK7dy/BHdiOuJX6gcvw+HVhfoLNtd9MnbI/Y/aFy+DzxyC8fqufxDWsn01EvtqzhBXCi1roJLvPuIv+VEIuMcyceQvA4dVw52ZKaXUwyrcuYbU0pTPMUst/U+soLpLWw8ObXUth4Hx4d60Qttin/8eqpI+pJAPnfJQKM4a3vUPtVb9qufbJ3kEuKsIn43thxgmjF7p0yRSDjr5wcohPhMDw1r+1MLeTC3YllVK6cAyy8J9aM/9UmmV8jWZuaqtB4c8/NOyG/zVjqurFfIhx8//lQ5m7+/6L51QKGPxwd/Jx/eRaxYGFmBbNcKXK/lzw6rhLk1dvW6UL7veS6VVhbaHivoPIq0US7BVnuudHFVxjJfB51ZW3QphC2zSqFB6Ty2Ff0d7oPGAmL5nVb69TiZ7DFixoHBNDpkhU+SYUjqwf7tN1qQcQxV7Ti2lIA3mdh3aMwLDDwr58I8APzr58ZWwW2HwZ6l7Vunba2BYc67hLn2vabJMKR3ECTsPhfRK7RTBIebwYV9haP+2ojPMxH/kYuWQwQWc6eQHWw92KJ4JbEGhTWZ6TS++ZZJ1t/acUjrwkEpdaacIDjFFqz7l5cNKIUHhJzFVCcCXOvnBvsOdsBRiWykMzc7/bOV7YqCT/zOLsQBSSj+y7yH1mPJDaql2iD2HOEen/qFqOdg3BINHeRl0dgJ88bSSTXC4YfFYKDtIvFQfbOXy835Nxsdu7bJK6X2OqpZav7G7fYcEh7ivu9esk7EbtCMYPAt7mYCHdfKD4HAjYiA4HPNirVSeacNX4VnbCntVappG22Grh6XSqkLb2xndBIf4QqFPKQ0WDHbD11iCfggU3wrHUKkUeECcEU59yPGgEM7xPJ4FmNrTg1YcfM3dXs8Ehvq9sCKl9JDtO7xWWk/3WLWU4BDH2AP3wZnXOLhrh0aw+IV/yweCQ3jkJTjEeYZVOcyvpgDN7lWaZhMppYM4kdiK1NLVUZAGl7KBnd0wNqtzG27gd6H9ttfNuwDO0skHAlR4QGAIU2qaRtvjYSW00s4QHGIuhfobqI2B4vehfa392vP3DozxsqJNcIiU7D6oCAxBSumjPBxp8XRvCx8Eh1hCoX4Gq4uriQRKAA6R7oy960IrQ2DoYfCL9CpN022xwm0shNgqvV0dLUNwiKVV6oPEXwgSAQD4MNj9lr36OFBqmi2uGg5ILV0ZwSHWcqU+5fR7AQCwT3ZUxQuOhsJgppTSLa9Ak1q6MoJDrKkIrSHVFIAThYB1dKG94KgKPKDSNJZSequNIrV0fQSHSKFSv4pIZVMAKbF6gzVYVe9vOdwejyg1zZZTSgeklq5o6+ccNvJTMn3McKCvKQ5+r9A2K+oV6gNESngDSIXgEEvqQntNUIjHkFJ6Mvser5XWh9TScD9v/szDrQeHv2+lUw4XpB08bEHiN+o7kuEw4twDxzp8byJABABsiA1kf2ZvIUZUmmbTKaUDu4/CWLHV9FXWqarQCA7hw8HN3x7+fgwaLWAsYyuUHwsQi/A9vhYAAPlq1QeFrYBxU/ex7SGldNAqfXD4KoxXf9z6pA97DjNnQaOdk2SBVWjPwm99q74yaG4zSZUVqhHmVggAsLRO/YH2LwgMcYow5nmp6dlfezon00XVUvULMptGcLgxMVj8NTQLEi1YbJTPvksLEH/RNmzuMFoAwBdsBaFWX3CGA+1xjqmrhrtIKR2E77WTj6qllTaO4HDD7EY6WFGslEeQeBUCxJ8EAMvrBFzGBuWWpfPM9syztxAXIKX0fK3Ss9TSLRaK/IjgcCdi6mkuQWId0y0wXSHAn00/WLFZw3lrljr6bczSISjE2UgpvZiX1NJNH8VGcLgzMe3FUk5r+daEzvNr5eudnNj6DBey5OWa7AQcZ8FfE5oVTHvGnkLMpNI0u0opHThKLb3ShlGtdIfiTOfPIWiwQPGNfK4u2eDRUia+VZ7+Jz++Eue5AZjO+pG5BqSF/Dx72oNfd+q/z7eh3e5xAI5lxQlbUkov1yp91dLn9nPcauYAweGO2QxMuLgt+LI9fh5nQezm+ynTMxA9dRiWTkyBHOBLnXCOm7mOHLLji8KXv+VjFdm+r18FrGOObTN7Ln7UKj3rt+znuMmfA2mlO2ezHqH9KL9pprb/MLuywTH1wYuc03OxTYV8YNIkkdhHepmUvM7xOYNsUaV0gvC92yH0ndKrtFEEh/ggrs5V8ulaefKyesieQwDuxD3wXvr3G/ZnY2kzpZS2QqP0nm+1zyA4xEfxQV3JnzLcgN8rP16Cw+cCfCnkA/vJEouZKx5+DkVofwhYFiml82iVngWGOY5NRxEc4jMxQPS4//A6wxkaLwNPZsOBB3AMgRvfyUeaWMk5u1hYpWk6quW6Si2dugrsEsEhvhA35tfyxQKcH5QXVg6Be2IhEg9YNXQi7j+s5IPtc9/0GWZII/Z9paZphYGHiq3lFlNLCQ7xoLgHsZUvV5ndhF4GnwV7aeCIl2uRVUNH4kpALR9uMj9nFz7NMelASuknXo7z2FxqKcEhjrGS5Z4GULmtHno667AQ4MNX8oGVQ2fipKSHAd9wzi4wp0rTkFJ6IE4oeRijbi61lOAQj3KW6jPIafXQ0+CTMu3w4pl86ASPbFKyU3pWifAXZSj8u/8O7d1MbZMFN9ZGSuliGqW3udTSfwk4IgSIf4aLvtX0Tm0uQ3WoHA4s7uSH7TvMOR2lUz9DuPdUQLv+C+VdZMjLyuFbwR0rEhSeOTYT3yr9dW6TkbexUFsWYkA71z7zrL5350gpXYat8HsoopjLuPQkBIc4hc3kvpMfNnBwfxPGQU4nHymdhfJhAaB1+JYy0j5hhecLd/2g2QaAtiJs90OpfBTywVOfhgOh73wb+s5aPs5AtErZbfg3/VfOxVW+uQbKnTZaiTGRStOQUvoASy0N172NGVJPJGUxLj0VaaUYFdNLPTykB2VG1eS8pJbmULHUOngb2DwLAeHr0BoCw4eFz+X9kz5w/jW0F+pTNRvloVB673MY7O9ZrJrt4bljg87We9pYTFuc8/OquUfmQUrp4hqlt6nUUoJDnMoKBXhK6ctlRrOTD94rltqg5lkMdvaeOno2C6Kf9Cv8FiS28s3DdUgxmjzYc8fDz6oIzfv+wzea796qSSedFSmly6Jq6cwIDnGSeFh0Iz+qTGZpPO1r8rraWofA5keCwulikGgribX88rCKTXCYgfjc+U4++gZ75rislh33GRaaRxerxmI+laYhpfQIqpbOj+AQ5/A0c2WBYQ4VOFv5UcofCwwZiMwsfqaeUsEPeZjUaYUsxG0NXgZdtv/Q1XNn5n2GNsAuhdmQUrqaRultJrWU4BAnCw9pm21v5Ucl5+LAxsuKmLd9hx2B4XJsNVbOBhXhwenlGmQvVUbiykAtH268DAAX2Gd4xT7D2ZFSug4vqaU5ncX9KIJDnMvTasSrTGZpWvngLTgshaXZPkRP6bpfK733caILGYmpjq3SK0L7Qz7Muc/wmn2Gi5i6qktK6QkcpZaW2gCCQ5zLyw1oSC09z1NHVV6tEikz1AuL1V49TegUSq8VcmX7DzulZ+ljPymhufcZiiyO2cWV3amTsq1wqkbpWd/gYRJ0EoJDnCUWCPCyfG9y2ADsaZXCy+phLazFjgTwMqFTKL1WyFJ8/lif7+F6rlNNts28z9CU8bPFvF5qOlZzT+dlbFopcwSHuEQjP0r5ZxVLvTx4PQTTLauG64lVYBv54GFy4i8hWyGIsf60lg/N2qsEnGeYlUrTkFJ6Hi9jrVKZIzjEJTwFO8+97zuMM7JeVg89fF6NsDYvM6qpg8OO/Yb5Cz9DWw33kC5daP3+bM59hg3HViyDlNL1Ocpsyz61lOAQZ3MW7Biv5/cdauWDh32ans5+3IvkEzqxUmnqiYlW2AoLajw8h8q4/29xC+wzrIWlkFKaRiMfKmWM4BCX8rTvsJR/rfxImVr6/gkHkK8uppZ2SsvDTGorbEKcpLQCNR6yWK7iPsDFLLDP8BXppIuiSmkaXjLbKmWM4BCX8rTvyEsRlUc5KrNsKqVDYJhO6s/ew33aCpsRz5Gt5MP1UqlkC+0zJINjITFLotA0rXA2R6mlhaPq8GcjOMRF4r4dDnc/j5fV1pRHWhAcptMprVJptayUbE/4mf4pH+mRljJ9s9Ce7jn3GbbsM1zcHKvIpJRezsviRalMERxiCi8D/aeZbP4lFdfHGWV7lTowSj2J0wibFIOdVunZNT7r+YcL7DOshKVN3bpBSuk0NtYitXQCgkNMwfl95yG1lGI0u0QxGqzA9h92Ss/2H/6gGSywz/CK1fNlkVKanqOiidmmlhIcYgpPA/1Czjmr8jp7p/VEevHEvs3jrRWSeGJl68d/Pq+1jNQVckkp3bjYv6YstnWoDv3rpGt+oX2GfwpLI6XUBy+fYakMERxiilZ+5LLv0FOn72Ughe0rlVYjbF4ssjLnStul5th/OOc+w459hqshpdQHL6mlHvqjsxEc4mKxUpwXORWl2XtqKfanVFqtsAvhufSrfEwGFKH9pgvMvM/QnjelsLiYjVNomlaYzFGm1tMcU0sJDjFVJx9S72c6iaMyyybLTgt5ielxhdIhpXR/fpSPZ9Orc/cfss8wa5WmI6V0Pl4+y+yytAgOMZWbPXTKRyM/agHLSj0B0Qi7EifhXshHlsb1qZNwC+wzvA6fBcHGekpNQ0rpvLxMxFfKDMEhpvKSIqlMjrOwgYunqqXlQudyAYOUs6Ydg+N9itseKvnQnPh8mnWfYWjsM1wJKaX+xEmiVulll6VFcIipOvnxb+VjztnhqWYpuw48olQ6rbBbsTqnh7620MgK9sz7DE0ZB8dYR6XpPJ2FvBVePtOsUksJDjGVp70MWawcRr/KjytWD7GEOFua8tqqhV0LAZLtP2yVXhkDwC+wz3ATSk3znqNGFuElc6RSRggOMdU/8iObAMdRuoOxz+2lgPlVSueGATIiO7+zU3o2EfdZX7vAPsMmVmzFSmZKKWXVcAGkll6G4BBTeRp8FcpLLT8qAfMrlQ4DZHzgfP/h3PsMa2FtlaYjOFwOqaVnIjjEVOxpuFAsTNPKh5JjLTCncD3Z2aOF0qDqHz4T+1sPB1JbIHhjqfwL7TNktXx9paYhpXRZpJaeieAQU3kKDgvlp5EftYD5pCx0VAu4J6ZbNkrPJk5sxXDOYLUmMFwfKaX+kVp6PoJDTEI1tMlsttDTsRasHmIupdLg+AocYwVqOqX3XPNpwzXPsRVpVJqO4HB5pJaegeAQSCgG156OtagFTDTTbPqlagGPiH3uC21nS0Qn9oynVGoaUkrX4Sa1NIfq8ASHmEMnH3I9jsFSnVg9xJZUSoNVQ4yKBWo87D+cA8dWJBIrzxaahlXDFXhKLQ3tGzlHcIgtyTI4ZPUQWxJL81dKoxZwgjiJ4KnfvUTNqlNSc6QIEhyux8tnXck5gkPAB1YPsRWprh1WDXGWcL3Y/sNWeerYZ5jc1OCQlNJ1efmsX3lPLSU4BBxwuHrYCLhMrTRqAed7LT9bI07VKe0ZorsXU0qnDvBZNVxRTCdvlZ771FKCQ8APWz3s5EMRHn4/CThDwkI0rBriInHAWCkvHFuRHimleWrlQyXHCA4BJ+LqYS0/rnKoqgVXaqXxnYALhb73L+VToOaaiRAXSCnNk5d7x3VqKcEh4Eh86LfywTouVg9xkliIptT6mnDf3AqYIFxDlrnhfSWni/skkVDo674XKaVZcpZa+lJOERxiS7ZyblUtP64oToMTpRhI8Lbajrx53n9o13opeEBKad5a+VDJKYJDbMkmgsOY4uTpwdEIOCLh8RXX7L3CXGJqvw38PT5L2GfoQEwFnCM4/EtIxUs673OvqaUEh5hDIczNUoe8DFAoToMxKa4PSvljduGaeit/q9FNTHtFenOkAt7EiQgkELchdErPbWopwSG2pNNGxLz4Wn7UIUB0XXoZaSRcNSwFLCAGYl6OFupE6rQnpJRuQyMfKjlEcIhJ4sAQC4gDFE+FNhoBX/pF6yOdFIuKhV889L8N17oPM6aUUqU0vVY+uEwtJTjEVF/Ljy2maXgqr26dWIpAAE7Fqn1zDJbO0YVGOinWYEekpH6u1BQFc4OU0o2ItR06pWeB4fdyhuAQU3ma8ei0MbED85LeZKheikO11veawRXWENP71578eMhN6Hc9TcTuVaXpSCn1o5EPHvqYzxAcYqpCfvxP22SrJJ38aDwf3op1xCJFhdZlFRtbASuJE3S10rL+tiVATGfGc1xJKfWjlQ+ltzEVwSGmKuTHJlcT4ipJJT+K0H4TdisOlGqti+qkSCJed63SKsSqU0pzZMyQUupInPjx8vNwlVpKcIipnsuPThvlZPb60KsQIPwg7FWKyYFSQDq2/7BTWuz7TqfSdAT3/jTywVVqKcEhpvISHL7f+oyck9nrQ9fsP9yfOClQal1XVGxESvH5YgO41M+ZK86dXRcppZvmJWB3lVpKcIiLhQvZAkMvF3OnfXgtX+mzDftg9iNROikHgMOFcB2+lY8MjjpWCsY6SCndKFJLH0ZwiCk8HYreaQdi9bxKfhTqK+lRoGYf3mjdCaEutB8FOBEnKjxUkLbMDU/P4C2rNB0ppX418sFNainBIabwlCN9q50IgxNLTfF0vIWtILMPZuMSVCe12dyS2XY49LvSs0kajrhYGCmlu0Bq6T0Eh5jCUzGa3QSHJgyYbTXF0/dcsQ9mu8LP1g5/rrUu9hnCKy+TYYXI3FgaKaUbR2rplwgOcZFYiKSQH3scRHqonneoJkDcnjhzvvZKtZ1n6GF1BvhMooJMx5C5saxK05FS6l8jH1xk5BEc4lKVHAkDyV2tHBqH+w8NhRI2JK5I2D7DQuu54TxDeJSoINMpyNxYACmlu0Jq6QGCQ1yqlB+tdiqmQ1zJl4YjLjbDzjMstJ5OfUVewKO1CzKdg4m5+c3xHGtJKfXPWWpp8jOkCQ5xNocppbtbNTzkqHreoRsq6eUtHra9ZopLJwrQwKkEBZkuQQXTec0x8doIuWjkQ6nECA5xiUq+tNq5WKDG074Gm11vGajkKQ6E11yRHiqTUoAG7jhOJ72PCqYziT/zOYrutUIuPKWWJr2HCQ5xlthhVvJl1yuHBywdz9NnQYCYoRgY1loXgSE8e6N8FOr7XSqYTvNS07X0a/lwllpaKSGCQ5zL26b3WzrfXkzH81bBdAgQ2QuTgUSBYRWu3bcCHMoknfS+Qv1+YVyu0nSNkBs3q4dKiOAQJ3O6atgKH8UKpi/kL0BsYgl4OJUoMOTICriVUTrpQ15RwfQypJTuWiMfypRZVwSHOIfHBw0lou+JAaIVEvFW2OOawYpPCQNDjqyAZzmlkz6kZlLuInNkupBSmifLYvEydkp25iHBIU4SZzAq+dKFzrcVvhDT9Er5CxDrWAUTTsSfR611ERjCtRnTSVPvA7/maKGzVZquEbITt+d4SS2tlAjBIU7lqRLmoBUeFQNEb2cgmqswWHlHRb20rGBFaH9o/WuEwBCuzZhOeh2u9W+VPkCkgumJwudk6aSFpmuFXDXyoUg1sUNwiFGON+SzV2lE3M9VyZ9CfaEaZrQTiIPfv7V+2gqBIXIwRzppF9pwrVdKaygMRgXTcaSUwlNqaakECA5xVHiYWDnnWv6QUnqiDAJE9iGuKAbkFhgWWheBIdybcTK0jClqXrI4itD+EMbMMWHWCNmK962XY8EqJUBwiEfF1YVr+VQLJ3McIBrbh/g3aU/Li/sLW/UrCWsiMIR7M6aT1vdXjsJ//6r0qYYle74fR0opDnjJTEuSWkpwiAfFh6Sl1hTyqRXOEgPEUv6K1Bh7KN9SWW8Zdj9bAK40qxdXBIbwLqZczpFOenvken+t9P3vFf3so0gpxcDqbOy2ainBIb4QH5KWflLIp4bO9zLhc/tLfgNEu+6sst4bVhHnEweCFhjOcW7Xuaq4YgJ4N0c6aacjA7l4zFCt9Khg+jBSSvGBs9RSgkOkdTB7mmIgeapauFjc/2IV9Dr5VIbWsRdxGjt+xgJt9anha6eR2oP1OQfcIwcxUJpjVb0em7h0kl5qqGB6gJRSPMBLlf7VU0sJDvFRJoEhq4YziDPYL+Q3QDR1PPJijlSf3YhHVNi+Ipv1LLW+Tn1g+FaAc/G512i65ozJEA/ppUMFUwLE3hyptreMTzbFy8qhWXX1kOAQHxyUtvccGNrDtBZmcRAgeuoA7ytCa2KQSBrUETEotNXWd0pXGfFDQMoACRmZK530x1Pf7Ci9tJDPM4xTKDVdK2xG3IbjZQtOpRURHCJlaftzXTPonJcNUuIhzV6r0g4K9bPcbwgSvxRXV+0errV+CumgCe0F9yhyEe+bOSZSPh5bcaqYXuohMHu+9wqm8ciuQtO1wtZ08uHpmmMfgsMdO0g/a5VuQHmqjoqHywmfrc161/Kv1KcgcdfppsNKoa2qqg/MCqVje61enztABlJZ8tiKM3hILzVXO9/jXWkenrNwcBlPP9NaKyE43KmD1cJU6Wfnei0sKgbfltfeyb9Sn9JNv9/Tvpl76aO10gaFNrB9wcQNMjRLOumUaz9OplTyod7jhFucJJhjP9d7siY2qZMf5VqrhwSHOxPPO/tN/WphoTzYzGwrLC58zn/Kf6GaQ4X6VTOrbvrbllNO7XuL1Uf/Udr00YHNqD7n3kRuYhBUaRoL7EpNFPtcL2n9dsTFN9qXuVZMWTXcJm/ZMJVWQHC4EwerDbZaWCkfpJOuLO5DfCb/+xDvq9SnnL7bSqAYA8JfQrOAsFWa6qMPsf2/3zJTvjvetx+MmjGd9GrG69+ecZ3Ss5/vbo64iNdCpXmQUr9N/5Mv1Rr35xLB4TPBjTi4tJVCL6sN5+jkZzC8O3EfYqV8VhEHhb4MFF/GkvWuxUmc+wGhpX57+bfbAOhVvDanaek7+eA71mH1M/2bV2sF4z/i/Dk3a8qT0n8A1g/OQjYJ1kEAAAAASUVORK5CYII="

st.set_page_config(
    page_title="Bora Design // Suite Creative Cloud",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# CSS: ADOBE SPECTRUM DARK // CREATIVE CLOUD INDUSTRIAL STUDIO
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }

    /* Fondo Obsidian Studio Spectrum */
    .stApp {
        background-color: #121212 !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(230, 36, 56, 0.08) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(20, 115, 230, 0.08) 0px, transparent 50%),
            radial-gradient(at 50% 100%, rgba(18, 18, 18, 0.9) 0px, transparent 50%) !important;
        color: #E6E6E6 !important;
    }

    /* Contenedor compacto sin desbordes */
    .block-container {
        padding-top: 0.6rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 1280px !important;
    }

    /* Barra Superior Adobe Suite */
    .adobe-navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #1A1A1A;
        border: 1px solid #2B2B2B;
        border-radius: 8px;
        padding: 8px 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.45);
    }

    .adobe-nav-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .adobe-app-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #FF1744 0%, #B71C1C 100%);
        color: #FFFFFF;
        font-weight: 900;
        font-size: 0.88rem;
        border-radius: 6px;
        box-shadow: 0 2px 8px rgba(230, 36, 56, 0.4);
        letter-spacing: -0.04em;
    }

    .adobe-app-title {
        font-size: 0.92rem;
        font-weight: 800;
        color: #F5F5F5;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin: 0;
        line-height: 1.1;
    }

    .adobe-app-sub {
        font-size: 0.68rem;
        font-weight: 500;
        color: #8C8C8C;
        letter-spacing: 0.02em;
        margin: 0;
    }

    .adobe-suite-chips {
        display: flex;
        gap: 6px;
        align-items: center;
    }

    .adobe-chip {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.66rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        border: 1px solid transparent;
    }

    .chip-nest { background: rgba(20, 115, 230, 0.15); color: #4EA4F5; border-color: rgba(20, 115, 230, 0.35); }
    .chip-resto { background: rgba(245, 158, 11, 0.15); color: #FBBF24; border-color: rgba(245, 158, 11, 0.35); }
    .chip-cloud { background: rgba(38, 142, 108, 0.15); color: #34D399; border-color: rgba(38, 142, 108, 0.35); }

    .pulse-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: #22C55E;
        box-shadow: 0 0 6px #22C55E;
        animation: adobe-pulse 2s infinite ease-in-out;
    }

    @keyframes adobe-pulse {
        0% { transform: scale(0.9); opacity: 0.7; }
        50% { transform: scale(1.25); opacity: 1; }
        100% { transform: scale(0.9); opacity: 0.7; }
    }

    /* Adobe CC Workspace KPI Tiles */
    .adobe-kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
        margin-bottom: 12px;
    }

    .adobe-kpi-card {
        background: #181818;
        border: 1px solid #282828;
        border-radius: 6px;
        padding: 10px 14px;
        position: relative;
        overflow: hidden;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }

    .adobe-kpi-card:hover {
        border-color: #383838;
        transform: translateY(-1px);
    }

    .adobe-kpi-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
    }

    .kpi-blue::before { background: #1473E6; }
    .kpi-green::before { background: #22C55E; }
    .kpi-amber::before { background: #F59E0B; }
    .kpi-crimson::before { background: #E62438; }

    .adobe-kpi-label {
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #8C8C8C;
        margin-bottom: 2px;
    }

    .adobe-kpi-val {
        font-size: 1.45rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.1;
        font-feature-settings: "tnum" 1;
    }

    .adobe-kpi-sub {
        font-size: 0.68rem;
        font-weight: 500;
        color: #6E6E6E;
    }

    /* Adobe Inspector Panel Cards */
    .adobe-seat-card {
        background: #181818;
        border: 1px solid #282828;
        border-radius: 8px;
        padding: 12px 14px;
        margin-bottom: 10px;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
        position: relative;
    }

    .adobe-seat-card:hover {
        border-color: #383838;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    }

    .adobe-seat-card.card-activa { border-left: 3px solid #22C55E; }
    .adobe-seat-card.card-bloqueada { border-left: 3px solid #E62438; }
    .adobe-seat-card.card-vencida { border-left: 3px solid #F59E0B; }

    .adobe-card-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 6px;
    }

    .adobe-seat-title {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .adobe-prod-badge {
        display: inline-block;
        padding: 1px 6px;
        font-size: 0.65rem;
        font-weight: 800;
        border-radius: 4px;
        background: #1473E6;
        color: #FFFFFF;
        letter-spacing: 0.04em;
    }

    .adobe-seat-name {
        font-size: 0.95rem;
        font-weight: 700;
        color: #FFFFFF;
    }

    .adobe-prop-row {
        font-size: 0.75rem;
        color: #A3A3A3;
        margin-bottom: 6px;
    }

    .adobe-mono-box {
        font-family: 'JetBrains Mono', Consolas, monospace;
        font-size: 0.76rem;
        font-weight: 600;
        background: #111111;
        border: 1px solid #242424;
        border-radius: 5px;
        padding: 4px 8px;
        color: #58A6FF;
        letter-spacing: 0.04em;
        margin: 3px 0;
        word-break: break-all;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .adobe-mono-key {
        color: #34D399 !important;
        border-color: #164E37 !important;
        background: #0B1C14 !important;
    }

    /* Pestañas estilo Adobe Spectrum Panel Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #161616 !important;
        border: 1px solid #282828 !important;
        border-radius: 6px !important;
        padding: 3px !important;
        gap: 3px !important;
        margin-bottom: 12px !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #9E9E9E !important;
        background: transparent !important;
        border-radius: 4px !important;
        font-weight: 600 !important;
        font-size: 0.78rem !important;
        padding: 6px 12px !important;
        border: none !important;
        transition: all 0.15s ease !important;
    }

    .stTabs [aria-selected="true"] {
        color: #FFFFFF !important;
        background-color: #262626 !important;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.4) !important;
    }

    /* Botones Estilo Adobe CC */
    .stButton>button {
        background: #242424 !important;
        color: #E6E6E6 !important;
        font-weight: 600 !important;
        font-size: 0.78rem !important;
        border-radius: 5px !important;
        border: 1px solid #363636 !important;
        padding: 5px 10px !important;
        min-height: 34px !important;
        transition: all 0.15s ease !important;
    }

    .stButton>button:hover {
        background: #2E2E2E !important;
        border-color: #4A4A4A !important;
        color: #FFFFFF !important;
        transform: translateY(-1px) !important;
    }

    .stButton>button:active {
        transform: translateY(0) !important;
    }

    /* Botones primarios Adobe Accent */
    .btn-adobe-primary button {
        background: linear-gradient(180deg, #E62438 0%, #C41829 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid #FF4D5E !important;
        box-shadow: 0 2px 8px rgba(230, 36, 56, 0.3) !important;
    }

    .btn-adobe-primary button:hover {
        background: linear-gradient(180deg, #FF3347 0%, #D81C2E 100%) !important;
        box-shadow: 0 4px 12px rgba(230, 36, 56, 0.5) !important;
    }

    /* Inputs estilo Adobe Dark */
    .stTextInput>div>div>input, .stSelectbox>div>div, .stTextArea textarea, .stNumberInput input {
        background-color: #141414 !important;
        color: #F0F0F0 !important;
        border: 1px solid #2B2B2B !important;
        border-radius: 5px !important;
        font-size: 0.82rem !important;
    }

    .stTextInput>div>div>input:focus, .stTextArea textarea:focus {
        border-color: #1473E6 !important;
        box-shadow: 0 0 0 1px #1473E6 !important;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .adobe-kpi-grid {
            grid-template-columns: repeat(2, 1fr) !important;
        }
        .adobe-suite-chips {
            display: none !important;
        }
        .adobe-app-title {
            font-size: 0.82rem !important;
        }
        .block-container {
            padding-left: 0.4rem !important;
            padding-right: 0.4rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# LOGIN SEGURO CON HMAC
# ------------------------------------------------------------------------------
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "intentos_fallidos" not in st.session_state:
    st.session_state.intentos_fallidos = 0
if "bloqueado_hasta" not in st.session_state:
    st.session_state.bloqueado_hasta = 0.0

if not st.session_state.autenticado:
    _, col_login, _ = st.columns([1, 1.8, 1])
    with col_login:
        st.markdown(f"""
            <div style="background: #181818; border: 1px solid #2B2B2B; border-radius: 10px; padding: 24px; text-align: center; margin-top: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
                <div style="display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; background: linear-gradient(135deg, #FF1744 0%, #B71C1C 100%); color: #FFF; font-weight: 900; font-size: 1.15rem; border-radius: 8px; margin-bottom: 12px; box-shadow: 0 4px 14px rgba(230,36,56,0.4);">
                    Bo
                </div>
                <h3 style="margin: 0 0 4px 0; font-weight: 800; color: #FFFFFF; font-size: 1.15rem; letter-spacing: 0.04em;">BORA DESIGN CREATIVE CLOUD</h3>
                <p style="color: #8C8C8C; font-size: 0.75rem; margin-bottom: 18px;">Centro Maestro de Licenciamiento y Telemetría Industrial</p>
                <div style="height: 1px; background: #262626; margin-bottom: 18px;"></div>
            </div>
        """, unsafe_allow_html=True)

        ahora_login = time.time()
        if ahora_login < st.session_state.bloqueado_hasta:
            restante = int(st.session_state.bloqueado_hasta - ahora_login)
            st.error(f"Acceso bloqueado por seguridad ({restante}s restantes).")
            st.stop()

        pwd = st.text_input("Credencial Maestra de Administrador", type="password", placeholder="••••••••••••")
        if st.button("ACCEDER A LA SUITE", use_container_width=True):
            if hmac.compare_digest(pwd.encode("utf-8"), CLAVE_ADMINISTRADOR.encode("utf-8")):
                st.session_state.autenticado = True
                st.session_state.intentos_fallidos = 0
                st.rerun()
            else:
                st.session_state.intentos_fallidos += 1
                if st.session_state.intentos_fallidos >= MAX_INTENTOS_LOGIN:
                    st.session_state.bloqueado_hasta = time.time() + SEGUNDOS_BLOQUEO_LOGIN
                    st.session_state.intentos_fallidos = 0
                    st.error(f"Demasiados intentos fallidos. Bloqueado temporalmente por {SEGUNDOS_BLOQUEO_LOGIN}s.")
                else:
                    rest = MAX_INTENTOS_LOGIN - st.session_state.intentos_fallidos
                    st.error(f"Credencial incorrecta ({rest} intentos restantes).")
    st.stop()

# ------------------------------------------------------------------------------
# SERVICIO CRIPTOGRÁFICO Y GESTOR FIREBASE CON TOKEN RESISTENTE
# ------------------------------------------------------------------------------
def obtener_token_firebase():
    """Recupera el token secreto para autenticar escrituras en Firebase RTDB."""
    # 1. Intentar desde st.secrets de Streamlit Community Cloud
    try:
        if hasattr(st, "secrets"):
            if "BORA_FIREBASE_AUTH" in st.secrets:
                return str(st.secrets["BORA_FIREBASE_AUTH"]).strip()
            if "BORA_FIREBASE_SECRET" in st.secrets:
                return str(st.secrets["BORA_FIREBASE_SECRET"]).strip()
    except Exception:
        pass

    # 2. Intentar desde variables de entorno
    token = os.environ.get("BORA_FIREBASE_AUTH", os.environ.get("BORA_FIREBASE_SECRET", "")).strip()
    if token:
        return token

    # 3. Intentar desde archivos locales candidatos
    candidatos = [
        "admin_secret.txt",
        "firebase_secret.key",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "admin_secret.txt"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "firebase_secret.key"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "admin_secret.txt"),
    ]
    for f_sec in candidatos:
        if f_sec and os.path.isfile(f_sec):
            try:
                with open(f_sec, "r", encoding="utf-8") as _f:
                    t = _f.read().strip()
                    if t:
                        return t
            except Exception:
                pass

    # 4. Fallback maestro del sistema (garantiza que boradesign.streamlit.app nunca devuelva 401)
    return FIREBASE_SECRET_DEFAULT


def peticion_firebase(metodo, ruta, datos=None, timeout=8):
    """Realiza una petición HTTP REST autenticada a Firebase Realtime Database."""
    base = FIREBASE_URL.rstrip('/')
    url = f"{base}/{ruta}.json"
    token = obtener_token_firebase()
    if token:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}auth={token}"

    body = json.dumps(datos).encode("utf-8") if datos is not None else None
    req = urllib.request.Request(url, data=body, method=metodo, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as he:
        # Registrar y propagar error para visibilidad
        msg_err = f"Firebase HTTP Error {he.code}: {he.reason}"
        st.session_state["ultimo_error_firebase"] = msg_err
        raise RuntimeError(msg_err) from he
    except Exception as e:
        st.session_state["ultimo_error_firebase"] = str(e)
        raise e


def generar_clave_firmada_universal(hwid_cliente, dias_vigencia=30):
    """Genera clave en formato Universal de 4 Bloques (XXXX-XXXX-XXXX-XXXX). Compatible con el 100% de clientes."""
    hwid_limpio = hwid_cliente.strip().upper()
    dia_actual_utc = int(time.time() // 86400)
    dia_vencimiento = dia_actual_utc + int(dias_vigencia)
    offset_dias = max(1, min(65535, dia_vencimiento - EPOCA_BASE_DIAS))
    hex_vencimiento = f"{offset_dias:04X}"
    hex_salt = f"{int(time.time() * 10) & 0xFFFF:04X}"

    mensaje = f"{hwid_limpio}|{hex_vencimiento}|{hex_salt}".encode("utf-8")
    firma = hmac.new(SECRETO_MAESTRO_BORA, mensaje, hashlib.sha256).hexdigest().upper()
    clave_4b = f"{hex_vencimiento}-{hex_salt}-{firma[0:4]}-{firma[4:8]}"
    return clave_4b, dia_vencimiento


def generar_clave_firmada_v3(hwid_cliente, dias_vigencia=30, producto="NEST"):
    """Genera clave en formato V3 de 5 Bloques (PROD-XXXX-XXXX-XXXX-XXXX) para instalaciones modernas."""
    hwid_limpio = hwid_cliente.strip().upper()
    dia_actual_utc = int(time.time() // 86400)
    dia_vencimiento = dia_actual_utc + int(dias_vigencia)
    offset_dias = max(1, min(65535, dia_vencimiento - EPOCA_BASE_DIAS))
    hex_vencimiento = f"{offset_dias:04X}"
    hex_salt = f"{int(time.time() * 10) & 0xFFFF:04X}"
    prod = str(producto or "NEST").strip().upper()

    mensaje = f"{prod}|{hwid_limpio}|{hex_vencimiento}|{hex_salt}".encode("utf-8")
    firma = hmac.new(SECRETO_MAESTRO_BORA, mensaje, hashlib.sha256).hexdigest().upper()
    clave_5b = f"{prod}-{hex_vencimiento}-{hex_salt}-{firma[0:4]}-{firma[4:8]}"
    return clave_5b, dia_vencimiento


def extraer_dia_vencimiento_de_clave(clave_str):
    """Extrae el día de vencimiento absoluto en formato días epoch."""
    try:
        partes = str(clave_str).strip().upper().split("-")
        if len(partes) == 5 and len(partes[1]) == 4:
            return EPOCA_BASE_DIAS + int(partes[1], 16)
        if len(partes) == 4 and len(partes[0]) == 4:
            return EPOCA_BASE_DIAS + int(partes[0], 16)
    except Exception:
        pass
    return 0


def detectar_formato_clave(clave_str):
    """Detecta si una clave es de 4 bloques (Universal) o 5 bloques (Suite V3)."""
    partes = str(clave_str or "").strip().upper().split("-")
    if len(partes) == 5:
        return "5b"
    return "4b"


def detectar_producto_de_equipo_o_clave(info_equipo):
    """Detecta el módulo de software asociado al equipo."""
    if isinstance(info_equipo, dict):
        p = str(info_equipo.get("producto") or "").strip().upper()
        if p in ("NEST", "REST", "BORA", "SUITE"):
            return p
        c = str(info_equipo.get("clave") or "").strip().upper()
        if c.startswith("REST-"): return "REST"
        if c.startswith("NEST-"): return "NEST"
        if c.startswith("BORA-") or c.startswith("SUITE-"): return "BORA"
    return "NEST"


def redactar_mensaje_whatsapp(destinatario, dias_rest, pc_nom, hwid, clave_activa=""):
    """Genera mensaje formal y profesional para enviar por WhatsApp al cliente."""
    saludo = f"¡Hola, {destinatario}!" if destinatario else "¡Hola!"
    estado = f"vence en *{dias_rest} día(s)*" if dias_rest > 0 else "se encuentra actualmente *VENCIDA*"
    equipo_info = f" ({pc_nom})" if pc_nom else f" ({hwid})"
    
    bloque_clave = ""
    if clave_activa and clave_activa != "---":
        bloque_clave = f"\n\n🔑 *Tu Clave de Activación Oficial:*\n`{clave_activa}`\n_(Cópiala y pégala en la ventana de Bora Design en tu PC)_"

    return (
        f"{saludo}\n\n"
        f"Te saludamos del equipo de soporte de *Bora Design*.\n"
        f"Te confirmamos que tu licencia de *Bora Design NestPro*{equipo_info} {estado}.{bloque_clave}\n\n"
        f"Para cualquier consulta técnica o renovación de bobina, estamos atentos para asistirte de inmediato.\n\n"
        f"¡Gracias por optimizar tu producción con Bora Design!"
    )

# ------------------------------------------------------------------------------
# SINCRONIZACIÓN DE DATOS CLOUD EN TIEMPO REAL
# ------------------------------------------------------------------------------
try:
    raw_equipos = peticion_firebase("GET", "equipos") or {}
    equipos_data = raw_equipos if isinstance(raw_equipos, dict) else {}
    sync_ok = True
except Exception as e:
    equipos_data = {}
    sync_ok = False
    st.sidebar.error(f"Falla de sincronización Firebase: {e}")

ahora_ts = int(time.time())
dia_hoy = int(ahora_ts // 86400)
hora_actual_str = time.strftime("%H:%M:%S")

total_pcs = len(equipos_data)
online_pcs = sum(
    1 for v in equipos_data.values()
    if isinstance(v, dict) and int(v.get("ultimo_ping", 0)) > 0 and (ahora_ts - int(v.get("ultimo_ping", 0))) <= 75
)
activas_pcs = sum(
    1 for v in equipos_data.values()
    if isinstance(v, dict) and not v.get("bloqueado", False) and int(v.get("dia_vencimiento", 0)) > dia_hoy
)
atencion_pcs = sum(
    1 for v in equipos_data.values()
    if isinstance(v, dict) and (
        v.get("bloqueado", False)
        or int(v.get("dia_vencimiento", 0)) <= dia_hoy
        or (0 < int(v.get("dia_vencimiento", 0)) - dia_hoy <= 5)
    )
)

# ------------------------------------------------------------------------------
# NAVBAR SUPERIOR ADOBE SUITE // CREATIVE CLOUD HEADER
# ------------------------------------------------------------------------------
col_nav_brand, col_nav_act = st.columns([4, 1.2])

with col_nav_brand:
    st.markdown(f"""
        <div class="adobe-navbar">
            <div class="adobe-nav-left">
                <div class="adobe-app-badge">Bo</div>
                <div>
                    <div class="adobe-app-title">BORA DESIGN // CREATIVE CLOUD CONSOLE</div>
                    <div class="adobe-app-sub">Adobe Suite Architecture • Multi-Tenant License Server</div>
                </div>
                <div class="adobe-suite-chips">
                    <span class="adobe-chip chip-nest">NP NestPro</span>
                    <span class="adobe-chip chip-resto">RP RestoPro</span>
                    <span class="adobe-chip chip-cloud">
                        <span class="pulse-dot"></span>
                        <span>Cloud RTDB</span>
                    </span>
                </div>
            </div>
            <div style="font-size: 0.72rem; color: #8C8C8C; font-weight: 600;">
                <span>{hora_actual_str} UTC</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_nav_act:
    col_rf, col_so = st.columns(2)
    with col_rf:
        if st.button("🔄 Sync", help="Sincronizar datos en tiempo real", use_container_width=True):
            st.rerun()
    with col_so:
        if st.button("🚪 Salir", help="Cerrar sesión de administrador", use_container_width=True):
            st.session_state.autenticado = False
            st.rerun()

# ------------------------------------------------------------------------------
# ADOBE CC BENTO METRICS (4 TILES DE PRECISIÓN)
# ------------------------------------------------------------------------------
st.markdown(f"""
    <div class="adobe-kpi-grid">
        <div class="adobe-kpi-card kpi-blue">
            <div class="adobe-kpi-label">Licencias Registradas</div>
            <div class="adobe-kpi-val" style="color: #58A6FF;">{total_pcs}</div>
            <div class="adobe-kpi-sub">Total de Equipos HWID</div>
        </div>
        <div class="adobe-kpi-card kpi-green">
            <div class="adobe-kpi-label">Suscripciones Activas</div>
            <div class="adobe-kpi-val" style="color: #34D399;">{activas_pcs}</div>
            <div class="adobe-kpi-sub">Acceso total habilitado</div>
        </div>
        <div class="adobe-kpi-card kpi-amber">
            <div class="adobe-kpi-label">Equipos en Producción</div>
            <div class="adobe-kpi-val" style="color: #FBBF24;">{online_pcs}</div>
            <div class="adobe-kpi-sub">Ping activo &le;75 seg</div>
        </div>
        <div class="adobe-kpi-card kpi-crimson">
            <div class="adobe-kpi-label">Requieren Atención</div>
            <div class="adobe-kpi-val" style="color: #FDA4AF;">{atencion_pcs}</div>
            <div class="adobe-kpi-sub">&le;5 días o pausadas</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PESTAÑAS PRINCIPALES DEL WORKSPACE ADOBE
# ------------------------------------------------------------------------------
tab_asientos, tab_activador, tab_inventario, tab_telemetria, tab_comunicados, tab_seguridad, tab_ota = st.tabs([
    "🖥️ Equipos (Seats)",
    "⚡ Activar Licencia (Foundry)",
    "📋 Inventario Global",
    "📊 Telemetría y Ahorro",
    "📢 Difusión Corel (Broadcast)",
    "🛡️ Kill-Switch & Seguridad",
    "🚀 Actualizaciones OTA"
])

todos_talleres = sorted(list({
    str(v.get("taller", "")).strip() for v in equipos_data.values()
    if isinstance(v, dict) and str(v.get("taller", "")).strip() and str(v.get("taller", "")).strip() != "Sin asignar"
} | set(PRESETS_ETIQUETAS)))

# ==============================================================================
# TAB 1: GESTIÓN DE EQUIPOS (ADOBE SEATS INSPECTOR)
# ==============================================================================
with tab_asientos:
    col_s1, col_s2, col_s3 = st.columns([2, 1.2, 1.2])
    with col_s1:
        busqueda_txt = st.text_input("Buscar", placeholder="Filtrar por HWID, Taller, Operador, PC...", label_visibility="collapsed").strip().lower()
    with col_s2:
        filtro_estado = st.selectbox(
            "Estado",
            ["Todos los Estados", "🟢 En Producción (Online)", "⚠️ Por Vencer (≤5d)", "🚫 Pausadas / Vencidas"],
            label_visibility="collapsed"
        )
    with col_s3:
        filtro_taller = st.selectbox(
            "Taller",
            ["Todos los Talleres"] + todos_talleres + ["Sin asignar"],
            label_visibility="collapsed"
        )

    equipos_filtrados = {}
    for hwid, info in sorted(equipos_data.items()):
        if not isinstance(info, dict):
            continue

        taller = str(info.get("taller", "")).strip() or "Sin asignar"
        cliente = str(info.get("cliente", "")).strip() or "Sin asignar"
        pc = str(info.get("pc_nombre", "")).strip()
        bloqueado = bool(info.get("bloqueado", False))
        dia_venc = int(info.get("dia_vencimiento", 0))
        ultimo_ts = int(info.get("ultimo_ping", 0))

        en_linea = (ahora_ts - ultimo_ts) <= 75 if ultimo_ts > 0 else False
        dias_rest = max(0, dia_venc - dia_hoy) if dia_venc > 0 else 0

        if busqueda_txt:
            corpus = f"{hwid} {taller} {cliente} {pc}".lower()
            if busqueda_txt not in corpus:
                continue

        if filtro_estado == "🟢 En Producción (Online)" and not en_linea:
            continue
        elif filtro_estado == "⚠️ Por Vencer (≤5d)" and not (not bloqueado and 0 < dias_rest <= 5):
            continue
        elif filtro_estado == "🚫 Pausadas / Vencidas" and not (bloqueado or dias_rest == 0):
            continue

        if filtro_taller != "Todos los Talleres":
            if filtro_taller == "Sin asignar" and taller != "Sin asignar":
                continue
            elif filtro_taller != "Sin asignar" and taller.lower() != filtro_taller.lower():
                continue

        equipos_filtrados[hwid] = info

    if not equipos_filtrados:
        st.info("No se encontraron equipos bajo los criterios de búsqueda.")
    else:
        st.caption(f"Mostrando **{len(equipos_filtrados)}** de **{total_pcs}** licencias asignadas.")

        for hwid, info in equipos_filtrados.items():
            taller = str(info.get("taller", "")).strip() or "Sin asignar"
            cliente = str(info.get("cliente", "")).strip() or "Sin asignar"
            pc = info.get("pc_nombre", "PC")
            usuario_win = info.get("usuario_pc", "")
            bloqueado = bool(info.get("bloqueado", False))
            dia_venc = int(info.get("dia_vencimiento", 0))
            clave_act = info.get("clave", "---") or "---"
            ultimo_ts = int(info.get("ultimo_ping", 0))
            prod_nom = detectar_producto_de_equipo_o_clave(info)
            formato_actual = detectar_formato_clave(clave_act)

            en_linea = (ahora_ts - ultimo_ts) <= 75 if ultimo_ts > 0 else False
            dias_rest = max(0, dia_venc - dia_hoy) if dia_venc > 0 else 0

            if bloqueado:
                card_cls = "card-bloqueada"
                badge_lic = "<span class='adobe-chip' style='background: rgba(230,36,56,0.18); color: #FDA4AF; border-color: rgba(230,36,56,0.4);'>🚫 SUSPENDIDA</span>"
                vig_txt = f"<span style='color: #FDA4AF; font-weight: 700;'>Pausada temporalmente</span>"
            elif dias_rest > 0:
                card_cls = "card-activa"
                col_c = "#34D399" if dias_rest > 5 else "#FBBF24"
                badge_lic = "<span class='adobe-chip' style='background: rgba(34,197,94,0.18); color: #34D399; border-color: rgba(34,197,94,0.4);'>✔ ACTIVA</span>"
                vig_txt = f"<span style='color: {col_c}; font-weight: 700;'>{dias_rest} día(s) restantes</span>"
            else:
                card_cls = "card-vencida"
                badge_lic = "<span class='adobe-chip' style='background: rgba(245,158,11,0.18); color: #FBBF24; border-color: rgba(245,158,11,0.4);'>⏳ VENCIDA</span>"
                vig_txt = "<span style='color: #FBBF24; font-weight: 700;'>0 días (Requiere renovación)</span>"

            badge_online = "<span class='adobe-chip chip-cloud'>🟢 ONLINE</span>" if en_linea else "<span class='adobe-chip' style='background: rgba(100,116,139,0.15); color: #94A3B8; border-color: rgba(100,116,139,0.3);'>⚫ OFFLINE</span>"
            tag_formato = "<span style='font-size: 0.65rem; color: #34D399; background: #064E3B; padding: 2px 5px; border-radius: 3px;'>4B Universal</span>" if formato_actual == "4b" else "<span style='font-size: 0.65rem; color: #60A5FA; background: #1E3A8A; padding: 2px 5px; border-radius: 3px;'>5B Suite</span>"

            st.markdown(f"""
                <div class="adobe-seat-card {card_cls}">
                    <div class="adobe-card-top">
                        <div class="adobe-seat-title">
                            <span class="adobe-prod-badge">{prod_nom}</span>
                            <span class="adobe-seat-name">{cliente}</span>
                            <span style="font-size: 0.70rem; color: #8C8C8C; background: #222; padding: 2px 6px; border-radius: 4px;">🏷️ {taller}</span>
                        </div>
                        <div style="display: flex; gap: 6px; align-items: center;">
                            {badge_online}
                            {badge_lic}
                        </div>
                    </div>
                    <div class="adobe-prop-row">
                        🖥️ Dispositivo: <b>{pc}</b> {f'({usuario_win})' if usuario_win else ''} • {vig_txt}
                    </div>
                    <div class="adobe-mono-box">
                        <span>HWID: {hwid}</span>
                        <span style="color: #8C8C8C; font-size: 0.68rem;">1-PC Binding</span>
                    </div>
                    <div class="adobe-mono-box adobe-mono-key">
                        <span>LICENCIA: {clave_act}</span>
                        {tag_formato}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Barra de Herramientas de Asiento (Adobe Toolbar)
            c_b1, c_b2, c_b3, c_b4, c_b5 = st.columns([1.3, 1.3, 1.1, 1.4, 0.6])

            with c_b1:
                if st.button("⚡ +30 Días (Auto)", key=f"btn_30_{hwid}", use_container_width=True):
                    try:
                        dia_base = max(dia_hoy, dia_venc)
                        total_nuevos = (dia_base - dia_hoy) + 30
                        # Generar clave en formato Universal (4 bloques) para garantizar compatibilidad con versiones cliente antiguas
                        nueva_cl, nuevo_venc = generar_clave_firmada_universal(hwid, total_nuevos)
                        peticion_firebase("PATCH", f"equipos/{hwid}", {
                            "clave": nueva_cl,
                            "producto": prod_nom,
                            "dia_vencimiento": nuevo_venc,
                            "bloqueado": False,
                            "clave_bloqueada": ""
                        })
                        st.toast(f"¡+30 días aplicados a {cliente}!", icon="⚡")
                        time.sleep(0.4)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al renovar: {e}")

            with c_b2:
                msg_wsp = redactar_mensaje_whatsapp(cliente if cliente != "Sin asignar" else taller, dias_rest, pc, hwid, clave_act)
                msg_enc = urllib.parse.quote(msg_wsp)
                link_wsp = f"https://api.whatsapp.com/send?text={msg_enc}"
                st.markdown(f"""
                    <a href="{link_wsp}" target="_blank" style="text-decoration: none;">
                        <button style="width: 100%; min-height: 34px; background: #064E3B; color: #34D399; font-weight: 700; font-size: 0.78rem; border: 1px solid #059669; border-radius: 5px; cursor: pointer;">
                            💬 WhatsApp
                        </button>
                    </a>
                """, unsafe_allow_html=True)

            with c_b3:
                if bloqueado:
                    if st.button("🔓 Reactivar", key=f"unb_{hwid}", use_container_width=True):
                        try:
                            v_rest = dia_venc
                            if v_rest <= dia_hoy and clave_act and clave_act != "---":
                                v_rest = extraer_dia_vencimiento_de_clave(clave_act)
                            if v_rest <= dia_hoy:
                                nueva_cl, nuevo_venc = generar_clave_firmada_universal(hwid, 30)
                                peticion_firebase("PATCH", f"equipos/{hwid}", {
                                    "bloqueado": False, "clave_bloqueada": "", "clave": nueva_cl, "dia_vencimiento": nuevo_venc
                                })
                            else:
                                peticion_firebase("PATCH", f"equipos/{hwid}", {
                                    "bloqueado": False, "clave_bloqueada": "", "dia_vencimiento": v_rest
                                })
                            st.toast("Equipo reactivado correctamente", icon="🔓")
                            time.sleep(0.4)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al desbloquear: {e}")
                else:
                    if st.button("🚫 Suspender", key=f"blk_{hwid}", use_container_width=True):
                        try:
                            peticion_firebase("PATCH", f"equipos/{hwid}", {"bloqueado": True, "clave_bloqueada": clave_act})
                            st.toast("Equipo suspendido", icon="🚫")
                            time.sleep(0.4)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al suspender: {e}")

            with c_b4:
                if st.button("🔄 Clave 4B (Fix)", key=f"c4b_{hwid}", help="Regenera y asegura clave Universal de 4 bloques compatible con todas las versiones del cliente", use_container_width=True):
                    try:
                        dias_fijos = max(3, dias_rest if dias_rest > 0 else 30)
                        nueva_cl_4b, nuevo_venc_4b = generar_clave_firmada_universal(hwid, dias_fijos)
                        peticion_firebase("PATCH", f"equipos/{hwid}", {
                            "clave": nueva_cl_4b,
                            "producto": prod_nom,
                            "dia_vencimiento": nuevo_venc_4b,
                            "bloqueado": False,
                            "clave_bloqueada": ""
                        })
                        st.toast(f"Clave Universal 4B generada: {nueva_cl_4b}", icon="🔑")
                        time.sleep(0.4)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al generar clave: {e}")

            with c_b5:
                with st.popover("⚙️"):
                    st.write(f"**Inspector:** `{cliente}`")
                    ed_tal = st.text_input("Taller:", value="" if taller == "Sin asignar" else taller, key=f"t_{hwid}")
                    ed_cli = st.text_input("Operador:", value="" if cliente == "Sin asignar" else cliente, key=f"c_{hwid}")
                    if st.button("Guardar Cambios", key=f"sv_{hwid}"):
                        peticion_firebase("PATCH", f"equipos/{hwid}", {
                            "taller": ed_tal.strip() or "Sin asignar",
                            "cliente": ed_cli.strip() or "Sin asignar"
                        })
                        st.rerun()

                    st.divider()
                    d_fij = st.number_input("Días de suscripción:", min_value=1, max_value=365, value=30, key=f"df_{hwid}")
                    if st.button("Asignar Días Exactos", key=f"bdf_{hwid}"):
                        cl_f, v_f = generar_clave_firmada_universal(hwid, d_fij)
                        peticion_firebase("PATCH", f"equipos/{hwid}", {
                            "clave": cl_f, "dia_vencimiento": v_f, "bloqueado": False, "clave_bloqueada": ""
                        })
                        st.rerun()

                    st.divider()
                    if st.button("🗑️ Eliminar Registro", key=f"del_{hwid}"):
                        peticion_firebase("DELETE", f"equipos/{hwid}")
                        st.rerun()

# ==============================================================================
# TAB 2: ACTIVADOR Y GENERADOR UNIVERSAL (LICENSE FOUNDRY)
# ==============================================================================
with tab_activador:
    st.markdown("#### ⚡ Generador de Claves y Activación Cloud Inmediata")
    st.markdown("Genera credenciales criptográficas universales compatibles con CorelDRAW 2017 a 2026 y activa el asiento en Firebase.")

    col_act1, col_act2 = st.columns([1.2, 1.2])

    with col_act1:
        sel_prod_reg = st.selectbox(
            "Módulo de Software (Producto):",
            ["NestPro (Industrial 2D)", "RestoPro (Patronaje)", "Suite Bora Completa"],
            index=0
        )
        nuevo_hwid = st.text_input("Hardware ID (HWID) del Cliente:", placeholder="BORA-XXXX-XXXX-XXXX").strip().upper()

        c_tal, c_cli = st.columns(2)
        with c_tal:
            sel_tal = st.selectbox("Taller / Empresa:", PRESETS_ETIQUETAS + ["Personalizado", "Sin asignar"])
            in_tal = st.text_input("Nombre de Taller:") if sel_tal == "Personalizado" else sel_tal
        with c_cli:
            in_cli = st.text_input("Operador / Diseñador:", placeholder="Ej: Manuel Monroy, Taller 1...").strip()

    with col_act2:
        tipo_formato = st.radio(
            "Formato de Clave Criptográfica:",
            [
                "Universal (4 Bloques: XXXX-XXXX-XXXX-XXXX) [RECOMENDADO - 100% COMPATIBLE]",
                "Suite V3 (5 Bloques: NEST-XXXX-XXXX-XXXX-XXXX) [Instalaciones v4.6+]"
            ],
            index=0
        )

        dias_reg = st.number_input("Días de Vigencia Oficial:", min_value=1, max_value=730, value=30)
        st.write("Presets Rápidos de Suscripción:")
        cd1, cd2, cd3, cd4 = st.columns(4)
        with cd1:
            if st.button("7d Demo"): dias_reg = 7
        with cd2:
            if st.button("15d Quincenal"): dias_reg = 15
        with cd3:
            if st.button("30d Mensual"): dias_reg = 30
        with cd4:
            if st.button("365d Anual"): dias_reg = 365

        auto_nube = st.checkbox("Sincronizar y autorizar automáticamente en Firebase Cloud", value=True)

    st.markdown("---")
    if st.button("⚡ GENERAR LICENCIA Y REGISTRAR EN LA NUBE", use_container_width=True):
        if not nuevo_hwid.startswith("BORA-") or len(nuevo_hwid) < 15:
            st.error("Error: El formato de Hardware ID es inválido. Debe comenzar por 'BORA-' y contener al menos 15 caracteres (Ej: BORA-FBD1-BB9B-E6C1).")
        else:
            try:
                prod_cod = "NEST" if "NestPro" in sel_prod_reg else ("REST" if "RestoPro" in sel_prod_reg else "BORA")
                es_universal = "Universal" in tipo_formato

                if es_universal:
                    cl_generada, venc_ts = generar_clave_firmada_universal(nuevo_hwid, int(dias_reg))
                else:
                    cl_generada, venc_ts = generar_clave_firmada_v3(nuevo_hwid, int(dias_reg), producto=prod_cod)

                if auto_nube:
                    peticion_firebase("PATCH", f"equipos/{nuevo_hwid}", {
                        "taller": in_tal or "Sin asignar",
                        "cliente": in_cli or "Sin asignar",
                        "producto": prod_cod,
                        "clave": cl_generada,
                        "dia_vencimiento": venc_ts,
                        "bloqueado": False,
                        "clave_bloqueada": "",
                        "fecha_registro": int(time.time())
                    })

                fecha_venc_str = datetime.datetime.fromtimestamp(venc_ts * 86400).strftime("%d/%m/%Y")
                st.success(f"¡Licencia generada con éxito para {in_cli or nuevo_hwid}! Vence el {fecha_venc_str} ({dias_reg} días).")

                st.markdown(f"""
                    <div style="background: #0B1C14; border: 1px solid #164E37; border-radius: 8px; padding: 16px; margin: 12px 0;">
                        <div style="font-size: 0.70rem; color: #8C8C8C; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;">CLAVE OFICIAL GENERADA:</div>
                        <div style="font-family: 'JetBrains Mono', Consolas, monospace; font-size: 1.25rem; font-weight: 800; color: #34D399; letter-spacing: 0.06em;">
                            {cl_generada}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                st.code(cl_generada, language="text")

                # WhatsApp directo
                msg_wsp = redactar_mensaje_whatsapp(in_cli, int(dias_reg), "PC", nuevo_hwid, cl_generada)
                link_wsp = f"https://api.whatsapp.com/send?text={urllib.parse.quote(msg_wsp)}"
                st.markdown(f"""
                    <a href="{link_wsp}" target="_blank" style="text-decoration: none;">
                        <button style="width: 100%; min-height: 40px; background: #064E3B; color: #34D399; font-weight: 700; font-size: 0.85rem; border: 1px solid #059669; border-radius: 6px; cursor: pointer; margin-top: 8px;">
                            💬 Enviar Clave a WhatsApp del Cliente
                        </button>
                    </a>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error durante la generación o sincronización: {e}")

# ==============================================================================
# TAB 3: INVENTARIO GLOBAL TABULAR
# ==============================================================================
with tab_inventario:
    st.markdown("#### 📋 Catálogo Completo de Asientos y Equipos")
    filas_t = []
    for hwid, info in sorted(equipos_data.items()):
        if not isinstance(info, dict):
            continue
        taller = str(info.get("taller", "")).strip() or "Sin asignar"
        cliente = str(info.get("cliente", "")).strip() or "Sin asignar"
        pc = info.get("pc_nombre", "PC")
        bloqueado = bool(info.get("bloqueado", False))
        dia_venc = int(info.get("dia_vencimiento", 0))
        clave_act = info.get("clave", "---") or "---"
        ultimo_ts = int(info.get("ultimo_ping", 0))

        en_linea = (ahora_ts - ultimo_ts) <= 75 if ultimo_ts > 0 else False
        dias_rest = max(0, dia_venc - dia_hoy) if dia_venc > 0 else 0
        ult_ping_str = datetime.datetime.fromtimestamp(ultimo_ts).strftime("%d/%m %H:%M") if ultimo_ts > 0 else "Nunca"

        if bloqueado:
            est_txt = "🚫 SUSPENDIDA"
        elif dias_rest > 0:
            est_txt = f"✔ ACTIVA ({dias_rest}d)"
        else:
            est_txt = "⏳ VENCIDA"

        filas_t.append({
            "HWID": hwid,
            "Taller": taller,
            "Usuario": cliente,
            "PC": pc,
            "Conexión": "🟢 Online" if en_linea else "⚫ Offline",
            "Estado": est_txt,
            "Días": dias_rest,
            "Último Ping": ult_ping_str,
            "Clave": clave_act
        })

    if filas_t:
        st.dataframe(filas_t, use_container_width=True, hide_index=True)
    else:
        st.info("No se registran datos en la base de datos de Firebase.")

# ==============================================================================
# TAB 4: TELEMETRÍA Y AHORRO TEXTIL
# ==============================================================================
with tab_telemetria:
    st.markdown("#### 📊 Análisis de Producción Textil y Retorno de Inversión")
    st.markdown("Telemetría en tiempo real recibida directamente desde los montajes efectuados en CorelDRAW.")

    try:
        data_tel = peticion_firebase("GET", "telemetria") or {}
    except Exception:
        data_tel = {}

    tot_metros = 0.0
    tot_ahorro = 0.0
    tot_piezas = 0
    filas_tel = []

    for hw, v in data_tel.items():
        if isinstance(v, dict):
            m = float(v.get("total_metros", 0.0))
            ah = float(v.get("total_ahorro_metros", 0.0))
            pz = int(v.get("total_piezas", 0))
            tot_metros += m
            tot_ahorro += ah
            tot_piezas += pz
            t_nom = v.get("taller", equipos_data.get(hw, {}).get("taller", "Sin asignar"))
            pc_nom = v.get("pc_nombre", equipos_data.get(hw, {}).get("pc_nombre", hw[:8]))
            ef_str = f"{float(v.get('ultimo_aprovechamiento', 0.0)):.1f}%" if v.get("ultimo_aprovechamiento") else "—"
            u_ts = int(v.get("ultimo_montaje_fecha", 0))
            u_str = datetime.datetime.fromtimestamp(u_ts).strftime("%d/%m %H:%M") if u_ts > 0 else "—"

            filas_tel.append({
                "Taller": t_nom,
                "Dispositivo": pc_nom,
                "HWID": hw,
                "Metros Procesados": f"{m:.2f} m",
                "Metros Ahorrados": f"{ah:.2f} m",
                "Prendas Anidadas": pz,
                "Eficiencia Promedio": ef_str,
                "Última Actividad": u_str
            })

    c_m1, c_m2, c_m3, c_m4 = st.columns(4)
    with c_m1:
        st.metric("Metraje Procesado", f"{tot_metros:.2f} m")
    with c_m2:
        st.metric("Tela Ahorrada", f"{tot_ahorro:.2f} m", delta="Optimización Bobina")
    with c_m3:
        st.metric("Prendas Montadas", f"{tot_piezas} uds")
    with c_m4:
        st.metric("Ahorro Estimado (USD)", f"${tot_ahorro * 3.0:.1f} USD", delta="ROI Taller")

    st.markdown("---")
    st.markdown("##### 🏭 Producción por Taller Conectado:")
    if filas_tel:
        st.dataframe(filas_tel, use_container_width=True, hide_index=True)
    else:
        st.info("Aún no se ha registrado telemetría de corte en los talleres.")

# ==============================================================================
# TAB 5: DIFUSIÓN COREL (BROADCAST ANNOUNCEMENTS)
# ==============================================================================
with tab_comunicados:
    st.markdown("#### 📢 Transmisor de Comunicados a CorelDRAW")
    st.markdown("Emite ventanas emergentes oficiales que aparecen instantáneamente en la interfaz de los talleres.")

    try:
        an_actual = peticion_firebase("GET", "anuncios/general") or {}
    except Exception:
        an_actual = {}

    if an_actual.get("activo"):
        st.success(f"🟢 **COMUNICADO ACTIVO EN LA NUBE:**\n\n**{an_actual.get('titulo', 'Aviso')}**: {an_actual.get('mensaje', '')}")
        if st.button("❌ RETIRAR COMUNICADO DE TODAS LAS PANTALLAS", use_container_width=True):
            peticion_firebase("PUT", "anuncios/general", {"activo": False, "mensaje": "", "fecha": int(time.time())})
            st.warning("El comunicado ha sido desactivado en la nube.")
            st.rerun()
    else:
        st.info("○ No hay comunicados activos en este momento.")

    with st.form("form_anuncio_central"):
        tit_an = st.text_input("Título del Comunicado:", value=an_actual.get("titulo", "Aviso de Bora Design"))
        msg_an = st.text_area("Cuerpo del Mensaje (se mostrará al iniciar CorelDRAW):", value=an_actual.get("mensaje", ""))
        
        if st.form_submit_button("📢 TRANSMITIR A TODOS LOS TALLERES EN TIEMPO REAL", use_container_width=True):
            if msg_an.strip():
                ts = int(time.time())
                peticion_firebase("PUT", "anuncios/general", {
                    "activo": True,
                    "titulo": tit_an.strip(),
                    "mensaje": msg_an.strip(),
                    "fecha": ts,
                    "id": str(ts)
                })
                st.success("¡Comunicado emitido a todas las pantallas!")
                st.rerun()
            else:
                st.error("Por favor ingresa un mensaje válido.")

# ==============================================================================
# TAB 6: SEGURIDAD Y KILL-SWITCH
# ==============================================================================
with tab_seguridad:
    st.markdown("#### 🛡️ Centro de Control de Integridad y Kill-Switch")
    st.markdown("Monitorea intentos de alteración de reloj y permite el corte inmediato de licencias.")

    try:
        alertas_data = peticion_firebase("GET", "alertas_seguridad") or {}
    except Exception:
        alertas_data = {}

    filas_al = []
    for k, v in alertas_data.items():
        if isinstance(v, dict):
            f_ts = int(v.get("fecha", 0))
            f_str = datetime.datetime.fromtimestamp(f_ts).strftime("%d/%m/%Y %H:%M") if f_ts > 0 else "—"
            filas_al.append({
                "Fecha": f_str,
                "Tipo de Alerta": v.get("tipo", "SEGURIDAD"),
                "HWID": v.get("hwid", k),
                "Dispositivo": v.get("pc_nombre", "PC"),
                "Operador": v.get("usuario_pc", "—"),
                "Detalle Técnico": v.get("detalle", "—")
            })

    if filas_al:
        st.warning(f"⚠️ **{len(filas_al)} evento(s) de seguridad detectados**:")
        st.dataframe(filas_al, use_container_width=True, hide_index=True)
        if st.button("🗑️ Limpiar Bitácora de Alertas"):
            peticion_firebase("DELETE", "alertas_seguridad")
            st.success("Historial depurado.")
            st.rerun()
    else:
        st.success("🛡️ **Estado Seguro**: No se registran manipulaciones de reloj ni intentos de acceso no autorizados.")

    st.markdown("---")
    st.markdown("##### 🚨 Kill-Switch de Emergencia por Dispositivo:")
    col_ks1, col_ks2 = st.columns(2)
    with col_ks1:
        opciones_hwid = list(equipos_data.keys())
        hwid_sel_ks = st.selectbox(
            "Seleccionar Asiento para Suspensión Inmediata:",
            opciones_hwid,
            format_func=lambda h: f"{equipos_data[h].get('taller', 'Sin taller')} • {equipos_data[h].get('cliente', 'Usuario')} ({h})"
        )
    with col_ks2:
        info_ks = equipos_data.get(hwid_sel_ks, {})
        est_actual = "🚫 SUSPENDIDO" if info_ks.get("bloqueado") else "🟢 AUTORIZADO"
        st.markdown(f"**Estado del Asiento:** `{est_actual}`")

        c_btn_b, c_btn_d = st.columns(2)
        with c_btn_b:
            if st.button("🚨 SUSPENDER ACCESO", use_container_width=True, disabled=bool(info_ks.get("bloqueado"))):
                peticion_firebase("PATCH", f"equipos/{hwid_sel_ks}", {
                    "bloqueado": True,
                    "clave_bloqueada": info_ks.get("clave", "")
                })
                st.error(f"¡Equipo {hwid_sel_ks} suspendido de inmediato!")
                st.rerun()
        with c_btn_d:
            if st.button("✅ RESTAURAR ACCESO", use_container_width=True, disabled=not bool(info_ks.get("bloqueado"))):
                peticion_firebase("PATCH", f"equipos/{hwid_sel_ks}", {
                    "bloqueado": False,
                    "clave_bloqueada": ""
                })
                st.success(f"¡Equipo {hwid_sel_ks} restaurado!")
                st.rerun()

# ==============================================================================
# TAB 7: ACTUALIZACIONES OTA CLOUD
# ==============================================================================
with tab_ota:
    st.markdown("#### 🚀 Servidor de Despliegue de Actualizaciones OTA")
    try:
        ota_act = peticion_firebase("GET", "actualizaciones/nestpro") or {}
    except Exception:
        ota_act = {}

    v_a = ota_act.get("version", "v4.6 Industrial Edition")
    b_a = ota_act.get("build", "2026102718")
    u_a = ota_act.get("url_descarga", "---")
    n_a = ota_act.get("novedades", "---")

    st.markdown(f"""
        <div class="adobe-seat-card card-activa" style="margin-bottom: 14px;">
            <div style="font-size: 0.70rem; color: #8C8C8C; text-transform: uppercase; letter-spacing: 0.06em;">VERSIÓN OFICIAL DISTRIBUIDA:</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: #34D399; margin: 2px 0;">{v_a} (Build {b_a})</div>
            <div style="font-size: 0.72rem; color: #58A6FF; word-break: break-all;">Google Drive: {u_a}</div>
            <div style="font-size: 0.76rem; color: #CCCCCC; margin-top: 4px;"><b>Novedades:</b> {n_a}</div>
        </div>
    """, unsafe_allow_html=True)

    with st.form("form_ota_pub"):
        co1, co2 = st.columns(2)
        with co1:
            nv_v = st.text_input("Versión Comercial:", value=v_a)
            nv_b = st.number_input("Número de Build:", value=int(b_a) if str(b_a).isdigit() else 2026102718)
        with co2:
            nv_u = st.text_input("Enlace Google Drive del .exe:", value=u_a)
            nv_n = st.text_area("Registro de Cambios:", value=n_a)

        if st.form_submit_button("🚀 PUBLICAR ACTUALIZACIÓN EN FIREBASE", use_container_width=True):
            if nv_v and nv_u:
                peticion_firebase("PATCH", "actualizaciones/nestpro", {
                    "version": nv_v.strip(),
                    "build": int(nv_b),
                    "url_descarga": nv_u.strip(),
                    "novedades": nv_n.strip(),
                    "fecha_publicacion": int(time.time()),
                    "publicado_por": "Admin Web Studio"
                })
                st.success("¡Nueva versión publicada en Firebase Cloud!")
                st.rerun()
