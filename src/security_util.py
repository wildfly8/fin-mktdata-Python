class SecurityUtil:

    @staticmethod
    def chopExchangeCodePrefix(fullTicker):
        idx = fullTicker.find(":")
        if idx >= 0:
            return fullTicker[idx + 1:]
        return fullTicker

    @staticmethod
    def chopExchangeCodeSuffix(fullTicker):
        idx = fullTicker.rfind(".")
        if idx >= 0 and ("V".lower() == fullTicker[idx + 1:].lower() or "TO".lower() == fullTicker[idx + 1:].lower() or \
                         "AX".lower() == fullTicker[idx + 1:].lower() or "HK".lower() == fullTicker[idx + 1:].lower()):
            return fullTicker[:idx]
        return fullTicker
