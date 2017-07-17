class User:
    def __init__(self,  userID, sTimestamp, fTimestamp, timezoneOffset, duration, distance, sClusterID, fClusterID, isPredicted, rank, guessProbability, numpred):
        self.userID = userID
        self.sTimestamp = [int(float(sTimestamp))]
        self.fTimestamp = [int(float(fTimestamp))]
        self.timezoneOffset = [int(float(timezoneOffset))]
        self.duration = [int(float(duration))]
        self.distance = [int(float(distance))]
        self.sClusterID = [sClusterID]
        self.fClusterID = [fClusterID]
        self.isPredicted = [isPredicted]
        self.rank = [rank]
        self.guessProbability = [guessProbability]
        self.numpred = [numpred]
        self.gbUser = 0

    def append_user(self, sTimestamp, fTimestamp, timezoneOffset, duration, distance, sClusterID, fClusterID, isPredicted, rank, guessProbability, numpred):
        self.sTimestamp.append(int(float(sTimestamp)))
        self.fTimestamp.append(int(float(fTimestamp)))
        self.timezoneOffset.append(int(float(timezoneOffset)))
        self.duration.append(int(float(duration)))
        self.distance.append(int(float(distance)))
        self.sClusterID.append(sClusterID)
        self.fClusterID.append(fClusterID)
        self.isPredicted.append(isPredicted)
        self.rank.append(rank)
        self.guessProbability.append(guessProbability)
        self.numpred.append(numpred)
