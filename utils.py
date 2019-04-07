# For getIP
import netifaces as ni
import tokens

async def ms_to_text(ms):
    d = ms // (3600 * 24 * 1000)
    ms = ms % (3600 * 24 * 1000)
    h = ms // (3600 * 1000)
    ms = ms % (3600 * 1000)
    m = ms // (60 * 1000)

    text = str(d).replace(".0","") + (" giorno, " if d == 1 else " giorni, ") + str(h).replace(".0","") + (" ora, " if h == 1 else " ore, ") + "e " + str(m).replace(".0","") + (" minuto" if m == 1 else " minuti")
    return text

async def getIP():
    try:
        wlan = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    except:
        wlan = "Something went wrong."
    try:
        eth = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    except:
        eth = "Something went wrong."
    return "Ethernet: " + str(eth) + "\nWlan: " + str(wlan)

async def isAdmin(update):
    if(str(update['from']['id']) in tokens.admin_ids):
        return True
    else:
        return False
