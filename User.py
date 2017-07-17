class User:
    def __init__(self,  userID, sTimestamp, fTimestamp, timezoneOffset, duration, distance, sClusterID, fClusterID, isPredicted):
        self.userID = userID
        self.sTimestamp = [sTimestamp]
        self.fTimestamp = [fTimestamp]
        self.timezoneOffset = [timezoneOffset]
        self.duration = [duration]
        self.distance = [distance]
        self.sClusterID = [sClusterID]
        self.fClusterID = [fClusterID]
        self.isPredicted = [isPredicted]
        self.gbUser = 0

    def appendUser(self, sTimestamp, fTimestamp, timezoneOffset, duration, distance, sClusterID, fClusterID, isPredicted):
        self.sTimestamp.append(sTimestamp)
        self.fTimestamp.append(fTimestamp)
        self.timezoneOffset.append(timezoneOffset)
        self.duration.append(duration)
        self.distance.append(distance)
        self.sClusterID.append(sClusterID)
        self.fClusterID.append(fClusterID)
        self.isPredicted.append(isPredicted)