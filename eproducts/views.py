from subprocess import call

def deliver(name, surname, email, file_name, file_type):
    delievered = False
    import ipdb; ipdb.set_trace()
    if file_type == "audiodownload":
        try:
            call(['mp3.sh',
              '"%s %s" %s "%s"' % (name, surname, email, file_name)])
        except OSError:
            pass
        else:
            delievered = True
    return delievered