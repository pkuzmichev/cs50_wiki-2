import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import secrets
import markdown2

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))

def list_search_matches(search):
    """
    Search by matches
    """
    if type(search) is str:
        matches = [s for s in list_entries() if search.lower() in s.lower()]
        return matches

def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        return False
    else:
        default_storage.save(filename, ContentFile(content))
        return True

def update(title, content):
    """
    Update content file
    """
    with open(f"entries/{title}.md", "w") as f:
        f.write(content)

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return markdown2.markdown(f.read().decode("utf-8"))
    except FileNotFoundError:
        return None

def random():
    return secrets.choice(list_entries())
