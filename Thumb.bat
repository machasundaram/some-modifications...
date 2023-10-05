ffmpeg -i decrypted.mp4 -vf "drawtext='fontfile=C\\:/Windows/Fonts/arial.ttf:timecode='00\\:00\\:00\\:00':r=25:text='\:':fontsize=25:fontcolor=white:x=1:y=1:box=1:boxcolor=black@0.5',select=not(mod(n\,75)),tile=5x4,smartblur=1.5:-0.35:-3.5:0.65:0.25:2.0" -vsync 2 -s 1920x1080 -f image2 zthumbnails%%03d.png
START zthumbnails001.png


