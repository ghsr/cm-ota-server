import logging


def get_file(filename):
    try:
        # Use basketbuild for all URLs
        return "https://s.basketbuild.com/uploads/devs/GHsR/CM-13/i9105p/" + filename
    except Exception, e:
        logging.error("Unable to query CDN " + str(e))
        return None
