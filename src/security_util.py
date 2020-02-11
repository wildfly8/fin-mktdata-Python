class SecurityUtil:

    @staticmethod
    def getYahooAPITicker(ticker):
        yahooTicker = ticker
        idxFirst = yahooTicker.find(".")
        if idxFirst >= 0:
            idxLast = yahooTicker.rfind(".")
            if idxFirst == idxLast:
                if "V".lower() != yahooTicker[idxLast+1:].lower() and "TO".lower() != yahooTicker[idxLast+1:].lower() and \
                        "AX".lower() != yahooTicker[idxLast+1:].lower() and "HK".lower() != yahooTicker[idxLast+1:].lower():
                    yahooTicker = yahooTicker.replace(".", "-")
            else:
                yahooTicker = yahooTicker.replace(".", "-", 1)
        return  yahooTicker

    @staticmethod
    def chopExchangeCodePrefix(fullTicker):
        idx = fullTicker.find(":")
        if idx >= 0:
            return fullTicker[idx+1:]
        return fullTicker

    @staticmethod
    def chopExchangeCodeSuffix(fullTicker):
        idx = fullTicker.rfind(".")
        if idx >= 0 and ("V".lower() == fullTicker[idx+1:].lower() or "TO".lower() == fullTicker[idx+1:].lower() or \
                         "AX".lower() == fullTicker[idx+1:].lower() or "HK".lower() == fullTicker[idx+1:].lower()):
            return fullTicker[:idx]
        return fullTicker
