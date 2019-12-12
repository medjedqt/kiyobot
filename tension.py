def Ext(ension):
	if ension in (".jpg", ".png", ".bmp", ".webp", ".ai", ".gif", ".ico", ".jpeg", ".ps", ".psd", ".svg", ".tif", ".tiff"):
		type = "Image File"
	elif ension in (".mp4", ".3gp", ".avi", ".flv", ".m4v", ".mkv", ".mov", ".wmv"):
		type = "Video File"
	elif ension in (".zip", ".rar", ".7z", ".arj", ".deb", ".pkg", ".rpm", ".tar.gz", ".z"):
		type = "Zip File"
	elif ension in (".mp3", ".aif", ".cda", ".mid", ".midi", ".mpa", ".ogg", ".wav", ".wma", ".wpl"):
		type = "Audio File"
	elif ension in (".txt", ".pdf", ".tex", ".doc", ".docx"):
		type = "Text File"
	elif ension in (".bin", ".dmg", ".iso", ".toast", ".vcd"):
		type = "Disc File"
	elif ension in (".fnt", ".fon", ".otf", ".ttf"):
		type = "Font File"
	else:
		type = "Unknown File"
	return type;
