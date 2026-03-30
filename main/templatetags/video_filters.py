from django import template
import re

register = template.Library()

@register.filter
def embed_video(url):
    # YouTube short
    if "youtu.be" in url:
        video_id = url.split("/")[-1].split("?")[0]
        return f"https://www.youtube.com/embed/{video_id}"
    
    # YouTube classique
    if "youtube.com/watch" in url:
        match = re.search(r"v=([^&]+)", url)
        if match:
            return f"https://www.youtube.com/embed/{match.group(1)}"
    
    # Facebook vidéo
    if "facebook.com" in url:
        return f"https://www.facebook.com/plugins/video.php?href={url}"
    
    return url