import logging


def get_file(filename, device):
    try:
        # Use basketbuild for all URLs
        if device == "i9105p":
            return "https://basketbuild.com/uploads/devs/GHsR/CM-13/i9105p/" + filename
        elif device == "i9152":
            return "https://basketbuild.com/uploads/devs/Kiborg_Man/CM13/" + filename
        else:
            raise Exception("Unknown device")
    except Exception, e:
        logging.error("Unable to query CDN " + str(e))
        return None
