def Ext(ension):
	if ension in (".jpg", ".png", ".bmp", ".webp", ".ai", ".gif", ".ico", ".jpeg", ".ps", ".psd", ".svg", ".tif", ".tiff"):
		extype = "Image File"
	elif ension in (".mp4", ".3gp", ".avi", ".flv", ".m4v", ".mkv", ".mov", ".wmv"):
		extype = "Video File"
	elif ension in (".zip", ".rar", ".7z", ".arj", ".deb", ".pkg", ".rpm", ".tar.gz", ".z"):
		extype = "Zip File"
	elif ension in (".mp3", ".aif", ".cda", ".mid", ".midi", ".mpa", ".ogg", ".wav", ".wma", ".wpl"):
		extype = "Audio File"
	elif ension in (".txt", ".pdf", ".tex", ".doc", ".docx"):
		extype = "Text File"
	elif ension in (".bin", ".dmg", ".iso", ".toast", ".vcd"):
		extype = "Disc File"
	elif ension in (".fnt", ".fon", ".otf", ".ttf"):
		extype = "Font File"
	else:
		extype = "Unknown File"
	return extype
