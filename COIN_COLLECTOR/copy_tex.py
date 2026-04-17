import shutil
import os

src_grass = os.path.join(os.environ["USERPROFILE"], ".gemini", "antigravity", "brain", "924f0dd1-e107-4b0c-b348-7cf7b4768e90", "grass_texture_1776182405669.png")
src_coin = os.path.join(os.environ["USERPROFILE"], ".gemini", "antigravity", "brain", "924f0dd1-e107-4b0c-b348-7cf7b4768e90", "coin_texture_1776182388693.png")

if not os.path.exists("textures"):
    os.makedirs("textures")

if os.path.exists(src_grass):
    shutil.copy(src_grass, "textures/grass.png")
if os.path.exists(src_coin):
    shutil.copy(src_coin, "textures/coin.png")
