def Ext(ension):
	if ension in (".jpg", ".png", ".bmp", ".webp"):
		type = "Image File"
	elif ension in (".mp4", ".3gp"):
		type = "Video File"
	elif ension in (".zip", ".rar"):
		type = "Zip File"
	else:
		type = "Unknown File"
	return type;
